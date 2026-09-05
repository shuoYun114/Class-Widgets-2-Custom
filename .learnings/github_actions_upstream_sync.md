# Learning: 开源项目二改后的 GitHub Actions 自动追随上游更新与云端编译发布流水线

## 1. 核心需求
- 开源二改项目（Downstream Fork/Customization）如何实现：当官方上游（Upstream）发布新版本时，自动检测、自动合并（Merge/Rebase）、自动化测试、自动编译打包 Windows EXE 并自动发布 GitHub Release。

## 2. 关键架构设计
1. **轻量级版本基线记录 (`.upstream_version`)**：
   记录上次同步的上游 Commit SHA，定时任务（Cron）启动时仅拉取 upstream 检查 HEAD SHA，若无变动则直接退出，不浪费 GitHub Actions 每月的免费构建分钟数。
2. **自动化测试守门员（Quality Gate）**：
   在打包前必须运行全量回归与对抗测试套件（如 157 项 pytest），一旦官方改动与二改逻辑发生冲突或导致断言失败，流水线立即阻断，绝不向用户发布有缺陷或崩溃的应用程序。
3. **安全权限配置**：
   流水线必须声明 `permissions: contents: write`，并在 `actions/checkout@v4` 中注入 `token: ${{ secrets.GITHUB_TOKEN }}`，以支持将同步后的 commit 推回 main 分支并自动创建 Release。
4. **单 Job 极致流转 (Single Windows Job)**：
   直接在 `windows-latest` 环境中依次执行：检查 -> 合并 -> 测试 -> 打包 (`build_exe.py`) -> 发布 (`action-gh-release`)，避免跨 Job 压缩传输数百兆 EXE 构建中间件。
