# Learning: QML 桌面透明窗口动画卡顿（掉帧）深度排查与极致性能优化

## 1. 故障现象
- **现象描述**：侧边栏功能逻辑正常，但当鼠标悬浮在侧边栏弹出按钮、划过课程胶囊弹出详情气泡、或点击展开全周大面板时，视觉动画明显“一卡一卡的”（Stuttering / 严重掉帧）。

## 2. 根因剖析 (Root Causes)

### 根因 1: 动画过程中频繁触发 Win32 API `SetWindowRgn` 同步阻塞 (最致命)
- **机制**：Qt 中对顶级无边框分层窗口调用 `setMask(mask)`，在 Windows 底层会调用 Win32 API `SetWindowRgn`。
- **代价**：`SetWindowRgn` 是同步阻塞的系统调用，会强行挂起桌面窗口管理器（DWM）的 DirectComposition / OpenGL / Direct3D 提交，并在 CPU/系统内核级重新计算并刷新窗口裁剪区域。
- **缺陷暴露**：
  在之前的代码中，悬浮按钮的显示/隐藏、气泡的淡入/淡出、甚至光标在小胶囊上 hover 变色时，都在向 Python 发射 `geometryChanged()` 信号，导致在 200ms 的动画播放过程中，Python 连续调用了 3~4 次 `setMask`！
  每次阻塞 20~50ms，导致 QML 渲染线程的动画帧被操作系统硬生生丢弃打断。

### 根因 2: `DropShadow` 的重度 GPU/CPU 卷积采样与无缓存失效
- **机制**：`Qt5Compat.GraphicalEffects` 中的 `DropShadow` 是基于高斯模糊着色器实现的离屏渲染效果。
- **代价**：原代码中，全周大面板（840x620 像素）使用了 `samples: 32; radius: 28;`。每一帧每个像素都要进行 32 次采样计算，双向卷积开销极其沉重。
- 此外，未设置 `cached: true` 和 `fast: true`，在配合 `scale` 缩放变换时，源项尺寸每一帧都在变，导致 GPU 离屏 FBO 纹理每一帧都在销毁重建与重新模糊计算。

### 根因 3: `scale` 几何缩放引发子树文本抗锯齿连续重新光栅化 (Re-rasterization)
- **机制**：对包含大量 `Text` 元素的复杂容器（如周课表矩阵含有上百个文本节点）应用 `scale: 0.94 -> 1.0` 缩放动画时，Qt Quick 的字体引擎在每一帧都需要对亚像素字形进行重新采样和几何形变计算，配合 `liquidBack` 超越曲线的过冲震荡，造成剧烈的渲染管线拥堵。

---

## 3. 永久防御与性能优化准则 (Defense & Optimization Rules)

1. **静态预留交互包围盒 (Avoid Dynamic setMask during Animations)**：
   - 对于停留在屏幕边缘的小组件/侧边栏，在 NORMAL 状态下直接向外预留弹出按钮与详情气泡的工作矩形（如向左延伸 210px）。
   - 按钮滑出/滑入、气泡弹出/收回、光标移动等所有高频微交互**完全发生在预留包围盒内，绝不触发 `setMask`**！
   - `setMask` 仅在状态机发生大跨度迁移（NORMAL <-> EXPANDED <-> COLLAPSED）时才执行 1 次。
2. **纯 GPU 矩阵平移（Translation）取代几何缩放（Scale）**：
   - 侧边栏所有展开、弹出、滑入效果均采用 `transform: Translate { ... }` 配合纯透明度淡入（`opacity`）。
   - `transform: Translate` 在 GPU 场景图中只是纯矩阵偏移（Offset），**完全零文本重栅格化、零布局重排（Zero Layout Reflow）**，帧率稳跑满 60/120 FPS。
3. **DropShadow 轻量化准则**：
   - 凡使用 `DropShadow`，必须显式声明 `cached: true` 和 `fast: true`。
   - 采样数 `samples` 严格控制在 8~9，半径 `radius` 控制在 8~14，杜绝 24~32 的过杀参数。
4. **窗口级遮罩更新防抖保护**：
   - 在 Python 端 `schedule_mask_update` 设定防抖延迟（如 35ms），彻底消除高频突发事件导致的连续系统调用阻塞。
