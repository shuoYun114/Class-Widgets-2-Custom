# -*- coding: utf-8 -*-
"""
测试侧边栏课表数据聚合接口 (sidebarDaySchedule 与 sidebarWeekSchedule)
"""
import sys
from datetime import datetime
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
    WeekType,
)
from src.core.schedule.runtime import ScheduleRuntime


@pytest.fixture(scope="session")
def qapp():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


@pytest.fixture
def mock_central(qapp):
    central = MagicMock()
    central.configs.schedule.time_offset = 0
    central.configs.schedule.preparation_time = 2
    central.configs.schedule.reschedule_day = {}
    central.configs.schedule.class_swap = None
    central.notification = MagicMock()
    return central


@pytest.fixture
def sample_schedule():
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
            id="sub_cs",
            name="计算机科学",
            simplifiedName="计科",
            teacher="李老师",
            location="实验楼 204",
            color="#50E3C2",
        ),
    ]

    entries_day1 = [
        Entry(
            id="entry_1",
            type=EntryType.CLASS,
            startTime="08:00",
            endTime="08:45",
            subjectId="sub_math",
            title=None,
        ),
        Entry(
            id="entry_2",
            type=EntryType.CLASS,
            startTime="09:00",
            endTime="09:45",
            subjectId="sub_cs",
            title=None,
        ),
    ]

    entries_day2 = [
        Entry(
            id="entry_3",
            type=EntryType.CLASS,
            startTime="10:00",
            endTime="10:45",
            subjectId="sub_math",
            title=None,
        ),
    ]

    days = [
        Timeline(
            id="timeline_1",
            dayOfWeek=[1],
            weeks=WeekType.ALL,
            entries=entries_day1,
        ),
        Timeline(
            id="timeline_2",
            dayOfWeek=[2],
            weeks=WeekType.ALL,
            entries=entries_day2,
        ),
    ]

    meta = MetaInfo(
        id="meta_1",
        startDate="2026-09-01",
        maxWeekCycle=1,
    )

    return ScheduleData(
        meta=meta,
        subjects=subjects,
        days=days,
        overrides=[],
    )


def test_sidebar_day_schedule_structure(mock_central, sample_schedule):
    """验证 sidebarDaySchedule 返回数据结构与字段类型"""
    runtime = ScheduleRuntime(mock_central)
    # 模拟当前时间为周一 08:30 (在第一节课中)
    now = datetime(2026, 9, 7, 8, 30)  # 2026-09-07 是周一
    runtime.current_time = now
    runtime.current_offset_time = now
    runtime.current_day_of_week = 1

    runtime.schedule = sample_schedule
    runtime.current_day = runtime.services.get_day_entries(sample_schedule, now)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, now)
    runtime._progress = runtime.get_progress_percent()
    day_schedule = runtime.sidebarDaySchedule

    assert isinstance(day_schedule, list)
    assert len(day_schedule) == 2

    first = day_schedule[0]
    assert first["id"] == "entry_1"
    assert first["subjectName"] == "高等数学"
    assert first["teacher"] == "张教授"
    assert first["location"] == "教三 101"
    assert first["color"] == "#4A90E2"
    assert first["startTime"] == "08:00"
    assert first["endTime"] == "08:45"
    assert first["timeRange"] == "08:00 - 08:45"
    assert first["type"] == "class"
    assert first["isCurrent"] is True
    assert 0.0 <= first["progress"] <= 1.0

    second = day_schedule[1]
    assert second["id"] == "entry_2"
    assert second["subjectName"] == "计算机科学"
    assert second["isCurrent"] is False
    assert second["progress"] == 0.0


def test_sidebar_week_schedule_matrix(mock_central, sample_schedule):
    """验证 sidebarWeekSchedule 整周矩阵结构"""
    runtime = ScheduleRuntime(mock_central)
    now = datetime(2026, 9, 7, 8, 30)  # 周一
    runtime.current_time = now
    runtime.current_offset_time = now
    runtime.current_day_of_week = 1
    runtime.schedule = sample_schedule

    week_schedule = runtime.sidebarWeekSchedule
    assert isinstance(week_schedule, dict)
    assert "currentDayOfWeek" in week_schedule
    assert "days" in week_schedule
    assert set(week_schedule["days"].keys()) == {"1", "2", "3", "4", "5", "6", "7"}

    # 周一有 2 门课
    assert len(week_schedule["days"]["1"]) == 2
    # 周二有 1 门课
    assert len(week_schedule["days"]["2"]) == 1
    # 周三无课
    assert len(week_schedule["days"]["3"]) == 0


def test_sidebar_empty_schedule(mock_central):
    """验证空课表时 sidebarDaySchedule 与 sidebarWeekSchedule 的鲁棒性"""
    runtime = ScheduleRuntime(mock_central)
    runtime.schedule = None
    runtime.current_day = None

    assert runtime.sidebarDaySchedule == []
    week = runtime.sidebarWeekSchedule
    assert isinstance(week, dict)
    assert len(week["days"]) == 7
    for day_list in week["days"].values():
        assert day_list == []


def test_sidebar_completed_day(mock_central, sample_schedule):
    """验证一天课程全部结束后的进度与高亮标记"""
    runtime = ScheduleRuntime(mock_central)
    # 模拟周一晚上 21:00 (所有课均已结束)
    now = datetime(2026, 9, 7, 21, 0)
    runtime.current_time = now
    runtime.current_offset_time = now
    runtime.current_day_of_week = 1

    runtime.schedule = sample_schedule
    runtime.current_day = runtime.services.get_day_entries(sample_schedule, now)
    runtime.current_entry = runtime.services.get_current_entry(runtime.current_day, now)
    day_schedule = runtime.sidebarDaySchedule

    assert len(day_schedule) == 2
    for entry in day_schedule:
        assert entry["isCurrent"] is False
        assert entry["progress"] == 1.0
