# E2E Test Infra: Class-Widgets-2 侧边课表栏系统

## Test Philosophy
- **需求驱动与黑盒验证 (Requirement-Driven & Opaque-Box)**:
  所有端到端与集成测试严格基于 `ORIGINAL_REQUEST.md` (R1-R5) 中的用户交互行为与功能规格，不依赖内部临时变量。
- **系统化四层测试分级 (4-Tier Test Architecture)**:
  采用等价类划分 (Category-Partition)、边界值分析 (BVA)、成对交互 (Pairwise) 与真实场景负载测试。

---

## Feature Inventory
| # | Feature | Source (Requirement) | Tier 1 | Tier 2 | Tier 3 |
|---|---------|----------------------|:------:|:------:|:------:|
| F1 | 当天课表竖条胶囊主体 | ORIGINAL_REQUEST §1 | 5 | 5 | ✓ |
| F2 | 当前课程状态与高亮 | ORIGINAL_REQUEST §1 | 5 | 5 | ✓ |
| F3 | 课程悬浮气泡卡片 | ORIGINAL_REQUEST §1 | 5 | 5 | ✓ |
| F4 | 悬浮双按钮滑出与收起 | ORIGINAL_REQUEST §2 | 5 | 5 | ✓ |
| F5 | 防误触延时缓冲机制 (300ms) | ORIGINAL_REQUEST §2 | 5 | 5 | ✓ |
| F6 | 全周课表网格大面板 | ORIGINAL_REQUEST §3 | 5 | 5 | ✓ |
| F7 | 外部点击与单一收回交互 | ORIGINAL_REQUEST §3 | 5 | 5 | ✓ |
| F8 | 隐藏收起与贴边呼出小胶囊 | ORIGINAL_REQUEST §4 | 5 | 5 | ✓ |
| F9 | 贴边小胶囊高亮与呼出恢复 | ORIGINAL_REQUEST §4 | 5 | 5 | ✓ |
| F10 | WidgetsWindow 遮罩穿透 (setMask) | ORIGINAL_REQUEST §5 | 5 | 5 | ✓ |
| F11 | 设置中心配置与状态记忆 | ORIGINAL_REQUEST §5 | 5 | 5 | ✓ |

---

## Test Architecture
- **运行环境**: Python 3.12 + PySide6 6.10.3 (基于项目 `.venv` 与 `uv`)
- **测试执行命令**: `uv run pytest tests/e2e/ -v`
- **测试套件目录**:
  - `tests/e2e/test_sidebar_model.py`: 检验当天课表与整周课表聚合数据完整性、高亮逻辑与边界
  - `tests/e2e/test_sidebar_mask.py`: 检验竖条/大面板/小胶囊状态下的 `QRegion` 遮罩与穿透区域计算
  - `tests/e2e/test_sidebar_config.py`: 检验 Settings 开关与折叠状态持久化读写
  - `tests/e2e/test_sidebar_e2e_scenarios.py`: 检验综合用户行为时序（移入滑出、缓冲超时、展开全周、外部点击收回、贴边呼出）

---

## Coverage Thresholds
- **Tier 1 (功能覆盖)**: 11 × 5 = 55 个基础测试用例
- **Tier 2 (边界与极端值)**: 11 × 5 = 55 个边界与鲁棒性用例 (无课程空表、超长课程名、时钟跳变瞬间、快速反复移入移出、多显示器越界)
- **Tier 3 (特性组合成对覆盖)**: 11 个跨状态组合测试用例 (例如：全周展开中切换配置开关、收起贴边后时钟跨天、悬浮按钮滑出过程中直接点击折叠等)
- **Tier 4 (真实应用场景)**: 6 个完整端到端用户行为场景
- **总测试用例目标**: ≥ 127 个测试验证点

---

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | 学生全天上课正常流转（课前、正在上课高亮、课间倒计时、换课） | F1, F2, F3 | Medium |
| 2 | 查看课程详情后临时展开全周排课并收回 | F1, F3, F4, F6, F7 | High |
| 3 | 鼠标掠过竖条边缘防误触（移出后 200ms 快速移回 vs 350ms 完全收回） | F4, F5 | Medium |
| 4 | 专注模式隐藏贴边，随后点击边缘小胶囊恢复 | F1, F8, F9, F10 | Medium |
| 5 | 设置中心关闭侧边栏并在下次启动时恢复记忆状态 | F1, F8, F10, F11 | High |
| 6 | 极限操作压力测试：快速连击展开/收回/折叠同时进行窗口遮罩穿透点击 | F4, F5, F6, F7, F8, F9, F10 | High |
