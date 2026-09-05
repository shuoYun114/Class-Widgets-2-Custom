# Learning: QML 侧边栏折叠态遮罩竞争裁剪与贴边胶囊暗色背景隐形防御

## 1. 故障现象
- **现象描述**：用户在侧边课表栏点击“收起隐藏竖条”后，侧边栏完全消失（边缘没有任何可见按钮，鼠标悬停在屏幕右侧边缘毫无反应且无法点击），用户不得不去点击屏幕顶部的浮窗（`FloatingWidgetContainer`）才能唤回。
- **排查凭证**：逐帧像素提取与时序分析（视频 `unknown_2026.09.05-20.05.mp4`）。

## 2. 根因剖析 (Root Cause)
1. **遮罩竞争剪切 (Mask Race Condition & DWM Physical Clipping)**：
   - 在 `ScheduleSidebar.qml` 的 `getInteractiveRects()` 中使用了 `if (edgeCapsule.visible && edgeCapsule.opacity > 0.05)`。
   - 当用户点击收起按钮瞬间，`sidebarState` 变为 `"COLLAPSED"`，并触发 `geometryChanged()`。
   - Python 端经过 35ms 防抖后调用 `update_mask()`。此时小胶囊刚触发 180ms 的淡入动画，其 `opacity` 尚未超过 0.05，导致 `getInteractiveRects()` 返回空列表 `[]`。
   - Python 因此将窗口遮罩设置为 `QRect(0, 0, 1, 1)`（1x1 极小区域）。
   - **致命漏洞**：动画结束（180ms 后）没有发出任何信号通知 Python 重新更新遮罩！Windows DWM 物理裁剪了小胶囊所在区域，导致其在操作系统层面不可见且无法捕获鼠标事件。
   - 直到用户点击顶部浮窗，浮窗触发了配置重刷并调用 `update_mask()`，此时动画已完成，遮罩才重新包裹小胶囊。
2. **暗色背景视觉隐形与碰撞箱过窄**：
   - 原 `EdgeRestoreCapsule.qml` 静态不透明度仅 `0.40`，背景色为深灰黑 `#1C1B20`（70% 透明度），叠加后仅 28% 不透明度；在深色软件背景（如 Radeon 纯黑控制面板）前视觉上近乎完全隐形，用户产生“最小化后消失”的错觉。

## 3. 防御策略与修复规范 (One-Strike Permanent Defense)
1. **折叠遮罩即时性原则 (Mask Immediacy Principle)**：
   - 交互遮罩（Mask）的生命周期必须绑定于**逻辑状态（State Machine）**而非视觉过渡动画（Visual Transition/Opacity）。
   - 折叠态激活瞬间，必须无条件立即将贴边呼出小胶囊的物理几何区域写入 mask，绝不等待动画过渡。
2. **多态双向连接兜底**：
   - 监听胶囊的 `visible` 与 `isActive` 信号，确保任何尺寸或状态跃迁均能可靠触发遮罩重排。
3. **高对比度边缘视觉设计**：
   - 贴边常驻唤回组件在深浅色模式下均必须具备高清晰度轮廓（静态不透明度提升至 0.88+，主题色发光边框，内部设置圆角垂直拉手条），即便在纯黑或复杂背景下也能一眼辨识。
