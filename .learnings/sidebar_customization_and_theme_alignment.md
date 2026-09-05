# Learning: 侧边栏多维自定义体系与主程序主题双模式对齐规范

## 1. 架构目标
为贴边驻留抽屉条提供高自由度的自定义能力（贴靠边缘选择、Y 轴高度微调、双模式圆角与透明度），同时实现与主程序官方设计语言（线性高光渐变、毛玻璃质感、色彩模型）100% 深度融合，且在主程序【设置 -> 小组件】页面实现无缝集成。

## 2. 核心工程决策与防御模式
1. **双模式外观继承链 (Appearance Fallback Chain)**：
   - 采用 `customAppearance ? sidebarValue : globalValue` 响应式流水线。
   - 默认状态下关闭独立外观开关，保证用户调整主程序全局小组件圆角与透明度时，侧边栏能够 0 摩擦无感同步；开启后才使用侧边栏专属值。
2. **左右对称镜像与遮罩自适应 (Bidirectional Mirroring & Mask)**：
   - 当侧边栏切换至 `left` 靠左边缘贴靠时，悬浮操作按钮与弹出气泡必须完全镜像至右侧弹出。
   - 遮罩计算 `getInteractiveRects()` 必须根据 `isLeftEdge` 动态向右扩展预留 210px 交互区域，且收起图标与折叠箭头自适应反向（`‹` ↔ `›`，`⇥` ↔ `⇤`）。
3. **主程序材质复刻 (Shader/Gradient Alignment)**：
   - 严格采用主程序 `Widget.qml` 的 `LinearGradient` + `OpacityMask` 渐变边框架构，杜绝单调的纯色边框。
