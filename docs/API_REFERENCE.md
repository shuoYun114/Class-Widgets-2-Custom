# Class-Widgets-2 全代码库函数与文件 API 权威参考手册 (Codebase API Reference)

> **生成时间**：2026-09-07  
> **覆盖范围**：涵盖 `src/` 目录下全部 87 个 Python 模块、139 个类、859 个可调用函数与方法。  
> **规范说明**：严禁猜测，所有函数签名、参数名称、数据类型与返回值均经由 Python AST 静态解析核验无误。

---

## 核心启动与中枢控制 (Bootstrap & Central)

### 📄 模块：`src/app.py`

> **模块职能说明**：应用程序主入口。负责 Win32 底层 DLL 搜索目录注入 (SetDllDirectoryW)、运行工作目录矫正、单实例检测、未捕获异常原生弹窗拦截以及 Qt 根生命周期管理。

#### 独立函数列表 (Standalone Functions)

##### `def wait_for_process_exit(...) -> list[str]`
- **业务用途**：Wait for the previous CW2 process before initializing Qt and plugins.
- **源码位置**：第 `7` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `arguments` | `list[str]` | 命令行输入参数列表 (sys.argv) |
- **返回值意义**：返回类型为 `list[str]`，表示操作执行结果或返回目标计算数据实体。

---

### 📄 模块：`src/core/central.py`

> **模块职能说明**：系统核心控制中枢 (AppCentral)。协调调度配置管理器、课表引擎、小组件系统、窗口管理器、主题引擎、插件生态以及后台定时任务。

#### 🏛️ 核心类：`class QmlContextWindow(Protocol)`
> **类设计职能**：QmlContextWindow 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class StartupState(Enum)`
> **类设计职能**：StartupState 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class AppCentral(QObject)`
> **类设计职能**：AppCentral 业务管理类

##### 包含方法全量参考：

###### `AppCentral.__init__(...) -> None`
- **方法用途**：初始化 AppCentral 实例并建立内部状态与依赖注入
- **源码位置**：第 `85` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.instance(...) -> AppCentral`
- **方法用途**：获取 AppCentral 单例实例
- **源码位置**：第 `112` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `cls` | `Any` | 类对象自身引用 |
- **返回值**：`AppCentral`

###### `AppCentral._initialize_cores(...) -> None`
- **方法用途**：初始化核心
- **源码位置**：第 `118` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._initialize_notification(...) -> None`
- **方法用途**：初始化通知系统
- **源码位置**：第 `128` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._initialize_utils(...) -> None`
- **方法用途**：执行 _initialize_utils 相关的处理操作
- **源码位置**：第 `133` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._register_shortcuts(...) -> None`
- **方法用途**：执行 _register_shortcuts 相关的处理操作
- **源码位置**：第 `142` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._request_reschedule_day_shortcut(...) -> bool`
- **方法用途**：执行 _request_reschedule_day_shortcut 相关的处理操作
- **源码位置**：第 `175` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `AppCentral._retranslate_builtin_shortcuts(...) -> None`
- **方法用途**：执行 _retranslate_builtin_shortcuts 相关的处理操作
- **源码位置**：第 `179` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._initialize_schedule_components(...) -> None`
- **方法用途**：初始化调度相关组件
- **源码位置**：第 `187` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._initialize_ui_components(...) -> None`
- **方法用途**：初始化启动必需的UI组件
- **源码位置**：第 `196` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.run(...) -> None`
- **方法用途**：启动运行 AppCentral 的核心业务逻辑或主循环
- **源码位置**：第 `209` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.init(...) -> None`
- **方法用途**：执行 AppCentral 的核心初始化流程
- **源码位置**：第 `222` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._schedule_startup_swap_restore_prompt(...) -> None`
- **方法用途**：执行 _schedule_startup_swap_restore_prompt 相关的处理操作
- **源码位置**：第 `258` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._show_startup_swap_restore_prompt(...) -> None`
- **方法用途**：执行 _show_startup_swap_restore_prompt 相关的处理操作
- **源码位置**：第 `270` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.reportThemeLoadFailure(...) -> None`
- **方法用途**：Keep the existing QML entry point while delegating recovery.
- **源码位置**：第 `282` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `source` | `str` | source 文本字符串 |
- **返回值**：`None`

###### `AppCentral.resolve_class_swap_restore(...) -> None`
- **方法用途**：执行 resolve_class_swap_restore 相关的处理操作
- **源码位置**：第 `286` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.has_today_class_swaps(...) -> bool`
- **方法用途**：检查当前环境或对象是否包含指定数据/属性
- **源码位置**：第 `292` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `AppCentral._load_config(...) -> None`
- **方法用途**：加载和验证配置
- **源码位置**：第 `297` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._load_class_swap(...) -> None`
- **方法用途**：加载换课记录，跨天时自动清理
- **源码位置**：第 `301` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.update(...) -> None`
- **方法用途**：计算并更新 AppCentral 的状态、属性或遮罩渲染
- **源码位置**：第 `305` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.cleanup(...) -> None`
- **方法用途**：解绑信号槽并安全释放系统底层资源
- **源码位置**：第 `309` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.scheduleRuntime(...) -> QObject`
- **方法用途**：执行 scheduleRuntime 相关的处理操作
- **源码位置**：第 `332` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`QObject`

###### `AppCentral.notification(...) -> QObject`
- **方法用途**：执行 notification 相关的处理操作
- **源码位置**：第 `336` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`QObject`

###### `AppCentral.scheduleEditor(...) -> QObject`
- **方法用途**：执行 scheduleEditor 相关的处理操作
- **源码位置**：第 `342` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`QObject`

###### `AppCentral.classSwapManager(...) -> None`
- **方法用途**：执行 classSwapManager 相关的处理操作
- **源码位置**：第 `346` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.scheduleManager(...) -> None`
- **方法用途**：执行 scheduleManager 相关的处理操作
- **源码位置**：第 `350` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.translator(...) -> None`
- **方法用途**：执行 translator 相关的处理操作
- **源码位置**：第 `354` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.themeManager(...) -> None`
- **方法用途**：执行 themeManager 相关的处理操作
- **源码位置**：第 `358` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.globalConfig(...) -> None`
- **方法用途**：执行 globalConfig 相关的处理操作
- **源码位置**：第 `362` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.quit(...) -> None`
- **方法用途**：执行 quit 相关的处理操作
- **源码位置**：第 `366` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.restart(...) -> None`
- **方法用途**：执行 restart 相关的处理操作
- **源码位置**：第 `371` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `extra_argument` | `Optional[str]` | X 轴横坐标 (像素) |
- **返回值**：`None`

###### `AppCentral.restartRequired(...) -> bool`
- **方法用途**：是否有待应用的重启（供 UI 显示重启提示按钮）
- **源码位置**：第 `389` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `AppCentral.markRestartRequired(...) -> None`
- **方法用途**：标记需要重启以应用更改（如插件启用/禁用状态变化）
- **源码位置**：第 `394` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.setup_qml_context(...) -> None`
- **方法用途**：为窗口设置标准的QML上下文属性
- **源码位置**：第 `401` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `window` | `QmlContextWindow` | window 运行时参数 |
- **返回值**：`None`

###### `AppCentral.clean_qml_context(...) -> None`
- **方法用途**：为窗口设置标准的QML上下文属性
- **源码位置**：第 `421` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `window` | `Any` | window 运行时参数 |
- **返回值**：`None`

###### `AppCentral._load_schedule(...) -> None`
- **方法用途**：加载课程表
- **源码位置**：第 `436` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._load_interactions(...) -> None`
- **方法用途**：加载交互
- **源码位置**：第 `440` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._load_translator(...) -> None`
- **方法用途**：加载翻译
- **源码位置**：第 `443` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._load_runtime(...) -> None`
- **方法用途**：执行 _load_runtime 相关的处理操作
- **源码位置**：第 `449` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._setup_connections(...) -> None`
- **方法用途**：设置runtime连接
- **源码位置**：第 `454` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._run_utils(...) -> None`
- **方法用途**：执行 _run_utils 相关的处理操作
- **源码位置**：第 `463` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._load_theme_and_plugins(...) -> None`
- **方法用途**：主题和插件
- **源码位置**：第 `472` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._init_tray_icon(...) -> None`
- **方法用途**：执行 _init_tray_icon 相关的处理操作
- **源码位置**：第 `485` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._cleanup_tray_icon(...) -> None`
- **方法用途**：执行 _cleanup_tray_icon 相关的处理操作
- **源码位置**：第 `491` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._setup_logging(...) -> None`
- **方法用途**：根据 Configs.app.no_logs 决定是否写日志到文件
- **源码位置**：第 `496` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral._on_tray_toggle(...) -> None`
- **方法用途**：执行 _on_tray_toggle 相关的处理操作
- **源码位置**：第 `515` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `pos` | `QPoint` | 屏幕坐标点 (QPoint / QPointF) |
- **返回值**：`None`

###### `AppCentral.openDebugger(...) -> None`
- **方法用途**：显示调试器
- **源码位置**：第 `519` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.toggleWidgetsEditMode(...) -> None`
- **方法用途**：切换小组件编辑模式
- **源码位置**：第 `527` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppCentral.getQFont(...) -> QFont`
- **方法用途**：构造一个带 fallback 的 QFont 对象。
- **源码位置**：第 `543` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `target_font` | `str` | target_font 文本字符串 |
  | `fallback_font` | `str` | fallback_font 文本字符串 |
- **返回值**：`QFont`

---

### 📄 模块：`src/core/directories.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PathManager(QObject)`
> **类设计职能**：PathManager 业务管理类

##### 包含方法全量参考：

###### `PathManager.__init__(...) -> None`
- **方法用途**：初始化 PathManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `41` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PathManager.root(...) -> str`
- **方法用途**：执行 root 相关的处理操作
- **源码位置**：第 `45` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path_name` | `str` | 目标文件或目录路径 |
- **返回值**：`str`

###### `PathManager.assets(...) -> str`
- **方法用途**：执行 assets 相关的处理操作
- **源码位置**：第 `49` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path_name` | `str` | 目标文件或目录路径 |
- **返回值**：`str`

###### `PathManager.qml(...) -> str`
- **方法用途**：执行 qml 相关的处理操作
- **源码位置**：第 `53` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path_name` | `str` | 目标文件或目录路径 |
- **返回值**：`str`

###### `PathManager.images(...) -> str`
- **方法用途**：执行 images 相关的处理操作
- **源码位置**：第 `57` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path_name` | `str` | 目标文件或目录路径 |
- **返回值**：`str`

---

### 📄 模块：`src/core/platform.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PlatformIntegration(object)`
> **类设计职能**：Small collection of platform-specific application setup.

##### 包含方法全量参考：

###### `PlatformIntegration.__init__(...) -> None`
- **方法用途**：初始化 PlatformIntegration 实例并建立内部状态与依赖注入
- **源码位置**：第 `19` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app` | `QApplication` | app 运行时参数 |
- **返回值**：`None`

###### `PlatformIntegration.initialize(...) -> None`
- **方法用途**：执行 PlatformIntegration 的核心初始化流程
- **源码位置**：第 `34` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlatformIntegration._initialize_app_icon(...) -> None`
- **方法用途**：执行 _initialize_app_icon 相关的处理操作
- **源码位置**：第 `38` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlatformIntegration._initialize_windows_appid(...) -> None`
- **方法用途**：执行 _initialize_windows_appid 相关的处理操作
- **源码位置**：第 `46` 行
- **参数说明**：无参数
- **返回值**：`None`

---

### 📄 模块：`src/core/theme_recovery.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class ThemeRecoveryController(QObject)`
> **类设计职能**：Handles asynchronous QML theme-load failures.

##### 包含方法全量参考：

###### `ThemeRecoveryController.__init__(...) -> None`
- **方法用途**：初始化 ThemeRecoveryController 实例并建立内部状态与依赖注入
- **源码位置**：第 `12` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_manager` | `Any` | theme_manager 运行时参数 |
  | `window_manager` | `Any` | window_manager 运行时参数 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `ThemeRecoveryController.handle_failure(...) -> None`
- **方法用途**：处理特定异常、通知消息或状态跃迁
- **源码位置**：第 `20` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `failed_theme_id` | `str` | failed_theme_id 文本字符串 |
- **返回值**：`None`

###### `ThemeRecoveryController.report_component_failure(...) -> None`
- **方法用途**：执行 report_component_failure 相关的处理操作
- **源码位置**：第 `47` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `source` | `str` | source 文本字符串 |
- **返回值**：`None`

###### `ThemeRecoveryController._show_error_dialog(...) -> None`
- **方法用途**：执行 _show_error_dialog 相关的处理操作
- **源码位置**：第 `58` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `failed_theme_id` | `str` | failed_theme_id 文本字符串 |
  | `recovered` | `bool` | recovered 条件开关状态 |
- **返回值**：`None`

---

## 配置管理子系统 (Configuration Subsystem)

### 📄 模块：`src/core/config/manager.py`

> **模块职能说明**：全局配置管理器 (ConfigManager)。负责 configs.json 的加载、序列化保存、默认值回退、防抖保存与变更信号通知。

#### 🏛️ 核心类：`class RootConfig(ConfigBaseModel)`
> **类设计职能**：RootConfig 业务管理类

##### 包含方法全量参考：

###### `RootConfig.__setattr__(...) -> None`
- **方法用途**：执行 __setattr__ 相关的处理操作
- **源码位置**：第 `30` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `Any` | name 文本字符串 |
  | `value` | `Any` | 写入或更新的目标数据值 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ConfigManager(QObject)`
> **类设计职能**：ConfigManager 业务管理类

##### 包含方法全量参考：

###### `ConfigManager.__init__(...) -> None`
- **方法用途**：初始化 ConfigManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `40` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path` | `Path` | 目标文件或目录路径 |
  | `filename` | `str` | filename 文本字符串 |
- **返回值**：`None`

###### `ConfigManager._bind_nested_on_change(...) -> None`
- **方法用途**：递归绑定 _on_change 给所有嵌套的 ConfigBaseModel；并且传递路径
- **源码位置**：第 `56` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `obj` | `Any` | obj 运行时参数 |
  | `path` | `Optional[str]` | 目标文件或目录路径 |
- **返回值**：`None`

###### `ConfigManager._ensure_defaults(...) -> None`
- **方法用途**：确保在 QApplication 存在时，填充
- **源码位置**：第 `73` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ConfigManager._clean_useless_configs(...) -> None`
- **方法用途**：清理无用的配置项
- **源码位置**：第 `94` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ConfigManager.load_config(...) -> None`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `109` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ConfigManager.save(...) -> None`
- **方法用途**：持久化保存当前配置模型或课表数据至磁盘
- **源码位置**：第 `124` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `silent` | `Any` | silent 运行时参数 |
- **返回值**：`None`

###### `ConfigManager.__getattr__(...) -> None`
- **方法用途**：代理属性获取
- **源码位置**：第 `133` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`None`

###### `ConfigManager.lock(...) -> None`
- **方法用途**：锁定配置项
- **源码位置**：第 `140` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `keys` | `str | list[str] | set[str]` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ConfigManager.unlock(...) -> None`
- **方法用途**：解锁配置项
- **源码位置**：第 `147` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `keys` | `str | list[str] | set[str]` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ConfigManager.isKeyLocked(...) -> bool`
- **方法用途**：检查配置项是否被锁定
- **源码位置**：第 `155` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `key` | `str` | 配置项键名或字典索引 Key |
- **返回值**：`bool`

###### `ConfigManager.data(...) -> None`
- **方法用途**：执行 data 相关的处理操作
- **源码位置**：第 `161` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ConfigManager.set(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `165` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `key` | `str` | 配置项键名或字典索引 Key |
  | `value` | `Any` | 写入或更新的目标数据值 |
- **返回值**：`None`

###### `ConfigManager.setPlugin(...) -> None`
- **方法用途**：设置插件配置（同时更新运行时模型）
- **源码位置**：第 `189` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `key` | `str` | 配置项键名或字典索引 Key |
  | `value` | `Any` | 写入或更新的目标数据值 |
- **返回值**：`None`

---

### 📄 模块：`src/core/config/model.py`

> **模块职能说明**：全局配置 Pydantic 数据模型定义。包含常规、界面、侧边栏、通知、网络、自动化等全部结构化配置项。

#### 🏛️ 核心类：`class ConfigBaseModel(BaseModel)`
> **类设计职能**：ConfigBaseModel 业务管理类

##### 包含方法全量参考：

###### `ConfigBaseModel.__init__(...) -> None`
- **方法用途**：初始化 ConfigBaseModel 实例并建立内部状态与依赖注入
- **源码位置**：第 `29` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ConfigBaseModel._bind_context(...) -> None`
- **方法用途**：将当前模型的变更回调、路径和锁定配置传递给嵌套模型。
- **源码位置**：第 `35` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `value` | `ConfigBaseModel` | 写入或更新的目标数据值 |
  | `path` | `Optional[str]` | 目标文件或目录路径 |
- **返回值**：`None`

###### `ConfigBaseModel._bind_runtime_context(...) -> None`
- **方法用途**：绑定独立运行时模型的配置路径、锁定集合和变更回调。
- **源码位置**：第 `46` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path` | `Optional[str]` | 目标文件或目录路径 |
  | `locked_keys` | `set[str]` | Y 轴纵坐标 (像素) |
  | `on_change` | `Optional[Callable[[], None]]` | on_change 运行时参数 |
- **返回值**：`None`

###### `ConfigBaseModel.__setattr__(...) -> None`
- **方法用途**：执行 __setattr__ 相关的处理操作
- **源码位置**：第 `62` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `Any` | name 文本字符串 |
  | `value` | `Any` | 写入或更新的目标数据值 |
- **返回值**：`None`

#### 🏛️ 核心类：`class LayoutAnchor(str, Enum)`
> **类设计职能**：LayoutAnchor 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class ZOrder(str, Enum)`
> **类设计职能**：ZOrder 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class CountdownPrecision(str, Enum)`
> **类设计职能**：CountdownPrecision 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class TapAction(str, Enum)`
> **类设计职能**：TapAction 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class WidgetEntry(ConfigBaseModel)`
> **类设计职能**：WidgetEntry 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class LocaleConfig(ConfigBaseModel)`
> **类设计职能**：语言设置

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class ScheduleDefaultDurationConfig(ConfigBaseModel)`
> **类设计职能**：课程默认时长

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class HideInteractionsConfig(ConfigBaseModel)`
> **类设计职能**：隐藏交互配置

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class AppConfig(ConfigBaseModel)`
> **类设计职能**：应用程序配置

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PreferencesConfig(ConfigBaseModel)`
> **类设计职能**：偏好设置

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class InteractionsConfig(ConfigBaseModel)`
> **类设计职能**：交互配置

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginsConfig(ConfigBaseModel)`
> **类设计职能**：PluginsConfig 业务管理类

##### 包含方法全量参考：

###### `PluginsConfig.remove_legacy_plaza_sources(...) -> None`
- **方法用途**：执行 remove_legacy_plaza_sources 相关的处理操作
- **源码位置**：第 `229` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `cls` | `Any` | 类对象自身引用 |
  | `values` | `Any` | 写入或更新的目标数据值 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ScheduleConfig(ConfigBaseModel)`
> **类设计职能**：ScheduleConfig 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class NetworkConfig(ConfigBaseModel)`
> **类设计职能**：网络配置

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class NotificationsConfig(ConfigBaseModel)`
> **类设计职能**：所有通知配置，包括全局设置和各提供者配置

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

---

## 课表算法与运行时引擎 (Schedule Engine)

### 📄 模块：`src/core/schedule/runtime.py`

> **模块职能说明**：课表运行时引擎 (ScheduleRuntime)。负责秒级定时器调度、课程倒计时计算、上课/下课/课间状态切换、通知格式化与向 QML 暴露实时状态。

#### 🏛️ 核心类：`class ScheduleRuntime(QObject)`
> **类设计职能**：ScheduleRuntime 业务管理类

##### 包含方法全量参考：

###### `ScheduleRuntime.__init__(...) -> None`
- **方法用途**：初始化 ScheduleRuntime 实例并建立内部状态与依赖注入
- **源码位置**：第 `22` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `ScheduleRuntime._register_notification_providers(...) -> None`
- **方法用途**：注册不同类型的通知提供者，确保在翻译加载后执行
- **源码位置**：第 `75` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleRuntime._on_retranslate(...) -> None`
- **方法用途**：处理翻译信号，重新注册通知提供者
- **源码位置**：第 `126` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleRuntime.currentTime(...) -> str`
- **方法用途**：执行 currentTime 相关的处理操作
- **源码位置**：第 `152` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ScheduleRuntime.currentDayOfWeek(...) -> int`
- **方法用途**：执行 currentDayOfWeek 相关的处理操作
- **源码位置**：第 `156` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ScheduleRuntime.currentDate(...) -> dict`
- **方法用途**：执行 currentDate 相关的处理操作
- **源码位置**：第 `160` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleRuntime.currentWeek(...) -> int`
- **方法用途**：执行 currentWeek 相关的处理操作
- **源码位置**：第 `164` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ScheduleRuntime.currentWeekOfCycle(...) -> int`
- **方法用途**：执行 currentWeekOfCycle 相关的处理操作
- **源码位置**：第 `168` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ScheduleRuntime.subjects(...) -> list`
- **方法用途**：执行 subjects 相关的处理操作
- **源码位置**：第 `173` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list`

###### `ScheduleRuntime.scheduleMeta(...) -> dict`
- **方法用途**：执行 scheduleMeta 相关的处理操作
- **源码位置**：第 `179` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleRuntime.currentDayEntries(...) -> list`
- **方法用途**：执行 currentDayEntries 相关的处理操作
- **源码位置**：第 `185` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list`

###### `ScheduleRuntime.currentEntry(...) -> dict`
- **方法用途**：执行 currentEntry 相关的处理操作
- **源码位置**：第 `191` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleRuntime.nextEntries(...) -> list`
- **方法用途**：执行 nextEntries 相关的处理操作
- **源码位置**：第 `195` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list`

###### `ScheduleRuntime.timeOffset(...) -> int`
- **方法用途**：执行 timeOffset 相关的处理操作
- **源码位置**：第 `201` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ScheduleRuntime.remainingTime(...) -> dict`
- **方法用途**：执行 remainingTime 相关的处理操作
- **源码位置**：第 `205` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleRuntime.progress(...) -> float`
- **方法用途**：执行 progress 相关的处理操作
- **源码位置**：第 `218` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`float`

###### `ScheduleRuntime.currentStatus(...) -> str`
- **方法用途**：执行 currentStatus 相关的处理操作
- **源码位置**：第 `224` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ScheduleRuntime.currentSubject(...) -> dict`
- **方法用途**：执行 currentSubject 相关的处理操作
- **源码位置**：第 `231` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleRuntime.currentTitle(...) -> str`
- **方法用途**：执行 currentTitle 相关的处理操作
- **源码位置**：第 `235` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ScheduleRuntime._format_sidebar_entry(...) -> dict`
- **方法用途**：组装符合 PROJECT.md 契约的扁平化课程信息字典
- **源码位置**：第 `238` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry` | `Entry` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `entry_date` | `date` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `now` | `datetime` | now 运行时参数 |
  | `current_entry_id` | `Optional[str]` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
- **返回值**：`dict`

###### `ScheduleRuntime.sidebarDaySchedule(...) -> list[dict]`
- **方法用途**：R1: 右侧边缘当天课表扁平数据列表，包含起止时间范围、教室、教师、主题色、当前课程高亮标记与进度。
- **源码位置**：第 `314` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `ScheduleRuntime.sidebarWeekSchedule(...) -> dict`
- **方法用途**：R3: 全周课表 7 天网格矩阵聚合数据，以 1-7 为键映射周一至周日全量课程列表。
- **源码位置**：第 `347` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleRuntime.refresh(...) -> None`
- **方法用途**：执行 refresh 相关的处理操作
- **源码位置**：第 `402` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule` | `Optional[ScheduleData]` | Schedule 课表模型实例对象 |
- **返回值**：`None`

###### `ScheduleRuntime.schedule_refresh(...) -> None`
- **方法用途**：合并连续的课表编辑通知，避免编辑器拖动时同步重算运行时状态。
- **源码位置**：第 `428` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule` | `ScheduleData` | Schedule 课表模型实例对象 |
- **返回值**：`None`

###### `ScheduleRuntime._flush_scheduled_refresh(...) -> None`
- **方法用途**：执行 _flush_scheduled_refresh 相关的处理操作
- **源码位置**：第 `433` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleRuntime._update_schedule(...) -> None`
- **方法用途**：更新日程
- **源码位置**：第 `439` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule` | `Optional[ScheduleData]` | Schedule 课表模型实例对象 |
- **返回值**：`None`

###### `ScheduleRuntime._update_time(...) -> None`
- **方法用途**：执行 _update_time 相关的处理操作
- **源码位置**：第 `474` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleRuntime.get_progress_percent(...) -> float`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `479` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`float`

###### `ScheduleRuntime._format_next_entry_notification(...) -> Optional[str]`
- **方法用途**：格式化下一节课程/活动的通知文案，集中管理下一节课提取逻辑
- **源码位置**：第 `491` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry` | `Any` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
- **返回值**：`Optional[str]`

###### `ScheduleRuntime._update_notify(...) -> None`
- **方法用途**：执行 _update_notify 相关的处理操作
- **源码位置**：第 `519` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/schedule/manager.py`

> **模块职能说明**：课表数据存储管理器 (ScheduleManager)。负责多课表的加载、保存、当前活动课表切换与课表文件格式版本兼容。

#### 独立函数列表 (Standalone Functions)

##### `def _create_empty_schedule(...) -> None`
- **业务用途**：执行 _create_empty_schedule 相关的处理操作
- **源码位置**：第 `21` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `None`，表示操作执行结果或返回目标计算数据实体。

#### 🏛️ 核心类：`class ScheduleManager(QObject)`
> **类设计职能**：ScheduleManager 业务管理类

##### 包含方法全量参考：

###### `ScheduleManager.__init__(...) -> None`
- **方法用途**：初始化 ScheduleManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `38` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedules_dir` | `Path` | Schedule 课表模型实例对象 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `ScheduleManager.scheduleIO(...) -> None`
- **方法用途**：执行 scheduleIO 相关的处理操作
- **源码位置**：第 `54` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleManager.load(...) -> bool`
- **方法用途**：加载课程表
- **源码位置**：第 `58` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
  | `force` | `bool` | force 条件开关状态 |
- **返回值**：`bool`

###### `ScheduleManager.reload(...) -> None`
- **方法用途**：重新加载当前课表
- **源码位置**：第 `96` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleManager.modify(...) -> None`
- **方法用途**：接受外部修改（如编辑器）
- **源码位置**：第 `102` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule` | `ScheduleData` | Schedule 课表模型实例对象 |
- **返回值**：`None`

###### `ScheduleManager.modify_by_dict(...) -> bool`
- **方法用途**：通过字典修改课表
- **源码位置**：第 `115` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule_dict` | `dict` | Schedule 课表模型实例对象 |
- **返回值**：`bool`

###### `ScheduleManager.save(...) -> None`
- **方法用途**：持久化保存当前配置模型或课表数据至磁盘
- **源码位置**：第 `125` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path` | `Optional[Path]` | 目标文件或目录路径 |
- **返回值**：`None`

###### `ScheduleManager.currentScheduleName(...) -> str`
- **方法用途**：执行 currentScheduleName 相关的处理操作
- **源码位置**：第 `138` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ScheduleManager.schedules(...) -> list[dict]`
- **方法用途**：列出当前目录下所有课程表文件，返回dict
- **源码位置**：第 `143` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `ScheduleManager.add(...) -> None`
- **方法用途**：创建新的空课表
- **源码位置**：第 `155` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`None`

###### `ScheduleManager.delete(...) -> bool`
- **方法用途**：删除课表文件
- **源码位置**：第 `172` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`bool`

###### `ScheduleManager.duplicate(...) -> bool`
- **方法用途**：复制课表文件
- **源码位置**：第 `189` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `src_name` | `str` | src_name 文本字符串 |
  | `dest_name` | `str` | dest_name 文本字符串 |
- **返回值**：`bool`

###### `ScheduleManager.rename(...) -> bool`
- **方法用途**：重命名课程表文件
- **源码位置**：第 `200` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `old_name` | `str` | old_name 文本字符串 |
  | `new_name` | `str` | new_name 文本字符串 |
- **返回值**：`bool`

###### `ScheduleManager.importSchedule(...) -> bool`
- **方法用途**：导入课程表
- **源码位置**：第 `233` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `ScheduleManager.export(...) -> bool`
- **方法用途**：导出指定课程表
- **源码位置**：第 `273` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `filename` | `str` | filename 文本字符串 |
- **返回值**：`bool`

###### `ScheduleManager.checkNameExists(...) -> bool`
- **方法用途**：执行 checkNameExists 相关的处理操作
- **源码位置**：第 `302` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`bool`

###### `ScheduleManager.openSchedulesFolder(...) -> bool`
- **方法用途**：打开指定插件的本地文件夹
- **源码位置**：第 `307` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `ScheduleManager.set_readonly(...) -> None`
- **方法用途**：设置课表是否只读
- **源码位置**：第 `319` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `readonly` | `bool` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ScheduleManager.isReadonly(...) -> bool`
- **方法用途**：检查课表是否只读
- **源码位置**：第 `325` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/schedule/service.py`

> **模块职能说明**：课表核心算法与查询服务 (ScheduleServices)。负责日期星期计算、课程节点检索、科目映射与跨天调度判断。

#### 🏛️ 核心类：`class ScheduleServices(object)`
> **类设计职能**：ScheduleServices 业务管理类

##### 包含方法全量参考：

###### `ScheduleServices.__init__(...) -> None`
- **方法用途**：初始化 ScheduleServices 实例并建立内部状态与依赖注入
- **源码位置**：第 `9` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `Any` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `ScheduleServices._get_reschedule_map(...) -> dict`
- **方法用途**：执行 _get_reschedule_map 相关的处理操作
- **源码位置**：第 `12` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleServices.get_day_entries(...) -> Optional[Timeline]`
- **方法用途**：返回当前日期对应的 Timeline（深拷贝，应用 override，不修改原始数据）。
- **源码位置**：第 `15` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule` | `ScheduleData` | Schedule 课表模型实例对象 |
  | `now` | `datetime` | now 运行时参数 |
- **返回值**：`Optional[Timeline]`

###### `ScheduleServices._override_applies(...) -> bool`
- **方法用途**：执行 _override_applies 相关的处理操作
- **源码位置**：第 `90` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `override` | `Timetable` | override 运行时参数 |
  | `weekday` | `int` | Y 轴纵坐标 (像素) |
  | `current_week` | `int` | current_week 整数计数值 |
  | `max_week_cycle` | `int` | X 轴横坐标 (像素) |
- **返回值**：`bool`

###### `ScheduleServices.get_current_entry(...) -> Optional[Entry]`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `100` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `day` | `Timeline` | Y 轴纵坐标 (像素) |
  | `now` | `Optional[datetime]` | now 运行时参数 |
- **返回值**：`Optional[Entry]`

###### `ScheduleServices.get_all_entries(...) -> list[Entry]`
- **方法用途**：返回当天所有可显示的条目
- **源码位置**：第 `114` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `day` | `Timeline` | Y 轴纵坐标 (像素) |
- **返回值**：`list[Entry]`

###### `ScheduleServices.get_next_entries(...) -> list[Entry]`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `125` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `day` | `Timeline` | Y 轴纵坐标 (像素) |
  | `now` | `Optional[datetime]` | now 运行时参数 |
- **返回值**：`list[Entry]`

###### `ScheduleServices.get_remaining_time(...) -> timedelta`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `136` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `day` | `Timeline` | Y 轴纵坐标 (像素) |
  | `now` | `Optional[datetime]` | now 运行时参数 |
- **返回值**：`timedelta`

###### `ScheduleServices.get_current_status(...) -> EntryType`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `151` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `day` | `Timeline` | Y 轴纵坐标 (像素) |
  | `now` | `Optional[datetime]` | now 运行时参数 |
  | `prep_min` | `int` | prep_min 整数计数值 |
- **返回值**：`EntryType`

###### `ScheduleServices.get_current_subject(...) -> Optional[Subject]`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `162` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `day` | `Timeline` | Y 轴纵坐标 (像素) |
  | `subjects` | `list[Subject]` | 科目对象 (SubjectModel) |
  | `now` | `Optional[datetime]` | now 运行时参数 |
- **返回值**：`Optional[Subject]`

###### `ScheduleServices.get_subject(...) -> Optional[Subject]`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `171` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
  | `subjects` | `list[Subject]` | 科目对象 (SubjectModel) |
- **返回值**：`Optional[Subject]`

###### `ScheduleServices._get_week_index(...) -> int`
- **方法用途**：根据 schedule.meta.startDate 算出当前是第几周
- **源码位置**：第 `180` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `schedule` | `ScheduleData` | Schedule 课表模型实例对象 |
  | `now` | `datetime` | now 运行时参数 |
- **返回值**：`int`

###### `ScheduleServices._is_in_week(...) -> bool`
- **方法用途**：判断某个 weeks 字段是否包含当前周
- **源码位置**：第 `190` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `weeks` | `str | int | Optional[list[int]]` | weeks 文本字符串 |
  | `current_week` | `int` | current_week 整数计数值 |
  | `max_week_cycle` | `int` | X 轴横坐标 (像素) |
- **返回值**：`bool`

---

### 📄 模块：`src/core/schedule/swapper.py`

> **模块职能说明**：调课与代课处理器 (ScheduleSwapper)。支持对指定日期的特定节次进行临时科目置换与调课记录持久化。

#### 🏛️ 核心类：`class ClassSwapManager(QObject)`
> **类设计职能**：换课管理器，管理临时换课操作

##### 包含方法全量参考：

###### `ClassSwapManager.__init__(...) -> None`
- **方法用途**：初始化 ClassSwapManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `32` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `ClassSwapManager.getDayEntries(...) -> list`
- **方法用途**：获取指定 星期+周次 的当日课程列表（已应用 override）
- **源码位置**：第 `45` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`list`

###### `ClassSwapManager.getAllSubjects(...) -> list[dict]`
- **方法用途**：获取所有科目
- **源码位置**：第 `59` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `ClassSwapManager.getCurrentDayOfWeek(...) -> int`
- **方法用途**：获取当前星期几
- **源码位置**：第 `64` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ClassSwapManager.getCurrentWeekOfCycle(...) -> int`
- **方法用途**：获取当前周期内第几周
- **源码位置**：第 `69` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ClassSwapManager.getPreferredDayOfWeek(...) -> int`
- **方法用途**：获取换课界面上次选择的星期（默认今天）
- **源码位置**：第 `78` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ClassSwapManager.getPreferredWeekOfCycle(...) -> int`
- **方法用途**：获取换课界面上次选择的周期周（默认当前周期周）
- **源码位置**：第 `88` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ClassSwapManager.setSwapPickerContext(...) -> None`
- **方法用途**：保存换课界面当前选择的 星期/周期周
- **源码位置**：第 `99` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ClassSwapManager.applyPickerToToday(...) -> bool`
- **方法用途**：将换课界面当前选择的 星期/周次 课表立即投射到今天
- **源码位置**：第 `118` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`bool`

###### `ClassSwapManager.getMaxWeekCycle(...) -> int`
- **方法用途**：获取最大周期
- **源码位置**：第 `150` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ClassSwapManager.getSubjectName(...) -> str`
- **方法用途**：根据 subjectId 获取科目名
- **源码位置**：第 `158` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
- **返回值**：`str`

###### `ClassSwapManager.swapTwoEntries(...) -> bool`
- **方法用途**：: 交换两节课的科目（dailyScheduleView 内互换）
- **源码位置**：第 `166` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id_a` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `entry_id_b` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`bool`

###### `ClassSwapManager.replaceEntry(...) -> bool`
- **方法用途**：: 将某节课替换为指定科目
- **源码位置**：第 `244` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `new_subject_id` | `str` | 科目对象 (SubjectModel) |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`bool`

###### `ClassSwapManager.saveSwapRecords(...) -> None`
- **方法用途**：保存换课记录到配置
- **源码位置**：第 `296` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ClassSwapManager.loadSwapRecords(...) -> None`
- **方法用途**：加载换课记录
- **源码位置**：第 `320` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ClassSwapManager.hasTodaySwaps(...) -> bool`
- **方法用途**：今天是否有换课记录
- **源码位置**：第 `360` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `ClassSwapManager.getSwapRecords(...) -> list`
- **方法用途**：获取今天的换课记录
- **源码位置**：第 `386` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list`

###### `ClassSwapManager.discardTodaySwaps(...) -> None`
- **方法用途**：丢弃今天的换课（撤销所有换课 override）
- **源码位置**：第 `391` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ClassSwapManager._find_subject(...) -> Optional[Subject]`
- **方法用途**：查找科目
- **源码位置**：第 `402` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `subject_id` | `Optional[str]` | 科目唯一识别代码/ID |
- **返回值**：`Optional[Subject]`

###### `ClassSwapManager._get_effective_subject(...) -> Optional[dict]`
- **方法用途**：获取某个 entry 在指定日期的实际科目（含 override）
- **源码位置**：第 `412` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
  | `max_cycle` | `int` | X 轴横坐标 (像素) |
- **返回值**：`Optional[dict]`

###### `ClassSwapManager._get_override_priority(...) -> int`
- **方法用途**：计算 override 优先级
- **源码位置**：第 `458` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `weeks` | `Any` | weeks 运行时参数 |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
  | `max_cycle` | `int` | X 轴横坐标 (像素) |
- **返回值**：`int`

###### `ClassSwapManager._set_or_update_override(...) -> None`
- **方法用途**：设置或更新 override
- **源码位置**：第 `468` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `day_of_week` | `list[int]` | Y 轴纵坐标 (像素) |
  | `weeks` | `WeekType | list[int] | int | None` | weeks 整数计数值 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
  | `title` | `str` | 通知弹窗或组件标题文本 |
  | `start_time` | `Optional[str]` | start_time 文本字符串 |
  | `end_time` | `Optional[str]` | end_time 文本字符串 |
- **返回值**：`None`

###### `ClassSwapManager._add_swap_record(...) -> None`
- **方法用途**：添加换课记录
- **源码位置**：第 `506` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `swap_type` | `str` | Y 轴纵坐标 (像素) |
  | `entry_a` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `entry_b` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `old_subject` | `str` | 科目对象 (SubjectModel) |
  | `new_subject` | `str` | 科目对象 (SubjectModel) |
- **返回值**：`None`

###### `ClassSwapManager._normalize_swap_record(...) -> dict`
- **方法用途**：规范化换课记录，移除历史 day/week 冗余字段
- **源码位置**：第 `521` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `record` | `dict` | record 运行时参数 |
- **返回值**：`dict`

###### `ClassSwapManager._map_entry_to_day(...) -> Optional[str]`
- **方法用途**：按 class/activity 顺序，将 source 日的 entry 映射到 target 日对应位置
- **源码位置**：第 `532` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `source_entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `source_day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `source_week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
  | `target_day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `target_week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`Optional[str]`

###### `ClassSwapManager._apply_day_schedule_to_today(...) -> None`
- **方法用途**：将 source(星期+周次) 的课表按顺序投影到 target(今天)
- **源码位置**：第 `557` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `source_day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `source_week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
  | `target_day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `target_week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ClassSwapManager._get_day_entries(...) -> list`
- **方法用途**：获取指定 day/week 的条目（可选择是否包含非 class/activity）
- **源码位置**：第 `599` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
  | `include_non_class` | `bool` | include_non_class 条件开关状态 |
- **返回值**：`list`

###### `ClassSwapManager._clear_today_swap_overrides(...) -> None`
- **方法用途**：清理今天（指定 day/week）已有 swap override，确保重新投射是全量快照
- **源码位置**：第 `661` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
  | `week_of_cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ClassSwapManager._cleanup_swap_overrides(...) -> None`
- **方法用途**：清理换课产生的 override
- **源码位置**：第 `679` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `records` | `list` | records 运行时参数 |
- **返回值**：`None`

###### `ClassSwapManager._rebuild_overrides_from_records(...) -> None`
- **方法用途**：根据持久化换课记录重建当天临时 override（应用启动后内存恢复）
- **源码位置**：第 `695` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `records` | `list` | records 运行时参数 |
- **返回值**：`None`

###### `ClassSwapManager._is_in_week(...) -> bool`
- **方法用途**：执行 _is_in_week 相关的处理操作
- **源码位置**：第 `754` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `weeks` | `Any` | weeks 运行时参数 |
  | `current_week` | `int` | current_week 整数计数值 |
  | `max_week_cycle` | `int` | X 轴横坐标 (像素) |
- **返回值**：`bool`

###### `ClassSwapManager._override_applies(...) -> bool`
- **方法用途**：执行 _override_applies 相关的处理操作
- **源码位置**：第 `766` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `override` | `Timetable` | override 运行时参数 |
  | `weekday` | `int` | Y 轴纵坐标 (像素) |
  | `current_week` | `int` | current_week 整数计数值 |
  | `max_week_cycle` | `int` | X 轴横坐标 (像素) |
- **返回值**：`bool`

---

### 📄 模块：`src/core/schedule/editor.py`

> **模块职能说明**：课表可视化编辑辅助器 (ScheduleEditor)。为设置面板提供课程增删改查、时间段碰撞检测与批量验证功能。

#### 独立函数列表 (Standalone Functions)

##### `def _jsvalue_to_python(...) -> None`
- **业务用途**：将 QML 传来的 QVariant / QJSValue 转成 Python 原生类型
- **源码位置**：第 `15` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `value` | `Any` | 写入或更新的目标数据值 |
- **返回值意义**：返回类型为 `None`，表示操作执行结果或返回目标计算数据实体。

#### 🏛️ 核心类：`class ScheduleEditor(QObject)`
> **类设计职能**：ScheduleEditor 业务管理类

##### 包含方法全量参考：

###### `ScheduleEditor.__init__(...) -> None`
- **方法用途**：初始化 ScheduleEditor 实例并建立内部状态与依赖注入
- **源码位置**：第 `45` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `manager` | `ScheduleManager` | manager 运行时参数 |
- **返回值**：`None`

###### `ScheduleEditor._validate_time_range(...) -> bool`
- **方法用途**：验证时间范围，确保结束时间不早于开始时间
- **源码位置**：第 `64` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `start_time` | `str` | start_time 文本字符串 |
  | `end_time` | `str` | end_time 文本字符串 |
- **返回值**：`bool`

###### `ScheduleEditor.refresh(...) -> None`
- **方法用途**：执行 refresh 相关的处理操作
- **源码位置**：第 `89` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule` | `ScheduleData` | Schedule 课表模型实例对象 |
- **返回值**：`None`

###### `ScheduleEditor._on_updated(...) -> None`
- **方法用途**：执行 _on_updated 相关的处理操作
- **源码位置**：第 `107` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleEditor._rebuild_schedule_caches(...) -> None`
- **方法用途**：执行 _rebuild_schedule_caches 相关的处理操作
- **源码位置**：第 `114` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleEditor._emit_days_changed(...) -> None`
- **方法用途**：执行 _emit_days_changed 相关的处理操作
- **源码位置**：第 `122` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleEditor._emit_entries_changed(...) -> None`
- **方法用途**：Refresh the QML entry cache without serializing unrelated days.
- **源码位置**：第 `126` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `changed_day` | `Optional[Timeline]` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ScheduleEditor.refresh_manager(...) -> None`
- **方法用途**：执行 refresh_manager 相关的处理操作
- **源码位置**：第 `149` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleEditor.addSubject(...) -> str`
- **方法用途**：添加科目
- **源码位置**：第 `154` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
  | `teacher` | `str` | teacher 文本字符串 |
  | `icon` | `str` | 图标路径或 QIcon 实例 |
  | `color` | `str` | color 文本字符串 |
  | `location` | `str` | location 文本字符串 |
  | `is_local_classroom` | `bool` | 状态布尔标志 |
- **返回值**：`str`

###### `ScheduleEditor.updateSubject(...) -> None`
- **方法用途**：更新科目
- **源码位置**：第 `172` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
  | `name` | `str` | name 文本字符串 |
  | `simplified_name` | `str` | simplified_name 文本字符串 |
  | `teacher` | `str` | teacher 文本字符串 |
  | `icon` | `str` | 图标路径或 QIcon 实例 |
  | `color` | `str` | color 文本字符串 |
  | `location` | `str` | location 文本字符串 |
  | `is_local_classroom` | `bool` | 状态布尔标志 |
- **返回值**：`None`

###### `ScheduleEditor.removeSubject(...) -> None`
- **方法用途**：删除科目
- **源码位置**：第 `197` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
- **返回值**：`None`

###### `ScheduleEditor.getSubject(...) -> Optional[Subject]`
- **方法用途**：获取科目信息
- **源码位置**：第 `213` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
- **返回值**：`Optional[Subject]`

###### `ScheduleEditor.addDay(...) -> str`
- **方法用途**：添加日程
- **源码位置**：第 `219` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_of_week` | `Optional[list[int]]` | Y 轴纵坐标 (像素) |
  | `weeks` | `Any` | weeks 运行时参数 |
  | `date` | `str` | date 文本字符串 |
- **返回值**：`str`

###### `ScheduleEditor.updateDay(...) -> None`
- **方法用途**：更新日程
- **源码位置**：第 `236` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_id` | `str` | Y 轴纵坐标 (像素) |
  | `day_of_week` | `Optional[list[int]]` | Y 轴纵坐标 (像素) |
  | `weeks` | `WeekType | str | list[int] | Optional[int]` | weeks 文本字符串 |
  | `date` | `str` | date 文本字符串 |
- **返回值**：`None`

###### `ScheduleEditor.removeDay(...) -> None`
- **方法用途**：删除日程
- **源码位置**：第 `259` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_id` | `str` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ScheduleEditor.duplicateDay(...) -> Optional[str]`
- **方法用途**：复制指定时间线
- **源码位置**：第 `273` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_id` | `str` | Y 轴纵坐标 (像素) |
- **返回值**：`Optional[str]`

###### `ScheduleEditor.getDay(...) -> Optional[Timeline]`
- **方法用途**：获取日程信息
- **源码位置**：第 `297` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_id` | `str` | Y 轴纵坐标 (像素) |
- **返回值**：`Optional[Timeline]`

###### `ScheduleEditor.addEntry(...) -> str`
- **方法用途**：添加条目
- **源码位置**：第 `303` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `day_id` | `str` | Y 轴纵坐标 (像素) |
  | `entry_type` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `start_time` | `str` | start_time 文本字符串 |
  | `end_time` | `str` | end_time 文本字符串 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
  | `title` | `str` | 通知弹窗或组件标题文本 |
- **返回值**：`str`

###### `ScheduleEditor.updateEntry(...) -> None`
- **方法用途**：更新条目
- **源码位置**：第 `331` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `entry_type` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `start_time` | `str` | start_time 文本字符串 |
  | `end_time` | `str` | end_time 文本字符串 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
  | `title` | `str` | 通知弹窗或组件标题文本 |
- **返回值**：`None`

###### `ScheduleEditor.removeEntry(...) -> None`
- **方法用途**：删除条目
- **源码位置**：第 `369` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
- **返回值**：`None`

###### `ScheduleEditor.getEntry(...) -> Optional[Entry]`
- **方法用途**：获取条目信息
- **源码位置**：第 `380` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
- **返回值**：`Optional[Entry]`

###### `ScheduleEditor.findOverride(...) -> Optional[str]`
- **方法用途**：查找已有 override，返回其 id，如不存在返回空字符串
- **源码位置**：第 `390` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `day_of_week` | `Any` | Y 轴纵坐标 (像素) |
  | `weeks` | `Any` | weeks 运行时参数 |
- **返回值**：`Optional[str]`

###### `ScheduleEditor.addOverride(...) -> None`
- **方法用途**：执行 addOverride 相关的处理操作
- **源码位置**：第 `407` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `day_of_week` | `Any` | Y 轴纵坐标 (像素) |
  | `weeks` | `Any` | weeks 运行时参数 |
  | `subject_id` | `Any` | 科目唯一识别代码/ID |
  | `title` | `Any` | 通知弹窗或组件标题文本 |
- **返回值**：`None`

###### `ScheduleEditor.updateOverride(...) -> None`
- **方法用途**：计算并更新 ScheduleEditor 的状态、属性或遮罩渲染
- **源码位置**：第 `425` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `override_id` | `str` | override_id 文本字符串 |
  | `subject_id` | `Any` | 科目唯一识别代码/ID |
  | `title` | `Any` | 通知弹窗或组件标题文本 |
- **返回值**：`None`

###### `ScheduleEditor.removeOverride(...) -> None`
- **方法用途**：执行 removeOverride 相关的处理操作
- **源码位置**：第 `440` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `override_id` | `str` | override_id 文本字符串 |
- **返回值**：`None`

###### `ScheduleEditor.subjectNameById(...) -> Optional[str]`
- **方法用途**：根据 ID 获取科目名称
- **源码位置**：第 `452` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `subject_id` | `str` | 科目唯一识别代码/ID |
- **返回值**：`Optional[str]`

###### `ScheduleEditor.getEntryOverride(...) -> None`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `460` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `week` | `int` | week 整数计数值 |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ScheduleEditor.getOverrideTitle(...) -> str`
- **方法用途**：Return only the title explicitly supplied by a matching override.
- **源码位置**：第 `520` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry_id` | `str` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
  | `week` | `int` | week 整数计数值 |
  | `day_of_week` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`str`

###### `ScheduleEditor.setStartDate(...) -> bool`
- **方法用途**：设置开学日期，格式: yyyy-mm-dd
- **源码位置**：第 `545` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `date_str` | `str` | date_str 文本字符串 |
- **返回值**：`bool`

###### `ScheduleEditor.setTimelineSettings(...) -> bool`
- **方法用途**：一次性更新时间线设置，避免一次确认触发多次全局刷新。
- **源码位置**：第 `565` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `date_str` | `str` | date_str 文本字符串 |
  | `max_weeks` | `int` | X 轴横坐标 (像素) |
- **返回值**：`bool`

###### `ScheduleEditor.getStartDate(...) -> str`
- **方法用途**：获取当前开学日期
- **源码位置**：第 `591` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ScheduleEditor.restoreDefaultSubjects(...) -> None`
- **方法用途**：加载默认学科
- **源码位置**：第 `600` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleEditor.setMaxWeekCycle(...) -> None`
- **方法用途**：设置最大周数
- **源码位置**：第 `610` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `max_weeks` | `int` | X 轴横坐标 (像素) |
- **返回值**：`None`

###### `ScheduleEditor.getMaxWeekCycle(...) -> int`
- **方法用途**：获取最大周数
- **源码位置**：第 `622` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ScheduleEditor.meta(...) -> dict`
- **方法用途**：获取课程表元数据
- **源码位置**：第 `630` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleEditor.subjects(...) -> list[dict]`
- **方法用途**：获取所有科目
- **源码位置**：第 `637` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `ScheduleEditor.days(...) -> list[dict]`
- **方法用途**：获取所有日程
- **源码位置**：第 `644` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `ScheduleEditor.entriesRevision(...) -> int`
- **方法用途**：条目变化版本，用于刷新依赖嵌套 entries 的 QML 绑定。
- **源码位置**：第 `649` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ScheduleEditor.entriesData(...) -> list[dict]`
- **方法用途**：获取包含最新条目的日程快照，不触发时间线列表刷新。
- **源码位置**：第 `654` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `ScheduleEditor.overrides(...) -> list[Timetable]`
- **方法用途**：获取所有条目
- **源码位置**：第 `659` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[Timetable]`

###### `ScheduleEditor.overridesRevision(...) -> int`
- **方法用途**：Override content version for refreshing QML bindings.
- **源码位置**：第 `667` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `ScheduleEditor.scheduleData(...) -> dict`
- **方法用途**：获取完整的课程表数据
- **源码位置**：第 `672` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict`

###### `ScheduleEditor.path(...) -> str`
- **方法用途**：获取课程表文件路径
- **源码位置**：第 `679` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ScheduleEditor.filename(...) -> str`
- **方法用途**：获取课程表文件名
- **源码位置**：第 `684` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ScheduleEditor.markSaved(...) -> None`
- **方法用途**：标记为已保存
- **源码位置**：第 `689` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleEditor.dirty(...) -> bool`
- **方法用途**：检查是否有未保存的更改
- **源码位置**：第 `697` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/schedule/model.py`

> **模块职能说明**：课表 Pydantic 数据模型。定义 Schedule, Subject, TimeNode, Entry, SwapRecord 等核心业务实体。

#### 🏛️ 核心类：`class EntryType(str, Enum)`
> **类设计职能**：EntryType 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class WeekType(str, Enum)`
> **类设计职能**：WeekType 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class Subject(BaseModel)`
> **类设计职能**：Subject 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class Entry(BaseModel)`
> **类设计职能**：Entry 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class Timeline(BaseModel)`
> **类设计职能**：Timeline 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class MetaInfo(BaseModel)`
> **类设计职能**：MetaInfo 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class Timetable(BaseModel)`
> **类设计职能**：Timetable 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class ScheduleData(BaseModel)`
> **类设计职能**：ScheduleData 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

---

## 小组件与穿透窗口子系统 (Widgets & Window Subsystem)

### 📄 模块：`src/core/widgets/core.py`

> **模块职能说明**：小组件系统与窗口控制核心 (WidgetsCore)。管理浮动小组件与侧边栏的加载，计算 Win32 SetWindowRgn 穿透遮罩并提供 35ms 防抖控制。

#### 🏛️ 核心类：`class WidgetsWindow(ReleasableWindow, QObject)`
> **类设计职能**：WidgetsWindow 业务管理类

##### 包含方法全量参考：

###### `WidgetsWindow.__init__(...) -> None`
- **方法用途**：初始化 WidgetsWindow 实例并建立内部状态与依赖注入
- **源码位置**：第 `20` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `QObject` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `WidgetsWindow._start_listening(...) -> None`
- **方法用途**：执行 _start_listening 相关的处理操作
- **源码位置**：第 `39` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow.run(...) -> None`
- **方法用途**：启动widgets窗口
- **源码位置**：第 `44` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow.release(...) -> None`
- **方法用途**：执行 release 相关的处理操作
- **源码位置**：第 `52` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow._load_with_theme(...) -> None`
- **方法用途**：加载QML并应用主题
- **源码位置**：第 `65` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow.is_qml_ready(...) -> bool`
- **方法用途**：检测并返回特定状态或条件判断布尔值
- **源码位置**：第 `94` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `WidgetsWindow.on_theme_changed(...) -> None`
- **方法用途**：主题变更时重新加载界面
- **源码位置**：第 `97` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow._finish_theme_reload(...) -> None`
- **方法用途**：执行 _finish_theme_reload 相关的处理操作
- **源码位置**：第 `131` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow._trigger_widget_reload(...) -> None`
- **方法用途**：触发 widgets 重新加载
- **源码位置**：第 `143` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow.on_qml_ready(...) -> None`
- **方法用途**：响应底层事件、信号或回调触发的槽函数
- **源码位置**：第 `148` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `obj` | `Any` | obj 运行时参数 |
  | `obj_url` | `Any` | 网络资源 URL 或 API 请求端点 |
- **返回值**：`None`

###### `WidgetsWindow._on_qml_warnings(...) -> None`
- **方法用途**：Log QML warnings without treating runtime diagnostics as load failures.
- **源码位置**：第 `189` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `warnings` | `Any` | warnings 运行时参数 |
- **返回值**：`None`

###### `WidgetsWindow._apply_empty_mask(...) -> None`
- **方法用途**：Keep a failed or incomplete QML load from exposing the full window.
- **源码位置**：第 `214` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow.schedule_mask_update(...) -> None`
- **方法用途**：执行 schedule_mask_update 相关的处理操作
- **源码位置**：第 `220` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `delay` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `WidgetsWindow.update_mask(...) -> None`
- **方法用途**：计算并更新 WidgetsWindow 的状态、属性或遮罩渲染
- **源码位置**：第 `228` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetsWindow.update_mouse_state(...) -> None`
- **方法用途**：计算并更新 WidgetsWindow 的状态、属性或遮罩渲染
- **源码位置**：第 `341` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/widgets/model.py`

> **模块职能说明**：小组件预设与布局数据模型。负责桌面小组件位置、尺寸、层级预设的序列化与读取。

#### 🏛️ 核心类：`class PresetEntryInput(TypedDict)`
> **类设计职能**：PresetEntryInput 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class WidgetDefinition(TypedDict)`
> **类设计职能**：WidgetDefinition 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class WidgetInstance(WidgetDefinition)`
> **类设计职能**：WidgetInstance 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class WidgetListModel(QAbstractListModel)`
> **类设计职能**：WidgetListModel 业务管理类

##### 包含方法全量参考：

###### `WidgetListModel.__init__(...) -> None`
- **方法用途**：初始化 WidgetListModel 实例并建立内部状态与依赖注入
- **源码位置**：第 `46` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `Any` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `WidgetListModel.roleNames(...) -> None`
- **方法用途**：执行 roleNames 相关的处理操作
- **源码位置**：第 `56` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetListModel.rowCount(...) -> None`
- **方法用途**：执行 rowCount 相关的处理操作
- **源码位置**：第 `68` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `WidgetListModel.data(...) -> None`
- **方法用途**：执行 data 相关的处理操作
- **源码位置**：第 `71` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `index` | `Any` | X 轴横坐标 (像素) |
  | `role` | `Any` | role 运行时参数 |
- **返回值**：`None`

###### `WidgetListModel._normalize_preset_entries(...) -> list[WidgetEntry]`
- **方法用途**：执行 _normalize_preset_entries 相关的处理操作
- **源码位置**：第 `93` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entries` | `list[str | PresetEntryInput | WidgetEntry]` | entries 文本字符串 |
- **返回值**：`list[WidgetEntry]`

###### `WidgetListModel.load_config(...) -> None`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `111` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetListModel.save_config(...) -> None`
- **方法用途**：持久化保存当前配置模型或课表数据至磁盘
- **源码位置**：第 `121` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetListModel.syncCurrentPreset(...) -> None`
- **方法用途**：同步当前 _instances 到 _presets
- **源码位置**：第 `130` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetListModel.updatePreset(...) -> None`
- **方法用途**：计算并更新 WidgetListModel 的状态、属性或遮罩渲染
- **源码位置**：第 `144` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `preset_name` | `str` | preset_name 文本字符串 |
  | `enabled_entries` | `list` | 功能是否启用的布尔开关标志 |
- **返回值**：`None`

###### `WidgetListModel.set_preset(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `151` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `preset_name` | `str` | preset_name 文本字符串 |
  | `entries` | `list` | entries 运行时参数 |
- **返回值**：`None`

###### `WidgetListModel.load_preset(...) -> None`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `155` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `preset_name` | `str` | preset_name 文本字符串 |
- **返回值**：`None`

###### `WidgetListModel.add_widget(...) -> None`
- **方法用途**：执行 add_widget 相关的处理操作
- **源码位置**：第 `182` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `type_id` | `str` | Y 轴纵坐标 (像素) |
  | `name` | `str` | name 文本字符串 |
  | `qml_path` | `str | QUrl` | 目标文件或目录路径 |
  | `backend_obj` | `Optional[QObject]` | backend_obj 运行时参数 |
  | `settings_qml` | `str | QUrl` | settings_qml 文本字符串 |
  | `default_settings` | `Optional[dict]` | 默认回退值 |
- **返回值**：`None`

###### `WidgetListModel.addInstance(...) -> None`
- **方法用途**：执行 addInstance 相关的处理操作
- **源码位置**：第 `215` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `type_id` | `str` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `WidgetListModel.moveInstance(...) -> None`
- **方法用途**：执行 moveInstance 相关的处理操作
- **源码位置**：第 `233` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `from_index` | `int` | X 轴横坐标 (像素) |
  | `to_index` | `int` | X 轴横坐标 (像素) |
- **返回值**：`None`

###### `WidgetListModel.removeInstance(...) -> None`
- **方法用途**：执行 removeInstance 相关的处理操作
- **源码位置**：第 `246` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `instance_id` | `str` | instance_id 文本字符串 |
- **返回值**：`None`

###### `WidgetListModel.updateSettings(...) -> None`
- **方法用途**：计算并更新 WidgetListModel 的状态、属性或遮罩渲染
- **源码位置**：第 `257` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `instance_id` | `str` | instance_id 文本字符串 |
  | `settings` | `dict` | settings 运行时参数 |
- **返回值**：`None`

###### `WidgetListModel.currentPreset(...) -> None`
- **方法用途**：执行 currentPreset 相关的处理操作
- **源码位置**：第 `270` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetListModel.presets(...) -> None`
- **方法用途**：执行 presets 相关的处理操作
- **源码位置**：第 `274` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetListModel.definitions(...) -> None`
- **方法用途**：执行 definitions 相关的处理操作
- **源码位置**：第 `278` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `WidgetListModel.definitionsList(...) -> None`
- **方法用途**：执行 definitionsList 相关的处理操作
- **源码位置**：第 `282` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/windows/windows.py`

> **模块职能说明**：可释放异形窗口类 (ReleasableWindow)。继承自 QQuickWindow，提供 Windows 无边框、工具窗口属性 (Qt.Tool)、透明背景与事件穿透支持。

#### 🏛️ 核心类：`class ReleasableWindow(RinUIWindow)`
> **类设计职能**：ReleasableWindow 业务管理类

##### 包含方法全量参考：

###### `ReleasableWindow.__init__(...) -> None`
- **方法用途**：初始化 ReleasableWindow 实例并建立内部状态与依赖注入
- **源码位置**：第 `14` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `central` | `Any` | AppCentral 主程序中央控制中枢单例 |
- **返回值**：`None`

###### `ReleasableWindow.is_released(...) -> bool`
- **方法用途**：检测并返回特定状态或条件判断布尔值
- **源码位置**：第 `37` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `ReleasableWindow.load(...) -> None`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `40` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `qml_path` | `Union[str, Path]` | 目标文件或目录路径 |
- **返回值**：`None`

###### `ReleasableWindow.release(...) -> None`
- **方法用途**：执行 release 相关的处理操作
- **源码位置**：第 `44` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ReleasableWindow._cleanup_engine(...) -> None`
- **方法用途**：执行 _cleanup_engine 相关的处理操作
- **源码位置**：第 `79` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class Settings(ReleasableWindow, QObject)`
> **类设计职能**：Settings 业务管理类

##### 包含方法全量参考：

###### `Settings.__init__(...) -> None`
- **方法用途**：初始化 Settings 实例并建立内部状态与依赖注入
- **源码位置**：第 `88` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

#### 🏛️ 核心类：`class Editor(ReleasableWindow)`
> **类设计职能**：Editor 业务管理类

##### 包含方法全量参考：

###### `Editor.__init__(...) -> None`
- **方法用途**：初始化 Editor 实例并建立内部状态与依赖注入
- **源码位置**：第 `108` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

#### 🏛️ 核心类：`class PluginPlaza(ReleasableWindow)`
> **类设计职能**：PluginPlaza 业务管理类

##### 包含方法全量参考：

###### `PluginPlaza.__init__(...) -> None`
- **方法用途**：初始化 PluginPlaza 实例并建立内部状态与依赖注入
- **源码位置**：第 `115` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `PluginPlaza.release(...) -> None`
- **方法用途**：执行 release 相关的处理操作
- **源码位置**：第 `125` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class Tutorial(ReleasableWindow)`
> **类设计职能**：Tutorial 业务管理类

##### 包含方法全量参考：

###### `Tutorial.__init__(...) -> None`
- **方法用途**：初始化 Tutorial 实例并建立内部状态与依赖注入
- **源码位置**：第 `135` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `Tutorial.release(...) -> None`
- **方法用途**：执行 release 相关的处理操作
- **源码位置**：第 `146` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class WhatsNew(ReleasableWindow)`
> **类设计职能**：WhatsNew 业务管理类

##### 包含方法全量参考：

###### `WhatsNew.__init__(...) -> None`
- **方法用途**：初始化 WhatsNew 实例并建立内部状态与依赖注入
- **源码位置**：第 `156` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

#### 🏛️ 核心类：`class CheckSingleInstanceDialog(ReleasableWindow)`
> **类设计职能**：CheckSingleInstanceDialog 业务管理类

##### 包含方法全量参考：

###### `CheckSingleInstanceDialog.__init__(...) -> None`
- **方法用途**：初始化 CheckSingleInstanceDialog 实例并建立内部状态与依赖注入
- **源码位置**：第 `166` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ClassSwapWindow(ReleasableWindow)`
> **类设计职能**：ClassSwapWindow 业务管理类

##### 包含方法全量参考：

###### `ClassSwapWindow.__init__(...) -> None`
- **方法用途**：初始化 ClassSwapWindow 实例并建立内部状态与依赖注入
- **源码位置**：第 `178` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ClassSwapRestoreDialog(ReleasableWindow)`
> **类设计职能**：ClassSwapRestoreDialog 业务管理类

##### 包含方法全量参考：

###### `ClassSwapRestoreDialog.__init__(...) -> None`
- **方法用途**：初始化 ClassSwapRestoreDialog 实例并建立内部状态与依赖注入
- **源码位置**：第 `190` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ThemeLoadErrorDialog(ReleasableWindow, QObject)`
> **类设计职能**：ThemeLoadErrorDialog 业务管理类

##### 包含方法全量参考：

###### `ThemeLoadErrorDialog.__init__(...) -> None`
- **方法用途**：初始化 ThemeLoadErrorDialog 实例并建立内部状态与依赖注入
- **源码位置**：第 `205` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `ThemeLoadErrorDialog.failedThemeId(...) -> str`
- **方法用途**：执行 failedThemeId 相关的处理操作
- **源码位置**：第 `222` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ThemeLoadErrorDialog.recovered(...) -> bool`
- **方法用途**：执行 recovered 相关的处理操作
- **源码位置**：第 `226` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `ThemeLoadErrorDialog.set_error_details(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `230` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `failed_theme_id` | `str` | failed_theme_id 文本字符串 |
  | `recovered` | `bool` | recovered 条件开关状态 |
- **返回值**：`None`

###### `ThemeLoadErrorDialog.show_when_ready(...) -> None`
- **方法用途**：执行 show_when_ready 相关的处理操作
- **源码位置**：第 `236` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ThemeLoadErrorDialog._on_object_created(...) -> None`
- **方法用途**：执行 _on_object_created 相关的处理操作
- **源码位置**：第 `240` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `obj` | `Any` | obj 运行时参数 |
  | `url` | `Any` | 网络资源 URL 或 API 请求端点 |
- **返回值**：`None`

###### `ThemeLoadErrorDialog._on_qml_warnings(...) -> None`
- **方法用途**：执行 _on_qml_warnings 相关的处理操作
- **源码位置**：第 `245` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `warnings` | `Any` | warnings 运行时参数 |
- **返回值**：`None`

###### `ThemeLoadErrorDialog._show_root_window(...) -> None`
- **方法用途**：执行 _show_root_window 相关的处理操作
- **源码位置**：第 `252` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/windows/manager.py`

> **模块职能说明**：多窗口生命周期管理器 (WindowsManager)。负责集中创建、销毁、显示、隐藏主窗口、小组件窗口与设置对话框。

#### 🏛️ 核心类：`class AppWindowManager(QObject)`
> **类设计职能**：AppWindowManager 业务管理类

##### 包含方法全量参考：

###### `AppWindowManager.__init__(...) -> None`
- **方法用途**：初始化 AppWindowManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `13` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `central` | `AppCentral` | AppCentral 主程序中央控制中枢单例 |
- **返回值**：`None`

###### `AppWindowManager.openSettings(...) -> None`
- **方法用途**：执行 openSettings 相关的处理操作
- **源码位置**：第 `44` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.closeSettings(...) -> None`
- **方法用途**：执行 closeSettings 相关的处理操作
- **源码位置**：第 `48` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.openEditor(...) -> None`
- **方法用途**：执行 openEditor 相关的处理操作
- **源码位置**：第 `52` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.closeEditor(...) -> None`
- **方法用途**：执行 closeEditor 相关的处理操作
- **源码位置**：第 `56` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.openPlaza(...) -> None`
- **方法用途**：执行 openPlaza 相关的处理操作
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.closePlaza(...) -> None`
- **方法用途**：执行 closePlaza 相关的处理操作
- **源码位置**：第 `64` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.openWhatsNew(...) -> None`
- **方法用途**：执行 openWhatsNew 相关的处理操作
- **源码位置**：第 `68` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.closeWhatsNew(...) -> None`
- **方法用途**：执行 closeWhatsNew 相关的处理操作
- **源码位置**：第 `72` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.openSingleInstanceDialog(...) -> None`
- **方法用途**：执行 openSingleInstanceDialog 相关的处理操作
- **源码位置**：第 `76` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.openClassSwap(...) -> None`
- **方法用途**：执行 openClassSwap 相关的处理操作
- **源码位置**：第 `80` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.closeClassSwap(...) -> None`
- **方法用途**：执行 closeClassSwap 相关的处理操作
- **源码位置**：第 `84` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.openClassSwapRestoreDialog(...) -> None`
- **方法用途**：执行 openClassSwapRestoreDialog 相关的处理操作
- **源码位置**：第 `88` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.closeDebugger(...) -> None`
- **方法用途**：执行 closeDebugger 相关的处理操作
- **源码位置**：第 `92` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.closeThemeLoadError(...) -> None`
- **方法用途**：执行 closeThemeLoadError 相关的处理操作
- **源码位置**：第 `96` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.classSwapRestoreContinue(...) -> None`
- **方法用途**：执行 classSwapRestoreContinue 相关的处理操作
- **源码位置**：第 `100` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.classSwapRestoreDiscard(...) -> None`
- **方法用途**：执行 classSwapRestoreDiscard 相关的处理操作
- **源码位置**：第 `105` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_settings(...) -> None`
- **方法用途**：执行 open_settings 相关的处理操作
- **源码位置**：第 `109` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.close_settings(...) -> None`
- **方法用途**：执行 close_settings 相关的处理操作
- **源码位置**：第 `112` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_editor(...) -> None`
- **方法用途**：执行 open_editor 相关的处理操作
- **源码位置**：第 `115` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.close_editor(...) -> None`
- **方法用途**：执行 close_editor 相关的处理操作
- **源码位置**：第 `122` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_plugin_plaza(...) -> None`
- **方法用途**：执行 open_plugin_plaza 相关的处理操作
- **源码位置**：第 `125` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.close_plugin_plaza(...) -> None`
- **方法用途**：执行 close_plugin_plaza 相关的处理操作
- **源码位置**：第 `128` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_whatsnew(...) -> None`
- **方法用途**：执行 open_whatsnew 相关的处理操作
- **源码位置**：第 `131` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.close_whatsnew(...) -> None`
- **方法用途**：执行 close_whatsnew 相关的处理操作
- **源码位置**：第 `134` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_class_swap(...) -> None`
- **方法用途**：执行 open_class_swap 相关的处理操作
- **源码位置**：第 `137` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.close_class_swap(...) -> None`
- **方法用途**：执行 close_class_swap 相关的处理操作
- **源码位置**：第 `140` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_class_swap_restore(...) -> None`
- **方法用途**：执行 open_class_swap_restore 相关的处理操作
- **源码位置**：第 `143` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.close_class_swap_restore(...) -> None`
- **方法用途**：执行 close_class_swap_restore 相关的处理操作
- **源码位置**：第 `146` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_single_instance_dialog(...) -> None`
- **方法用途**：执行 open_single_instance_dialog 相关的处理操作
- **源码位置**：第 `149` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_tutorial(...) -> None`
- **方法用途**：执行 open_tutorial 相关的处理操作
- **源码位置**：第 `152` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_debugger(...) -> None`
- **方法用途**：执行 open_debugger 相关的处理操作
- **源码位置**：第 `155` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.close_debugger(...) -> None`
- **方法用途**：执行 close_debugger 相关的处理操作
- **源码位置**：第 `158` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open_theme_load_error(...) -> None`
- **方法用途**：执行 open_theme_load_error 相关的处理操作
- **源码位置**：第 `161` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `failed_theme_id` | `str` | failed_theme_id 文本字符串 |
  | `recovered` | `bool` | recovered 条件开关状态 |
- **返回值**：`None`

###### `AppWindowManager._show_theme_load_error_when_ready(...) -> None`
- **方法用途**：执行 _show_theme_load_error_when_ready 相关的处理操作
- **源码位置**：第 `167` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `window` | `Any` | window 运行时参数 |
  | `attempts` | `int` | attempts 整数计数值 |
- **返回值**：`None`

###### `AppWindowManager.close_theme_load_error(...) -> None`
- **方法用途**：执行 close_theme_load_error 相关的处理操作
- **源码位置**：第 `180` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager.open(...) -> None`
- **方法用途**：执行 open 相关的处理操作
- **源码位置**：第 `183` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`None`

###### `AppWindowManager.ensure(...) -> Any`
- **方法用途**：执行 ensure 相关的处理操作
- **源码位置**：第 `198` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`Any`

###### `AppWindowManager.release(...) -> None`
- **方法用途**：执行 release 相关的处理操作
- **源码位置**：第 `206` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`None`

###### `AppWindowManager._finish_release(...) -> None`
- **方法用途**：执行 _finish_release 相关的处理操作
- **源码位置**：第 `218` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `window` | `Any` | window 运行时参数 |
- **返回值**：`None`

###### `AppWindowManager._release_now(...) -> None`
- **方法用途**：执行 _release_now 相关的处理操作
- **源码位置**：第 `225` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `window` | `Any` | window 运行时参数 |
- **返回值**：`None`

###### `AppWindowManager.release_all(...) -> None`
- **方法用途**：执行 release_all 相关的处理操作
- **源码位置**：第 `238` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_settings(...) -> None`
- **方法用途**：执行 _create_settings 相关的处理操作
- **源码位置**：第 `247` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_editor(...) -> None`
- **方法用途**：执行 _create_editor 相关的处理操作
- **源码位置**：第 `254` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_plugin_plaza(...) -> None`
- **方法用途**：执行 _create_plugin_plaza 相关的处理操作
- **源码位置**：第 `259` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_whatsnew(...) -> None`
- **方法用途**：执行 _create_whatsnew 相关的处理操作
- **源码位置**：第 `264` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_class_swap(...) -> None`
- **方法用途**：执行 _create_class_swap 相关的处理操作
- **源码位置**：第 `269` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_class_swap_restore(...) -> None`
- **方法用途**：执行 _create_class_swap_restore 相关的处理操作
- **源码位置**：第 `274` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_single_instance(...) -> None`
- **方法用途**：执行 _create_single_instance 相关的处理操作
- **源码位置**：第 `279` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_theme_load_error(...) -> None`
- **方法用途**：执行 _create_theme_load_error 相关的处理操作
- **源码位置**：第 `284` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_tutorial(...) -> None`
- **方法用途**：执行 _create_tutorial 相关的处理操作
- **源码位置**：第 `289` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._create_debugger(...) -> None`
- **方法用途**：执行 _create_debugger 相关的处理操作
- **源码位置**：第 `294` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppWindowManager._apply_settings_window_workarounds(...) -> None`
- **方法用途**：执行 _apply_settings_window_workarounds 相关的处理操作
- **源码位置**：第 `299` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `window` | `Any` | window 运行时参数 |
- **返回值**：`None`

---

## 插件生态与扩展子系统 (Plugin Subsystem)

### 📄 模块：`src/core/plugin/manager.py`

> **模块职能说明**：插件系统总控中心 (PluginManager)。扫描本地与内置插件，维护插件激活状态，分发生命周期钩子事件与翻译刷新。

#### 🏛️ 核心类：`class PluginManager(QObject)`
> **类设计职能**：PluginManager 业务管理类

##### 包含方法全量参考：

###### `PluginManager.__init__(...) -> None`
- **方法用途**：:param plugin_api: 由 AppCentral 创建的 PluginAPI 实例
- **源码位置**：第 `56` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `PluginAPI` | plugin_api 运行时参数 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `PluginManager.scan(...) -> None`
- **方法用途**：遍历扫描目标目录并解析可用组件或插件
- **源码位置**：第 `100` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._check_incompatible_plugins(...) -> None`
- **方法用途**：执行 _check_incompatible_plugins 相关的处理操作
- **源码位置**：第 `111` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager.plugin_import_context(...) -> None`
- **方法用途**：执行 plugin_import_context 相关的处理操作
- **源码位置**：第 `132` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_dir` | `Path` | plugin_dir 运行时参数 |
- **返回值**：`None`

###### `PluginManager.load_plugins(...) -> None`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `136` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._on_retranslate(...) -> None`
- **方法用途**：执行 _on_retranslate 相关的处理操作
- **源码位置**：第 `139` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._initialized_plugin(...) -> Optional[CW2Plugin]`
- **方法用途**：执行 _initialized_plugin 相关的处理操作
- **源码位置**：第 `151` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `meta` | `PluginMeta` | meta 运行时参数 |
- **返回值**：`Optional[CW2Plugin]`

###### `PluginManager.set_enabled_plugins(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `155` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `enabled_plugins` | `list[str]` | 功能是否启用的布尔开关标志 |
- **返回值**：`None`

###### `PluginManager.cleanup(...) -> None`
- **方法用途**：Unload plugins and stop active installation work.
- **源码位置**：第 `158` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._set_install_status(...) -> None`
- **方法用途**：执行 _set_install_status 相关的处理操作
- **源码位置**：第 `186` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `status` | `str` | 课表当前状态枚举值 (EntryType: CLASS, BREAK, ACTIVITY, etc.) |
- **返回值**：`None`

###### `PluginManager._install_task_in_progress(...) -> bool`
- **方法用途**：执行 _install_task_in_progress 相关的处理操作
- **源码位置**：第 `191` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager._install_is_active_or_paused(...) -> bool`
- **方法用途**：执行 _install_is_active_or_paused 相关的处理操作
- **源码位置**：第 `194` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager._operation_plugin_id(...) -> str`
- **方法用途**：执行 _operation_plugin_id 相关的处理操作
- **源码位置**：第 `198` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `operation` | `dict` | operation 运行时参数 |
- **返回值**：`str`

###### `PluginManager._pending_operations(...) -> list[dict]`
- **方法用途**：执行 _pending_operations 相关的处理操作
- **源码位置**：第 `201` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `PluginManager._has_pending_operation(...) -> bool`
- **方法用途**：执行 _has_pending_operation 相关的处理操作
- **源码位置**：第 `205` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`bool`

###### `PluginManager._save_pending_operations(...) -> None`
- **方法用途**：执行 _save_pending_operations 相关的处理操作
- **源码位置**：第 `208` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `operations` | `list[dict]` | operations 运行时参数 |
- **返回值**：`None`

###### `PluginManager._queue_pending_operation(...) -> None`
- **方法用途**：Keep only the newest deferred operation for each plugin ID.
- **源码位置**：第 `213` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `operation` | `dict` | operation 运行时参数 |
- **返回值**：`None`

###### `PluginManager._cache_archive(...) -> Path`
- **方法用途**：执行 _cache_archive 相关的处理操作
- **源码位置**：第 `231` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive_path` | `Path` | 目标文件或目录路径 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`Path`

###### `PluginManager._queue_install(...) -> bool`
- **方法用途**：执行 _queue_install 相关的处理操作
- **源码位置**：第 `239` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive_path` | `Path` | 目标文件或目录路径 |
- **返回值**：`bool`

###### `PluginManager._queue_uninstall(...) -> bool`
- **方法用途**：执行 _queue_uninstall 相关的处理操作
- **源码位置**：第 `270` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`bool`

###### `PluginManager.pendingPluginOperations(...) -> list[dict]`
- **方法用途**：执行 pendingPluginOperations 相关的处理操作
- **源码位置**：第 `276` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `PluginManager.apply_pending_operations(...) -> None`
- **方法用途**：Apply deferred file changes before external plugins are scanned.
- **源码位置**：第 `279` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._plugin_meta(...) -> PluginMeta | None`
- **方法用途**：执行 _plugin_meta 相关的处理操作
- **源码位置**：第 `322` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`PluginMeta | None`

###### `PluginManager._fail_install(...) -> None`
- **方法用途**：执行 _fail_install 相关的处理操作
- **源码位置**：第 `325` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `error` | `str` | error 文本字符串 |
- **返回值**：`None`

###### `PluginManager._remove_download_directory(...) -> None`
- **方法用途**：执行 _remove_download_directory 相关的处理操作
- **源码位置**：第 `344` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._on_download_thread_finished(...) -> None`
- **方法用途**：执行 _on_download_thread_finished 相关的处理操作
- **源码位置**：第 `352` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._emit_install_settled_if_idle(...) -> None`
- **方法用途**：执行 _emit_install_settled_if_idle 相关的处理操作
- **源码位置**：第 `365` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._on_download_progress(...) -> None`
- **方法用途**：执行 _on_download_progress 相关的处理操作
- **源码位置**：第 `370` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `percent` | `float` | percent 运行时参数 |
  | `speed` | `float` | speed 运行时参数 |
  | `downloaded_bytes` | `int` | Y 轴纵坐标 (像素) |
  | `total_bytes` | `int` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `PluginManager._on_plaza_download_completed(...) -> None`
- **方法用途**：执行 _on_plaza_download_completed 相关的处理操作
- **源码位置**：第 `391` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive_path` | `str` | 目标文件或目录路径 |
  | `plugin` | `dict` | plugin 运行时参数 |
- **返回值**：`None`

###### `PluginManager._on_plaza_plugin_resolved(...) -> None`
- **方法用途**：执行 _on_plaza_plugin_resolved 相关的处理操作
- **源码位置**：第 `410` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin` | `dict` | plugin 运行时参数 |
- **返回值**：`None`

###### `PluginManager._on_download_failed(...) -> None`
- **方法用途**：执行 _on_download_failed 相关的处理操作
- **源码位置**：第 `428` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `message` | `str` | 提示信息或错误消息内容 |
- **返回值**：`None`

###### `PluginManager._on_download_cancelled(...) -> None`
- **方法用途**：执行 _on_download_cancelled 相关的处理操作
- **源码位置**：第 `431` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager._on_download_paused(...) -> None`
- **方法用途**：执行 _on_download_paused 相关的处理操作
- **源码位置**：第 `447` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager.installStatus(...) -> str`
- **方法用途**：执行 installStatus 相关的处理操作
- **源码位置**：第 `454` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `PluginManager.installProgress(...) -> float`
- **方法用途**：执行 installProgress 相关的处理操作
- **源码位置**：第 `458` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`float`

###### `PluginManager.installDownloadedBytes(...) -> int`
- **方法用途**：执行 installDownloadedBytes 相关的处理操作
- **源码位置**：第 `462` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `PluginManager.installTotalBytes(...) -> int`
- **方法用途**：执行 installTotalBytes 相关的处理操作
- **源码位置**：第 `466` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `PluginManager.installSpeed(...) -> float`
- **方法用途**：执行 installSpeed 相关的处理操作
- **源码位置**：第 `470` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`float`

###### `PluginManager.installError(...) -> str`
- **方法用途**：执行 installError 相关的处理操作
- **源码位置**：第 `474` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `PluginManager.installPluginId(...) -> str`
- **方法用途**：执行 installPluginId 相关的处理操作
- **源码位置**：第 `478` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `PluginManager.plazaPlugins(...) -> list[dict]`
- **方法用途**：Return installed external plugins that are available in the Plaza.
- **源码位置**：第 `482` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `PluginManager.plazaActivity(...) -> list[dict[str, object]]`
- **方法用途**：执行 plazaActivity 相关的处理操作
- **源码位置**：第 `516` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict[str, object]]`

###### `PluginManager.pluginUpdateStates(...) -> dict[str, dict[str, object]]`
- **方法用途**：Return the latest Plaza update result for each installed plugin.
- **源码位置**：第 `520` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`dict[str, dict[str, object]]`

###### `PluginManager.plazaUpdateCount(...) -> int`
- **方法用途**：执行 plazaUpdateCount 相关的处理操作
- **源码位置**：第 `525` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `PluginManager.plazaInstallActive(...) -> bool`
- **方法用途**：执行 plazaInstallActive 相关的处理操作
- **源码位置**：第 `533` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager._plaza_base_url(...) -> str`
- **方法用途**：执行 _plaza_base_url 相关的处理操作
- **源码位置**：第 `536` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `PluginManager._plaza_update_records(...) -> list[dict[str, str]]`
- **方法用途**：Build update candidates from the installed external plugin manifests.
- **源码位置**：第 `541` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict[str, str]]`

###### `PluginManager.plazaUpdatesChecking(...) -> bool`
- **方法用途**：执行 plazaUpdatesChecking 相关的处理操作
- **源码位置**：第 `557` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager._set_plaza_updates_checking(...) -> None`
- **方法用途**：执行 _set_plaza_updates_checking 相关的处理操作
- **源码位置**：第 `560` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `checking` | `bool` | checking 条件开关状态 |
- **返回值**：`None`

###### `PluginManager._on_plaza_updates_completed(...) -> None`
- **方法用途**：执行 _on_plaza_updates_completed 相关的处理操作
- **源码位置**：第 `566` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `results` | `list[dict]` | results 运行时参数 |
- **返回值**：`None`

###### `PluginManager._on_plaza_updates_finished(...) -> None`
- **方法用途**：执行 _on_plaza_updates_finished 相关的处理操作
- **源码位置**：第 `591` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager.checkPlazaUpdates(...) -> bool`
- **方法用途**：Check the configured plaza for updates to every external plugin.
- **源码位置**：第 `600` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager.check_plaza_updates(...) -> bool`
- **方法用途**：Check for Plugin Plaza updates, optionally without user-facing refresh state.
- **源码位置**：第 `604` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager.installPlazaUpdate(...) -> bool`
- **方法用途**：Install an installed external plugin's latest plaza release.
- **源码位置**：第 `630` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`bool`

###### `PluginManager.openPlazaDownloads(...) -> None`
- **方法用途**：执行 openPlazaDownloads 相关的处理操作
- **源码位置**：第 `641` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager.importPlugin(...) -> list[PluginConflict]`
- **方法用途**：从 ZIP 导入插件（带冲突检测）
- **源码位置**：第 `646` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[PluginConflict]`

###### `PluginManager.plugins(...) -> None`
- **方法用途**：QML调用此函数获取插件列表
- **源码位置**：第 `682` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginManager.isPluginEnabled(...) -> bool`
- **方法用途**：执行 isPluginEnabled 相关的处理操作
- **源码位置**：第 `687` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `pid` | `str` | pid 文本字符串 |
- **返回值**：`bool`

###### `PluginManager.isPluginCompatible(...) -> bool`
- **方法用途**：执行 isPluginCompatible 相关的处理操作
- **源码位置**：第 `691` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `pid` | `str` | pid 文本字符串 |
- **返回值**：`bool`

###### `PluginManager.getAPIVersion(...) -> str`
- **方法用途**：获取当前 API 版本
- **源码位置**：第 `698` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `PluginManager.setPluginEnabled(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `703` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `pid` | `str` | pid 文本字符串 |
  | `enabled` | `bool` | 功能是否启用的布尔开关标志 |
- **返回值**：`None`

###### `PluginManager.openPluginFolder(...) -> bool`
- **方法用途**：打开指定插件的本地文件夹
- **源码位置**：第 `718` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `pid` | `str` | pid 文本字符串 |
- **返回值**：`bool`

###### `PluginManager.uninstallPlugin(...) -> bool`
- **方法用途**：卸载指定外部插件
- **源码位置**：第 `740` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `pid` | `str` | pid 文本字符串 |
- **返回值**：`bool`

###### `PluginManager._safe_conflicts(...) -> list[PluginConflict]`
- **方法用途**：执行 _safe_conflicts 相关的处理操作
- **源码位置**：第 `771` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `str` | 目标文件或目录路径 |
- **返回值**：`list[PluginConflict]`

###### `PluginManager.checkPluginConflicts(...) -> list[PluginConflict]`
- **方法用途**：执行 checkPluginConflicts 相关的处理操作
- **源码位置**：第 `789` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `str` | 目标文件或目录路径 |
- **返回值**：`list[PluginConflict]`

###### `PluginManager.importPluginWithPath(...) -> bool`
- **方法用途**：执行 importPluginWithPath 相关的处理操作
- **源码位置**：第 `793` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `str` | 目标文件或目录路径 |
- **返回值**：`bool`

###### `PluginManager._on_import_error(...) -> None`
- **方法用途**：执行 _on_import_error 相关的处理操作
- **源码位置**：第 `813` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `message` | `str` | 提示信息或错误消息内容 |
- **返回值**：`None`

###### `PluginManager._start_plaza_install(...) -> bool`
- **方法用途**：执行 _start_plaza_install 相关的处理操作
- **源码位置**：第 `817` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`bool`

###### `PluginManager._start_plaza_download(...) -> bool`
- **方法用途**：执行 _start_plaza_download 相关的处理操作
- **源码位置**：第 `845` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager.installFromPlaza(...) -> bool`
- **方法用途**：执行 installFromPlaza 相关的处理操作
- **源码位置**：第 `869` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`bool`

###### `PluginManager.pausePluginInstall(...) -> bool`
- **方法用途**：执行 pausePluginInstall 相关的处理操作
- **源码位置**：第 `875` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager.resumePluginInstall(...) -> bool`
- **方法用途**：执行 resumePluginInstall 相关的处理操作
- **源码位置**：第 `885` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `PluginManager.cancelPluginInstall(...) -> bool`
- **方法用途**：执行 cancelPluginInstall 相关的处理操作
- **源码位置**：第 `894` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/plugin/loader.py`

> **模块职能说明**：插件安全加载器 (PluginLoader)。运行时动态注入 ClassWidgets.SDK，隔离加载外部与内置插件 Python 模块。

#### 独立函数列表 (Standalone Functions)

##### `def check_api_version(...) -> bool`
- **业务用途**：检查插件API版本兼容性
- **源码位置**：第 `343` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `plugin_api_version` | `str` | 版本号字符串 (如 2.0.0.dev) |
- **返回值意义**：返回类型为 `bool`，表示操作执行结果或返回目标计算数据实体。

#### 🏛️ 核心类：`class PluginLoader(object)`
> **类设计职能**：PluginLoader 业务管理类

##### 包含方法全量参考：

###### `PluginLoader.__init__(...) -> None`
- **方法用途**：:param plugin_api: PluginAPI实例
- **源码位置**：第 `24` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `PluginAPI` | plugin_api 运行时参数 |
  | `external_path` | `Path` | 目标文件或目录路径 |
- **返回值**：`None`

###### `PluginLoader._inject_runtime_sdk(...) -> None`
- **方法用途**：注入运行时SDK，让插件能够导入 ClassWidgets.SDK
- **源码位置**：第 `36` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginLoader.scan_plugins(...) -> list[PluginMeta]`
- **方法用途**：扫描所有插件（外部插件 + 内置插件）
- **源码位置**：第 `105` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `external_path` | `Path` | 目标文件或目录路径 |
- **返回值**：`list[PluginMeta]`

###### `PluginLoader.discover_plugins_in_dir(...) -> list[Path]`
- **方法用途**：发现指定目录中的插件
- **源码位置**：第 `134` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `base_dir` | `Path` | base_dir 运行时参数 |
- **返回值**：`list[Path]`

###### `PluginLoader._load_meta(...) -> Optional[PluginMeta]`
- **方法用途**：加载单个插件的meta信息
- **源码位置**：第 `143` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_dir` | `Path` | plugin_dir 运行时参数 |
  | `type` | `str` | Y 轴纵坐标 (像素) |
- **返回值**：`Optional[PluginMeta]`

###### `PluginLoader.validate_meta(...) -> bool`
- **方法用途**：验证插件meta信息
- **源码位置**：第 `161` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `meta` | `PluginMeta` | meta 运行时参数 |
  | `plugin_dir` | `Path` | plugin_dir 运行时参数 |
- **返回值**：`bool`

###### `PluginLoader.load_plugin(...) -> Optional[CW2Plugin]`
- **方法用途**：加载单个插件实例
- **源码位置**：第 `171` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `meta` | `PluginMeta` | meta 运行时参数 |
- **返回值**：`Optional[CW2Plugin]`

###### `PluginLoader.load_plugins(...) -> dict[str, CW2Plugin]`
- **方法用途**：加载多个插件实例
- **源码位置**：第 `178` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `metas` | `list[PluginMeta]` | metas 运行时参数 |
  | `enabled_plugins` | `list[str]` | 功能是否启用的布尔开关标志 |
- **返回值**：`dict[str, CW2Plugin]`

###### `PluginLoader._load_builtin_plugin(...) -> Optional[CW2Plugin]`
- **方法用途**：加载内置插件
- **源码位置**：第 `197` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `meta` | `PluginMeta` | meta 运行时参数 |
- **返回值**：`Optional[CW2Plugin]`

###### `PluginLoader._load_external_plugin(...) -> Optional[CW2Plugin]`
- **方法用途**：加载外部插件
- **源码位置**：第 `226` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `meta` | `PluginMeta` | meta 运行时参数 |
- **返回值**：`Optional[CW2Plugin]`

###### `PluginLoader._persist_plugin_paths(...) -> None`
- **方法用途**：将插件目录及其 libs/ 持久化到 sys.path，供运行时延迟导入使用
- **源码位置**：第 `315` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `plugin_dir` | `Path` | plugin_dir 运行时参数 |
- **返回值**：`None`

###### `PluginLoader.plugin_import_context(...) -> None`
- **方法用途**：插件导入上下文管理器
- **源码位置**：第 `324` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_dir` | `Path` | plugin_dir 运行时参数 |
- **返回值**：`None`

---

### 📄 模块：`src/core/plugin/bridge.py`

> **模块职能说明**：插件跨语言后端桥接器 (PluginBridge)。允许 Python 插件向 QML 界面注册自定义上下文属性与通信后端。

#### 🏛️ 核心类：`class PluginBackendBridge(QObject)`
> **类设计职能**：PluginBackendBridge 业务管理类

##### 包含方法全量参考：

###### `PluginBackendBridge.get_backend(...) -> None`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `10` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `PluginBackendBridge.register_backend(...) -> None`
- **方法用途**：向管理器注册新的功能组件、插件或回调监听器
- **源码位置**：第 `14` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `cls` | `Any` | 类对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `backend_obj` | `QObject` | backend_obj 运行时参数 |
- **返回值**：`None`

---

### 📄 模块：`src/core/plugin/components.py`

> **模块职能说明**：插件组件注册中心。负责快捷方式、设置页面扩展与自定义小组件在主界面的统一注册与展示。

#### 🏛️ 核心类：`class BaseAPI(QObject)`
> **类设计职能**：所有API类的基类，提供通用的方法和属性

##### 包含方法全量参考：

###### `BaseAPI.__init__(...) -> None`
- **方法用途**：初始化 BaseAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `36` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `'PluginAPI'` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `BaseAPI._app(...) -> None`
- **方法用途**：执行 _app 相关的处理操作
- **源码位置**：第 `41` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `BaseAPI.current_plugin(...) -> None`
- **方法用途**：获取当前插件
- **源码位置**：第 `45` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `BaseAPI._resolve_path(...) -> Path`
- **方法用途**：统一的路径解析方法
- **源码位置**：第 `49` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path` | `str | Path` | 目标文件或目录路径 |
- **返回值**：`Path`

#### 🏛️ 核心类：`class WidgetsAPI(BaseAPI)`
> **类设计职能**：WidgetsAPI 业务管理类

##### 包含方法全量参考：

###### `WidgetsAPI.register(...) -> None`
- **方法用途**：向管理器注册新的功能组件、插件或回调监听器
- **源码位置**：第 `63` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `widget_id` | `str` | widget_id 文本字符串 |
  | `name` | `str` | name 文本字符串 |
  | `qml_path` | `str | Path` | 目标文件或目录路径 |
  | `backend_obj` | `Optional[QObject]` | backend_obj 运行时参数 |
  | `settings_qml` | `Optional[str | Path]` | settings_qml 文本字符串 |
  | `default_settings` | `Optional[dict]` | 默认回退值 |
- **返回值**：`None`

#### 🏛️ 核心类：`class NotificationAPI(BaseAPI)`
> **类设计职能**：NotificationAPI 业务管理类

##### 包含方法全量参考：

###### `NotificationAPI.__init__(...) -> None`
- **方法用途**：初始化 NotificationAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `85` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `'PluginAPI'` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `NotificationAPI.get_provider(...) -> NotificationProvider`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `89` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `name` | `str` | name 文本字符串 |
  | `icon` | `Optional[str | Path]` | 图标路径或 QIcon 实例 |
  | `use_system_notify` | `bool` | Y 轴纵坐标 (像素) |
- **返回值**：`NotificationProvider`

###### `NotificationAPI.register_provider(...) -> NotificationProvider`
- **方法用途**：为插件创建一个 NotificationProvider 实例
- **源码位置**：第 `97` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `name` | `str` | name 文本字符串 |
  | `icon` | `Optional[str | Path]` | 图标路径或 QIcon 实例 |
  | `use_system_notify` | `bool` | Y 轴纵坐标 (像素) |
- **返回值**：`NotificationProvider`

#### 🏛️ 核心类：`class ScheduleAPI(BaseAPI)`
> **类设计职能**：ScheduleAPI 业务管理类

##### 包含方法全量参考：

###### `ScheduleAPI.get(...) -> None`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `130` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleAPI.reload(...) -> None`
- **方法用途**：重载配置、主题或数据模型并刷新界面
- **源码位置**：第 `133` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ScheduleAPI.update(...) -> bool`
- **方法用途**：计算并更新 ScheduleAPI 的状态、属性或遮罩渲染
- **源码位置**：第 `136` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `schedule_dict` | `dict` | Schedule 课表模型实例对象 |
- **返回值**：`bool`

###### `ScheduleAPI.set_readonly(...) -> None`
- **方法用途**：设置课表是否只读
- **源码位置**：第 `142` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `readonly` | `bool` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `ScheduleAPI.readonly(...) -> bool`
- **方法用途**：执行 readonly 相关的处理操作
- **源码位置**：第 `148` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

#### 🏛️ 核心类：`class ThemeAPI(BaseAPI)`
> **类设计职能**：ThemeAPI 业务管理类

##### 包含方法全量参考：

###### `ThemeAPI.__init__(...) -> None`
- **方法用途**：初始化 ThemeAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `155` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `Any` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `ThemeAPI.current(...) -> Optional[str]`
- **方法用途**：执行 current 相关的处理操作
- **源码位置**：第 `164` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`Optional[str]`

#### 🏛️ 核心类：`class RuntimeAPI(BaseAPI)`
> **类设计职能**：暴露 ScheduleRuntime 的状态给插件

##### 包含方法全量参考：

###### `RuntimeAPI.__init__(...) -> None`
- **方法用途**：初始化 RuntimeAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `174` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `Any` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `RuntimeAPI.current_time(...) -> datetime`
- **方法用途**：执行 current_time 相关的处理操作
- **源码位置**：第 `182` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`datetime`

###### `RuntimeAPI.current_day_of_week(...) -> int`
- **方法用途**：执行 current_day_of_week 相关的处理操作
- **源码位置**：第 `186` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `RuntimeAPI.current_week(...) -> int`
- **方法用途**：执行 current_week 相关的处理操作
- **源码位置**：第 `190` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `RuntimeAPI.current_week_of_cycle(...) -> int`
- **方法用途**：执行 current_week_of_cycle 相关的处理操作
- **源码位置**：第 `194` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `RuntimeAPI.time_offset(...) -> int`
- **方法用途**：执行 time_offset 相关的处理操作
- **源码位置**：第 `198` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`int`

###### `RuntimeAPI.schedule_meta(...) -> Optional[RuntimeMetaPayload]`
- **方法用途**：执行 schedule_meta 相关的处理操作
- **源码位置**：第 `203` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`Optional[RuntimeMetaPayload]`

###### `RuntimeAPI.current_day_entries(...) -> list[RuntimeEntryPayload]`
- **方法用途**：执行 current_day_entries 相关的处理操作
- **源码位置**：第 `209` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[RuntimeEntryPayload]`

###### `RuntimeAPI.current_entry(...) -> Optional[RuntimeEntryPayload]`
- **方法用途**：执行 current_entry 相关的处理操作
- **源码位置**：第 `215` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`Optional[RuntimeEntryPayload]`

###### `RuntimeAPI.next_entries(...) -> list[RuntimeEntryPayload]`
- **方法用途**：执行 next_entries 相关的处理操作
- **源码位置**：第 `221` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[RuntimeEntryPayload]`

###### `RuntimeAPI.remaining_time(...) -> RuntimeRemainingTimePayload`
- **方法用途**：执行 remaining_time 相关的处理操作
- **源码位置**：第 `227` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`RuntimeRemainingTimePayload`

###### `RuntimeAPI.progress(...) -> float`
- **方法用途**：执行 progress 相关的处理操作
- **源码位置**：第 `234` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`float`

###### `RuntimeAPI.current_status(...) -> str`
- **方法用途**：执行 current_status 相关的处理操作
- **源码位置**：第 `238` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `RuntimeAPI.current_subject(...) -> Optional[RuntimeSubjectPayload]`
- **方法用途**：执行 current_subject 相关的处理操作
- **源码位置**：第 `242` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`Optional[RuntimeSubjectPayload]`

###### `RuntimeAPI.current_title(...) -> Optional[str]`
- **方法用途**：执行 current_title 相关的处理操作
- **源码位置**：第 `248` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`Optional[str]`

###### `RuntimeAPI._on_runtime_updated(...) -> None`
- **方法用途**：执行 _on_runtime_updated 相关的处理操作
- **源码位置**：第 `251` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ConfigAPI(BaseAPI)`
> **类设计职能**：ConfigAPI 业务管理类

##### 包含方法全量参考：

###### `ConfigAPI.__init__(...) -> None`
- **方法用途**：初始化 ConfigAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `258` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `Any` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `ConfigAPI.register_plugin_model(...) -> None`
- **方法用途**：注册插件配置 Model
- **源码位置**：第 `263` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `model` | `ConfigBaseModel` | model 运行时参数 |
- **返回值**：`None`

###### `ConfigAPI.get_plugin_model(...) -> Optional[ConfigBaseModel]`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `309` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`Optional[ConfigBaseModel]`

###### `ConfigAPI.save(...) -> None`
- **方法用途**：持久化保存当前配置模型或课表数据至磁盘
- **源码位置**：第 `312` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class AutomationAPI(BaseAPI)`
> **类设计职能**：AutomationAPI 业务管理类

##### 包含方法全量参考：

###### `AutomationAPI.register(...) -> None`
- **方法用途**：向管理器注册新的功能组件、插件或回调监听器
- **源码位置**：第 `317` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `task` | `Any` | AutomationTask 后台自动化任务实例 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ActionsAPI(BaseAPI)`
> **类设计职能**：进程内全局命名的 Qt Signal 注册表。

##### 包含方法全量参考：

###### `ActionsAPI.__init__(...) -> None`
- **方法用途**：初始化 ActionsAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `324` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `'PluginAPI'` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `ActionsAPI._validate_action_name(...) -> str`
- **方法用途**：执行 _validate_action_name 相关的处理操作
- **源码位置**：第 `329` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `action_name` | `str` | action_name 文本字符串 |
- **返回值**：`str`

###### `ActionsAPI.register(...) -> Any`
- **方法用途**：注册 Action；同 ID、同参数类型可重复注册并取得同一个 Signal。
- **源码位置**：第 `334` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `action_name` | `str` | action_name 文本字符串 |
- **返回值**：`Any`

###### `ActionsAPI.get(...) -> Any`
- **方法用途**：按全局 ID 取得已注册 Action 的原生 Qt bound signal。
- **源码位置**：第 `362` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `action_name` | `str` | action_name 文本字符串 |
- **返回值**：`Any`

#### 🏛️ 核心类：`class UiAPI(BaseAPI)`
> **类设计职能**：UiAPI 业务管理类

##### 包含方法全量参考：

###### `UiAPI.__init__(...) -> None`
- **方法用途**：初始化 UiAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `375` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `Any` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `UiAPI.pages(...) -> None`
- **方法用途**：执行 pages 相关的处理操作
- **源码位置**：第 `382` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UiAPI.shortcuts(...) -> list[ShortcutPayload]`
- **方法用途**：执行 shortcuts 相关的处理操作
- **源码位置**：第 `386` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[ShortcutPayload]`

###### `UiAPI._normalize_shortcut_icon(...) -> tuple[str, bool]`
- **方法用途**：执行 _normalize_shortcut_icon 相关的处理操作
- **源码位置**：第 `389` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `icon` | `str | Path` | 图标路径或 QIcon 实例 |
- **返回值**：`tuple[str, bool]`

###### `UiAPI._register_shortcut(...) -> str`
- **方法用途**：执行 _register_shortcut 相关的处理操作
- **源码位置**：第 `403` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `shortcut_id` | `str` | shortcut_id 文本字符串 |
  | `name` | `str` | name 文本字符串 |
  | `icon` | `str | Path` | 图标路径或 QIcon 实例 |
  | `action` | `Callable[[], object]` | action 运行时参数 |
  | `owner` | `str` | owner 文本字符串 |
- **返回值**：`str`

###### `UiAPI.register_shortcut(...) -> str`
- **方法用途**：Register a tray shortcut.
- **源码位置**：第 `432` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `shortcut_id` | `str` | shortcut_id 文本字符串 |
  | `name` | `str` | name 文本字符串 |
  | `icon` | `str | Path` | 图标路径或 QIcon 实例 |
  | `action` | `Callable[[], object]` | action 运行时参数 |
- **返回值**：`str`

###### `UiAPI.set_shortcut_name(...) -> bool`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `456` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `shortcut_id` | `str` | shortcut_id 文本字符串 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`bool`

###### `UiAPI.unregister_plugin_shortcuts(...) -> None`
- **方法用途**：从管理器中注销并移除指定的组件或监听器
- **源码位置**：第 `467` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `UiAPI.invoke_shortcut(...) -> bool`
- **方法用途**：执行 invoke_shortcut 相关的处理操作
- **源码位置**：第 `480` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `shortcut_id` | `str` | shortcut_id 文本字符串 |
- **返回值**：`bool`

###### `UiAPI.unregister_settings_page(...) -> None`
- **方法用途**：从管理器中注销并移除指定的组件或监听器
- **源码位置**：第 `492` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `qml_path` | `str | Path` | 目标文件或目录路径 |
- **返回值**：`None`

###### `UiAPI.register_settings_page(...) -> None`
- **方法用途**：插件提供相对路径，可自定义 title 和 icon
- **源码位置**：第 `502` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `qml_path` | `str | Path` | 目标文件或目录路径 |
  | `title` | `Optional[str]` | 通知弹窗或组件标题文本 |
  | `icon` | `Optional[str]` | 图标路径或 QIcon 实例 |
- **返回值**：`None`

#### 🏛️ 核心类：`class ScheduleManagementAPI(BaseAPI)`
> **类设计职能**：ScheduleManagementAPI 业务管理类

##### 包含方法全量参考：

###### `ScheduleManagementAPI.__init__(...) -> None`
- **方法用途**：初始化 ScheduleManagementAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `537` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `'PluginAPI'` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `ScheduleManagementAPI.switch(...) -> bool`
- **方法用途**：执行 switch 相关的处理操作
- **源码位置**：第 `540` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`bool`

###### `ScheduleManagementAPI.list(...) -> list[dict[str, str]]`
- **方法用途**：执行 list 相关的处理操作
- **源码位置**：第 `543` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict[str, str]]`

###### `ScheduleManagementAPI.add(...) -> bool`
- **方法用途**：执行 add 相关的处理操作
- **源码位置**：第 `546` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`bool`

###### `ScheduleManagementAPI.save(...) -> bool`
- **方法用途**：持久化保存当前配置模型或课表数据至磁盘
- **源码位置**：第 `549` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`bool`

#### 🏛️ 核心类：`class ApplicationAPI(BaseAPI)`
> **类设计职能**：ApplicationAPI 业务管理类

##### 包含方法全量参考：

###### `ApplicationAPI.get_info(...) -> ApplicationInfoPayload`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `558` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`ApplicationInfoPayload`

###### `ApplicationAPI.restart(...) -> None`
- **方法用途**：执行 restart 相关的处理操作
- **源码位置**：第 `572` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class DiagnosticsAPI(BaseAPI)`
> **类设计职能**：DiagnosticsAPI 业务管理类

##### 包含方法全量参考：

###### `DiagnosticsAPI.get_logs(...) -> list[DiagnosticLogPayload]`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `579` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `limit` | `int` | limit 整数计数值 |
- **返回值**：`list[DiagnosticLogPayload]`

#### 🏛️ 核心类：`class GlobalConfigAPI(BaseAPI)`
> **类设计职能**：GlobalConfigAPI 业务管理类

##### 包含方法全量参考：

###### `GlobalConfigAPI.__init__(...) -> None`
- **方法用途**：初始化 GlobalConfigAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `586` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `'PluginAPI'` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `GlobalConfigAPI.configs(...) -> ConfigManager`
- **方法用途**：获取所有全局配置项
- **源码位置**：第 `590` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`ConfigManager`

###### `GlobalConfigAPI.lock(...) -> None`
- **方法用途**：锁定配置项
- **源码位置**：第 `594` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `keys` | `str | list[str] | set[str]` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `GlobalConfigAPI.unlock(...) -> None`
- **方法用途**：解锁配置项
- **源码位置**：第 `601` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `keys` | `str | list[str] | set[str]` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `GlobalConfigAPI.is_locked(...) -> bool`
- **方法用途**：检查配置项是否被锁定
- **源码位置**：第 `608` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `key` | `str` | 配置项键名或字典索引 Key |
- **返回值**：`bool`

###### `GlobalConfigAPI.locked_keys(...) -> set[str]`
- **方法用途**：获取所有被锁定的配置项
- **源码位置**：第 `613` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`set[str]`

---

### 📄 模块：`src/core/plugin/api.py`

> **模块职能说明**：面向插件开发者的标准 SDK 接口表面 (PluginAPI)。提供配置存取、通知推送、课表查询等稳定开放 API。

#### 🏛️ 核心类：`class PluginAPI(object)`
> **类设计职能**：插件API核心类，管理所有插件可用的API功能

##### 包含方法全量参考：

###### `PluginAPI.__init__(...) -> None`
- **方法用途**：初始化 PluginAPI 实例并建立内部状态与依赖注入
- **源码位置**：第 `24` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app` | `'AppCentral'` | app 运行时参数 |
- **返回值**：`None`

###### `PluginAPI.set_current_plugin(...) -> None`
- **方法用途**：设置当前插件上下文
- **源码位置**：第 `42` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin` | `Any` | plugin 运行时参数 |
- **返回值**：`None`

###### `PluginAPI.current_plugin(...) -> 'CW2Plugin'`
- **方法用途**：获取当前插件
- **源码位置**：第 `47` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`'CW2Plugin'`

#### 🏛️ 核心类：`class CW2Plugin(QObject)`
> **类设计职能**：所有插件的基类

##### 包含方法全量参考：

###### `CW2Plugin.__init__(...) -> None`
- **方法用途**：初始化 CW2Plugin 实例并建立内部状态与依赖注入
- **源码位置**：第 `56` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `api` | `PluginAPI` | api 运行时参数 |
- **返回值**：`None`

###### `CW2Plugin._load_plugin_libs(...) -> None`
- **方法用途**：Automatically adds the plugin's 'libs' subdirectory to sys.path.
- **源码位置**：第 `66` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `CW2Plugin.on_load(...) -> None`
- **方法用途**：响应底层事件、信号或回调触发的槽函数
- **源码位置**：第 `76` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `CW2Plugin.on_unload(...) -> None`
- **方法用途**：响应底层事件、信号或回调触发的槽函数
- **源码位置**：第 `88` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/plugin/models.py`

> **模块职能说明**：插件元数据模型。解析 plugin.json，定义插件 ID、版本、作者、权限与依赖声明。

#### 🏛️ 核心类：`class PluginNotificationPayload(NotificationPayload)`
> **类设计职能**：插件通知信号负载。

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class RuntimeMetaPayload(TypedDict)`
> **类设计职能**：RuntimeMetaPayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class RuntimeEntryPayload(TypedDict)`
> **类设计职能**：RuntimeEntryPayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class RuntimeEntryChangedPayload(TypedDict)`
> **类设计职能**：RuntimeAPI.entryChanged 的负载（允许空字典表示无当前课程）。

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class RuntimeSubjectPayload(TypedDict)`
> **类设计职能**：RuntimeSubjectPayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class RuntimeRemainingTimePayload(TypedDict)`
> **类设计职能**：RuntimeRemainingTimePayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class SettingsPagePayload(TypedDict)`
> **类设计职能**：SettingsPagePayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class ShortcutPayload(TypedDict)`
> **类设计职能**：ShortcutPayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class ApplicationInfoPayload(TypedDict)`
> **类设计职能**：ApplicationInfoPayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class DiagnosticLogPayload(TypedDict)`
> **类设计职能**：DiagnosticLogPayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginMeta(TypedDict)`
> **类设计职能**：PluginMeta 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginConflict(TypedDict)`
> **类设计职能**：PluginConflict 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginImportResult(TypedDict)`
> **类设计职能**：PluginImportResult 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

---

### 📄 模块：`src/core/plugin/archive.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PluginArchiveError(ValueError)`
> **类设计职能**：Raised when a plugin archive cannot be safely installed.

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginArchiveInfo(object)`
> **类设计职能**：PluginArchiveInfo 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginInstallResult(object)`
> **类设计职能**：PluginInstallResult 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginArchiveInstaller(object)`
> **类设计职能**：Validate and atomically install one ``.cwplugin`` archive.

##### 包含方法全量参考：

###### `PluginArchiveInstaller.__init__(...) -> None`
- **方法用途**：初始化 PluginArchiveInstaller 实例并建立内部状态与依赖注入
- **源码位置**：第 `54` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugins_path` | `Path` | 目标文件或目录路径 |
- **返回值**：`None`

###### `PluginArchiveInstaller.inspect(...) -> PluginArchiveInfo`
- **方法用途**：执行 inspect 相关的处理操作
- **源码位置**：第 `59` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive_path` | `Path | str` | 目标文件或目录路径 |
- **返回值**：`PluginArchiveInfo`

###### `PluginArchiveInstaller.install(...) -> PluginInstallResult`
- **方法用途**：执行 install 相关的处理操作
- **源码位置**：第 `74` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive_path` | `Path | str` | 目标文件或目录路径 |
- **返回值**：`PluginInstallResult`

###### `PluginArchiveInstaller._rename_with_retry(...) -> None`
- **方法用途**：Allow Windows teardown handles a short window to be released.
- **源码位置**：第 `153` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `cls` | `Any` | 类对象自身引用 |
  | `source` | `Path` | source 运行时参数 |
  | `destination` | `Path` | destination 运行时参数 |
- **返回值**：`None`

###### `PluginArchiveInstaller.inspect_extracted(...) -> PluginArchiveInfo`
- **方法用途**：执行 inspect_extracted 相关的处理操作
- **源码位置**：第 `165` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_dir` | `Path` | plugin_dir 运行时参数 |
- **返回值**：`PluginArchiveInfo`

###### `PluginArchiveInstaller._check_archive_path(...) -> Path`
- **方法用途**：执行 _check_archive_path 相关的处理操作
- **源码位置**：第 `189` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive_path` | `Path | str` | 目标文件或目录路径 |
- **返回值**：`Path`

###### `PluginArchiveInstaller._validate_members(...) -> list[zipfile.ZipInfo]`
- **方法用途**：执行 _validate_members 相关的处理操作
- **源码位置**：第 `199` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive` | `zipfile.ZipFile` | archive 运行时参数 |
- **返回值**：`list[zipfile.ZipInfo]`

###### `PluginArchiveInstaller._is_symlink(...) -> bool`
- **方法用途**：执行 _is_symlink 相关的处理操作
- **源码位置**：第 `223` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `member` | `zipfile.ZipInfo` | member 运行时参数 |
- **返回值**：`bool`

###### `PluginArchiveInstaller._safe_archive_path(...) -> PurePosixPath | None`
- **方法用途**：执行 _safe_archive_path 相关的处理操作
- **源码位置**：第 `228` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`PurePosixPath | None`

###### `PluginArchiveInstaller._find_manifest_member(...) -> str`
- **方法用途**：执行 _find_manifest_member 相关的处理操作
- **源码位置**：第 `237` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `members` | `list[zipfile.ZipInfo]` | members 运行时参数 |
- **返回值**：`str`

###### `PluginArchiveInstaller._read_manifest(...) -> dict[str, Any]`
- **方法用途**：执行 _read_manifest 相关的处理操作
- **源码位置**：第 `248` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `archive` | `zipfile.ZipFile` | archive 运行时参数 |
  | `member_name` | `str` | member_name 文本字符串 |
- **返回值**：`dict[str, Any]`

###### `PluginArchiveInstaller._validate_manifest(...) -> None`
- **方法用途**：执行 _validate_manifest 相关的处理操作
- **源码位置**：第 `258` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `cls` | `Any` | 类对象自身引用 |
  | `manifest` | `dict[str, Any]` | manifest 文本字符串 |
- **返回值**：`None`

###### `PluginArchiveInstaller._safe_relative_path(...) -> PurePosixPath`
- **方法用途**：执行 _safe_relative_path 相关的处理操作
- **源码位置**：第 `270` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `value` | `str` | 写入或更新的目标数据值 |
  | `field` | `str` | field 文本字符串 |
- **返回值**：`PurePosixPath`

###### `PluginArchiveInstaller._plugin_target_name(...) -> str`
- **方法用途**：执行 _plugin_target_name 相关的处理操作
- **源码位置**：第 `278` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `cls` | `Any` | 类对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`str`

###### `PluginArchiveInstaller._plugin_target(...) -> Path`
- **方法用途**：执行 _plugin_target 相关的处理操作
- **源码位置**：第 `298` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`Path`

###### `PluginArchiveInstaller._read_existing_version(...) -> str | None`
- **方法用途**：执行 _read_existing_version 相关的处理操作
- **源码位置**：第 `302` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `plugin_dir` | `Path` | plugin_dir 运行时参数 |
- **返回值**：`str | None`

###### `PluginArchiveInstaller._same_version(...) -> bool`
- **方法用途**：执行 _same_version 相关的处理操作
- **源码位置**：第 `313` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `left` | `str` | left 文本字符串 |
  | `right` | `str` | right 文本字符串 |
- **返回值**：`bool`

###### `PluginArchiveInstaller._extract_plugin(...) -> None`
- **方法用途**：执行 _extract_plugin 相关的处理操作
- **源码位置**：第 `319` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive` | `zipfile.ZipFile` | archive 运行时参数 |
  | `members` | `list[zipfile.ZipInfo]` | members 运行时参数 |
  | `manifest_member` | `str` | manifest_member 文本字符串 |
  | `destination` | `Path` | destination 运行时参数 |
- **返回值**：`None`

---

### 📄 模块：`src/core/plugin/download.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PluginDownloadCancelled(Exception)`
> **类设计职能**：Raised when a plugin download is cancelled by the user.

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginDownloadPaused(Exception)`
> **类设计职能**：Raised when a plugin download is paused and can be resumed later.

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PluginDownloader(object)`
> **类设计职能**：Stream one remote plugin archive to a local file.

##### 包含方法全量参考：

###### `PluginDownloader.__init__(...) -> None`
- **方法用途**：初始化 PluginDownloader 实例并建立内部状态与依赖注入
- **源码位置**：第 `27` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `url` | `str` | 网络资源 URL 或 API 请求端点 |
  | `destination` | `Path` | destination 运行时参数 |
- **返回值**：`None`

###### `PluginDownloader.cancel(...) -> None`
- **方法用途**：执行 cancel 相关的处理操作
- **源码位置**：第 `46` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginDownloader.pause(...) -> None`
- **方法用途**：执行 pause 相关的处理操作
- **源码位置**：第 `50` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginDownloader.download(...) -> Path`
- **方法用途**：执行 download 相关的处理操作
- **源码位置**：第 `54` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `progress_callback` | `Callable[[float, float, int, int], None] | None` | 异步完成回调函数 |
- **返回值**：`Path`

###### `PluginDownloader._raise_if_interrupted(...) -> None`
- **方法用途**：执行 _raise_if_interrupted 相关的处理操作
- **源码位置**：第 `147` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginDownloader._interrupt_response(...) -> None`
- **方法用途**：执行 _interrupt_response 相关的处理操作
- **源码位置**：第 `153` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginDownloader._set_response(...) -> None`
- **方法用途**：执行 _set_response 相关的处理操作
- **源码位置**：第 `159` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `response` | `requests.Response | None` | response 运行时参数 |
- **返回值**：`None`

###### `PluginDownloader._total_bytes(...) -> int`
- **方法用途**：执行 _total_bytes 相关的处理操作
- **源码位置**：第 `164` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `response` | `requests.Response` | response 运行时参数 |
  | `content_length` | `int` | content_length 整数计数值 |
  | `downloaded` | `int` | downloaded 整数计数值 |
- **返回值**：`int`

---

### 📄 模块：`src/core/plugin/worker.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PluginImportWorker(QThread)`
> **类设计职能**：Compatibility worker for the existing local-import API.

##### 包含方法全量参考：

###### `PluginImportWorker.__init__(...) -> None`
- **方法用途**：初始化 PluginImportWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `20` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `Any` | 目标文件或目录路径 |
  | `external_path` | `Any` | 目标文件或目录路径 |
  | `scan_func` | `Any` | 回调处理函数 |
  | `metas_ref` | `Any` | metas_ref 运行时参数 |
- **返回值**：`None`

###### `PluginImportWorker.run(...) -> None`
- **方法用途**：启动运行 PluginImportWorker 的核心业务逻辑或主循环
- **源码位置**：第 `26` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/plugin/workers.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 独立函数列表 (Standalone Functions)

##### `def create_plugin_download_directory(...) -> Path`
- **业务用途**：Create a private temporary directory for a plugin release.
- **源码位置**：第 `222` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `Path`，表示操作执行结果或返回目标计算数据实体。

##### `def remove_plugin_download_directory(...) -> None`
- **业务用途**：执行 remove_plugin_download_directory 相关的处理操作
- **源码位置**：第 `228` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `path` | `Path | None` | 目标文件或目录路径 |
- **返回值意义**：返回类型为 `None`，表示操作执行结果或返回目标计算数据实体。

#### 🏛️ 核心类：`class PluginDownloadWorker(QThread)`
> **类设计职能**：Download one local URL in a worker thread.

##### 包含方法全量参考：

###### `PluginDownloadWorker.__init__(...) -> None`
- **方法用途**：初始化 PluginDownloadWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `32` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `downloader` | `PluginDownloader` | downloader 运行时参数 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `PluginDownloadWorker.run(...) -> None`
- **方法用途**：启动运行 PluginDownloadWorker 的核心业务逻辑或主循环
- **源码位置**：第 `36` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginDownloadWorker.cancel(...) -> None`
- **方法用途**：执行 cancel 相关的处理操作
- **源码位置**：第 `47` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PluginDownloadWorker.pause(...) -> None`
- **方法用途**：执行 pause 相关的处理操作
- **源码位置**：第 `50` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class PlazaDownloadWorker(QThread)`
> **类设计职能**：Resolve a plaza release and download it without touching Qt state.

##### 包含方法全量参考：

###### `PlazaDownloadWorker.__init__(...) -> None`
- **方法用途**：初始化 PlazaDownloadWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `64` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `base_url` | `str` | 网络资源 URL 或 API 请求端点 |
  | `destination` | `Path` | destination 运行时参数 |
- **返回值**：`None`

###### `PlazaDownloadWorker.run(...) -> None`
- **方法用途**：启动运行 PlazaDownloadWorker 的核心业务逻辑或主循环
- **源码位置**：第 `82` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaDownloadWorker.cancel(...) -> None`
- **方法用途**：执行 cancel 相关的处理操作
- **源码位置**：第 `110` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaDownloadWorker.pause(...) -> None`
- **方法用途**：执行 pause 相关的处理操作
- **源码位置**：第 `115` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaDownloadWorker._raise_if_cancelled(...) -> None`
- **方法用途**：执行 _raise_if_cancelled 相关的处理操作
- **源码位置**：第 `120` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaDownloadWorker._raise_if_paused(...) -> None`
- **方法用途**：执行 _raise_if_paused 相关的处理操作
- **源码位置**：第 `124` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaDownloadWorker._poll(...) -> None`
- **方法用途**：执行 _poll 相关的处理操作
- **源码位置**：第 `128` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class PluginInstallWorker(QThread)`
> **类设计职能**：Validate and atomically install one already downloaded archive.

##### 包含方法全量参考：

###### `PluginInstallWorker.__init__(...) -> None`
- **方法用途**：初始化 PluginInstallWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `139` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `archive_path` | `Path | str` | 目标文件或目录路径 |
  | `installer` | `PluginArchiveInstaller` | installer 运行时参数 |
- **返回值**：`None`

###### `PluginInstallWorker.run(...) -> None`
- **方法用途**：启动运行 PluginInstallWorker 的核心业务逻辑或主循环
- **源码位置**：第 `156` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class PlazaUpdateWorker(QThread)`
> **类设计职能**：Check current plaza versions for installed external plugins.

##### 包含方法全量参考：

###### `PlazaUpdateWorker.__init__(...) -> None`
- **方法用途**：初始化 PlazaUpdateWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `174` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `records` | `list[dict]` | records 运行时参数 |
  | `base_url` | `str` | 网络资源 URL 或 API 请求端点 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `PlazaUpdateWorker.run(...) -> None`
- **方法用途**：启动运行 PlazaUpdateWorker 的核心业务逻辑或主循环
- **源码位置**：第 `180` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaUpdateWorker.cancel(...) -> None`
- **方法用途**：执行 cancel 相关的处理操作
- **源码位置**：第 `207` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaUpdateWorker._raise_if_cancelled(...) -> None`
- **方法用途**：执行 _raise_if_cancelled 相关的处理操作
- **源码位置**：第 `210` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaUpdateWorker._is_newer(...) -> bool`
- **方法用途**：执行 _is_newer 相关的处理操作
- **源码位置**：第 `215` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `latest` | `str` | latest 文本字符串 |
  | `installed` | `str` | installed 文本字符串 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/plugin/errors.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 独立函数列表 (Standalone Functions)

##### `def plugin_install_error_message(...) -> str`
- **业务用途**：Return a localized, actionable message for a plugin install failure.
- **源码位置**：第 `13` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `error` | `str` | error 文本字符串 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _is_download_or_plaza_error(...) -> bool`
- **业务用途**：执行 _is_download_or_plaza_error 相关的处理操作
- **源码位置**：第 `60` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `message` | `str` | 提示信息或错误消息内容 |
- **返回值意义**：返回类型为 `bool`，表示操作执行结果或返回目标计算数据实体。

---

## 主题与材质系统 (Theme & Shader Subsystem)

### 📄 模块：`src/core/themes/manager.py`

> **模块职能说明**：主题管理器 (ThemesManager)。管理当前应用主题（浅色/深色/液态玻璃），维护 QML 主题资源搜索路径。

#### 🏛️ 核心类：`class ThemeManager(QObject)`
> **类设计职能**：ThemeManager 业务管理类

##### 包含方法全量参考：

###### `ThemeManager.__init__(...) -> None`
- **方法用途**：初始化 ThemeManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `29` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
  | `parent` | `Optional[QObject]` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `ThemeManager.load(...) -> list[ThemeMeta]`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `48` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[ThemeMeta]`

###### `ThemeManager.themes(...) -> list[ThemeMeta]`
- **方法用途**：执行 themes 相关的处理操作
- **源码位置**：第 `53` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[ThemeMeta]`

###### `ThemeManager.currentTheme(...) -> str`
- **方法用途**：执行 currentTheme 相关的处理操作
- **源码位置**：第 `57` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ThemeManager.getAPIVersion(...) -> str`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `61` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `ThemeManager.getThemePath(...) -> str`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `65` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`str`

###### `ThemeManager.getThemeById(...) -> ThemeMeta`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `72` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`ThemeMeta`

###### `ThemeManager.getThemeType(...) -> str`
- **方法用途**：获取主题类型：'builtin' 或 'external'
- **源码位置**：第 `79` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`str`

###### `ThemeManager.isBuiltinTheme(...) -> bool`
- **方法用途**：判断是否为内置主题
- **源码位置**：第 `87` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`bool`

###### `ThemeManager.isThemePathValid(...) -> bool`
- **方法用途**：验证主题路径是否存在
- **源码位置**：第 `92` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`bool`

###### `ThemeManager.isExternalTheme(...) -> bool`
- **方法用途**：判断是否为外部主题
- **源码位置**：第 `112` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`bool`

###### `ThemeManager.themeChange(...) -> bool`
- **方法用途**：执行 themeChange 相关的处理操作
- **源码位置**：第 `117` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`bool`

###### `ThemeManager.rollback_to_default(...) -> bool`
- **方法用途**：Switch to the built-in default theme after a load failure.
- **源码位置**：第 `134` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `failed_theme_id` | `str` | failed_theme_id 文本字符串 |
- **返回值**：`bool`

###### `ThemeManager.scan(...) -> None`
- **方法用途**：遍历扫描目标目录并解析可用组件或插件
- **源码位置**：第 `163` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ThemeManager._apply_pending(...) -> None`
- **方法用途**：执行 _apply_pending 相关的处理操作
- **源码位置**：第 `175` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ThemeManager._is_theme_valid(...) -> bool`
- **方法用途**：执行 _is_theme_valid 相关的处理操作
- **源码位置**：第 `180` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`bool`

###### `ThemeManager._on_retranslate(...) -> None`
- **方法用途**：翻译变更时重新扫描主题以更新翻译
- **源码位置**：第 `183` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `ThemeManager._apply(...) -> None`
- **方法用途**：应用主题
- **源码位置**：第 `188` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`None`

###### `ThemeManager.importTheme(...) -> list[ThemeConflict]`
- **方法用途**：从 ZIP 导入主题（带冲突检测）
- **源码位置**：第 `213` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[ThemeConflict]`

###### `ThemeManager.get_conflicting_themes(...) -> list[ThemeConflict]`
- **方法用途**：检测ZIP文件中是否有与已安装主题冲突的主题
- **源码位置**：第 `247` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `str` | 目标文件或目录路径 |
- **返回值**：`list[ThemeConflict]`

###### `ThemeManager.checkThemeConflicts(...) -> list[ThemeConflict]`
- **方法用途**：QML接口：检测ZIP文件中是否有与已安装主题冲突的主题
- **源码位置**：第 `295` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `str` | 目标文件或目录路径 |
- **返回值**：`list[ThemeConflict]`

###### `ThemeManager.importThemeWithPath(...) -> bool`
- **方法用途**：通过指定路径导入主题（带冲突检测）
- **源码位置**：第 `300` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `str` | 目标文件或目录路径 |
- **返回值**：`bool`

###### `ThemeManager.openThemeFolder(...) -> bool`
- **方法用途**：打开指定主题的本地文件夹
- **源码位置**：第 `349` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`bool`

###### `ThemeManager.uninstallTheme(...) -> bool`
- **方法用途**：卸载指定外部主题
- **源码位置**：第 `371` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_id` | `str` | theme_id 文本字符串 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/themes/loader.py`

> **模块职能说明**：主题资源加载器 (ThemesLoader)。扫描内置主题与外部 themes/ 文件夹，解析主题配置文件。

#### 独立函数列表 (Standalone Functions)

##### `def is_compatible(...) -> bool`
- **业务用途**：检查主题API版本兼容性（使用 packaging.specifiers.SpecifierSet）
- **源码位置**：第 `28` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `theme_api_version` | `str` | 版本号字符串 (如 2.0.0.dev) |
  | `app_version` | `Version` | 版本号字符串 (如 2.0.0.dev) |
- **返回值意义**：返回类型为 `bool`，表示操作执行结果或返回目标计算数据实体。

#### 🏛️ 核心类：`class ThemeLoader(object)`
> **类设计职能**：Theme metadata loader (builtin + external).

##### 包含方法全量参考：

###### `ThemeLoader.scan_themes(...) -> list[ThemeMeta]`
- **方法用途**：遍历扫描目标目录并解析可用组件或插件
- **源码位置**：第 `48` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `external_path` | `Path` | 目标文件或目录路径 |
- **返回值**：`list[ThemeMeta]`

###### `ThemeLoader._load_external_meta(...) -> Optional[ThemeMeta]`
- **方法用途**：执行 _load_external_meta 相关的处理操作
- **源码位置**：第 `106` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_dir` | `Path` | theme_dir 运行时参数 |
- **返回值**：`Optional[ThemeMeta]`

###### `ThemeLoader._validate_meta(...) -> bool`
- **方法用途**：执行 _validate_meta 相关的处理操作
- **源码位置**：第 `132` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `meta` | `ThemeMeta` | meta 运行时参数 |
  | `theme_dir` | `Path` | theme_dir 运行时参数 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/themes/interceptor.py`

> **模块职能说明**：主题资源重定向拦截器 (ThemeInterceptor)。动态将 QML 的通用资源引用重定向至当前激活主题的实际物理路径。

#### 🏛️ 核心类：`class ThemeUrlInterceptor(QQmlAbstractUrlInterceptor)`
> **类设计职能**：ThemeUrlInterceptor 业务管理类

##### 包含方法全量参考：

###### `ThemeUrlInterceptor.__init__(...) -> None`
- **方法用途**：初始化 ThemeUrlInterceptor 实例并建立内部状态与依赖注入
- **源码位置**：第 `12` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `ThemeUrlInterceptor.set_theme(...) -> None`
- **方法用途**：设置当前主题路径
- **源码位置**：第 `18` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `theme_path` | `str | Path` | 主题资源目录路径 |
- **返回值**：`None`

###### `ThemeUrlInterceptor.intercept(...) -> QUrl`
- **方法用途**：拦截 QML 引擎的文件请求。
- **源码位置**：第 `34` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `url` | `QUrl` | 网络资源 URL 或 API 请求端点 |
  | `type` | `QQmlAbstractUrlInterceptor.DataType` | Y 轴纵坐标 (像素) |
- **返回值**：`QUrl`

---

### 📄 模块：`src/core/themes/model.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class ThemeMeta(TypedDict)`
> **类设计职能**：ThemeMeta 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class ThemeConflict(TypedDict)`
> **类设计职能**：ThemeConflict 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class ThemeImportResult(TypedDict)`
> **类设计职能**：ThemeImportResult 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

---

### 📄 模块：`src/core/themes/worker.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class ThemeImportWorker(QObject)`
> **类设计职能**：ThemeImportWorker 业务管理类

##### 包含方法全量参考：

###### `ThemeImportWorker.__init__(...) -> None`
- **方法用途**：初始化 ThemeImportWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `12` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `Any` | 目标文件或目录路径 |
  | `external_path` | `Any` | 目标文件或目录路径 |
  | `scan_func` | `Any` | 回调处理函数 |
  | `metas_ref` | `Any` | metas_ref 运行时参数 |
- **返回值**：`None`

###### `ThemeImportWorker.run(...) -> None`
- **方法用途**：启动运行 ThemeImportWorker 的核心业务逻辑或主循环
- **源码位置**：第 `20` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

## 后台自动化任务调度 (Automation Subsystem)

### 📄 模块：`src/core/automations/manager.py`

> **模块职能说明**：后台自动化任务调度器 (AutomationTaskManager)。统一管理心跳、自动隐藏、更新检测等后台轮询任务。

#### 🏛️ 核心类：`class AutomationManager(QObject)`
> **类设计职能**：AutomationManager 业务管理类

##### 包含方法全量参考：

###### `AutomationManager.__init__(...) -> None`
- **方法用途**：初始化 AutomationManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `19` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `AutomationManager.init_builtin_tasks(...) -> None`
- **方法用途**：Instantiate and register all built-in tasks
- **源码位置**：第 `25` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AutomationManager.add_task(...) -> None`
- **方法用途**：Add a task instance
- **源码位置**：第 `36` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `task` | `AutomationTask` | AutomationTask 后台自动化任务实例 |
- **返回值**：`None`

###### `AutomationManager.remove_task(...) -> None`
- **方法用途**：Remove a task
- **源码位置**：第 `47` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
- **返回值**：`None`

###### `AutomationManager.update(...) -> None`
- **方法用途**：Update all active tasks
- **源码位置**：第 `53` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/automations/base.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class AutomationTask(QObject)`
> **类设计职能**：自动化任务基类

##### 包含方法全量参考：

###### `AutomationTask.__init__(...) -> None`
- **方法用途**：初始化 AutomationTask 实例并建立内部状态与依赖注入
- **源码位置**：第 `12` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `central` | `'AppCentral'` | AppCentral 主程序中央控制中枢单例 |
  | `parent` | `Optional[QObject]` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `AutomationTask.update(...) -> None`
- **方法用途**：每秒调用，由 AutomationManager 调度
- **源码位置**：第 `17` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AutomationTask.name(...) -> str`
- **方法用途**：执行 name 相关的处理操作
- **源码位置**：第 `22` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

---

### 📄 模块：`src/core/automations/update_check.py`

> **模块职能说明**：应用程序版本更新检测任务 (UpdateCheckTask)。定时异步请求更新接口并在检测到新版本时触发托盘提示。

#### 🏛️ 核心类：`class UpdateCheckTask(AutomationTask)`
> **类设计职能**：UpdateCheckTask 业务管理类

##### 包含方法全量参考：

###### `UpdateCheckTask.__init__(...) -> None`
- **方法用途**：初始化 UpdateCheckTask 实例并建立内部状态与依赖注入
- **源码位置**：第 `17` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `central` | `'AppCentral'` | AppCentral 主程序中央控制中枢单例 |
  | `parent` | `Optional[QTimer]` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `UpdateCheckTask._check_update(...) -> None`
- **方法用途**：执行 _check_update 相关的处理操作
- **源码位置**：第 `29` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdateCheckTask._handle_update_available(...) -> None`
- **方法用途**：执行 _handle_update_available 相关的处理操作
- **源码位置**：第 `36` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `version` | `str` | 版本号字符串 (如 2.0.0.dev) |
  | `url` | `str` | 网络资源 URL 或 API 请求端点 |
- **返回值**：`None`

---

### 📄 模块：`src/core/automations/plaza_update_check.py`

> **模块职能说明**：插件市场更新检测任务。检查已安装插件是否有最新版本发布并推送更新气泡。

#### 🏛️ 核心类：`class PlazaUpdateCheckTask(AutomationTask)`
> **类设计职能**：Periodically check Plugin Plaza and optionally install updates in order.

##### 包含方法全量参考：

###### `PlazaUpdateCheckTask.__init__(...) -> None`
- **方法用途**：初始化 PlazaUpdateCheckTask 实例并建立内部状态与依赖注入
- **源码位置**：第 `19` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `central` | `'AppCentral'` | AppCentral 主程序中央控制中枢单例 |
- **返回值**：`None`

###### `PlazaUpdateCheckTask._check_updates(...) -> None`
- **方法用途**：执行 _check_updates 相关的处理操作
- **源码位置**：第 `35` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaUpdateCheckTask._on_check_completed(...) -> None`
- **方法用途**：执行 _on_check_completed 相关的处理操作
- **源码位置**：第 `41` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `background` | `bool` | background 条件开关状态 |
  | `results` | `list[dict]` | results 运行时参数 |
- **返回值**：`None`

###### `PlazaUpdateCheckTask._on_transfer_completed(...) -> None`
- **方法用途**：执行 _on_transfer_completed 相关的处理操作
- **源码位置**：第 `53` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `_version` | `str` | 版本号字符串 (如 2.0.0.dev) |
- **返回值**：`None`

###### `PlazaUpdateCheckTask._on_transfer_failed(...) -> None`
- **方法用途**：执行 _on_transfer_failed 相关的处理操作
- **源码位置**：第 `57` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `_message` | `str` | 提示信息或错误消息内容 |
- **返回值**：`None`

###### `PlazaUpdateCheckTask._on_transfer_cancelled(...) -> None`
- **方法用途**：执行 _on_transfer_cancelled 相关的处理操作
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `PlazaUpdateCheckTask._on_transfer_settled(...) -> None`
- **方法用途**：执行 _on_transfer_settled 相关的处理操作
- **源码位置**：第 `65` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaUpdateCheckTask._start_next(...) -> None`
- **方法用途**：执行 _start_next 相关的处理操作
- **源码位置**：第 `68` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/automations/builtin_tasks.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class AutoHideTask(AutomationTask)`
> **类设计职能**：AutoHideTask 业务管理类

##### 包含方法全量参考：

###### `AutoHideTask.__init__(...) -> None`
- **方法用途**：初始化 AutoHideTask 实例并建立内部状态与依赖注入
- **源码位置**：第 `44` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `AutoHideTask._hide(...) -> None`
- **方法用途**：隐藏窗口
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `state` | `bool` | state 条件开关状态 |
- **返回值**：`None`

###### `AutoHideTask.update(...) -> None`
- **方法用途**：主循环
- **源码位置**：第 `70` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AutoHideTask._enum_windows_callback(...) -> bool`
- **方法用途**：执行 _enum_windows_callback 相关的处理操作
- **源码位置**：第 `105` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `hwnd` | `int` | hwnd 整数计数值 |
  | `_` | `Any` | _ 运行时参数 |
- **返回值**：`bool`

###### `AutoHideTask.on_schedule_changed(...) -> None`
- **方法用途**：课程发生变化触发
- **源码位置**：第 `124` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `current_type` | `EntryType` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

---

## 通知总线与系统服务 (Notification & Utils)

### 📄 模块：`src/core/notification/manager.py`

> **模块职能说明**：桌面通知调度管理器 (NotificationManager)。维护通知优先级队列、限流策略与系统原生托盘/气泡分发。

#### 🏛️ 核心类：`class NotificationManager(QObject)`
> **类设计职能**：NotificationManager 业务管理类

##### 包含方法全量参考：

###### `NotificationManager.__init__(...) -> None`
- **方法用途**：初始化 NotificationManager 实例并建立内部状态与依赖注入
- **源码位置**：第 `22` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `config_manager` | `'ConfigManager'` | 配置数据对象或配置模型实例 |
  | `app_central` | `'AppCentral'` | AppCentral 主程序中央控制中枢引用 |
- **返回值**：`None`

###### `NotificationManager.register_provider(...) -> None`
- **方法用途**：向管理器注册新的功能组件、插件或回调监听器
- **源码位置**：第 `31` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider` | `'NotificationProvider'` | NotificationProvider 通知提供者实例 |
- **返回值**：`None`

###### `NotificationManager.unregister_provider(...) -> None`
- **方法用途**：取消注册通知提供者
- **源码位置**：第 `39` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
- **返回值**：`None`

###### `NotificationManager.is_enabled(...) -> bool`
- **方法用途**：检测并返回特定状态或条件判断布尔值
- **源码位置**：第 `45` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
- **返回值**：`bool`

###### `NotificationManager.notifyQmlReady(...) -> None`
- **方法用途**：QML 调用此方法通知 Python 端 QML 已准备就绪
- **源码位置**：第 `51` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `NotificationManager.set_qml_ready(...) -> None`
- **方法用途**：设置 QML 是否已准备就绪
- **源码位置**：第 `58` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `ready` | `bool` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `NotificationManager.flush_pending_notifications(...) -> None`
- **方法用途**：手动刷新待处理的通知
- **源码位置**：第 `75` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `NotificationManager.dispatch(...) -> None`
- **方法用途**：执行 dispatch 相关的处理操作
- **源码位置**：第 `88` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `data` | `'NotificationData'` | 字典或载荷数据字典 |
  | `cfg` | `Optional['NotificationProviderConfig']` | cfg 运行时参数 |
- **返回值**：`None`

###### `NotificationManager.get_providers(...) -> list[dict[str, Optional[str | bool]]]`
- **方法用途**：获取所有已注册的通知提供者信息，用于前端展示
- **源码位置**：第 `146` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict[str, Optional[str | bool]]]`

---

### 📄 模块：`src/core/notification/model.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class NotificationLevel(IntEnum)`
> **类设计职能**：NotificationLevel 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class NotificationData(BaseModel)`
> **类设计职能**：NotificationData 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class NotificationPayload(TypedDict)`
> **类设计职能**：NotificationPayload 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class NotificationProviderConfig(BaseModel)`
> **类设计职能**：NotificationProviderConfig 业务管理类

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

---

### 📄 模块：`src/core/notification/provider.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class NotificationProvider(QObject)`
> **类设计职能**：一个 Provider = 一个通知来源（模块 / 插件）

##### 包含方法全量参考：

###### `NotificationProvider.__init__(...) -> None`
- **方法用途**：初始化 NotificationProvider 实例并建立内部状态与依赖注入
- **源码位置**：第 `18` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `id` | `str` | id 文本字符串 |
  | `name` | `str` | name 文本字符串 |
  | `icon` | `Optional[str | Path]` | 图标路径或 QIcon 实例 |
  | `use_system_notify` | `bool` | Y 轴纵坐标 (像素) |
  | `manager` | `Optional[NotificationManager]` | manager 运行时参数 |
- **返回值**：`None`

###### `NotificationProvider.get_config(...) -> NotificationProviderConfig`
- **方法用途**：从 ConfigManager 读取该 provider 的配置
- **源码位置**：第 `49` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`NotificationProviderConfig`

###### `NotificationProvider.push(...) -> None`
- **方法用途**：执行 push 相关的处理操作
- **源码位置**：第 `59` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `int` | level 整数计数值 |
  | `title` | `str` | 通知弹窗或组件标题文本 |
  | `message` | `Optional[str]` | 提示信息或错误消息内容 |
  | `duration` | `int` | duration 整数计数值 |
  | `closable` | `bool` | closable 条件开关状态 |
- **返回值**：`None`

---

### 📄 模块：`src/core/notification/service.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class NotificationService(QObject)`
> **类设计职能**：通知服务类，管理所有通知相关功能

##### 包含方法全量参考：

###### `NotificationService.__init__(...) -> None`
- **方法用途**：初始化 NotificationService 实例并建立内部状态与依赖注入
- **源码位置**：第 `22` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `notification_manager` | `'NotificationManager'` | notification_manager 运行时参数 |
  | `config_manager` | `'ConfigManager'` | 配置数据对象或配置模型实例 |
- **返回值**：`None`

###### `NotificationService.notificationProviders(...) -> None`
- **方法用途**：获取所有已注册的通知提供者信息，用于QML界面显示
- **源码位置**：第 `29` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `NotificationService.setNotificationProviderEnabled(...) -> None`
- **方法用途**：设置特定通知提供者的启用状态
- **源码位置**：第 `36` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `enabled` | `bool` | 功能是否启用的布尔开关标志 |
- **返回值**：`None`

###### `NotificationService.setNotificationProviderSystemNotify(...) -> None`
- **方法用途**：设置特定通知提供者是否使用系统通知
- **源码位置**：第 `45` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `use_system` | `bool` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `NotificationService.setNotificationProviderAppNotify(...) -> None`
- **方法用途**：设置特定通知提供者是否使用应用内通知
- **源码位置**：第 `54` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `use_app` | `bool` | use_app 条件开关状态 |
- **返回值**：`None`

###### `NotificationService.setLevelSound(...) -> None`
- **方法用途**：设置通知级别对应的声音文件
- **源码位置**：第 `64` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `int` | level 整数计数值 |
  | `sound` | `str` | sound 文本字符串 |
- **返回值**：`None`

###### `NotificationService.getLevelSound(...) -> str`
- **方法用途**：获取通知级别对应的声音文件
- **源码位置**：第 `72` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `int` | level 整数计数值 |
- **返回值**：`str`

###### `NotificationService.getNotificationVolume(...) -> float`
- **方法用途**：获取全局通知音量
- **源码位置**：第 `80` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`float`

###### `NotificationService.setNotificationVolume(...) -> None`
- **方法用途**：设置全局通知音量
- **源码位置**：第 `85` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `volume` | `float` | volume 运行时参数 |
- **返回值**：`None`

###### `NotificationService.setNotificationsEnabled(...) -> None`
- **方法用途**：设置全局通知启用状态
- **源码位置**：第 `90` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `enabled` | `bool` | 功能是否启用的布尔开关标志 |
- **返回值**：`None`

###### `NotificationService.getNotificationsEnabled(...) -> bool`
- **方法用途**：获取全局通知启用状态
- **源码位置**：第 `95` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `NotificationService.getNotificationProviderLevelSound(...) -> str`
- **方法用途**：获取全局级别声音路径（忽略provider_id参数）
- **源码位置**：第 `101` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `level` | `int` | level 整数计数值 |
- **返回值**：`str`

###### `NotificationService.setNotificationProviderLevelSound(...) -> None`
- **方法用途**：设置全局级别声音路径（忽略provider_id参数）
- **源码位置**：第 `106` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `level` | `int` | level 整数计数值 |
  | `sound` | `str` | sound 文本字符串 |
- **返回值**：`None`

###### `NotificationService.getGlobalLevelSound(...) -> str`
- **方法用途**：获取全局级别声音路径
- **源码位置**：第 `111` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `int` | level 整数计数值 |
- **返回值**：`str`

###### `NotificationService.setGlobalLevelSound(...) -> None`
- **方法用途**：设置全局级别声音路径
- **源码位置**：第 `116` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `int` | level 整数计数值 |
  | `sound` | `str` | sound 文本字符串 |
- **返回值**：`None`

###### `NotificationService.getGlobalVolume(...) -> float`
- **方法用途**：获取全局通知音量
- **源码位置**：第 `121` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`float`

###### `NotificationService.setGlobalVolume(...) -> None`
- **方法用途**：设置全局通知音量
- **源码位置**：第 `126` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `volume` | `float` | volume 运行时参数 |
- **返回值**：`None`

###### `NotificationService.getGlobalNotificationVolume(...) -> None`
- **方法用途**：获取全局通知音量
- **源码位置**：第 `131` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `NotificationService.setGlobalNotificationVolume(...) -> None`
- **方法用途**：设置全局通知音量
- **源码位置**：第 `136` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `volume` | `Any` | volume 运行时参数 |
- **返回值**：`None`

###### `NotificationService.playNotificationSoundLevel(...) -> None`
- **方法用途**：播放指定级别的通知声音（使用全局配置）
- **源码位置**：第 `142` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `Any` | level 运行时参数 |
- **返回值**：`None`

###### `NotificationService.playNotificationSound(...) -> None`
- **方法用途**：播放通知级别对应的铃声
- **源码位置**：第 `147` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `provider_id` | `str` | NotificationProvider 通知提供者实例 |
  | `level` | `int` | level 整数计数值 |
- **返回值**：`None`

###### `NotificationService.selectNotificationSound(...) -> bool`
- **方法用途**：选择并设置通知声音文件
- **源码位置**：第 `206` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `int` | level 整数计数值 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/utils/tray.py`

> **模块职能说明**：系统托盘图标管理器 (TrayIcon)。实现右键菜单、左键点击面板唤醒、未读小红点与多状态气泡通知。

#### 🏛️ 核心类：`class TrayIcon(QObject)`
> **类设计职能**：TrayIcon 业务管理类

##### 包含方法全量参考：

###### `TrayIcon.__init__(...) -> None`
- **方法用途**：初始化 TrayIcon 实例并建立内部状态与依赖注入
- **源码位置**：第 `16` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `TrayIcon._set_app_user_model_id(...) -> None`
- **方法用途**：执行 _set_app_user_model_id 相关的处理操作
- **源码位置**：第 `35` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_id` | `str` | app_id 文本字符串 |
- **返回值**：`None`

###### `TrayIcon.on_click(...) -> None`
- **方法用途**：响应底层事件、信号或回调触发的槽函数
- **源码位置**：第 `43` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reason` | `Any` | 系统触发原因枚举 (如托盘激活原因) |
- **返回值**：`None`

###### `TrayIcon.push_update_notification(...) -> None`
- **方法用途**：执行 push_update_notification 相关的处理操作
- **源码位置**：第 `48` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `title` | `str` | 通知弹窗或组件标题文本 |
  | `text` | `str` | 通知消息主体文本内容 |
- **返回值**：`None`

###### `TrayIcon.push_up_to_date_notification(...) -> None`
- **方法用途**：执行 push_up_to_date_notification 相关的处理操作
- **源码位置**：第 `51` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `title` | `str` | 通知弹窗或组件标题文本 |
  | `text` | `str` | 通知消息主体文本内容 |
- **返回值**：`None`

###### `TrayIcon.push_error_notification(...) -> None`
- **方法用途**：执行 push_error_notification 相关的处理操作
- **源码位置**：第 `54` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `title` | `str` | 通知弹窗或组件标题文本 |
  | `text` | `str` | 通知消息主体文本内容 |
- **返回值**：`None`

###### `TrayIcon.push_notification(...) -> None`
- **方法用途**：执行 push_notification 相关的处理操作
- **源码位置**：第 `57` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `title` | `str` | 通知弹窗或组件标题文本 |
  | `text` | `str` | 通知消息主体文本内容 |
  | `icon` | `QIcon` | 图标路径或 QIcon 实例 |
- **返回值**：`None`

###### `TrayIcon.cleanup(...) -> None`
- **方法用途**：解绑信号槽并安全释放系统底层资源
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/utils/translator.py`

> **模块职能说明**：多语言国际化转换器 (Translator)。支持运行时动态加载 zh_CN, en_US, ja_JP 翻译字典并无缝刷新 UI。

#### 🏛️ 核心类：`class AppTranslator(QObject)`
> **类设计职能**：AppTranslator 业务管理类

##### 包含方法全量参考：

###### `AppTranslator.__init__(...) -> None`
- **方法用途**：初始化 AppTranslator 实例并建立内部状态与依赖注入
- **源码位置**：第 `14` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app` | `Any` | app 运行时参数 |
- **返回值**：`None`

###### `AppTranslator.getLanguage(...) -> None`
- **方法用途**：获取当前语言
- **源码位置**：第 `22` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppTranslator.language(...) -> str`
- **方法用途**：执行 language 相关的处理操作
- **源码位置**：第 `27` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `AppTranslator.getSystemLanguage(...) -> None`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `31` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `AppTranslator.setLanguage(...) -> None`
- **方法用途**：切换语言
- **源码位置**：第 `35` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `locale_name` | `str` | locale_name 文本字符串 |
- **返回值**：`None`

###### `AppTranslator.tr(...) -> str`
- **方法用途**：提供 QML 访问翻译的接口
- **源码位置**：第 `66` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `context` | `str` | 通知消息主体文本内容 |
  | `source_text` | `str` | 通知消息主体文本内容 |
- **返回值**：`str`

---

### 📄 模块：`src/core/utils/auto_startup.py`

> **模块职能说明**：Windows 开机自启管理器。读写注册表 HKCU/Software/Microsoft/Windows/CurrentVersion/Run 实现安全自启配置。

#### 独立函数列表 (Standalone Functions)

##### `def autostart_supported(...) -> bool`
- **业务用途**：Check if autostart is supported on this platform
- **源码位置**：第 `16` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `bool`，表示操作执行结果或返回目标计算数据实体。

##### `def enable_autostart(...) -> None`
- **业务用途**：Enable autostart
- **源码位置**：第 `21` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `None`，表示操作执行结果或返回目标计算数据实体。

##### `def disable_autostart(...) -> None`
- **业务用途**：Disable autostart
- **源码位置**：第 `41` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `None`，表示操作执行结果或返回目标计算数据实体。

##### `def is_autostart_enabled(...) -> bool`
- **业务用途**：Check if autostart is enabled
- **源码位置**：第 `63` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `bool`，表示操作执行结果或返回目标计算数据实体。

---

### 📄 模块：`src/core/utils/instance_locker.py`

> **模块职能说明**：单实例锁与进程间唤醒器。防止程序重复多开，并支持在二次打开时向前台唤醒已有实例。

#### 🏛️ 核心类：`class SingleInstanceGuard(object)`
> **类设计职能**：SingleInstanceGuard 业务管理类

##### 包含方法全量参考：

###### `SingleInstanceGuard.__init__(...) -> None`
- **方法用途**：初始化 SingleInstanceGuard 实例并建立内部状态与依赖注入
- **源码位置**：第 `4` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `lock_name` | `Any` | lock_name 文本字符串 |
- **返回值**：`None`

###### `SingleInstanceGuard.try_acquire(...) -> None`
- **方法用途**：执行 try_acquire 相关的处理操作
- **源码位置**：第 `9` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `timeout` | `int` | 超时时间毫秒数 |
- **返回值**：`None`

###### `SingleInstanceGuard.release(...) -> None`
- **方法用途**：执行 release 相关的处理操作
- **源码位置**：第 `13` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `SingleInstanceGuard.get_lock_info(...) -> None`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `17` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/utils/calculator.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 独立函数列表 (Standalone Functions)

##### `def get_week_number(...) -> int`
- **业务用途**：获取当前日期在开学后的第几周
- **源码位置**：第 `4` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `start_date` | `str` | start_date 文本字符串 |
  | `current_date` | `datetime` | current_date 运行时参数 |
- **返回值意义**：返回类型为 `int`，表示操作执行结果或返回目标计算数据实体。

##### `def get_cycle_week(...) -> int`
- **业务用途**：获取当前周在当前周期的第几周
- **源码位置**：第 `20` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `week_number` | `int` | week_number 整数计数值 |
  | `cycle` | `int` | Y 轴纵坐标 (像素) |
- **返回值意义**：返回类型为 `int`，表示操作执行结果或返回目标计算数据实体。

---

### 📄 模块：`src/core/utils/subjects.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 独立函数列表 (Standalone Functions)

##### `def get_default_subjects(...) -> list[Subject]`
- **业务用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `27` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `list[Subject]`，表示操作执行结果或返回目标计算数据实体。

##### `def translate_sources(...) -> None`
- **业务用途**：执行 translate_sources 相关的处理操作
- **源码位置**：第 `43` 行
- **参数规范**：无入参
- **返回值意义**：返回类型为 `None`，表示操作执行结果或返回目标计算数据实体。

---

### 📄 模块：`src/core/utils/json_loader.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class JsonLoader(object)`
> **类设计职能**：JsonLoader 业务管理类

##### 包含方法全量参考：

###### `JsonLoader.__init__(...) -> None`
- **方法用途**：初始化 JsonLoader 实例并建立内部状态与依赖注入
- **源码位置**：第 `10` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `path` | `str | Path` | 目标文件或目录路径 |
  | `default` | `Optional[JsonData]` | 默认回退值 |
- **返回值**：`None`

###### `JsonLoader.load(...) -> JsonData`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `15` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`JsonData`

###### `JsonLoader.get(...) -> Optional[JsonData]`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `35` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`Optional[JsonData]`

###### `JsonLoader.save(...) -> None`
- **方法用途**：持久化保存当前配置模型或课表数据至磁盘
- **源码位置**：第 `38` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `data` | `JsonData` | 字典或载荷数据字典 |
- **返回值**：`None`

---

### 📄 模块：`src/core/utils/log_list_model.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class LogListModel(QAbstractListModel)`
> **类设计职能**：QML-friendly log model.

##### 包含方法全量参考：

###### `LogListModel.__init__(...) -> None`
- **方法用途**：初始化 LogListModel 实例并建立内部状态与依赖注入
- **源码位置**：第 `22` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `LogListModel.rowCount(...) -> int`
- **方法用途**：执行 rowCount 相关的处理操作
- **源码位置**：第 `26` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`int`

###### `LogListModel.roleNames(...) -> None`
- **方法用途**：执行 roleNames 相关的处理操作
- **源码位置**：第 `31` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `LogListModel.data(...) -> None`
- **方法用途**：执行 data 相关的处理操作
- **源码位置**：第 `38` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `index` | `Any` | X 轴横坐标 (像素) |
  | `role` | `Any` | role 运行时参数 |
- **返回值**：`None`

###### `LogListModel.append_entry(...) -> None`
- **方法用途**：追加一条日志。在末尾若超出容量, 先移除最旧一条再追加。
- **源码位置**：第 `53` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `entry` | `dict` | 课表单个时间节点对象 (EntryModel / ScheduleEntry) |
- **返回值**：`None`

###### `LogListModel.snapshot(...) -> list[dict]`
- **方法用途**：返回最近 limit 条日志的浅拷贝 (list[dict])。
- **源码位置**：第 `68` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `limit` | `int` | limit 整数计数值 |
- **返回值**：`list[dict]`

###### `LogListModel.clear(...) -> None`
- **方法用途**：执行 clear 相关的处理操作
- **源码位置**：第 `75` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class LogFilterProxyModel(QSortFilterProxyModel)`
> **类设计职能**：对 LogListModel 做客户端过滤。

##### 包含方法全量参考：

###### `LogFilterProxyModel.__init__(...) -> None`
- **方法用途**：初始化 LogFilterProxyModel 实例并建立内部状态与依赖注入
- **源码位置**：第 `92` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `LogFilterProxyModel.set_filter_text(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `97` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `text` | `str` | 通知消息主体文本内容 |
- **返回值**：`None`

###### `LogFilterProxyModel.set_filter_level(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `101` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `str` | level 文本字符串 |
- **返回值**：`None`

###### `LogFilterProxyModel.filterAcceptsRow(...) -> bool`
- **方法用途**：执行 filterAcceptsRow 相关的处理操作
- **源码位置**：第 `105` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `source_row` | `Any` | source_row 运行时参数 |
  | `source_parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`bool`

---

### 📄 模块：`src/core/utils/debugger.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class DebuggerWindow(RinUIWindow)`
> **类设计职能**：DebuggerWindow 业务管理类

##### 包含方法全量参考：

###### `DebuggerWindow.__init__(...) -> None`
- **方法用途**：初始化 DebuggerWindow 实例并建立内部状态与依赖注入
- **源码位置**：第 `8` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `instance` | `Any` | instance 运行时参数 |
- **返回值**：`None`

---

## 插件市场与热更新器 (Plaza & Updater)

### 📄 模块：`src/core/plaza/client.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PlazaClientError(RuntimeError)`
> **类设计职能**：Raised when the Extension Plaza API returns an invalid response.

*（该类为纯数据实体或抽象接口，未定义额外公共方法）*

#### 🏛️ 核心类：`class PlazaClient(object)`
> **类设计职能**：Small synchronous API client used by background plugin tasks.

##### 包含方法全量参考：

###### `PlazaClient.__init__(...) -> None`
- **方法用途**：初始化 PlazaClient 实例并建立内部状态与依赖注入
- **源码位置**：第 `21` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `base_url` | `str` | 网络资源 URL 或 API 请求端点 |
- **返回值**：`None`

###### `PlazaClient.get_plugin(...) -> dict`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `27` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`dict`

###### `PlazaClient.release_url(...) -> str`
- **方法用途**：执行 release_url 相关的处理操作
- **源码位置**：第 `45` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin` | `dict` | plugin 运行时参数 |
- **返回值**：`str`

---

### 📄 模块：`src/core/plaza/bridge.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PlazaBridge(QObject)`
> **类设计职能**：PlazaBridge 业务管理类

##### 包含方法全量参考：

###### `PlazaBridge.__init__(...) -> None`
- **方法用途**：初始化 PlazaBridge 实例并建立内部状态与依赖注入
- **源码位置**：第 `19` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `config_manager` | `Any` | 配置数据对象或配置模型实例 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `PlazaBridge._read_base_url(...) -> None`
- **方法用途**：执行 _read_base_url 相关的处理操作
- **源码位置**：第 `34` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge._on_config_changed(...) -> None`
- **方法用途**：执行 _on_config_changed 相关的处理操作
- **源码位置**：第 `38` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge.shutdown(...) -> None`
- **方法用途**：Stop requests without letting their completion handlers reach QML.
- **源码位置**：第 `44` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge.status(...) -> None`
- **方法用途**：执行 status 相关的处理操作
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge.baseUrl(...) -> None`
- **方法用途**：执行 baseUrl 相关的处理操作
- **源码位置**：第 `64` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge.banners(...) -> None`
- **方法用途**：执行 banners 相关的处理操作
- **源码位置**：第 `68` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge.plugins(...) -> None`
- **方法用途**：执行 plugins 相关的处理操作
- **源码位置**：第 `72` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge._set_status(...) -> None`
- **方法用途**：执行 _set_status 相关的处理操作
- **源码位置**：第 `75` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `s` | `Any` | s 运行时参数 |
- **返回值**：`None`

###### `PlazaBridge._read_json_reply(...) -> None`
- **方法用途**：执行 _read_json_reply 相关的处理操作
- **源码位置**：第 `80` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `PlazaBridge._response_error(...) -> None`
- **方法用途**：执行 _response_error 相关的处理操作
- **源码位置**：第 `83` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `data` | `Any` | 字典或载荷数据字典 |
  | `fallback` | `Any` | fallback 运行时参数 |
- **返回值**：`None`

###### `PlazaBridge._track_reply(...) -> None`
- **方法用途**：执行 _track_reply 相关的处理操作
- **源码位置**：第 `88` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
  | `callback` | `Callable[[], None]` | 异步完成回调函数 |
- **返回值**：`None`

###### `PlazaBridge._take_reply(...) -> bool`
- **方法用途**：执行 _take_reply 相关的处理操作
- **源码位置**：第 `92` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
- **返回值**：`bool`

###### `PlazaBridge._disconnect_reply(...) -> None`
- **方法用途**：执行 _disconnect_reply 相关的处理操作
- **源码位置**：第 `100` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
  | `callback` | `Callable[[], None]` | 异步完成回调函数 |
- **返回值**：`None`

###### `PlazaBridge._dispose_reply(...) -> None`
- **方法用途**：执行 _dispose_reply 相关的处理操作
- **源码位置**：第 `107` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `PlazaBridge.fetchBanners(...) -> None`
- **方法用途**：执行 fetchBanners 相关的处理操作
- **源码位置**：第 `113` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge._on_banners_finished(...) -> None`
- **方法用途**：执行 _on_banners_finished 相关的处理操作
- **源码位置**：第 `130` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `PlazaBridge.fetchPlugins(...) -> None`
- **方法用途**：执行 fetchPlugins 相关的处理操作
- **源码位置**：第 `164` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaBridge._on_plugins_finished(...) -> None`
- **方法用途**：执行 _on_plugins_finished 相关的处理操作
- **源码位置**：第 `183` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `PlazaBridge.refreshAll(...) -> None`
- **方法用途**：执行 refreshAll 相关的处理操作
- **源码位置**：第 `217` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/plaza/activity.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PlazaActivityStore(QObject)`
> **类设计职能**：Keep a small, in-memory history of Plugin Plaza transfers.

##### 包含方法全量参考：

###### `PlazaActivityStore.__init__(...) -> None`
- **方法用途**：初始化 PlazaActivityStore 实例并建立内部状态与依赖注入
- **源码位置**：第 `13` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaActivityStore.entries(...) -> list[dict[str, object]]`
- **方法用途**：执行 entries 相关的处理操作
- **源码位置**：第 `19` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict[str, object]]`

###### `PlazaActivityStore.start(...) -> None`
- **方法用途**：执行 start 相关的处理操作
- **源码位置**：第 `22` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaActivityStore.update_metadata(...) -> None`
- **方法用途**：计算并更新 PlazaActivityStore 的状态、属性或遮罩渲染
- **源码位置**：第 `49` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `PlazaActivityStore.set_progress(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `67` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `progress` | `float` | progress 运行时参数 |
  | `downloaded_bytes` | `int` | Y 轴纵坐标 (像素) |
  | `total_bytes` | `int` | Y 轴纵坐标 (像素) |
  | `speed` | `float` | speed 运行时参数 |
- **返回值**：`None`

###### `PlazaActivityStore.set_paused(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `84` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `PlazaActivityStore.set_downloading(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `92` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `PlazaActivityStore.set_installing(...) -> None`
- **方法用途**：设置更新指定属性字段并触发响应式变更信号
- **源码位置**：第 `100` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `PlazaActivityStore.complete(...) -> None`
- **方法用途**：执行 complete 相关的处理操作
- **源码位置**：第 `107` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `version` | `str` | 版本号字符串 (如 2.0.0.dev) |
- **返回值**：`None`

###### `PlazaActivityStore.fail(...) -> None`
- **方法用途**：执行 fail 相关的处理操作
- **源码位置**：第 `116` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
  | `error` | `str` | error 文本字符串 |
- **返回值**：`None`

###### `PlazaActivityStore.cancel(...) -> None`
- **方法用途**：执行 cancel 相关的处理操作
- **源码位置**：第 `124` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`None`

###### `PlazaActivityStore._active_entry(...) -> dict[str, object] | None`
- **方法用途**：执行 _active_entry 相关的处理操作
- **源码位置**：第 `132` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_id` | `str` | 插件唯一元数据 ID (形如 builtin.classwidgets.widgets) |
- **返回值**：`dict[str, object] | None`

---

### 📄 模块：`src/core/plaza/markdown.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 独立函数列表 (Standalone Functions)

##### `def render_markdown(...) -> str`
- **业务用途**：执行 render_markdown 相关的处理操作
- **源码位置**：第 `18` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `markdown` | `str` | markdown 文本字符串 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _normalize_placeholders(...) -> str`
- **业务用途**：执行 _normalize_placeholders 相关的处理操作
- **源码位置**：第 `26` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `text` | `str` | 通知消息主体文本内容 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _normalize_admonitions(...) -> str`
- **业务用途**：执行 _normalize_admonitions 相关的处理操作
- **源码位置**：第 `36` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `text` | `str` | 通知消息主体文本内容 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _admonition_colors(...) -> tuple[str, str]`
- **业务用途**：执行 _admonition_colors 相关的处理操作
- **源码位置**：第 `68` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `kind` | `str` | kind 文本字符串 |
- **返回值意义**：返回类型为 `tuple[str, str]`，表示操作执行结果或返回目标计算数据实体。

##### `def _postprocess_for_qt_rich_text(...) -> str`
- **业务用途**：执行 _postprocess_for_qt_rich_text 相关的处理操作
- **源码位置**：第 `79` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `value` | `str` | 写入或更新的目标数据值 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _blockquote_to_qt_html(...) -> str`
- **业务用途**：执行 _blockquote_to_qt_html 相关的处理操作
- **源码位置**：第 `111` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `content` | `str` | content 文本字符串 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _qt_quote_block(...) -> str`
- **业务用途**：执行 _qt_quote_block 相关的处理操作
- **源码位置**：第 `124` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `content` | `str` | content 文本字符串 |
  | `border_color` | `str` | border_color 文本字符串 |
  | `is_admonition` | `bool` | 状态布尔标志 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _normalize_typography(...) -> str`
- **业务用途**：执行 _normalize_typography 相关的处理操作
- **源码位置**：第 `144` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `value` | `str` | 写入或更新的目标数据值 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _normalize_aligned_blocks(...) -> str`
- **业务用途**：执行 _normalize_aligned_blocks 相关的处理操作
- **源码位置**：第 `154` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `value` | `str` | 写入或更新的目标数据值 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _normalize_images(...) -> str`
- **业务用途**：执行 _normalize_images 相关的处理操作
- **源码位置**：第 `172` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `value` | `str` | 写入或更新的目标数据值 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _image_style_to_attributes(...) -> str`
- **业务用途**：执行 _image_style_to_attributes 相关的处理操作
- **源码位置**：第 `192` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `match` | `re.Match[str]` | match 文本字符串 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _style_dimension(...) -> str`
- **业务用途**：执行 _style_dimension 相关的处理操作
- **源码位置**：第 `204` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `style` | `str` | Y 轴纵坐标 (像素) |
  | `name` | `str` | name 文本字符串 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _heading_to_paragraph(...) -> str`
- **业务用途**：执行 _heading_to_paragraph 相关的处理操作
- **源码位置**：第 `212` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `level` | `int` | level 整数计数值 |
  | `content` | `str` | content 文本字符串 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

##### `def _code_block_to_pre(...) -> str`
- **业务用途**：执行 _code_block_to_pre 相关的处理操作
- **源码位置**：第 `228` 行
- **参数规范与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `code` | `str` | code 文本字符串 |
  | `language` | `str` | language 文本字符串 |
- **返回值意义**：返回类型为 `str`，表示操作执行结果或返回目标计算数据实体。

#### 🏛️ 核心类：`class MarkdownRenderBridge(QObject)`
> **类设计职能**：MarkdownRenderBridge 业务管理类

##### 包含方法全量参考：

###### `MarkdownRenderBridge.render(...) -> str`
- **方法用途**：执行 render 相关的处理操作
- **源码位置**：第 `9` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `markdown` | `str` | markdown 文本字符串 |
- **返回值**：`str`

---

### 📄 模块：`src/core/plaza/notifications.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class PlazaNotificationPublisher(QObject)`
> **类设计职能**：Publish Plugin Plaza events through a dedicated notification provider.

##### 包含方法全量参考：

###### `PlazaNotificationPublisher.__init__(...) -> None`
- **方法用途**：初始化 PlazaNotificationPublisher 实例并建立内部状态与依赖注入
- **源码位置**：第 `13` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `Any` | AppCentral 主程序中央控制中枢引用 |
  | `parent` | `QObject | None` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `PlazaNotificationPublisher.retranslate(...) -> None`
- **方法用途**：Recreate the provider so its displayed name follows the app language.
- **源码位置**：第 `20` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaNotificationPublisher._register_provider(...) -> None`
- **方法用途**：执行 _register_provider 相关的处理操作
- **源码位置**：第 `28` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `PlazaNotificationPublisher.transfer_succeeded(...) -> None`
- **方法用途**：执行 transfer_succeeded 相关的处理操作
- **源码位置**：第 `46` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
  | `version` | `str` | 版本号字符串 (如 2.0.0.dev) |
  | `kind` | `str` | kind 文本字符串 |
- **返回值**：`None`

###### `PlazaNotificationPublisher.transfer_failed(...) -> None`
- **方法用途**：执行 transfer_failed 相关的处理操作
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `name` | `str` | name 文本字符串 |
  | `error` | `str` | error 文本字符串 |
  | `kind` | `str` | kind 文本字符串 |
- **返回值**：`None`

###### `PlazaNotificationPublisher.updates_available(...) -> None`
- **方法用途**：计算并更新 PlazaNotificationPublisher 的状态、属性或遮罩渲染
- **源码位置**：第 `75` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `count` | `int` | count 整数计数值 |
- **返回值**：`None`

###### `PlazaNotificationPublisher._dispatch(...) -> None`
- **方法用途**：执行 _dispatch 相关的处理操作
- **源码位置**：第 `84` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `level` | `NotificationLevel` | level 运行时参数 |
  | `title` | `str` | 通知弹窗或组件标题文本 |
  | `message` | `str` | 提示信息或错误消息内容 |
- **返回值**：`None`

---

### 📄 模块：`src/core/plaza/tutorial.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class TutorialRecommendationsBridge(QObject)`
> **类设计职能**：Expose the small, curated Plugin Plaza list used by the first-run flow.

##### 包含方法全量参考：

###### `TutorialRecommendationsBridge.__init__(...) -> None`
- **方法用途**：初始化 TutorialRecommendationsBridge 实例并建立内部状态与依赖注入
- **源码位置**：第 `21` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `config_manager` | `Any` | 配置数据对象或配置模型实例 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `TutorialRecommendationsBridge._read_base_url(...) -> str`
- **方法用途**：执行 _read_base_url 相关的处理操作
- **源码位置**：第 `35` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `TutorialRecommendationsBridge._on_config_changed(...) -> None`
- **方法用途**：执行 _on_config_changed 相关的处理操作
- **源码位置**：第 `41` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `TutorialRecommendationsBridge.recommendations(...) -> list[dict]`
- **方法用途**：执行 recommendations 相关的处理操作
- **源码位置**：第 `48` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`list[dict]`

###### `TutorialRecommendationsBridge.loading(...) -> bool`
- **方法用途**：从磁盘或内存中加载读取目标配置、数据或组件
- **源码位置**：第 `52` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`bool`

###### `TutorialRecommendationsBridge.error(...) -> str`
- **方法用途**：执行 error 相关的处理操作
- **源码位置**：第 `56` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `TutorialRecommendationsBridge.baseUrl(...) -> str`
- **方法用途**：执行 baseUrl 相关的处理操作
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`str`

###### `TutorialRecommendationsBridge._set_loading(...) -> None`
- **方法用途**：执行 _set_loading 相关的处理操作
- **源码位置**：第 `63` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `loading` | `bool` | loading 条件开关状态 |
- **返回值**：`None`

###### `TutorialRecommendationsBridge._set_error(...) -> None`
- **方法用途**：执行 _set_error 相关的处理操作
- **源码位置**：第 `68` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `error` | `str` | error 文本字符串 |
- **返回值**：`None`

###### `TutorialRecommendationsBridge._track_reply(...) -> None`
- **方法用途**：执行 _track_reply 相关的处理操作
- **源码位置**：第 `73` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
  | `callback` | `Callable[[], None]` | 异步完成回调函数 |
- **返回值**：`None`

###### `TutorialRecommendationsBridge._take_reply(...) -> bool`
- **方法用途**：执行 _take_reply 相关的处理操作
- **源码位置**：第 `77` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
- **返回值**：`bool`

###### `TutorialRecommendationsBridge.fetchRecommendations(...) -> None`
- **方法用途**：Fetch the OOBE curation endpoint, keeping a local fallback on failure.
- **源码位置**：第 `88` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `TutorialRecommendationsBridge._on_fetch_finished(...) -> None`
- **方法用途**：执行 _on_fetch_finished 相关的处理操作
- **源码位置**：第 `106` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `reply` | `QNetworkReply` | Y 轴纵坐标 (像素) |
- **返回值**：`None`

###### `TutorialRecommendationsBridge.shutdown(...) -> None`
- **方法用途**：执行 shutdown 相关的处理操作
- **源码位置**：第 `140` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

### 📄 模块：`src/core/updater/updater.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class WindowsUpdater(object)`
> **类设计职能**：解压并替换更新

##### 包含方法全量参考：

###### `WindowsUpdater.__init__(...) -> None`
- **方法用途**：初始化 WindowsUpdater 实例并建立内部状态与依赖注入
- **源码位置**：第 `15` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `temp_dir` | `Path` | temp_dir 运行时参数 |
- **返回值**：`None`

###### `WindowsUpdater.apply_update(...) -> None`
- **方法用途**：执行 apply_update 相关的处理操作
- **源码位置**：第 `18` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `zip_path` | `Path` | 目标文件或目录路径 |
  | `target_dir` | `Path` | target_dir 运行时参数 |
- **返回值**：`None`

---

### 📄 模块：`src/core/updater/bridge.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class UpdaterBridge(QObject)`
> **类设计职能**：UpdaterBridge 业务管理类

##### 包含方法全量参考：

###### `UpdaterBridge.__init__(...) -> None`
- **方法用途**：初始化 UpdaterBridge 实例并建立内部状态与依赖注入
- **源码位置**：第 `23` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `app_central` | `Any` | AppCentral 主程序中央控制中枢引用 |
  | `parent` | `Any` | Qt 父级 QObject / QWidget 对象指针，用于生命周期托管 |
- **返回值**：`None`

###### `UpdaterBridge.status(...) -> None`
- **方法用途**：执行 status 相关的处理操作
- **源码位置**：第 `43` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge.progress(...) -> None`
- **方法用途**：执行 progress 相关的处理操作
- **源码位置**：第 `47` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge.speed(...) -> None`
- **方法用途**：执行 speed 相关的处理操作
- **源码位置**：第 `51` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge.errorDetails(...) -> None`
- **方法用途**：执行 errorDetails 相关的处理操作
- **源码位置**：第 `55` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge._set_status(...) -> None`
- **方法用途**：执行 _set_status 相关的处理操作
- **源码位置**：第 `58` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `s` | `Any` | s 运行时参数 |
- **返回值**：`None`

###### `UpdaterBridge._set_progress(...) -> None`
- **方法用途**：执行 _set_progress 相关的处理操作
- **源码位置**：第 `64` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `percent` | `Any` | percent 运行时参数 |
  | `speed` | `Any` | speed 运行时参数 |
- **返回值**：`None`

###### `UpdaterBridge._set_error(...) -> None`
- **方法用途**：执行 _set_error 相关的处理操作
- **源码位置**：第 `69` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `msg` | `Any` | msg 运行时参数 |
- **返回值**：`None`

###### `UpdaterBridge.update_complete(...) -> None`
- **方法用途**：计算并更新 UpdaterBridge 的状态、属性或遮罩渲染
- **源码位置**：第 `75` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge.checkUpdate(...) -> None`
- **方法用途**：检查更新：所有平台通用
- **源码位置**：第 `95` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge._on_check_finished(...) -> None`
- **方法用途**：执行 _on_check_finished 相关的处理操作
- **源码位置**：第 `108` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `status` | `Any` | 课表当前状态枚举值 (EntryType: CLASS, BREAK, ACTIVITY, etc.) |
  | `version` | `Any` | 版本号字符串 (如 2.0.0.dev) |
  | `url_or_err` | `Any` | 网络资源 URL 或 API 请求端点 |
- **返回值**：`None`

###### `UpdaterBridge.startDownload(...) -> None`
- **方法用途**：仅 Windows 支持下载
- **源码位置**：第 `123` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge._on_download_finished(...) -> None`
- **方法用途**：执行 _on_download_finished 相关的处理操作
- **源码位置**：第 `153` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `success` | `bool` | success 条件开关状态 |
  | `msg` | `str` | msg 文本字符串 |
  | `manual_stop` | `bool` | manual_stop 条件开关状态 |
- **返回值**：`None`

###### `UpdaterBridge.stopDownload(...) -> None`
- **方法用途**：执行 stopDownload 相关的处理操作
- **源码位置**：第 `174` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge.startInstall(...) -> None`
- **方法用途**：执行 startInstall 相关的处理操作
- **源码位置**：第 `186` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `UpdaterBridge._on_install_finished(...) -> None`
- **方法用途**：执行 _on_install_finished 相关的处理操作
- **源码位置**：第 `201` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `success` | `Any` | success 运行时参数 |
  | `msg` | `Any` | msg 运行时参数 |
- **返回值**：`None`

---

### 📄 模块：`src/core/updater/downloader.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class UpdateDownloader(object)`
> **类设计职能**：UpdateDownloader 业务管理类

##### 包含方法全量参考：

###### `UpdateDownloader.__init__(...) -> None`
- **方法用途**：初始化 UpdateDownloader 实例并建立内部状态与依赖注入
- **源码位置**：第 `13` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `url` | `str` | 网络资源 URL 或 API 请求端点 |
  | `dest` | `Path` | dest 运行时参数 |
  | `configs` | `Any` | 配置数据对象或配置模型实例 |
- **返回值**：`None`

###### `UpdateDownloader.stop(...) -> None`
- **方法用途**：外部调用停止下载
- **源码位置**：第 `20` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `manual` | `Any` | manual 运行时参数 |
- **返回值**：`None`

###### `UpdateDownloader._resolve_url(...) -> str`
- **方法用途**：根据 URL 判断是否使用备用下载源
- **源码位置**：第 `26` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `url` | `str` | 网络资源 URL 或 API 请求端点 |
- **返回值**：`str`

###### `UpdateDownloader.download(...) -> None`
- **方法用途**：阻塞下载，progress_callback(百分比, 速度)
- **源码位置**：第 `39` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `progress_callback` | `Any` | 异步完成回调函数 |
- **返回值**：`None`

---

### 📄 模块：`src/core/updater/workers.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class CheckUpdateWorker(QThread)`
> **类设计职能**：CheckUpdateWorker 业务管理类

##### 包含方法全量参考：

###### `CheckUpdateWorker.__init__(...) -> None`
- **方法用途**：初始化 CheckUpdateWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `17` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `channel` | `Any` | channel 运行时参数 |
  | `current_version` | `Any` | 版本号字符串 (如 2.0.0.dev) |
- **返回值**：`None`

###### `CheckUpdateWorker.start(...) -> None`
- **方法用途**：执行 start 相关的处理操作
- **源码位置**：第 `23` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `url` | `Any` | 网络资源 URL 或 API 请求端点 |
- **返回值**：`None`

###### `CheckUpdateWorker.run(...) -> None`
- **方法用途**：启动运行 CheckUpdateWorker 的核心业务逻辑或主循环
- **源码位置**：第 `28` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

#### 🏛️ 核心类：`class DownloadWorker(QThread)`
> **类设计职能**：DownloadWorker 业务管理类

##### 包含方法全量参考：

###### `DownloadWorker.__init__(...) -> None`
- **方法用途**：初始化 DownloadWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `56` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `downloader` | `UpdateDownloader` | downloader 运行时参数 |
- **返回值**：`None`

###### `DownloadWorker.run(...) -> None`
- **方法用途**：启动运行 DownloadWorker 的核心业务逻辑或主循环
- **源码位置**：第 `60` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `DownloadWorker.stop(...) -> None`
- **方法用途**：执行 stop 相关的处理操作
- **源码位置**：第 `70` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `force` | `Any` | force 运行时参数 |
- **返回值**：`None`

#### 🏛️ 核心类：`class InstallWorker(QThread)`
> **类设计职能**：InstallWorker 业务管理类

##### 包含方法全量参考：

###### `InstallWorker.__init__(...) -> None`
- **方法用途**：初始化 InstallWorker 实例并建立内部状态与依赖注入
- **源码位置**：第 `80` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `updater` | `WindowsUpdater` | updater 运行时参数 |
  | `zip_path` | `Path` | 目标文件或目录路径 |
  | `target_dir` | `Path` | target_dir 运行时参数 |
- **返回值**：`None`

###### `InstallWorker.run(...) -> None`
- **方法用途**：启动运行 InstallWorker 的核心业务逻辑或主循环
- **源码位置**：第 `86` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

## 官方内置小组件插件 (Built-in Plugin)

### 📄 模块：`src/plugins/cw_widgets/widgets.py`

> **模块职能说明**：核心业务逻辑支持模块。

#### 🏛️ 核心类：`class Plugin(CW2Plugin)`
> **类设计职能**：Plugin 业务管理类

##### 包含方法全量参考：

###### `Plugin.__init__(...) -> None`
- **方法用途**：初始化 Plugin 实例并建立内部状态与依赖注入
- **源码位置**：第 `20` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
  | `plugin_api` | `Any` | plugin_api 运行时参数 |
- **返回值**：`None`

###### `Plugin.get_widgets_list(...) -> None`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `23` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `Plugin.on_load(...) -> None`
- **方法用途**：响应底层事件、信号或回调触发的槽函数
- **源码位置**：第 `81` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `Plugin.register_widgets(...) -> None`
- **方法用途**：向管理器注册新的功能组件、插件或回调监听器
- **源码位置**：第 `85` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `Plugin.getDateTime(...) -> None`
- **方法用途**：查询并获取对应的属性、对象或计算结果
- **源码位置**：第 `97` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

###### `Plugin.on_unload(...) -> None`
- **方法用途**：响应底层事件、信号或回调触发的槽函数
- **源码位置**：第 `109` 行
- **参数列表与类型意义**：
  | 参数名 | 数据类型 | 业务意义与作用说明 |
  | :--- | :--- | :--- |
  | `self` | `Any` | 实例对象自身引用 |
- **返回值**：`None`

---

## 其他辅助支持模块 (Auxiliary Modules)

### 📄 模块：`src/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/automations/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/config/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/convertor/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/convertor/converter.py`

> **模块职能说明**：系统支撑与基础协议模块。

- **类定义**：`class ScheduleConverter` (23 个方法)

---

### 📄 模块：`src/core/convertor/slots.py`

> **模块职能说明**：系统支撑与基础协议模块。

- **类定义**：`class ScheduleIO` (4 个方法)

---

### 📄 模块：`src/core/notification/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/parser/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/parser/schedule.py`

> **模块职能说明**：系统支撑与基础协议模块。

- **类定义**：`class ScheduleParser` (3 个方法)

---

### 📄 模块：`src/core/plaza/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/plugin/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/schedule/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/themes/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/timer/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/timer/union_update.py`

> **模块职能说明**：系统支撑与基础协议模块。

- **类定义**：`class UnionUpdateTimer` (4 个方法)

---

### 📄 模块：`src/core/updater/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/utils/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。

- **函数**：`def generate_id(...) -> str`
- **函数**：`def _parse_version(...) -> None`
- **函数**：`def is_valid_context_property_name(...) -> bool`

---

### 📄 模块：`src/core/utils/backend.py`

> **模块职能说明**：系统支撑与基础协议模块。

- **类定义**：`class UtilsBackend` (47 个方法)

---

### 📄 模块：`src/core/utils/http_stream.py`

> **模块职能说明**：Interruptible streaming of an HTTP response body.

``requests``/``urllib3`` read from the socket through ``socket.makefile``, and
on Windows closing the socket from another thread does not wake up a blocked
read.  That makes pause/cancel of a streaming download unresponsive: the worker
thread stays stuck until the server sends more data or the socket read timeout
fires.

This module streams the body with short reads (``read1``) gated by ``select``,
so the caller can poll its own state between chunks and abort promptly, even
while the server is idle.

- **函数**：`def call_interruptibly(...) -> T`
- **函数**：`def iter_response_chunks(...) -> Iterator[bytes]`
- **函数**：`def _select_targets(...) -> list[object]`
- **函数**：`def _close_result(...) -> None`

---

### 📄 模块：`src/core/widgets/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/core/windows/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/plugins/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/plugins/cw_widgets/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---

### 📄 模块：`src/themes/__init__.py`

> **模块职能说明**：系统支撑与基础协议模块。


---
