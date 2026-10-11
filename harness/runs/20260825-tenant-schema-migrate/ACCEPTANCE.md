# 验收清单 ACCEPTANCE

> 复制到 `.cursor/harness/runs/{yyyyMMdd-slug}/ACCEPTANCE.md` 后填写。  
> **功能是否「完成」以本文件为准；对话中的「好了」不能替代勾选。**

## 功能验收（对照 FEATURE_CARD 目标）

| ID | 验收项 | 结果 | 证据（路径/命令/截图说明） |
|----|--------|------|----------------------------|
| G1 | 启动时按 serviceCode 目录自动执行 pending 正向脚本 | ☐ pass / ☐ fail / ☐ n/a | 代码已挂 `loadAllDB`；待库表创建后联调 |
| G2 | 已成功脚本再次启动跳过 | ☐ pass / ☐ fail / ☐ n/a | `alreadySuccess` 查 `exec_status=1` |
| G3 | 一租户失败则本轮已成功项逆序回滚（跨 serviceCode） | ☐ pass / ☐ fail / ☐ n/a | `rollbackAll` + appliedStack |
| G4 | 缺配对回滚脚本则拒绝执行 | ☐ pass（单测） / ☐ fail / ☐ n/a | `TenantMigrateScriptScannerTest#scanAll_missingRollback` |
| G5 | 新租户 init 后补跑 pending migrate | ☐ pass / ☐ fail / ☐ n/a | `initDatabase` → `migrateForDatasource` |

## 静态检查 L1

| 项 | 命令或操作 | 结果 |
|----|------------|------|
| 后端编译（相关模块） | `mvn -pl mall-admin/mall-sys-core -am -DskipTests compile` | ☐ 待本地（环境 mvn 不可用） |
| 前端 eslint | n/a | ☐ n/a |
| 前端 vue-tsc | n/a | ☐ n/a |

## 模块小测试 L2

### L2-a Java（Service 等）

| 测试类（模块 src/test/java） | 单跑命令 | 结果 |
|------------------------------|----------|------|
| `com.yz.mall.sys.migrate.TenantMigrateScriptScannerTest` | `mvn -pl mall-admin/mall-sys-core -Dtest=TenantMigrateScriptScannerTest test` | ☐ 待本地 |

### L2-b Python（Controller API，定时平台）

> 本期无对外 Controller → **整表豁免**。

| 脚本路径 | 类型 | 单跑命令 | 本地结果 | 已上传定时平台 | 平台任务名/周期 |
|----------|------|----------|----------|----------------|-----------------|
| — | n/a | — | ☐ n/a | ☐ n/a | — |

## 场景验收 L3

| 用例 ID | 场景 | 期望 | 结果 |
|---------|------|------|------|
| T1 | 两租户同 service，脚本成功 | 两库变更一致，主库两条成功日志 | ☐ 待联调 |
| T2 | 第二租户正向失败 | 本轮已成功项全部回滚；后续中止 | ☐ 待联调 |
| T3 | 再次启动 | 已成功版本跳过 | ☐ 待联调 |
| T4 | 仅有正向无回滚文件 | 启动迁移中止并打错误日志 | ☐ 单测覆盖扫描层 |

## 代码检查（Review）

| 项 | 结果 |
|----|------|
| review-java-change / 人工或 Agent 审查 | ☐ 有条件通过 |
| 「必须修改」是否已清零 | ☐ 是（无必须修改） |
| 前端路由是否与动态菜单冲突 | ☐ n/a |
| 权限码、密钥、SQL 安全项 | ☐ 通过（无对外接口；JDBC 用配置账号，未日志密码） |

审查摘要：

```text
结论：有条件通过 — 核心链路已落地；主库 DDL 待执行；本机 mvn 未跑通。

必须修改：无

建议改进：
- 多实例同时启动可能并发执行同一脚本（可后续加分布式锁）
- 迁移失败会抛异常导致应用启动失败（符合「阻断」；若希望降级为仅告警需另开需求）

可后续处理：
- 日志查询接口 / 手动触发 API
- 管理端展示迁移结果
```

## 残留风险与豁免

| 项 | 原因 | 是否接受 |
|----|------|----------|
| 无 Python API 测试 | 本期无 HTTP 接口 | ☐ 接受 |
| 跨租户回滚非分布式事务 | 依赖回滚脚本正确性；回滚失败需人工介入 | ☐ 接受 |
| 主库表未建 | MCP 只读，DDL 待 DBA | ☐ 需处理后方可联调 |

## 最终确认

- [ ] 验收清单已更新，可视为本功能开发闭环完成（不含未授权的 push）  
- 确认人 / 日期：
