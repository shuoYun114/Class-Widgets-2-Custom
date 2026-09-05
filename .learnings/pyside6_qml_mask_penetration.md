# Learning: PySide6 与 QML 交互及全屏置顶透明窗口遮罩 (setMask) 穿透防御

## 1. 故障现象
- **现象描述**：启动桌面小组件后，屏幕上能显示小组件/浮窗，但鼠标无法点击桌面上的任何其他窗口或图标，整个操作系统像死锁一样；按 `Win + D` 切回桌面后，只要再次点击任意窗口，鼠标又无法点击任何内容。
- **危害等级**：严重（阻断操作系统层面的全部鼠标交互）。

## 2. 根因剖析 (Root Cause)
1. **QML 与 PySide6 数据类型不兼容**：
   - QML 中通过 JavaScript 返回的数组（如 `[[x, y, w, h], ...]`）在 Python 端通过 `obj.property(...)` 或调用 QML 方法获取时，类型为 `PySide6.QtQml.QJSValue`。
   - 在 Python 中，`QJSValue` **不是可迭代对象 (Iterable)**。
   - 直接执行 `for item in sidebar_rects:` 会触发未捕获的运行时异常：
     `TypeError: 'PySide6.QtQml.QJSValue' object is not iterable`
2. **Qt 全屏置顶透明窗口遮罩失效**：
   - `WidgetsWindow` 是一个全屏（1920x1080）置顶（`Qt.WindowStaysOnTopHint`）的无边框透明窗口。
   - 该窗口依赖 `update_mask()` 动态计算可见小组件的有效区域，并调用 `self.root_window.setMask(mask)`。
   - 当 `update_mask()` 在迭代 `sidebar_rects` 时抛出未捕获异常并崩溃中断，导致 `setMask(mask)` 从未执行成功。
   - 没有生效 mask 的全屏透明窗口覆盖在最顶层，无差别拦截截获了操作系统桌面上的所有鼠标点击，导致底层所有窗口均无法响应鼠标。

## 3. 防御策略与修复规范 (One-Strike Permanent Defense)
1. **QJSValue 安全解包规范**：
   - 所有从 QML 获取的动态对象，必须检查并调用 `.toVariant()`：
     ```python
     if hasattr(prop, "toVariant"):
         prop = prop.toVariant()
     ```
   - 即使对于内层元素（如二维数组的每一项），解包后也必须严格做类型与长度校验：
     ```python
     if hasattr(item, "toVariant"):
         item = item.toVariant()
     if isinstance(item, (list, tuple)) and len(item) == 4:
         ...
     ```
2. **全局核心函数零崩溃防线**：
   - `update_mask()` 属于核心级生命周期函数，涉及操作系统事件路由，所有子组件区域提取必须使用安全块包裹，杜绝任何未捕获异常中断执行流程。
3. **空掩码兜底防御**：
   - 在 Qt/Windows 中，`setMask(QRegion())` 会清除窗口遮罩，使得整个全屏窗口可见/可交互，从而覆盖全屏。
   - 当没有有效组件时，必须保持最小 1x1 像素的极小区域 `QRegion(QRect(0, 0, 1, 1))`，以防意外覆盖全屏。
