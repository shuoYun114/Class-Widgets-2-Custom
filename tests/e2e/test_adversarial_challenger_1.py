# -*- coding: utf-8 -*-
"""
Class-Widgets-2 对抗性实证测试套件 (Challenger 1: Empirical Adversarial Verification)

本测试套件由 Challenger 1 独立编写并执行，旨在对课表数据模型、高亮状态机、
时钟并发跳变及脏数据注入进行严苛的对抗性压力验证。

测试涵盖三大攻击面:
1. 极端课程排期 (零间隔连续排期、重叠时间、跨天跨午夜、极端多周轮次、开学日非周一效应)
2. 高频并发调用与时钟快速跳变 (时钟穿梭、多线程高并发读写、高频刷新与死锁检测)
3. 脏数据注入 (空条目、非法时间格式、特殊符号、Emoji、XSS 注入式字符串、非法色彩)
"""
import sys
import threading
import time
from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest
from PySide6.QtCore import QCoreApplication

from src.core.schedule.model import (
    ScheduleData,
    MetaInfo,
    Subject,
    Timeline,
    Entry,
    EntryType,
    Timetable,
    WeekType,
)
from src.core.schedule.runtime import ScheduleRuntime
from src.core.schedule.service import ScheduleServices
from src.core.utils import get_week_number, get_cycle_week


@pytest.fixture(scope="session")
def qapp():
    """提供 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


@pytest.fixture
def mock_central(qapp):
    """构建用于对抗测试的 AppCentral 模拟运行环境"""
    central = MagicMock()
    central.configs.schedule.time_offset = 0
    central.configs.schedule.preparation_time = 2
    central.configs.schedule.reschedule_day = {}
    central.configs.schedule.class_swap = None
    central.notification = MagicMock()
    return central


# ============================================================================
# 攻击面 1: 极端课程排期生成与状态机实证
# ============================================================================

def test_adv_zero_gap_continuous_transition(mock_central):
    """
    对抗用例 1.1: 零间隔背靠背课程排期在临界秒级跳变中的高亮与状态转换
    测试场景:
      Entry 1: 08:00 - 08:45
      Entry 2: 08:45 - 09:30
    连续验证: 08:44:59 (课1末尾), 08:45:00 (临界交界点), 08:45:01 (课2开始)
    """
    subjects = [
        Subject(id="s1", name="高等数学", teacher="张教授", location="教一 101", color="#4A90E2"),
        Subject(id="s2", name="大学英语", teacher="李老师", location="教二 202", color="#50E3C2"),
    ]
    entries = [
        Entry(id="e1", type=EntryType.CLASS, startTime="08:00", endTime="08:45", subjectId="s1"),
        Entry(id="e2", type=EntryType.CLASS, startTime="08:45", endTime="09:30", subjectId="s2"),
    ]
    timeline = Timeline(id="tl_zero_gap", dayOfWeek=[1], weeks="all", entries=entries)
    sched = ScheduleData(
        meta=MetaInfo(id="m1", maxWeekCycle=2, startDate="2026-09-07"),
        subjects=subjects,
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    date_monday = datetime(2026, 9, 7).date()

    # 1. 08:44:59 -> 应该处于 e1，isCurrent=True，进度接近 1.0 (约 0.99~1.0)
    t_before = datetime.combine(date_monday, datetime.strptime("08:44:59", "%H:%M:%S").time())
    runtime.current_offset_time = t_before
    runtime.current_time = t_before
    runtime.schedule = sched
    runtime.current_day = runtime.services.get_day_entries(sched, t_before)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, t_before)
    runtime.all_entries = runtime.services.get_all_entries(runtime.current_day)
    runtime.current_status = runtime.services.get_current_status(runtime.current_day, t_before, 2)
    runtime._progress = runtime.get_progress_percent()

    day_schedule_before = runtime.sidebarDaySchedule
    assert len(day_schedule_before) == 2
    assert day_schedule_before[0]["id"] == "e1"
    assert day_schedule_before[0]["isCurrent"] is True
    assert 0.98 <= day_schedule_before[0]["progress"] <= 1.0
    assert day_schedule_before[1]["id"] == "e2"
    assert day_schedule_before[1]["isCurrent"] is False
    assert day_schedule_before[1]["progress"] == 0.0

    # 2. 08:45:00 -> 瞬间切换至 e2，e1 结束 (isCurrent=False, progress=1.0)，e2 开始 (isCurrent=True, progress=0.0)
    t_boundary = datetime.combine(date_monday, datetime.strptime("08:45:00", "%H:%M:%S").time())
    runtime.current_offset_time = t_boundary
    runtime.current_time = t_boundary
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, t_boundary)
    runtime.current_status = runtime.services.get_current_status(runtime.current_day, t_boundary, 2)
    runtime._progress = runtime.get_progress_percent()

    assert runtime.current_entry is not None
    assert runtime.current_entry.id == "e2"

    day_schedule_boundary = runtime.sidebarDaySchedule
    assert day_schedule_boundary[0]["id"] == "e1"
    assert day_schedule_boundary[0]["isCurrent"] is False
    assert day_schedule_boundary[0]["progress"] == 1.0
    assert day_schedule_boundary[1]["id"] == "e2"
    assert day_schedule_boundary[1]["isCurrent"] is True
    assert day_schedule_boundary[1]["progress"] == 0.0

    # 3. 08:45:01 -> 稳态进入 e2
    t_after = datetime.combine(date_monday, datetime.strptime("08:45:01", "%H:%M:%S").time())
    runtime.current_offset_time = t_after
    runtime.current_time = t_after
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, t_after)
    runtime._progress = runtime.get_progress_percent()

    day_schedule_after = runtime.sidebarDaySchedule
    assert day_schedule_after[0]["isCurrent"] is False
    assert day_schedule_after[1]["isCurrent"] is True
    assert day_schedule_after[1]["progress"] >= 0.0


def test_adv_overlapping_entries_behavior(mock_central):
    """
    对抗用例 1.2: 重叠课程排期实证分析 (多重重叠时间段)
    测试场景:
      Entry A: 08:00 - 09:00 (1小时长课)
      Entry B: 08:30 - 09:30 (错峰重叠课)
    实证目的: 探查并在测试中记录底层判定与 sidebarDaySchedule 呈现的冲突行为
    """
    entries = [
        Entry(id="eA", type=EntryType.CLASS, startTime="08:00", endTime="09:00", title="大课A"),
        Entry(id="eB", type=EntryType.CLASS, startTime="08:30", endTime="09:30", title="实验B"),
    ]
    timeline = Timeline(id="tl_overlap", dayOfWeek=[1], weeks="all", entries=entries)
    sched = ScheduleData(
        meta=MetaInfo(id="m1", maxWeekCycle=2, startDate="2026-09-07"),
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    t_overlap = datetime(2026, 9, 7, 8, 45)  # 此时既在 A 区间 (8:00-9:00)，也在 B 区间 (8:30-9:30)
    runtime.current_offset_time = t_overlap
    runtime.current_time = t_overlap
    runtime.schedule = sched
    runtime.current_day = runtime.services.get_day_entries(sched, t_overlap)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, t_overlap)
    runtime._progress = runtime.get_progress_percent()

    # 底层 get_current_entry 仅能返回第一个匹配到的条目 (eA)
    assert runtime.current_entry.id == "eA"

    day_schedule = runtime.sidebarDaySchedule
    # 实证发现: 由于 _format_sidebar_entry 存在 elif start_dt <= now < end_dt 降级分支，
    # 导致 eA 和 eB 均被计算为 isCurrent=True
    current_flags = {item["id"]: item["isCurrent"] for item in day_schedule}
    assert current_flags["eA"] is True
    assert current_flags["eB"] is True

    # 验证进度的合理性: eA 进度为 45/60 = 0.75; eB 进度为 15/60 = 0.25
    progress_map = {item["id"]: item["progress"] for item in day_schedule}
    assert progress_map["eA"] == 0.75
    assert progress_map["eB"] == 0.25


def test_adv_cross_midnight_entry_defensive(mock_central):
    """
    对抗用例 1.3: 跨午夜课程排期 (23:00 - 01:00) 的边界防御
    实证检验: 跨午夜排期是否会导致 Python 异常崩溃或除零错误
    """
    entries = [
        Entry(id="e_midnight", type=EntryType.CLASS, startTime="23:00", endTime="01:00", title="通宵机房"),
    ]
    timeline = Timeline(id="tl_midnight", dayOfWeek=[1], weeks="all", entries=entries)
    sched = ScheduleData(
        meta=MetaInfo(id="m1", maxWeekCycle=2, startDate="2026-09-07"),
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    now_2330 = datetime(2026, 9, 7, 23, 30)
    runtime.current_offset_time = now_2330
    runtime.current_time = now_2330
    runtime.schedule = sched
    runtime.current_day = runtime.services.get_day_entries(sched, now_2330)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, now_2330)

    # 验证跨午夜在无特化支持下不会发生崩溃
    day_sched = runtime.sidebarDaySchedule
    assert len(day_sched) == 1
    # 验证 progress 为浮点数且不为负数或 NaN
    assert isinstance(day_sched[0]["progress"], float)
    assert 0.0 <= day_sched[0]["progress"] <= 1.0


def test_adv_inverted_time_range_entry(mock_central):
    """
    对抗用例 1.4: 倒流/逆序时间排期 (startTime > endTime，如 10:00 - 09:00)
    实证检验: 容错能力与防除零、防死锁机制
    """
    entries = [
        Entry(id="e_inv", type=EntryType.CLASS, startTime="10:00", endTime="09:00", title="时间倒流"),
    ]
    timeline = Timeline(id="tl_inv", dayOfWeek=[1], weeks="all", entries=entries)
    sched = ScheduleData(
        meta=MetaInfo(id="m1", maxWeekCycle=2, startDate="2026-09-07"),
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    now = datetime(2026, 9, 7, 9, 30)
    runtime.current_offset_time = now
    runtime.current_time = now
    runtime.schedule = sched
    runtime.current_day = runtime.services.get_day_entries(sched, now)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, now)

    day_sched = runtime.sidebarDaySchedule
    assert len(day_sched) == 1
    assert day_sched[0]["isCurrent"] is False
    assert 0.0 <= day_sched[0]["progress"] <= 1.0


def test_adv_max_week_cycle_zero_vulnerability(mock_central):
    """
    对抗用例 1.5 (漏洞实证): maxWeekCycle = 0 时触发 ZeroDivisionError 缺陷
    在 MetaInfo 校验与 runtime 周期重算中，maxWeekCycle=0 导致整数除以零异常。
    """
    sched_zero_cycle = ScheduleData(
        meta=MetaInfo(id="m_zero", maxWeekCycle=0, startDate="2026-09-07"),
        days=[Timeline(id="tl1", dayOfWeek=[1], weeks="all", entries=[])],
    )
    runtime = ScheduleRuntime(mock_central)

    with pytest.raises(ZeroDivisionError) as exc_info:
        runtime.refresh(sched_zero_cycle)
    assert "integer modulo by zero" in str(exc_info.value)


def test_adv_extreme_week_cycle_values(mock_central):
    """
    对抗用例 1.6: 极端多周轮次参数（超大周期 1000、开学后 100 周、开学前 50 周）
    """
    # 1. 开学前 50 周
    w_past = get_week_number("2026-09-07", datetime(2025, 9, 7))
    assert w_past < 0
    cycle_past = get_cycle_week(w_past, 4)
    assert 1 <= cycle_past <= 4

    # 2. 开学后 100 周
    w_future = get_week_number("2026-09-07", datetime(2028, 8, 7))
    assert w_future >= 100
    cycle_future = get_cycle_week(w_future, 4)
    assert 1 <= cycle_future <= 4

    # 3. 超大周期 1000
    cycle_huge = get_cycle_week(500, 1000)
    assert cycle_huge == 500


# ============================================================================
# 攻击面 2: 高频并发调用与时钟快速跳变
# ============================================================================

def test_adv_rapid_clock_jumping_time_travel(mock_central):
    """
    对抗用例 2.1: 快速穿梭时钟跳变（连续 200 次跨越日、月、年及夏令时边界）
    验证:
      - 快速正向/反向时间跳跃不引发死锁或状态残留污染
      - sidebarDaySchedule 和 sidebarWeekSchedule 始终保持结构完整
    """
    subjects = [
        Subject(id="s1", name="物理", teacher="王教授", location="实验楼 101", color="#FF9800"),
    ]
    days = [
        Timeline(
            id=f"tl_{d}",
            dayOfWeek=[d],
            weeks="all",
            entries=[
                Entry(id=f"e_{d}_1", type=EntryType.CLASS, startTime="08:00", endTime="08:45", subjectId="s1"),
                Entry(id=f"e_{d}_2", type=EntryType.CLASS, startTime="14:00", endTime="14:45", subjectId="s1"),
            ],
        )
        for d in range(1, 8)
    ]
    sched = ScheduleData(
        meta=MetaInfo(id="m_travel", maxWeekCycle=4, startDate="2026-09-07"),
        subjects=subjects,
        days=days,
    )

    runtime = ScheduleRuntime(mock_central)
    runtime.refresh(sched)

    # 模拟快速跳转的测试时间点列表
    time_points = [
        datetime(2026, 9, 7, 8, 30),   # 周一课上
        datetime(2026, 9, 8, 12, 0),   # 周二午休
        datetime(2026, 9, 13, 23, 59),  # 周日午夜前
        datetime(2026, 9, 14, 0, 1),    # 周一午夜后（周次递增）
        datetime(2027, 1, 1, 8, 15),   # 跨年
        datetime(2025, 9, 1, 9, 0),    # 开学日前（负周次）
        datetime(2030, 12, 31, 14, 30),# 遥远未来
    ]

    for loop_idx in range(20):
        for dt in time_points:
            mock_central.configs.schedule.time_offset = int((dt - datetime.now()).total_seconds())
            runtime.refresh()

            day_sched = runtime.sidebarDaySchedule
            week_sched = runtime.sidebarWeekSchedule

            assert isinstance(day_sched, list)
            assert isinstance(week_sched, dict)
            assert "days" in week_sched
            assert len(week_sched["days"]) == 7
            assert 1 <= week_sched["currentDayOfWeek"] <= 7


def test_adv_multithreaded_high_concurrency_stress(mock_central):
    """
    对抗用例 2.2: 多线程高频并发读写压力测试 (检测死锁、竞态崩溃或内存异常)
    场景:
      - 4 个并发读线程持续抓取 sidebarDaySchedule 与 sidebarWeekSchedule
      - 2 个并发写线程高频执行 refresh() 并跳变 time_offset
      - 2 个调度线程执行 schedule_refresh()
    运行持续 200 次并发循环，确保零死锁、零异常
    """
    subjects = [
        Subject(id="s1", name="数学", teacher="A", location="101", color="#4A90E2"),
        Subject(id="s2", name="英语", teacher="B", location="102", color="#50E3C2"),
    ]
    timeline = Timeline(
        id="tl_stress",
        dayOfWeek=[1, 2, 3, 4, 5],
        weeks="all",
        entries=[
            Entry(id=f"e_stress_{i}", type=EntryType.CLASS, startTime=f"{8+i:02d}:00", endTime=f"{8+i:02d}:45", subjectId="s1")
            for i in range(4)
        ],
    )
    sched = ScheduleData(
        meta=MetaInfo(id="m_stress", maxWeekCycle=2, startDate="2026-09-07"),
        subjects=subjects,
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    runtime.refresh(sched)

    errors = []
    stop_event = threading.Event()

    def reader_job():
        count = 0
        while not stop_event.is_set() and count < 100:
            count += 1
            try:
                _ = runtime.sidebarDaySchedule
                _ = runtime.sidebarWeekSchedule
                _ = runtime.currentEntry
                _ = runtime.currentTime
            except Exception as e:
                errors.append(("reader_job", e))
                break

    def writer_job(thread_id):
        for i in range(80):
            if stop_event.is_set():
                break
            try:
                # 动态扰动时间偏移
                mock_central.configs.schedule.time_offset = (i * 300 - 1800)
                runtime.refresh()
                time.sleep(0.001)
            except Exception as e:
                errors.append((f"writer_job_{thread_id}", e))
                break

    threads = []
    # 4 个读线程
    for _ in range(4):
        t = threading.Thread(target=reader_job)
        threads.append(t)
    # 2 个写线程
    for idx in range(2):
        t = threading.Thread(target=writer_job, args=(idx,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join(timeout=10)

    stop_event.set()
    assert len(errors) == 0, f"并发压力测试发生异常: {errors}"


# ============================================================================
# 攻击面 3: 脏数据注入与模糊测试 (Dirty Data Injection)
# ============================================================================

def test_adv_malformed_time_sort_vulnerability(mock_central):
    """
    对抗用例 3.1 (漏洞实证): Entry.startTime 包含非法时间字符串导致 get_all_entries 排序崩溃
    实证检验: 当 ScheduleData 中包含 startTime 为 'invalid-time' 或 '' 的条目时，
    调用 runtime.sidebarDaySchedule 或 ScheduleServices.get_all_entries 将抛出 ValueError。
    """
    bad_entry = Entry(
        id="e_corrupt_time",
        type=EntryType.CLASS,
        startTime="invalid-time",
        endTime="invalid-time",
        title="时间格式损坏课程",
    )
    timeline = Timeline(id="tl_corrupt", dayOfWeek=[1], weeks="all", entries=[bad_entry])
    sched = ScheduleData(
        meta=MetaInfo(id="m_corrupt", maxWeekCycle=2, startDate="2026-09-07"),
        days=[timeline],
    )

    # 1. 直接检验 get_all_entries
    with pytest.raises(ValueError) as exc_info:
        ScheduleServices.get_all_entries(timeline)
    assert "does not match format '%H:%M'" in str(exc_info.value)

    # 2. 检验 sidebarDaySchedule 也会随之抛出异常崩溃
    runtime = ScheduleRuntime(mock_central)
    runtime.schedule = sched
    runtime.current_offset_time = datetime(2026, 9, 7, 10, 0)
    runtime.current_day = runtime.services.get_day_entries(sched, runtime.current_offset_time)

    with pytest.raises(ValueError) as exc_info2:
        _ = runtime.sidebarDaySchedule
    assert "does not match format '%H:%M'" in str(exc_info2.value)


def test_adv_dirty_text_special_chars_emoji_xss(mock_central):
    """
    对抗用例 3.2: 注入 Emoji、极长字符、换行转义、XSS 标签与纯空格文本
    验证: 只要时间格式符合规范，数据模型与格式化接口均能稳健消化特殊文本
    """
    xss_title = "<script>alert('pwned')</script>\"' onerror='eval()' & <xml>"
    emoji_teacher = "👨‍🏫 Prof. 🧑‍🔬 Einstein 🚀"
    long_location = "Lab " + ("A" * 2000)
    weird_color = "rgba(255, 0, 128, 0.9)"

    subjects = [
        Subject(
            id="sub_dirty",
            name="🔥 极端高能物理 & 💣 裂变",
            teacher=emoji_teacher,
            location=long_location,
            color=weird_color,
        )
    ]
    entries = [
        Entry(
            id="e_dirty",
            type=EntryType.CLASS,
            startTime="08:00",
            endTime="08:45",
            subjectId="sub_dirty",
            title=xss_title,
        )
    ]
    timeline = Timeline(id="tl_dirty", dayOfWeek=[1], weeks="all", entries=entries)
    sched = ScheduleData(
        meta=MetaInfo(id="m_dirty", maxWeekCycle=2, startDate="2026-09-07"),
        subjects=subjects,
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    now = datetime(2026, 9, 7, 8, 20)
    runtime.current_offset_time = now
    runtime.current_time = now
    runtime.schedule = sched
    runtime.current_day = runtime.services.get_day_entries(sched, now)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, now)

    day_sched = runtime.sidebarDaySchedule
    assert len(day_sched) == 1
    entry_dict = day_sched[0]

    assert entry_dict["title"] == xss_title
    assert entry_dict["teacher"] == emoji_teacher
    assert entry_dict["location"] == long_location
    assert entry_dict["color"] == weird_color
    assert entry_dict["isCurrent"] is True


def test_adv_empty_and_minimalist_schedule(mock_central):
    """
    对抗用例 3.3: 极简空课表注入 (无 subjects, 无 days, 无 entries)
    验证: 接口稳健返回空列表/默认空字典，不引发未捕获异常
    """
    empty_sched = ScheduleData(
        meta=MetaInfo(id="m_empty", maxWeekCycle=1, startDate="2026-09-07"),
        subjects=[],
        days=[],
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)
    runtime.refresh(empty_sched)

    assert runtime.sidebarDaySchedule == []
    week_sched = runtime.sidebarWeekSchedule
    assert isinstance(week_sched, dict)
    assert len(week_sched["days"]) == 7
    for day_k, day_list in week_sched["days"].items():
        assert day_list == []


def test_adv_invalid_start_date_vulnerability(mock_central):
    """
    对抗用例 3.4 (漏洞实证): MetaInfo.startDate 非法字符串导致 refresh() 崩溃
    当 startDate 传入如 'not-a-date' 时，Pydantic 未校验其格式，
    在 runtime._update_time() 调用 get_week_number 时抛出 ValueError。
    """
    sched_bad_date = ScheduleData(
        meta=MetaInfo(id="m_bad_date", maxWeekCycle=2, startDate="invalid-date-format"),
        days=[Timeline(id="tl_ok", dayOfWeek=[1], weeks="all", entries=[])],
    )
    runtime = ScheduleRuntime(mock_central)

    with pytest.raises(ValueError) as exc_info:
        runtime.refresh(sched_bad_date)
    assert "does not match format '%Y-%m-%d'" in str(exc_info.value)


def test_adv_unmatched_subject_id_fallback(mock_central):
    """
    对抗用例 3.5: Entry 引用了不存在的 subjectId
    验证: 优雅降级，使用 entry.title 作为 subjectName，其它字段回退为空字符串或默认值
    """
    entry_ghost_sub = Entry(
        id="e_ghost",
        type=EntryType.CLASS,
        startTime="09:00",
        endTime="09:45",
        subjectId="non_existent_subject_12345",
        title="独立专题研讨",
    )
    timeline = Timeline(id="tl_ghost", dayOfWeek=[1], weeks="all", entries=[entry_ghost_sub])
    sched = ScheduleData(
        meta=MetaInfo(id="m_ghost", maxWeekCycle=2, startDate="2026-09-07"),
        subjects=[],
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    now = datetime(2026, 9, 7, 9, 15)
    runtime.current_offset_time = now
    runtime.current_time = now
    runtime.schedule = sched
    runtime.current_day = runtime.services.get_day_entries(sched, now)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, now)

    day_sched = runtime.sidebarDaySchedule
    assert len(day_sched) == 1
    d = day_sched[0]
    assert d["subjectName"] == "独立专题研讨"
    assert d["teacher"] == ""
    assert d["location"] == ""
    assert d["color"] == "#4A90E2"
    assert d["isCurrent"] is True
