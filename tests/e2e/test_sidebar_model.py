# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边栏课程表数据聚合与模型测试 (Tier 1 & Tier 2)

覆盖范围:
- Tier 1: 字段完整性、当前课程高亮、进度计算、气泡元数据映射、整周 7 天矩阵结构、多周轮次匹配、活动类型支持
- Tier 2: 空课表安全防御、起止时间精确边界、零时长除零防御、非法时间容错、超长文本与特殊字符、调休与换课机制
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
    if schedule:
        runtime.schedule_meta = schedule.meta
        max_cycle = schedule.meta.maxWeekCycle if schedule.meta else 1
        start_date = schedule.meta.startDate if schedule.meta else target_dt.strftime("%Y-%m-%d")
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
    """标准测试课表：包含数学、英语两门课，周一和周二有课"""
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
# Tier 1: 核心功能与字段完整性验证
# ============================================================================


def test_sidebar_day_schedule_fields_completeness(mock_central, standard_schedule):
    """Tier 1: 验证 sidebarDaySchedule 返回对象必须包含 PROJECT.md 契约规定的所有 12 个字段"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 20)  # 周一 08:20
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


def test_sidebar_day_schedule_current_highlight_in_class(mock_central, standard_schedule):
    """Tier 1: 正在上课时（08:22:30 处于 08:00-08:45 正中），对应条目 isCurrent 必须为 True，进度在 0.4 到 0.6 之间"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 22, 30)
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    first_lesson = day_schedule[0]
    second_lesson = day_schedule[1]

    assert first_lesson["isCurrent"] is True
    assert 0.4 <= first_lesson["progress"] <= 0.6
    assert first_lesson["subjectName"] == "高等数学"

    assert second_lesson["isCurrent"] is False
    assert second_lesson["progress"] == 0.0


def test_sidebar_day_schedule_status_before_class(mock_central, standard_schedule):
    """Tier 1: 上课前（07:50），所有课程 isCurrent 均为 False，进度均为 0.0"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 7, 50)
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    for item in day_schedule:
        assert item["isCurrent"] is False
        assert item["progress"] == 0.0


def test_sidebar_day_schedule_status_after_class(mock_central, standard_schedule):
    """Tier 1: 第一节课结束后（08:50），第一节课 progress 应为 1.0，isCurrent 为 False"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 50)  # 08:45 已下课，09:00 未上课
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert day_schedule[0]["isCurrent"] is False
    assert day_schedule[0]["progress"] == 1.0

    assert day_schedule[1]["isCurrent"] is False
    assert day_schedule[1]["progress"] == 0.0


def test_sidebar_day_schedule_subject_metadata_mapping(mock_central, standard_schedule):
    """Tier 1: 验证悬浮气泡所需的教室、教师、主题颜色等元数据正确关联映射"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 30)
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    math_item = day_schedule[0]
    assert math_item["subjectName"] == "高等数学"
    assert math_item["teacher"] == "张教授"
    assert math_item["location"] == "教三 101"
    assert math_item["color"] == "#4A90E2"
    assert math_item["timeRange"] == "08:00 - 08:45"

    eng_item = day_schedule[1]
    assert eng_item["subjectName"] == "大学英语"
    assert eng_item["teacher"] == "Smith 老师"
    assert eng_item["location"] == "外国语楼 302"
    assert eng_item["color"] == "#50E3C2"


def test_sidebar_week_schedule_matrix_structure(mock_central, standard_schedule):
    """Tier 1: 验证 sidebarWeekSchedule 整周网格矩阵返回包含 7 个周键的字典"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 10, 0)
    setup_runtime(runtime, standard_schedule, test_now)

    week_schedule = runtime.sidebarWeekSchedule
    assert isinstance(week_schedule, dict)
    assert week_schedule["currentDayOfWeek"] == 1
    assert "days" in week_schedule

    days_dict = week_schedule["days"]
    assert set(days_dict.keys()) == {"1", "2", "3", "4", "5", "6", "7"}
    assert len(days_dict["1"]) == 2  # 周一有 2 节课
    assert len(days_dict["2"]) == 1  # 周二有 1 节课
    assert len(days_dict["3"]) == 0  # 周三无课
    assert len(days_dict["7"]) == 0  # 周日无课


def test_sidebar_week_schedule_past_future_days_progress(mock_central, standard_schedule):
    """Tier 1: 验证全周矩阵中已过去的日期课程 progress 为 1.0，未来日期的课程 progress 为 0.0"""
    runtime = ScheduleRuntime(mock_central)
    # 当前为周二 14:00 (此时周一全天课程均已过去)
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
            weeks=[1],  # 仅单周
            entries=[
                Entry(id="e_s1", type=EntryType.CLASS, startTime="14:00", endTime="15:30", subjectId="sub_single")
            ],
        ),
        Timeline(
            id="tl_double",
            dayOfWeek=[1],
            weeks=[2],  # 仅双周
            entries=[
                Entry(id="e_d1", type=EntryType.CLASS, startTime="14:00", endTime="15:30", subjectId="sub_double")
            ],
        ),
    ]

    cycle_schedule = ScheduleData(
        meta=MetaInfo(id="meta_cycle", startDate="2026-09-07", maxWeekCycle=2),
        subjects=subjects,
        days=days,
        overrides=[],
    )

    runtime = ScheduleRuntime(mock_central)

    # 1. 模拟第 1 周周一（单周）
    single_week_now = datetime(2026, 9, 7, 14, 10)
    setup_runtime(runtime, cycle_schedule, single_week_now)

    day_schedule_1 = runtime.sidebarDaySchedule
    assert len(day_schedule_1) == 1
    assert day_schedule_1[0]["subjectName"] == "单周实验课"
    assert day_schedule_1[0]["isCurrent"] is True

    # 2. 模拟第 2 周周一（双周）
    double_week_now = datetime(2026, 9, 14, 14, 10)
    setup_runtime(runtime, cycle_schedule, double_week_now)

    day_schedule_2 = runtime.sidebarDaySchedule
    assert len(day_schedule_2) == 1
    assert day_schedule_2[0]["subjectName"] == "双周研讨课"
    assert day_schedule_2[0]["isCurrent"] is True


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
    test_now = datetime(2026, 9, 9, 16, 30)  # 周三
    setup_runtime(runtime, act_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 1
    item = day_schedule[0]
    assert item["title"] == "院系辩论赛"
    assert item["subjectName"] == "院系辩论赛"
    assert item["type"] == "activity"
    assert item["isCurrent"] is True


# ============================================================================
# Tier 2: 边界值、极端情况与安全防御测试
# ============================================================================


def test_sidebar_model_null_schedule_safety(mock_central):
    """Tier 2 边界: runtime.schedule 为 None 时返回安全空数据，严禁抛出未捕获异常"""
    runtime = ScheduleRuntime(mock_central)
    setup_runtime(runtime, None, datetime(2026, 9, 7, 8, 30))

    day_sched = runtime.sidebarDaySchedule
    assert day_sched == []

    week_sched = runtime.sidebarWeekSchedule
    assert isinstance(week_sched, dict)
    assert "days" in week_sched
    for day_key in range(1, 8):
        assert week_sched["days"][str(day_key)] == []


def test_sidebar_model_empty_day_schedule(mock_central, standard_schedule):
    """Tier 2 边界: 周日没有任何排课，sidebarDaySchedule 返回空列表"""
    runtime = ScheduleRuntime(mock_central)
    sunday_now = datetime(2026, 9, 13, 10, 0)  # 周日
    setup_runtime(runtime, standard_schedule, sunday_now)

    assert runtime.sidebarDaySchedule == []


def test_sidebar_model_exact_boundary_start_time(mock_central, standard_schedule):
    """Tier 2 边界: 刚好在上课开始时刻（08:00:00），课程必须判定为当前课程且进度为 0.0"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 0, 0)  # 08:00:00 压线
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    first_lesson = day_schedule[0]
    assert first_lesson["isCurrent"] is True
    assert first_lesson["progress"] == 0.0


def test_sidebar_model_exact_boundary_end_time(mock_central, standard_schedule):
    """Tier 2 边界: 刚好在下课时刻（08:45:00），课程已不属于当前课程且进度为 1.0"""
    runtime = ScheduleRuntime(mock_central)
    test_now = datetime(2026, 9, 7, 8, 45, 0)  # 08:45:00 下课压线
    setup_runtime(runtime, standard_schedule, test_now)

    day_schedule = runtime.sidebarDaySchedule
    first_lesson = day_schedule[0]
    assert first_lesson["isCurrent"] is False
    assert first_lesson["progress"] == 1.0


def test_sidebar_model_zero_duration_entry(mock_central):
    """Tier 2 边界: 起止时间相同（例如 09:00 - 09:00）的异常数据，必须有除以零防御"""
    days = [
        Timeline(
            id="tl_zero",
            dayOfWeek=[1],
            weeks="all",
            entries=[
                Entry(
                    id="e_zero",
                    type=EntryType.CLASS,
                    startTime="09:00",
                    endTime="09:00",
                    subjectId=None,
                    title="零时长通知",
                )
            ],
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
        subjectId=None,
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
        "2026-09-12": 1  # 2026-09-12 是周六，调休为周一课表
    }

    runtime = ScheduleRuntime(mock_central)
    saturday_now = datetime(2026, 9, 12, 8, 20)  # 周六早上
    setup_runtime(runtime, standard_schedule, saturday_now)

    day_schedule = runtime.sidebarDaySchedule
    assert len(day_schedule) == 2
    assert day_schedule[0]["subjectName"] == "高等数学"
    assert day_schedule[0]["isCurrent"] is True


def test_sidebar_model_class_swap_support(mock_central, standard_schedule):
    """Tier 2 边界: 临时换课机制（class_swap）支持临时替换整天课表"""
    mock_central.configs.schedule.class_swap = {
        "date": "2026-09-07",  # 2026-09-07 周一换成周二的课表
        "day_of_week": 2,
        "week_of_cycle": 1,
    }

    runtime = ScheduleRuntime(mock_central)
    monday_now = datetime(2026, 9, 7, 10, 20)
    setup_runtime(runtime, standard_schedule, monday_now)

    day_schedule = runtime.sidebarDaySchedule
    # 原周一有 2 节课，换成周二后应只有 1 节课
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
            entries=[
                Entry(id="entry_ov_1", type=EntryType.CLASS, startTime="08:00", endTime="08:45", subjectId="sub_1")
            ],
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
