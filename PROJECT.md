# Project: Class-Widgets-2 屏幕右侧边缘侧边课表栏 (Sidebar Schedule)

## Architecture
本功能为 Class-Widgets-2 引入常驻屏幕右侧边缘的极简侧边课表栏系统，深度整合 PySide6 原生窗口遮罩与 QML Fluent 响应式动效：
1. **渲染层 (QML)**:
   - 挂载于 `src/qml/MainInterface.qml`，作为全屏置顶窗口 `QQW.Window` 的顶层子组件，`objectName: "scheduleSidebar"`。
   - 内部由状态机管理 3 种显示状态：
     - `NORMAL`: 当天竖条常驻，左侧支持悬浮双按钮滑出与 300ms 缓冲防误触。
     - `EXPANDED`: 点击展开全周课表大面板，向左平滑展开，支持外部点击透明区域收回。
     - `COLLAPSED`: 竖条完全隐藏，屏幕右边缘显示微型贴边小胶囊按钮（`<` 图标），靠近高亮，点击呼出。
2. **数据与桥接层 (Python)**:
   - 扩展 `src/core/schedule/runtime.py` (`ScheduleRuntime`)，提供响应式属性 `sidebarDaySchedule`（当天扁平课表，包含起止时间范围、教室、教师、主题色、当前课程高亮标记 `isCurrent`、进度）与 `sidebarWeekSchedule`（整周 7 天课程网格矩阵）。
   - 依托 `UnionUpdateTimer` 1Hz 心跳驱动 `refresh()` 与数据自动更新。
3. **窗口交互与遮罩层 (PySide6 & Win32 Mask)**:
   - `src/core/widgets/core.py` (`WidgetsWindow.update_mask`): 收集桌面小组件容器、悬浮组件以及 `scheduleSidebar` 的当前有效交互矩形，生成 `QRegion` 并调用 `root_window.setMask(mask)`。
   - 除可见且处于激活态的交互组件外，全屏透明背景实现 100% 鼠标点击穿透。
   - 在全周大面板展开或菜单显示时，动态切换遮罩以支撑全局外部点击收回。
4. **配置与持久化层 (ConfigManager)**:
   - 扩展 `src/core/config/model.py` (`PreferencesConfig`)，增加 `schedule_sidebar_enabled` (默认 True) 和 `schedule_sidebar_collapsed` (默认 False)。
   - 在设置中心 `src/qml/ClassWidgets/pages/settings/General/Widgets.qml` 增加独立开关卡片，支持用户控制与状态持久化记忆。

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F1 | 当天课表竖条胶囊主体 (R1) | 深灰色半透明极简胶囊，宽度 140~180px，支持平滑滚动，贴合屏幕右侧垂直居中 | M1 | ORIGINAL_REQUEST §1 |
| F2 | 当前课程状态与高亮 (R1) | 自动识别当前时间所属课程并高亮突出显示，课间展示倒计时/预备状态 | M1 | ORIGINAL_REQUEST §1 |
| F3 | 课程悬浮气泡卡片 (R1) | 鼠标悬浮在任一课程条目上时，弹出悬浮卡片展示完整起止时间、教室、教师信息 | M1 | ORIGINAL_REQUEST §1 |
| F4 | 悬浮双按钮滑出与收起 (R2) | 鼠标移入竖条左侧区域时，平滑滑出“展开全周大面板”与“收起隐藏竖条”两个快捷操作按钮 | M2 | ORIGINAL_REQUEST §2 |
| F5 | 防误触延时缓冲机制 (R2) | 鼠标移出按钮与竖条后，保留 300ms 防误触缓冲期后再执行淡出收回动画 | M2 | ORIGINAL_REQUEST §2 |
| F6 | 全周课表网格大面板 (R3) | 点击上方展开按钮向左平滑展开整周网格矩阵课表大面板，直观呈现周一到周日课程 | M3 | ORIGINAL_REQUEST §3 |
| F7 | 外部点击与单一收回交互 (R3) | 大面板展开状态下，左侧操作区变为单一收回按钮；点击大面板外桌面空白区域自动平滑收回 | M3 | ORIGINAL_REQUEST §3 |
| F8 | 隐藏收起与贴边呼出小胶囊 (R4) | 点击下方收起按钮竖条完全隐藏，屏幕右侧边缘显示带 `<` 向左图标的贴边小胶囊 | M4 | ORIGINAL_REQUEST §4 |
| F9 | 贴边小胶囊高亮与呼出恢复 (R4) | 贴边小胶囊平时高透明度弱化视觉干扰，光标靠近时动态高亮，点击平滑恢复当天竖条 | M4 | ORIGINAL_REQUEST §4 |
| F10 | WidgetsWindow 遮罩穿透 (R5) | 更新 setMask 逻辑，精准计算侧边栏各状态可见区域，确保非交互区 100% 鼠标点击穿透 | M5 | ORIGINAL_REQUEST §5 |
| F11 | 设置中心配置与状态记忆 (R5) | 在 Settings 中增加独立启用开关，并对折叠/展开状态进行配置文件持久化记忆 | M5 | ORIGINAL_REQUEST §5 |

---

## Milestones
| # | Name | Scope | Dependencies | Status | Output |
|---|------|-------|-------------|--------|--------|
| M1 | R1: 当天课表竖条与数据模型 | Python 数据聚合属性 (sidebarDaySchedule) + DailyScheduleBar.qml + 课程高亮与悬浮气泡卡片 | none | DONE | commit `abbd682`, `3040de0` |
| M2 | R2: 悬浮双按钮交互与防误触缓冲 | SidebarHoverButtons.qml + 300ms 计时器防抖缓冲 + 弹性平滑进出动效 | M1 | DONE | commit `dd7424a` |
| M3 | R3: 全周课表大面板展开与收回 | Python 整周矩阵聚合 (sidebarWeekSchedule) + WeeklySchedulePanel.qml + 单一收回按钮 + 外部点击区域穿透/捕获收回 | M1, M2 | DONE | commit `dfb441f` |
| M4 | R4: 隐藏收起与边缘贴边呼出按钮 | EdgeRestoreCapsule.qml + 折叠隐藏状态机切换 + 贴边胶囊靠近高亮与点击恢复 | M1, M2 | DONE | commit `5db4add` |
| M5 | R5: 屏幕穿透遮罩与配置持久化 | WidgetsWindow.update_mask 适配 + PreferencesConfig 字段 + Settings.qml 开关与状态记忆 | M1, M2, M3, M4 | DONE | commit `448b0a3` |
| M-Final | 最终集成与 E2E 验收通过 | 执行 100% 自动化与集成测试，覆盖 R1-R5 边界场景与白盒审查 | M1, M2, M3, M4, M5 | DONE | 157 passed, 5方独立门禁 PASS (CLEAN) |

---

## Interface Contracts
### 1. Python (`ScheduleRuntime`) ↔ QML (`DailyScheduleBar.qml`, `WeeklySchedulePanel.qml`)
- **`sidebarDaySchedule: list[dict]`**:
  ```python
  [
      {
          "id": str,
          "title": str,
          "startTime": str,       # "08:00"
          "endTime": str,         # "08:45"
          "timeRange": str,       # "08:00 - 08:45"
          "subjectName": str,     # "高等数学"
          "teacher": str,         # "张教授"
          "location": str,        # "教三 101"
          "color": str,           # "#4A90E2"
          "isCurrent": bool,      # 当前是否正在上此课
          "progress": float,      # 0.0 ~ 1.0 (课程进度)
          "type": str             # "CLASS" | "ACTIVITY"
      }, ...
  ]
  ```
- **`sidebarWeekSchedule: dict`**:
  ```python
  {
      "currentDayOfWeek": int,    # 1 ~ 7
      "days": {
          "1": [ { ...entry }, ... ],
          "2": [ { ...entry }, ... ],
          ...
          "7": [ ... ]
      }
  }
  ```

### 2. QML (`ScheduleSidebar.qml`) ↔ Python (`WidgetsWindow`)
- **`objectName`**: `"scheduleSidebar"`
- **状态属性**:
  - `sidebarState`: `"NORMAL"` | `"EXPANDED"` | `"COLLAPSED"`
  - `interactiveRects`: 返回当前可见交互组件在窗口内的相对坐标列表 `[ [x, y, w, h], ... ]`
  - `isFullWeekExpanded`: `bool`，为 true 时 Python 触发临时全屏遮罩以支持外部点击收回
- **信号**:
  - `geometryChanged()`: 任何位置、尺寸、展开/折叠、气泡或按钮滑出滑入均发射此信号，触发 Python 帧级防抖 `schedule_mask_update()`。

### 3. 配置管理 (`ConfigManager` ↔ QML `Settings.qml`)
- **键路径**:
  - `preferences.schedule_sidebar_enabled`: `bool`，默认 `True`（侧边栏启用总开关）。
  - `preferences.schedule_sidebar_collapsed`: `bool`，默认 `False`（贴边折叠状态）。
  - `preferences.schedule_sidebar_edge`: `str`，默认 `"right"`（贴靠屏幕边缘，`"right"` | `"left"`）。
  - `preferences.schedule_sidebar_offset_y`: `int`，默认 `0`（垂直居中偏移量微调，`-500 ~ 500 px`）。
  - `preferences.schedule_sidebar_custom_appearance`: `bool`，默认 `False`（是否启用侧边栏独立外观）。
  - `preferences.schedule_sidebar_corner_radius`: `float`，默认 `22.0`（侧边栏独立圆角半径）。
  - `preferences.schedule_sidebar_opacity`: `float`，默认 `1.0`（侧边栏独立背景不透明度）。
- **调用接口**:
  - 读取: `Configs.data.preferences.schedule_sidebar_enabled`
  - 写入: `Configs.set("preferences.schedule_sidebar_enabled", val)`

---

## Code Layout
```
src/
├── core/
│   ├── config/
│   │   └── model.py                  # 扩展 PreferencesConfig (schedule_sidebar_enabled/collapsed)
│   ├── schedule/
│   │   └── runtime.py                # 扩展 sidebarDaySchedule / sidebarWeekSchedule 响应式属性
│   └── widgets/
│       └── core.py                   # 更新 update_mask 计算 scheduleSidebar 的动态 QRegion
└── qml/
    ├── MainInterface.qml             # 挂载 ScheduleSidebar 顶层实例 (z: 1100)
    └── ClassWidgets/
        ├── Components/
        │   └── sidebar/
        │       ├── ScheduleSidebar.qml       # 侧边栏总控容器、状态机与外部点击遮罩
        │       ├── DailyScheduleBar.qml      # R1: 当天课表竖条胶囊与平滑滚动、气泡
        │       ├── SidebarHoverButtons.qml   # R2: 悬浮双按钮与 300ms 延时缓冲
        │       ├── WeeklySchedulePanel.qml   # R3: 全周网格矩阵大面板
        │       └── EdgeRestoreCapsule.qml    # R4: 边缘 `<` 贴边小胶囊呼出按钮
        └── pages/
            └── settings/
                └── General/
                    └── Widgets.qml           # R5: 添加侧边栏启用开关卡片
tests/
└── e2e/
    ├── test_sidebar_model.py         # 数据模型与整周矩阵单测
    ├── test_sidebar_mask.py          # 遮罩计算与穿透测试
    └── test_sidebar_config.py        # 配置读写与持久化验证
```
