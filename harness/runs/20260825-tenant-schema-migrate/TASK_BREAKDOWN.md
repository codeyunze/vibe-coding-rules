# 任务拆分 TASK_BREAKDOWN

> 复制到 `.cursor/harness/runs/{yyyyMMdd-slug}/TASK_BREAKDOWN.md` 后填写。  
> **开发进度只更新本文件勾选，不靠聊天列表记忆。**

## 依赖顺序（强制）

建议顺序：`DDL → 后端 dao/core → 启动挂钩 → Java 单测 → Review`  
（本期无 Controller / 无前端 / 无 Python API 脚本）

## 任务清单

### A. 数据

- [x] A1 DDL：`saas_schema_migrate_log` 建表 SQL 落到 `mall-sys-startup/src/main/resources/db/`
- [ ] A2 （可选）本地执行 DDL；只读则记「待 DBA」— **MCP 只读，待 DBA 执行**

### B. 后端（yz-mall）

- [x] B1 Entity / Mapper（`mall-sys-dao`）：`SaasSchemaMigrateLog` + Mapper
- [x] B2 迁移核心（`mall-sys-core`）：扫描 / 配对校验 / 执行 / 失败全量回滚 / 主库日志
- [x] B3 启动挂钩：`loadAllDB()` 之后触发
- [x] B4 新租户挂钩：`initDatabase` 后补跑
- [x] B5 `sql/tenant-migrate/README.md` 约定说明
- [x] B6 （本期不做）Controller / 权限 / Feign / 网关

### C. 前端（yz-mall-web-admin-pc）

- [x] C1 本期不做（deferred）

### D. 测试（模块内小文件）

- [x] D1 Java：`TenantMigrateScriptScannerTest`
- [x] D2 Python API：n/a
- [ ] D3 前端：n/a
- [ ] D4 本机执行 D1：环境缺可用 `mvn`（`MAVEN_HOME` 无效），待本地补跑

### E. 检查与收尾

- [x] E1 自检 review-java-change 并回写 ACCEPTANCE
- [ ] E2 （仅用户要求时）commit；禁止擅自 push

## 任务明细（可增行）

| ID | 描述 | 仓库 | 路径/模块 | 依赖 | 状态 |
|----|------|------|-----------|------|------|
| A1 | 主库迁移日志表 DDL | yz-mall | `mall-sys-startup/.../db/saas_schema_migrate_log.sql` | - | done |
| B1 | Entity + Mapper | yz-mall | `mall-sys-dao` | A1 | done |
| B2 | `SaasTenantSchemaMigrateService` | yz-mall | `mall-sys-core` | B1 | done |
| B3 | `loadAllDB` 后调用 migrate | yz-mall | `SaasTenantServiceImpl` | B2 | done |
| B4 | `initDatabase` 后单租户 migrate | yz-mall | `SaasTenantServiceImpl` | B2 | done |
| B5 | 目录约定 README | yz-mall | `sql/tenant-migrate/README.md` | - | done |
| D1 | 配对校验与排序单测 | yz-mall | `TenantMigrateScriptScannerTest` | B2 | done |
| E1 | Review | yz-mall | - | D1 | done |

## 阻塞项

| ID | 原因 | 需要谁 | 状态 |
|----|------|--------|------|
| A2 | MCP 库只读，无法自动建表 | DBA / 本地写权限执行 DDL | open |
| D4 | `MAVEN_HOME` 指向无效路径，本机未跑通 mvn | 开发者本机 | open |

## 确认记录

- [x] 任务拆分已与用户对齐，可开始编码  
- 确认备注：问题 7 改为「任一失败阻断并回滚本轮全部已成功项」；用户确认可编码。
