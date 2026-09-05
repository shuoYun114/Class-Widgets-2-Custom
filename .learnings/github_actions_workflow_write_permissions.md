# Learning: GitHub Actions 自动提交与创建 Release 的仓库权限防御

## 1. 隐患背景
- 新建的 GitHub 仓库中，`Actions` 的默认工作流权限（Workflow Permissions）策略通常为只读（`default_workflow_permissions: "read"`）。
- 此时即使用户在 workflow YAML 中声明了 `permissions: contents: write`，由于仓库级安全策略限制，在执行 `git push` 或 `softprops/action-gh-release` 时依然会遭遇 `403 Resource not accessible by integration` 失败。

## 2. 自动化解决方案
通过 GitHub CLI / API 在仓库初始化时将该权限配置为 `write`：
```powershell
gh api -X PUT repos/<owner>/<repo>/actions/permissions/workflow -F default_workflow_permissions=write
```
执行后确认返回 `{"default_workflow_permissions":"write"}`，确保自动化云端 CI/CD 可以无缝进行跨版本追随提交与发布。
