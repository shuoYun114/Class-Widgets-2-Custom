from datetime import datetime, timedelta, date
from typing import Optional, TYPE_CHECKING

from PySide6.QtCore import QObject, Property, Signal, Slot, QCoreApplication, QTimer
from loguru import logger

from src.core.notification import NotificationProvider, NotificationData, NotificationLevel
from src.core.schedule.model import ScheduleData, MetaInfo, Timeline, Entry, EntryType, Subject
from src.core.schedule.service import ScheduleServices
from src.core.utils import get_cycle_week, get_week_number

if TYPE_CHECKING:
    from src.core.central import AppCentral
    from src.core.notification import NotificationManager


class ScheduleRuntime(QObject):
    updated = Signal()  # 文件更新
    currentsChanged = Signal(EntryType)  # 日程更新

    def __init__(self, app_central: "AppCentral"):
        super().__init__()
        self.app_central: "AppCentral" = app_central
        # self.schedule_path = Path(schedule_path)
        self.schedule: Optional[ScheduleData] = None
        self.services: ScheduleServices = ScheduleServices(app_central)
        self._pending_schedule: Optional[ScheduleData] = None
        self._refresh_timer = QTimer(self)
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.setInterval(50)
        self._refresh_timer.timeout.connect(self._flush_scheduled_refresh)
        self.current_time = datetime.now()
        self.current_offset_time = datetime.now()

        self.current_day_of_week: int = 0
        self.current_week = 0
        self.current_week_of_cycle: int = 0
        self.time_offset = 0

        self.schedule_meta: Optional[MetaInfo] = None
        self.current_day: Optional[Timeline] = None
        self.previous_entry: Optional[Entry] = None
        self.current_entry: Optional[Entry] = None
        self.all_entries: Optional[list[Entry]] = None
        self.next_entries: Optional[list[Entry]] = None
        self.remaining_time: Optional[timedelta] = None
        self._progress: Optional[float] = None
        self.current_status: Optional[EntryType] = None

        self.current_subject: Optional[Subject] = None
        self.current_title: Optional[str] = None

        # Separate notification providers for different notification types
        self.class_notification_provider: Optional[NotificationProvider] = None
        self.activity_notification_provider: Optional[NotificationProvider] = None
        self.break_notification_provider: Optional[NotificationProvider] = None
        self.free_notification_provider: Optional[NotificationProvider] = None
        self.preparation_bell_provider: Optional[NotificationProvider] = None
        
        self._register_notification_providers()

        # 连接到retranslate信号，在翻译加载后更新通知提供者名称
        app_central.retranslate.connect(self._on_retranslate)

    def _register_notification_providers(self) -> None:
        """注册不同类型的通知提供者，确保在翻译加载后执行"""
        if self.class_notification_provider is not None:
            return
            
        # Class notifications
        self.class_notification_provider = NotificationProvider(
            id="com.classwidgets.schedule.runtime.class",
            name=QCoreApplication.translate("NotificationProviders", "Class Notifications"),
            icon="ic_fluent_book_clock_20_regular",
            manager=self.app_central.notification,
            use_system_notify=True
        )
        
        # Activity notifications  
        self.activity_notification_provider = NotificationProvider(
            id="com.classwidgets.schedule.runtime.activity",
            name=QCoreApplication.translate("NotificationProviders", "Activity Notifications"),
            icon="ic_fluent_broad_activity_feed_20_regular",
            manager=self.app_central.notification,
            use_system_notify=True
        )
        
        # Break/Recess notifications
        self.break_notification_provider = NotificationProvider(
            id="com.classwidgets.schedule.runtime.break",
            name=QCoreApplication.translate("NotificationProviders", "Break Notifications"),
            icon="ic_fluent_drink_coffee_20_regular",
            manager=self.app_central.notification,
            use_system_notify=True
        )
        
        # Free time notifications
        self.free_notification_provider = NotificationProvider(
            id="com.classwidgets.schedule.runtime.free",
            name=QCoreApplication.translate("NotificationProviders", "Free Time Notifications"),
            icon="ic_fluent_person_running_20_regular",
            manager=self.app_central.notification,
            use_system_notify=True
        )
        
        # Preparation bell notifications
        self.preparation_bell_provider = NotificationProvider(
            id="com.classwidgets.schedule.runtime.preparation",
            name=QCoreApplication.translate("NotificationProviders", "Preparation Bell"),
            icon="ic_fluent_alert_urgent_20_regular",
            manager=self.app_central.notification,
            use_system_notify=True
        )

    @Slot()
    def _on_retranslate(self) -> None:
        """处理翻译信号，重新注册通知提供者"""
        # Unregister all existing providers
        providers = [
            "com.classwidgets.schedule.runtime.class",
            "com.classwidgets.schedule.runtime.activity", 
            "com.classwidgets.schedule.runtime.break",
            "com.classwidgets.schedule.runtime.free",
            "com.classwidgets.schedule.runtime.preparation"
        ]
        
        for provider_id in providers:
            self.app_central.notification.unregister_provider(provider_id)
            
        # Reset all providers to None
        self.class_notification_provider = None
        self.activity_notification_provider = None
        self.break_notification_provider = None
        self.free_notification_provider = None
        self.preparation_bell_provider = None
            
        # Re-register all providers with new translations
        self._register_notification_providers()

    # TIME
    @Property(str, notify=updated)
    def currentTime(self) -> str:
        return self.current_time.strftime("%H:%M:%S")

    @Property(int, notify=updated)
    def currentDayOfWeek(self) -> int:
        return self.current_day_of_week

    @Property(dict, notify=updated)
    def currentDate(self) -> dict:
        return { "year": self.current_time.year, "month": self.current_time.month, "day": self.current_time.day }

    @Property(int, notify=updated)
    def currentWeek(self) -> int:
        return self.current_week

    @Property(int, notify=updated)
    def currentWeekOfCycle(self) -> int:
        return self.current_week_of_cycle

    # SCHEDULE
    @Property(list, notify=updated)
    def subjects(self) -> list:
        if not self.schedule:
            return []
        return [s.model_dump() for s in self.schedule.subjects]

    @Property(dict, notify=updated)
    def scheduleMeta(self) -> dict:
        if self.schedule_meta is None:
            return {}
        return self.schedule_meta.model_dump()

    @Property(list, notify=updated)
    def currentDayEntries(self) -> list:  # 当前的日程
        if not self.current_day:
            return []
        return [entry.model_dump() for entry in self.current_day.entries]

    @Property(dict, notify=updated)
    def currentEntry(self) -> dict:
        return self.current_entry.model_dump() if self.current_entry else {}

    @Property(list, notify=updated)
    def nextEntries(self) -> list:  # 接下来的日程
        if not self.next_entries:
            return []
        return [entry.model_dump() for entry in self.next_entries]

    @Property(int, notify=updated)
    def timeOffset(self) -> int:
        return self.time_offset

    @Property(dict, notify=updated)
    def remainingTime(self) -> dict:
        if not self.remaining_time:
            return {
                "minute": 0,
                "second": 0
            }
        result = {
            "minute": self.remaining_time.seconds // 60,
            "second": self.remaining_time.seconds % 60
        }
        return result

    @Property(float, notify=updated)
    def progress(self) -> float:
        if not self._progress:
            return 0.0
        return self._progress

    @Property(str, notify=updated)
    def currentStatus(self) -> str:
        if not self.current_status:
            return EntryType.FREE.value
        return self.current_status.value

    # SUBJECT
    @Property(dict, notify=updated)
    def currentSubject(self) -> dict:
        return self.current_subject.model_dump() if self.current_subject else {}

    @Property(str, notify=updated)
    def currentTitle(self) -> str:
        return self.current_title or ""

    def _format_sidebar_entry(
        self,
        entry: Entry,
        entry_date: date,
        now: datetime,
        current_entry_id: Optional[str] = None,
    ) -> dict:
        """
        组装符合 PROJECT.md 契约的扁平化课程信息字典
        """
        subject = None
        if entry.subjectId and self.schedule and self.schedule.subjects:
            for s in self.schedule.subjects:
                if s.id == entry.subjectId:
                    subject = s
                    break

        subject_name = subject.name if subject else (entry.title or "")
        title = entry.title or (subject.name if subject else "")
        teacher = subject.teacher if (subject and subject.teacher) else ""
        location = subject.location if (subject and subject.location) else ""
        color = subject.color if (subject and subject.color) else "#4A90E2"
        entry_type = entry.type.value if hasattr(entry.type, "value") else str(entry.type)
        time_range = f"{entry.startTime} - {entry.endTime}"

        is_current = False
        progress = 0.0

        try:
            start_time = datetime.strptime(entry.startTime, "%H:%M").time()
            end_time = datetime.strptime(entry.endTime, "%H:%M").time()
            start_dt = datetime.combine(entry_date, start_time)
            end_dt = datetime.combine(entry_date, end_time)
        except Exception:
            start_dt = None
            end_dt = None

        if entry_date == now.date():
            if current_entry_id and entry.id == current_entry_id:
                is_current = True
                progress = float(self._progress if self._progress is not None else self.get_progress_percent())
            elif start_dt and end_dt:
                if now < start_dt:
                    is_current = False
                    progress = 0.0
                elif now >= end_dt:
                    is_current = False
                    progress = 1.0
                else:
                    is_current = True
                    total = (end_dt - start_dt).total_seconds()
                    progress = round((now - start_dt).total_seconds() / total, 2) if total > 0 else 1.0
        elif entry_date < now.date():
            is_current = False
            progress = 1.0
        else:
            is_current = False
            progress = 0.0

        return {
            "id": entry.id,
            "title": title,
            "startTime": entry.startTime,
            "endTime": entry.endTime,
            "timeRange": time_range,
            "subjectName": subject_name,
            "teacher": teacher,
            "location": location,
            "color": color,
            "isCurrent": is_current,
            "progress": float(progress),
            "type": entry_type,
        }

    # SIDEBAR SCHEDULE
    @Property(list, notify=updated)
    def sidebarDaySchedule(self) -> list[dict]:
        """
        R1: 右侧边缘当天课表扁平数据列表，包含起止时间范围、教室、教师、主题色、当前课程高亮标记与进度。
        """
        if not self.schedule or not self.current_day:
            return []

        now = self.current_offset_time
        entries = self.services.get_all_entries(self.current_day)
        curr_id = self.current_entry.id if self.current_entry else None

        return [
            self._format_sidebar_entry(entry, now.date(), now, curr_id)
            for entry in entries
        ]

    @Property(dict, notify=updated)
    def sidebarWeekSchedule(self) -> dict:
        """
        R3: 全周课表 7 天网格矩阵聚合数据，以 1-7 为键映射周一至周日全量课程列表。
        """
        now = self.current_offset_time
        curr_weekday = self.current_day_of_week or now.isoweekday()
        today_date = now.date()

        days_data = {}
        if not self.schedule:
            for day_idx in range(1, 8):
                days_data[str(day_idx)] = []
            return {
                "currentDayOfWeek": curr_weekday,
                "days": days_data,
            }

        curr_id = self.current_entry.id if self.current_entry else None
        monday_date = today_date - timedelta(days=curr_weekday - 1)

        for day_idx in range(1, 8):
            target_date = monday_date + timedelta(days=day_idx - 1)
            target_dt = datetime.combine(target_date, now.time())
            day_timeline = self.services.get_day_entries(self.schedule, target_dt)
            if not day_timeline:
                days_data[str(day_idx)] = []
                continue

            entries = self.services.get_all_entries(day_timeline)
            days_data[str(day_idx)] = [
                self._format_sidebar_entry(entry, target_date, now, curr_id)
                for entry in entries
            ]

        return {
            "currentDayOfWeek": curr_weekday,
            "days": days_data,
        }

    def refresh(self, schedule: Optional[ScheduleData] = None) -> None:
        self._refresh_timer.stop()
        if schedule is None:
            if self.schedule is None:
                return
            schedule = self.schedule
        self._update_schedule(schedule)
        self._update_time()
        self._update_notify()
        self.updated.emit()

    def schedule_refresh(self, schedule: ScheduleData) -> None:
        """合并连续的课表编辑通知，避免编辑器拖动时同步重算运行时状态。"""
        self._pending_schedule = schedule
        self._refresh_timer.start()

    def _flush_scheduled_refresh(self) -> None:
        schedule = self._pending_schedule
        self._pending_schedule = None
        if schedule is not None:
            self.refresh(schedule)

    def _update_schedule(self, schedule: Optional[ScheduleData]) -> None:
        """
        更新日程
        :param schedule:
        :return:
        """
        self.time_offset = self.app_central.configs.schedule.time_offset  # 时间偏移
        self.current_time = datetime.now()
        self.current_offset_time = self.current_time + timedelta(seconds=self.time_offset)  # 内部计算时间
        self.schedule = schedule or self.schedule
        self.schedule_meta = self.schedule.meta
        self.current_day = self.services.get_day_entries(self.schedule, self.current_offset_time)

        if self.current_day:
            self.current_entry = self.services.get_current_entry(self.current_day, self.current_offset_time)
            self.all_entries = self.services.get_all_entries(self.current_day)
            self.next_entries = self.services.get_next_entries(self.current_day, self.current_offset_time)
            self.remaining_time = self.services.get_remaining_time(self.current_day, self.current_offset_time)
            self.current_status = self.services.get_current_status(self.current_day, self.current_offset_time, self.app_central.configs.schedule.preparation_time)
            self.current_subject = self.services.get_current_subject(self.current_day, self.schedule.subjects,
                                                                     self.current_offset_time)
            self.current_title = getattr(self.current_entry, "title", None)
        else:
            self.current_entry = None
            self.all_entries = None
            self.next_entries = None
            self.remaining_time = None
            self.current_status = EntryType.FREE
            self.current_subject = None
            self.current_title = None

        self._progress = self.get_progress_percent()
        if self.previous_entry != self.current_entry:
            self.currentsChanged.emit(self.current_status)

    def _update_time(self) -> None:  # 更新时间
        self.current_day_of_week = self.current_offset_time.isoweekday()
        self.current_week = get_week_number(self.schedule.meta.startDate, self.current_offset_time)
        self.current_week_of_cycle = get_cycle_week(self.current_week, self.schedule.meta.maxWeekCycle)

    def get_progress_percent(self) -> float:
        if not self.current_entry:  # 空
            return 1

        now = self.current_offset_time
        start = datetime.combine(now.date(), datetime.strptime(self.current_entry.startTime, "%H:%M").time())
        end = datetime.combine(now.date(), datetime.strptime(self.current_entry.endTime, "%H:%M").time())

        if now <= start: return 0
        if now >= end: return 1
        return round((now - start).total_seconds() / (end - start).total_seconds(), 2)

    def _update_notify(self) -> None:
        if self.previous_entry != self.current_entry:
            self.previous_entry = self.current_entry
            status = self.current_status.value
            
            # Main status change notification
            if status == EntryType.CLASS.value:
                title = QCoreApplication.translate("ScheduleRuntime", "Class Started")
                message = None
                
                # Prioritize title over subject, skip if neither exists
                entry_title = getattr(self.current_entry, 'title', None)
                if entry_title:
                    message = entry_title
                elif self.current_subject:
                    subject_name = getattr(self.current_subject, 'name', '')
                    if subject_name:
                        message = subject_name
                        # Add teacher info if available
                        teacher = getattr(self.current_subject, 'teacher', None)
                        if teacher:
                            message += f" —— {teacher}"
                    
            elif status == EntryType.ACTIVITY.value:
                title = QCoreApplication.translate("ScheduleRuntime", "Activity Started")
                message = None
                
                # Activity only uses title, skip if no title
                entry_title = getattr(self.current_entry, 'title', None)
                if entry_title:
                    message = entry_title
                    
            elif status == EntryType.PREPARATION.value and self.next_entries:
                 title = QCoreApplication.translate("ScheduleRuntime", "Intermission")
                 message = None
                 
                 try:
                     next_entry = self.next_entries[0]
                     subject_dict = None
                     
                     if self.schedule and hasattr(self.schedule, 'subjects') and self.schedule.subjects:
                         sub = self.services.get_subject(next_entry.subjectId, self.schedule.subjects)
                         if sub:
                             subject_dict = sub.model_dump() if hasattr(sub, 'model_dump') else sub.__dict__
                     
                     if subject_dict and 'name' in subject_dict:
                         subject_name = subject_dict['name']
                         is_local = subject_dict.get('isLocalClassroom', True)
                         
                         if is_local:
                             message = QCoreApplication.translate("ScheduleRuntime", "Next: {}").format(subject_name)
                         else:
                             location = subject_dict.get('location', '')
                             if location:
                                 message = QCoreApplication.translate("ScheduleRuntime", "Next: {} at {}").format(subject_name, location)
                             else:
                                 message = QCoreApplication.translate("ScheduleRuntime", "Next: {} (Off-site)").format(subject_name)
                     else:
                         next_title = getattr(next_entry, 'title', '')
                         if next_title:
                             message = QCoreApplication.translate("ScheduleRuntime", "Next: {}").format(next_title)
                         
                 except (IndexError, AttributeError, TypeError) as e:
                     logger.warning(f"Error preparing preparation notification: {e}")
                     # Skip notification if we can't get proper information
                     message = None
                    
            elif status == EntryType.BREAK.value:
                 title = QCoreApplication.translate("ScheduleRuntime", "Recess")
                 
                 if self.next_entries:
                     message = None
                     try:
                         next_entry = self.next_entries[0]
                         subject_dict = None
                         
                         if self.schedule and hasattr(self.schedule, 'subjects') and self.schedule.subjects:
                             sub = self.services.get_subject(next_entry.subjectId, self.schedule.subjects)
                             if sub:
                                 subject_dict = sub.model_dump() if hasattr(sub, 'model_dump') else sub.__dict__
                         
                         if subject_dict and 'name' in subject_dict:
                             subject_name = subject_dict['name']
                             is_local = subject_dict.get('isLocalClassroom', True)
                             
                             if is_local:
                                 message = QCoreApplication.translate("ScheduleRuntime", "Next: {}").format(subject_name)
                             else:
                                 location = subject_dict.get('location', '')
                                 if location:
                                     message = QCoreApplication.translate("ScheduleRuntime", "Next: {} at {}").format(subject_name, location)
                                 else:
                                     message = QCoreApplication.translate("ScheduleRuntime", "Next: {} (Off-site)").format(subject_name)
                         else:
                             next_title = getattr(next_entry, 'title', '')
                             if next_title:
                                 message = QCoreApplication.translate("ScheduleRuntime", "Next: {}").format(next_title)
                             
                     except (IndexError, AttributeError, TypeError) as e:
                         logger.warning(f"Error preparing break notification: {e}")
                         # Skip notification if we can't get proper information
                         message = None
                 else:
                     message = QCoreApplication.translate("ScheduleRuntime", "Enjoy your break")
                    
            elif status == EntryType.FREE.value:
                title = QCoreApplication.translate("ScheduleRuntime", "Free Time")
                message = None  # Free time doesn't need message
                
            else:
                # Fallback for other statuses
                title = QCoreApplication.translate("ScheduleRuntime", "Status Changed")
                message = QCoreApplication.translate("ScheduleRuntime", "Current status: {}").format(status)
            
            try:
                # Choose appropriate notification provider based on status
                if status == EntryType.CLASS.value:
                    provider = self.class_notification_provider
                elif status == EntryType.ACTIVITY.value:
                    provider = self.activity_notification_provider
                elif status in {EntryType.PREPARATION.value, EntryType.BREAK.value}:
                    provider = self.break_notification_provider
                elif status == EntryType.FREE.value:
                    provider = self.free_notification_provider
                else:
                    provider = self.class_notification_provider  # fallback
                
                if provider:
                    data = NotificationData(
                        provider_id=provider.id,
                        level=NotificationLevel.ANNOUNCEMENT,
                        title=title,
                        message=message,
                        duration=5000,
                        closable=True
                    )
                    
                    cfg = provider.get_config()
                    provider.manager.dispatch(data, cfg)
                
            except Exception as e:
                logger.error(f"Failed to dispatch status notification: {e}")

        # Preparation bell notification
        if (
            self.next_entries and len(self.next_entries) > 0 and
            self.current_status == EntryType.PREPARATION
        ):
            try:
                next_entry = self.next_entries[0]
                next_start = datetime.strptime(next_entry.startTime, "%H:%M")
                next_start = datetime.combine(self.current_offset_time.date(), next_start.time())
                prep_min = getattr(self.app_central.configs.schedule, 'preparation_time', 2) or 2

                if next_start - timedelta(minutes=prep_min) == self.current_offset_time.replace(microsecond=0):
                    subject_dict = None
                    if self.schedule and hasattr(self.schedule, 'subjects') and self.schedule.subjects:
                        sub = self.services.get_subject(next_entry.subjectId, self.schedule.subjects)
                        if sub:
                            subject_dict = sub.model_dump() if hasattr(sub, 'model_dump') else sub.__dict__
                    
                    if subject_dict and 'name' in subject_dict:
                        subject_name = subject_dict['name']
                        is_local = subject_dict.get('isLocalClassroom', True)
                        
                        if is_local:
                            message = QCoreApplication.translate("ScheduleRuntime", "Coming up: {}").format(subject_name)
                        else:
                            location = subject_dict.get('location', '')
                            if location:
                                message = QCoreApplication.translate("ScheduleRuntime", "Coming up: {} at {}").format(subject_name, location)
                            else:
                                message = QCoreApplication.translate("ScheduleRuntime", "Coming up: {} (Off-site)").format(subject_name)
                    else:
                        next_title = getattr(next_entry, 'title', '')
                        if next_title:
                            message = QCoreApplication.translate("ScheduleRuntime", "Coming up: {}").format(next_title)
                        else:
                            message = None
                    
                    if self.preparation_bell_provider:
                        data = NotificationData(
                            provider_id=self.preparation_bell_provider.id,
                            level=NotificationLevel.ANNOUNCEMENT,
                            title=QCoreApplication.translate("ScheduleRuntime", "Preparation Bell"),
                            message=message,
                            duration=5000,
                            closable=True
                        )
                        
                        cfg = self.preparation_bell_provider.get_config()
                        self.preparation_bell_provider.manager.dispatch(data, cfg)
                    
            except (ValueError, AttributeError, TypeError, IndexError) as e:
                logger.warning(f"Error preparing preparation bell notification: {e}")

