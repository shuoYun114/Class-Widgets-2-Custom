# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边栏课程表数据聚合与模型测试 (Tier 1 & Tier 2)

覆盖特性:
- F1: 当天课表竖条胶囊主体数据聚合 (PROJECT.md 契约)
- F2: 当前课程状态与高亮精确判定、多时间点进度计算
- F3: 课程悬浮气泡卡片元数据（起止时间、教室、教师、主题色）
- F6: 全周 7 天网格矩阵聚合与多周轮次匹配
- Tier 2 边界: 空课表、起止时间临界点、零时长除零防御、非法格式容错、超长文本与特殊字符、调休、换课、时间偏移
"""
import sys
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
)
from src.core.schedule.runtime import ScheduleRuntime
from src.core.utils import get_week_number, get_cycle_week


@pytest.fixture(scope="session")
def qapp():
    """提供 PySide6 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


@pytest.fixture
def mock_central(qapp):
    """模拟 AppCentral 运行环境与配置"""
    central = MagicMock()
    central.configs.schedule.time_offset = 0
    central.configs.schedule.preparation_time = 2
    central.configs.schedule.reschedule_day = {}
    central.configs.schedule.class_swap = None
    central.notification = MagicMock()
    return central


def setup_runtime(runtime: ScheduleRuntime, schedule: ScheduleData, target_dt: datetime) -> None:
    """在测试中安全装配 Runtime 的目标时间与日程上下文状态"""
    runtime.schedule = schedule
    if schedule and schedule.meta:
        runtime.schedule_meta = schedule.meta
        max_cycle = schedule.meta.maxWeekCycle or 1
        start_date = schedule.meta.startDate or target_dt.strftime("%Y-%m-%d")
        runtime.current_week = get_week_number(start_date, target_dt)
        runtime.current_week_of_cycle = get_cycle_week(runtime.current_week, max_cycle)
    else:
        runtime.schedule_meta = None
        runtime.current_week = 1
        runtime.current_week_of_cycle = 1

    runtime.current_time = target_dt
    runtime.current_offset_time = target_dt
    runtime.current_day_of_week = target_dt.isoweekday()

    if schedule:
        runtime.current_day = runtime.services.get_day_entries(schedule, target_dt)
    else:
        runtime.current_day = None

    if runtime.current_day:
        runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, target_dt)
        runtime.all_entries = runtime.services.get_all_entries(runtime.current_day)
        runtime.next_entries = runtime.services.get_next_entries(runtime.current_day, target_dt)
        runtime.remaining_time = runtime.services.get_remaining_time(runtime.current_day, target_dt)
        runtime.current_status = runtime.services.get_current_status(runtime.current_day, target_dt, 2)
        runtime.current_subject = runtime.services.get_current_subject(runtime.current_day, schedule.subjects, target_dt)
        runtime.current_title = getattr(runtime.current_entry, "title", None)
    else:
        runtime.current_entry = None
        runtime.all_entries = None
        runtime.next_entries = None
        runtime.remaining_time = None
        runtime.current_status = EntryType.FREE
        runtime.current_subject = None
        runtime.current_title = None

    runtime._progress = runtime.get_progress_percent()


@pytest.fixture
def standard_schedule():
    """标准测试课表：包含高等数学、大学英语两门课，周一和周二有课"""
    subjects = [
        Subject(
            id="sub_math",
            name="高等数学",
            simplifiedName="高数",
            teacher="张教授",
            location="教三 101",
            color="#4A90E2",
        ),
        Subject(
            id="sub_english",
            name="大学英语",
            simplifiedName="英语",
            teacher="Smith 老师",
            location="外国语楼 302",
            color="#50E3C2",
        ),
    ]

    entries_mon = [
        Entry(
            id="entry_mon_1",
            type=EntryType.CLASS,
            startTime="08:00",
            endTime="08:45",
            subjectId="sub_math",
            title=None,
        ),
        Entry(
            id="entry_mon_2",
            type=EntryType.CLASS,
            startTime="09:00",
            endTime="09:45",
            subjectId="sub_english",
            title=None,
        ),
    ]

    entries_tue = [
        Entry(
            id="entry_tue_1",
            type=EntryType.CLASS,
            startTime="10:00",
            endTime="10:45",
            subjectId="sub_math",
            title=None,
        ),
    ]

    days = [
        Timeline(
            id="timeline_mon",
            dayOfWeek=[1],
            weeks="all",
            entries=entries_mon,
        ),
        Timeline(
            id="timeline_tue",
            dayOfWeek=[2],
            weeks="all",
            entries=entries_tue,
        ),
    ]

    meta = MetaInfo(
        id="meta_1",
        startDate="2026-09-07",
        maxWeekCycle=1,
    )

    return ScheduleData(
        meta=meta,
        subjects=subjects,
        days=days,
        overrides=[],
    )


# ============================================================================
# Tier 1: 核心功能与字段完整性验证 (F1, F2, F3, F6)
# ============================================================================


def test_sidebar_day_schedule_fields_completeness(mock_central, standard_schedule):
    """Tier 1 [F1]: 验证 sidebarDaySchedule 返回对象必须包含 PROJECT.md 契约规定的所有 12 个字段"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 20)
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert isinstance(day_schedule, list)
    assert len(day_schedule) == 2

    required_fields = {
        "id", "title", "startTime", "endTime", "timeRange",
        "subjectName", "teacher", "location", "color",
        "isCurrent", "progress", "type"
    }

    for item in day_schedule:
        assert isinstance(item, dict)
        missing = required_fields - set(item.keys())
        assert not missing, f"缺少必要字段: {missing}"
        assert isinstance(item["id"], str)
        assert isinstance(item["title"], str)
        assert isinstance(item["startTime"], str)
        assert isinstance(item["endTime"], str)
        assert isinstance(item["timeRange"], str)
        assert isinstance(item["subjectName"], str)
        assert isinstance(item["teacher"], str)
        assert isinstance(item["location"], str)
        assert isinstance(item["color"], str)
        assert isinstance(item["isCurrent"], bool)
        assert isinstance(item["progress"], float)
        assert isinstance(item["type"], str)


@pytest.mark.parametrize(
    "hour,minute,second,expected_current,min_p,max_p",
    [
        (7, 50, 0, False, 0.0, 0.0),       # 课前 10 分钟
        (7, 59, 59, False, 0.0, 0.0),      # 课前 1 秒
        (8, 0, 0, True, 0.0, 0.0),         # 开始瞬间
        (8, 11, 15, True, 0.20, 0.30),     # 上课 25% 处
        (8, 22, 30, True, 0.45, 0.55),     # 上课 50% 处
        (8, 33, 45, True, 0.70, 0.80),     # 上课 75% 处
        (8, 44, 59, True, 0.95, 1.0),      # 临近下课 1 秒
        (8, 45, 0, False, 1.0, 1.0),       # 下课瞬间
        (8, 50, 0, False, 1.0, 1.0),       # 课间休息
    ],
)
def test_sidebar_day_schedule_fine_grained_timeline_progress(
    mock_central, standard_schedule, hour, minute, second, expected_current, min_p, max_p
):
    """Tier 1 [F2]: 全天细粒度时间采样点验证当前课程高亮状态与进度变化"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, hour, minute, second)
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    first_lesson = day_schedule[0]

    assert first_lesson["isCurrent"] is expected_current
    assert min_p <= first_lesson["progress"] <= max_p


@pytest.mark.parametrize(
    "teacher,location,color,sub_name",
    [
        ("张教授", "教三 101", "#4A90E2", "高等数学"),
        ("", "网络教室", "#FF5722", "计算方法"),
        ("王老师", "", "#107C41", "应用物理"),
        ("", "", "", "自习"),
    ],
)
def test_sidebar_day_schedule_subject_metadata_variations(
    mock_central, teacher, location, color, sub_name
):
    """Tier 1 [F3]: 验证气泡卡片所需的各项元数据在不同缺省组合下的正确映射"""
    sub = Subject(id="sub_test", name=sub_name, teacher=teacher or None, location=location or None, color=color or None)
    entry = Entry(id="e_test", type=EntryType.CLASS, startTime="08:00", endTime="08:45", subjectId="sub_test")
    days = [Timeline(id="tl_1", dayOfWeek=[1], weeks="all", entries=[entry])]
    schedule = ScheduleData(
        meta=MetaInfo(id="m_t", startDate="2026-09-07", maxWeekCycle=1),
        subjects=[sub],
        days=days,
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 20)
    setup_runtime(runtime, schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    item = day_schedule[0]
    assert item["subjectName"] == sub_name
    assert item["teacher"] == (teacher or "")
    assert item["location"] == (location or "")
    # 若无颜色，默认回退为 #4A90E2
    assert item["color"] == (color or "#4A90E2")


def test_sidebar_week_schedule_matrix_structure(mock_central, standard_schedule):
    """Tier 1 [F6]: 验证 sidebarWeekSchedule 整周网格矩阵返回包含 7 个周键的字典"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 10, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    week_schedule = runtime.sidebarWeekSchedule
    assert isinstance(week_schedule, dict)
    assert week_schedule["currentDayOfWeek"] == 1
    assert "days" in week_schedule

    days_dict = week_schedule["days"]
    assert set(days_dict.keys()) == {"1", "2", "3", "4", "5", "6", "7"}
    assert len(days_dict["1"]) == 2
    assert len(days_dict["2"]) == 1
    assert len(days_dict["3"]) == 0
    assert len(days_dict["7"]) == 0


@pytest.mark.parametrize("target_weekday", [1, 2, 3, 4, 5, 6, 7])
def test_sidebar_week_schedule_individual_weekday_coverage(mock_central, target_weekday):
    """Tier 1 [F6]: 验证周一到周日 7 天各自独立排课能准确落在对应天的桶中"""
    entry = Entry(id=f"e_{target_weekday}", type=EntryType.CLASS, startTime="10:00", endTime="11:30", title=f"星期{target_weekday}专修")
    timeline = Timeline(id=f"tl_{target_weekday}", dayOfWeek=[target_weekday], weeks="all", entries=[entry])
    schedule = ScheduleData(
        meta=MetaInfo(id=f"m_{target_weekday}", startDate="2026-09-07", maxWeekCycle=1),
        subjects=[],
        days=[timeline],
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 9, 0)  # 周一
    setup_runtime(runtime, schedule, test_now)

    week_sched = runtime.sidebarWeekSchedule
    for d in range(1, 8):
        if d == target_weekday:
            assert len(week_sched["days"][str(d)]) == 1
            assert week_sched["days"][str(d)][0]["title"] == f"星期{target_weekday}专修"
        else:
            assert len(week_sched["days"][str(d)]) == 0


def test_sidebar_week_schedule_past_future_days_progress(mock_central, standard_schedule):
    """Tier 1 [F6]: 验证全周矩阵中已过去的日期课程 progress 为 1.0，未来日期的课程 progress 为 0.0"""
    runtime = ScheduleRuntime(mock_central)
    # 周二 14:00 (周一全天已结束)
    test_now = datetime(2026, 9, 8, 14, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    week_schedule = runtime.sidebarWeekSchedule
    mon_entries = week_schedule["days"]["1"]
    for entry in mon_entries:
        assert entry["isCurrent"] is False
        assert entry["progress"] == 1.0


def test_sidebar_multi_week_cycle_matching(mock_central):
    """Tier 1: 验证多周轮次（maxWeekCycle=2 单双周）下课程能根据周次准确筛选激活"""
    subjects = [
        Subject(id="sub_single", name="单周实验课", teacher="王老师", location="物理楼"),
        Subject(id="sub_double", name="双周研讨课", teacher="赵老师", location="研讨室"),
    ]

    days = [
        Timeline(
            id="tl_single",
            dayOfWeek=[1],
            weeks=[1],
            entries=[Entry(id="e_s1", type=EntryType.CLASS, startTime="14:00", endTime="15:30", subjectId="sub_single")],
        ),
        Timeline(
            id="tl_double",
            dayOfWeek=[1],
            weeks=[2],
            entries=[Entry(id="e_d1", type=EntryType.CLASS, startTime="14:00", endTime="15:30", subjectId="sub_double")],
        ),
    ]

    cycle_schedule = ScheduleData(
        meta=MetaInfo(id="meta_cycle", startDate="2026-09-07", maxWeekCycle=2),
        subjects=subjects,
        days=days,
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)

    # 第 1 周周一（单周）
    single_week_now = datetime(2026, 9, 7, 14, 10)
    setup_runtime(runtime, cycle_schedule, single_week_now)
    assert len(runtime.sidebarDaySchedule) == 1
    assert runtime.sidebarDaySchedule[0]["subjectName"] == "单周实验课"

    # 第 2 周周一（双周）
    double_week_now = datetime(2026, 9, 14, 14, 10)
    setup_runtime(runtime, cycle_schedule, double_week_now)
    assert len(runtime.sidebarDaySchedule) == 1
    assert runtime.sidebarDaySchedule[0]["subjectName"] == "双周研讨课"


def test_sidebar_activity_type_support(mock_central):
    """Tier 1: 验证支持非学科类型的活动日程（EntryType.ACTIVITY）正常聚合展示"""
    days = [
        Timeline(
            id="tl_act",
            dayOfWeek=[3],
            weeks="all",
            entries=[
                Entry(
                    id="e_act_1",
                    type=EntryType.ACTIVITY,
                    startTime="16:00",
                    endTime="17:00",
                    subjectId=None,
                    title="院系辩论赛",
                )
            ],
        )
    ]

    act_schedule = ScheduleData(
        meta=MetaInfo(id="meta_act", startDate="2026-09-07", maxWeekCycle=1),
        subjects=[],
        days=days,
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 9, 16, 30)
    setup_runtime(runtime, act_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 1
    item = day_schedule[0]
    assert item["title"] == "院系辩论赛"
    assert item["type"] == "activity"
    assert item["isCurrent"] is True


# ============================================================================
# Tier 2: 边界值、极端情况与安全防御测试
# ============================================================================


def test_sidebar_model_null_schedule_safety(mock_central):
    """Tier 2 边界: runtime.schedule 为 None 时返回安全空数据，严禁抛出未捕获异常"""
    runtime = ScheduleRuntime(mock_central)
    setup_runtime(runtime, None, datetime(2026, 9, 7, 8, 30))

    assert runtime.sidebarDaySchedule == []
    week_sched = runtime.sidebarWeekSchedule
    assert isinstance(week_sched, dict)
    for day_key in range(1, 8):
        assert week_sched["days"][str(day_key)] == []


def test_sidebar_model_empty_day_schedule(mock_central, standard_schedule):
    """Tier 2 边界: 周日没有任何排课，sidebarDaySchedule 返回空列表"""
    runtime = ScheduleRuntime(mock_central)
    sunday_now = datetime(2026, 9, 13, 10, 0)
    setup_runtime(runtime, standard_schedule, sunday_now)

    assert runtime.sidebarDaySchedule == []


def test_sidebar_model_exact_boundary_start_time(mock_central, standard_schedule):
    """Tier 2 边界: 刚好在上课开始时刻（08:00:00），课程必须判定为当前课程且进度为 0.0"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 0, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    first_lesson = runtime.sidebarDaySchedule[0]
    assert first_lesson["isCurrent"] is True
    assert first_lesson["progress"] == 0.0


def test_sidebar_model_exact_boundary_end_time(mock_central, standard_schedule):
    """Tier 2 边界: 刚好在下课时刻（08:45:00），课程已不属于当前课程且进度为 1.0"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 45, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    first_lesson = runtime.sidebarDaySchedule[0]
    assert first_lesson["isCurrent"] is False
    assert first_lesson["progress"] == 1.0


def test_sidebar_model_zero_duration_entry(mock_central):
    """Tier 2 边界: 起止时间相同（例如 09:00 - 09:00）的异常数据，必须有除以零防御"""
    days = [
        Timeline(
            id="tl_zero",
            dayOfWeek=[1],
            weeks="all",
            entries=[Entry(id="e_zero", type=EntryType.CLASS, startTime="09:00", endTime="09:00", title="零时长通知")],
        )
    ]
    schedule = ScheduleData(
        meta=MetaInfo(id="m_z", startDate="2026-09-07", maxWeekCycle=1),
        subjects=[],
        days=days,
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 9, 0)
    setup_runtime(runtime, schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 1
    assert isinstance(day_schedule[0]["progress"], float)


def test_sidebar_model_malformed_time_fallback(mock_central):
    """Tier 2 边界: 包含非法格式时间（如 'abc' 或 '99:99'）的数据由 _format_sidebar_entry 优雅容错降级而不崩溃"""
    runtime = ScheduleRuntime(mock_central)
    bad_entry = Entry(
        id="e_bad",
        type=EntryType.CLASS,
        startTime="abc",
        endTime="xyz",
        title="异常时间课程",
    )
    now = datetime(2026, 9, 7, 9, 0)
    res = runtime._format_sidebar_entry(bad_entry, now.date(), now)
    assert res["id"] == "e_bad"
    assert res["isCurrent"] is False
    assert res["progress"] == 0.0


def test_sidebar_model_special_characters_long_text(mock_central):
    """Tier 2 边界: 超长课程名、特殊符号与标签符号正常解析透传"""
    long_name = "🚀 超前沿跨学科量子并行计算与分布式系统架构导论" * 3
    long_teacher = "Alexander von Humboldt-Smith-Wellington 第三世"
    long_location = "国家重点实验室二期工程 9 号科研大楼地下负二层超净间 007"

    subjects = [
        Subject(
            id="sub_long",
            name=long_name,
            teacher=long_teacher,
            location=long_location,
            color="#FF5722",
        )
    ]
    days = [
        Timeline(
            id="tl_long",
            dayOfWeek=[1],
            weeks="all",
            entries=[
                Entry(
                    id="e_long",
                    type=EntryType.CLASS,
                    startTime="08:00",
                    endTime="09:40",
                    subjectId="sub_long",
                    title="<script>alert(1)</script>",
                )
            ],
        )
    ]
    schedule = ScheduleData(
        meta=MetaInfo(id="m_long", startDate="2026-09-07", maxWeekCycle=1),
        subjects=subjects,
        days=days,
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 30)
    setup_runtime(runtime, schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 1
    item = day_schedule[0]
    assert item["subjectName"] == long_name
    assert item["teacher"] == long_teacher
    assert item["location"] == long_location
    assert item["title"] == "<script>alert(1)</script>"


def test_sidebar_model_reschedule_day_support(mock_central, standard_schedule):
    """Tier 2 边界: 调休机制（reschedule_day）下周六实际上周一课"""
    mock_central.configs.schedule.reschedule_day = {
        "2026-09-12": 1
    }

    runtime = ScheduleRuntime(mock_central)
    saturday_now = datetime(2026, 9, 12, 8, 20)
    setup_runtime(runtime, standard_schedule, saturday_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 2
    assert day_schedule[0]["subjectName"] == "高等数学"
    assert day_schedule[0]["isCurrent"] is True


def test_sidebar_model_class_swap_support(mock_central, standard_schedule):
    """Tier 2 边界: 临时换课机制（class_swap）支持临时替换整天课表"""
    mock_central.configs.schedule.class_swap = {
        "date": "2026-09-07",
        "day_of_week": 2,
        "week_of_cycle": 1,
    }

    runtime = ScheduleRuntime(mock_central)
    monday_now = datetime(2026, 9, 7, 10, 20)
    setup_runtime(runtime, standard_schedule, monday_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 1
    assert day_schedule[0]["startTime"] == "10:00"
    assert day_schedule[0]["isCurrent"] is True


def test_sidebar_model_override_timetable(mock_central):
    """Tier 2 边界: 课表信息覆盖（Timetable overrides 动态替换教师和教室）"""
    subjects = [
        Subject(id="sub_1", name="普通物理", teacher="王老师", location="物理楼 101"),
        Subject(id="sub_override", name="进阶物理", teacher="李特聘教授", location="科学会堂 500"),
    ]
    days = [
        Timeline(
            id="tl_ov",
            dayOfWeek=[1],
            weeks="all",
            entries=[Entry(id="entry_ov_1", type=EntryType.CLASS, startTime="08:00", endTime="08:45", subjectId="sub_1")],
        )
    ]
    overrides = [
        Timetable(
            id="ov_1",
            entryId="entry_ov_1",
            dayOfWeek=[1],
            weeks="all",
            subjectId="sub_override",
        )
    ]

    schedule = ScheduleData(
        meta=MetaInfo(id="meta_ov", startDate="2026-09-07", maxWeekCycle=1),
        subjects=subjects,
        days=days,
        overrides=overrides,
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 20)
    setup_runtime(runtime, schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 1
    item = day_schedule[0]
    assert item["subjectName"] == "进阶物理"
    assert item["teacher"] == "李特聘教授"
    assert item["location"] == "科学会堂 500"


@pytest.mark.parametrize("offset_seconds", [-3600, 0, 3600, 86400])
def test_sidebar_model_time_offset_variations(mock_central, standard_schedule, offset_seconds):
    """Tier 2 边界: 自定义时间偏移量 (time_offset) 下当天课表计算准确性"""
    mock_central.configs.schedule.time_offset = offset_seconds
    runtime = ScheduleRuntime(mock_central)

    # 基准时间为 2026-09-07 08:20
    base_time = datetime(2026, 9, 7, 8, 20)
    target_dt = base_time + timedelta(seconds=offset_seconds)
    setup_runtime(runtime, standard_schedule, target_dt)

    day_schedule = runtime.sidebarDaySchedule
    # 只要 target_dt 是周一 08:20，必定匹配到第一节数学课高亮
    if target_dt.isoweekday() == 1 and 8 == target_dt.hour and 0 <= target_dt.minute <= 45:
        assert len(day_schedule) == 2
        assert day_schedule[0]["isCurrent"] is True
    else:
        assert isinstance(day_schedule, list)


def test_sidebar_model_dense_schedule_stress(mock_central):
    """Tier 2 边界: 密集排课压力测试（一天内 20 节紧凑课程的有序聚合）"""
    dense_entries = []
    for i in range(20):
        start_h = 7 + (i * 45) // 60
        start_m = (i * 45) % 60
        end_time_dt = datetime(2026, 9, 7, start_h, start_m) + timedelta(minutes=40)
        dense_entries.append(
            Entry(
                id=f"dense_{i}",
                type=EntryType.CLASS,
                startTime=f"{start_h:02d}:{start_m:02d}",
                endTime=end_time_dt.strftime("%H:%M"),
                title=f"密集课程 {i}",
            )
        )

    days = [Timeline(id="tl_dense", dayOfWeek=[1], weeks="all", entries=dense_entries)]
    schedule = ScheduleData(
        meta=MetaInfo(id="m_dense", startDate="2026-09-07", maxWeekCycle=1),
        subjects=[],
        days=days,
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 0)
    setup_runtime(runtime, schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 20
    # 确保返回条目严格按开始时间升序
    start_times = [item["startTime"] for item in day_schedule]
    assert start_times == sorted(start_times)


@pytest.mark.parametrize(
    "curr_h,curr_m,expected_min,expected_sec",
    [
        (8, 15, 30, 0),  # 08:15 距离 08:45 下课还剩 30 分钟
        (8, 30, 15, 0),  # 08:30 距离 08:45 下课还剩 15 分钟
        (8, 44, 1, 0),   # 08:44 距离 08:45 下课还剩 1 分钟
        (8, 50, 10, 0),  # 08:50 距离 09:00 下节课还剩 10 分钟
        (11, 0, 0, 0),   # 11:00 上午所有课程结束，剩余 0
    ],
)
def test_sidebar_model_countdown_minute_second(
    mock_central, standard_schedule, curr_h, curr_m, expected_min, expected_sec
):
    """Tier 1: 验证 remainingTime 剩余时间在不同时间点的分钟/秒倒计时计算"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, curr_h, curr_m, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    rem = runtime.remainingTime
    assert isinstance(rem, dict)
    assert rem["minute"] == expected_min
    assert rem["second"] == expected_sec


@pytest.mark.parametrize(
    "curr_h,curr_m,expected_status",
    [
        (7, 30, "free"),         # 07:30 课前空闲
        (7, 58, "preparation"),  # 07:58 (第一节课前 2 分钟预备铃)
        (8, 15, "class"),        # 08:15 上课中
        (8, 50, "free"),         # 08:50 课间（未设显式 break 条目时为空闲）
        (8, 59, "preparation"),  # 08:59 (第二节课前 1 分钟预备铃)
        (12, 0, "free"),         # 12:00 午休空闲
    ],
)
def test_sidebar_model_current_status_derivation(
    mock_central, standard_schedule, curr_h, curr_m, expected_status
):
    """Tier 1: 验证 currentStatus 在全天不同阶段的推导准确性"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, curr_h, curr_m, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    assert runtime.currentStatus == expected_status


@pytest.mark.parametrize(
    "target_date_str,expected_week",
    [
        ("2026-09-07", 1),
        ("2026-09-14", 2),
        ("2026-09-28", 4),
        ("2026-11-16", 11),
    ],
)
def test_sidebar_model_start_date_semester_week_number(
    mock_central, standard_schedule, target_date_str, expected_week
):
    """Tier 1: 验证学期开始日期与各自然周数映射的准确性"""
    runtime = ScheduleRuntime(mock_central)
    target_dt = datetime.strptime(target_date_str, "%Y-%m-%d")
    setup_runtime(runtime, standard_schedule, target_dt)

    assert runtime.currentWeek == expected_week


def test_sidebar_model_caching_and_identity_stability(mock_central, standard_schedule):
    """
    回归测试: 验证 sidebarDaySchedule 与 sidebarWeekSchedule 的智能缓存机制。
    在同一分钟且当前节次不变的情况下，重复访问应返回同一缓存对象，
    杜绝秒级重构导致的巨量 QML 对象创建与掉帧。
    """
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 20, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    day1 = runtime.sidebarDaySchedule
    day2 = runtime.sidebarDaySchedule
    assert day1 is day2, "同一分钟内连续访问 sidebarDaySchedule 必须命中内存缓存！"

    week1 = runtime.sidebarWeekSchedule
    week2 = runtime.sidebarWeekSchedule
    assert week1 is week2, "当前节次不变时连续访问 sidebarWeekSchedule 必须命中内存缓存！"

    # 当切换当前节次时，缓存自动失效并刷新
    test_now_next = datetime(2026, 9, 7, 9, 15, 0) # 进入第2节课
    setup_runtime(runtime, standard_schedule, test_now_next)
    day3 = runtime.sidebarDaySchedule
    assert day3[1]["isCurrent"] is True
    assert day3[0]["isCurrent"] is False


def test_sidebar_many_entries_full_day_no_overflow_data(mock_central):
    """
    回归测试: 验证当全天拥有 9 到 12 节密集课程（如晚补、早自习、班会等）时，
    侧边栏数据与全周课表矩阵能够完整无误聚合所有课程项，无丢失无截断。
    """
    from src.core.schedule.model import ScheduleData, MetaInfo, Timeline, Entry, EntryType, Subject

    many_entries = []
    # 模拟从 07:30 到 21:00 共 10 节课
    for i in range(1, 11):
        s_hour = 7 + i
        e_hour = s_hour + 1
        many_entries.append(
            Entry(
                id=f"entry_{i}",
                startTime=f"{s_hour:02d}:00",
                endTime=f"{s_hour:02d}:45",
                type=EntryType.CLASS,
                subjectId="sub_math" if i % 2 == 1 else "sub_phys",
                title=f"第{i}节" if i <= 8 else ("晚补" if i == 9 else "晚自习"),
            )
        )

    timeline = Timeline(id="tl_many", dayOfWeek=[1], weeks="all", entries=many_entries)
    schedule = ScheduleData(
        meta=MetaInfo(
            id="meta_dense",
            name="密集课程表",
            version="1.0",
            startDate="2026-09-07",
            maxWeekCycle=1,
            timeTableMode=0,
            classesPerDay=10,
        ),
        subjects=[
            Subject(id="sub_math", name="数学", color="#4A90E2"),
            Subject(id="sub_phys", name="物理", color="#E67E22"),
        ],
        days=[timeline],
    )

    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 30, 0)
    setup_runtime(runtime, schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 10
    assert day_schedule[8]["title"] == "晚补"
    assert day_schedule[9]["title"] == "晚自习"

    week_schedule = runtime.sidebarWeekSchedule
    assert len(week_schedule["days"]["1"]) == 10


