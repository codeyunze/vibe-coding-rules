# 需求卡片 FEATURE_CARD

> 复制到 `.cursor/harness/runs/{yyyyMMdd-slug}/FEATURE_CARD.md` 后填写。  
> **本文件是唯一需求真相源；对话中的理解必须以本文件为准并回写。**

## 元信息

| 项 | 内容 |
|----|------|
| 功能短名（slug） | `20260825-tenant-schema-migrate` |
| 创建日期 | 2026-08-25 |
| 设计文档路径 | （无独立设计文档；基于现有 `SaasTenantServiceImpl` 动态数据源 + `sql/tenant-init.sql`） |
| 后端仓库/模块 | `yz-mall` / `mall-admin`（mall-sys） |
| 前端仓库 | 本期不做 |
| 负责人确认 | ☑ 已确认 |

## 1. 目标（做什么）

- G1：在 `mall-sys-core` 的 `resources/sql/tenant-migrate/{serviceCode}/` 下按约定放置**正向脚本 + 对应回滚脚本**后，应用**启动时自动**对启用中的租户库执行尚未成功的增量脚本（DDL + 初始化数据）。
- G2：同一正向脚本对同一租户库**只执行一次**（成功记录写入主库统一日志表）。
- G3：**事务语义（跨租户）**：某一版本脚本在任一租户执行失败时，对该版本已成功执行的全部租户执行对应回滚脚本，本轮该版本视为失败（不继续后续版本）；失败原因写入主库日志。
- G4：与现有能力衔接：`tenant-init.sql` 仍负责新建租户首次建表；`initDatabase` 成功后对该租户补齐其 `serviceCode` 下已存在的 pending migrate（同样遵循失败回滚策略，仅影响该租户时：单租户场景回滚自身即可）。
- G5：复用 `SaasTenantDatasource` + `ScriptUtils`；不引入 Flyway/Liquibase。

## 2. 非目标（明确不做）

- 不做 Flyway/Liquibase 产品级能力。
- 不做管理端前端页面。
- **本期不做**迁移日志查询接口、**不做**专用权限码与手动触发 API（仅启动自动 + 新租户 init 后补跑）。
- 不改动网关 Session / `@DS("#session.tenantCode")` 业务路由逻辑。

## 3. 角色与权限

| 角色 | 能力 | 权限码（拟定） |
|------|------|----------------|
| — | 本期无对外运维接口 | — |

## 4. 数据与表

| 表名 | 变更类型（新建/改字段） | DDL 落盘路径 |
|------|-------------------------|--------------|
| `saas_schema_migrate_log`（主库） | 新建：记录「租户 + serviceCode + 脚本」执行/回滚结果 | `mall-sys-startup/src/main/resources/db/saas_schema_migrate_log.sql`（与同目录 `sys_open_client.sql` 风格一致） |

拟定字段：

| 字段 | 说明 |
|------|------|
| `id` | 主键 |
| `tenant_id` / `tenant_code` | 租户 |
| `service_code` | 服务标识（对应脚本目录） |
| `script_name` | 正向脚本文件名（如 `V20260825_001__xxx.sql`） |
| `script_checksum` | 正向脚本内容校验（防篡改后误跳过，可选记录） |
| `exec_status` | 1成功 / 2失败 / 3已回滚 |
| `error_msg` | 失败或回滚异常信息 |
| `exec_time` / `rollback_time` | 执行/回滚时间 |
| `create_time` / `update_time` / `invalid` | 基础字段 |

唯一性：同一租户同一 `service_code` 下同一 `script_name` 成功记录不重复执行（查询已成功则跳过）。

## 5. 后端接口

| 方法 | 路径 | 说明 | 权限码 | 正例期望 code | 反例期望 code |
|------|------|------|--------|---------------|---------------|
| — | — | 本期无 HTTP 接口 | — | — | — |

网关/路由注意：无新增对外 path。

## 6. 前端页面

| 菜单/路由 path | 页面路径 | 说明 |
|----------------|----------|------|
| — | — | 本期不做 |

## 7. 跨服务 / 消息 / 缓存（若有）

### 目录与命名

```text
mall-sys-core/src/main/resources/sql/tenant-migrate/{serviceCode}/
  VyyyyMMdd_NNN__描述.sql              # 正向
  VyyyyMMdd_NNN__描述.rollback.sql     # 回滚（与正向同前缀，后缀 .rollback.sql）
```

- 按 `serviceCode` 分目录；仅对该 `service_code` 且 `ds_status=1` 的数据源执行。
- 同目录下按文件名字典序执行；每个正向脚本必须存在配对回滚脚本，否则启动报错并中止该 serviceCode 本轮迁移。

### 启动流程（`loadAllDB` 之后）

1. 扫描 `sql/tenant-migrate/*/` 下所有 serviceCode 目录。
2. 对每个 serviceCode，按脚本版本顺序：
   - 过滤出主库日志中尚未 `exec_status=1` 的租户集合（该 service 下启用数据源）。
   - 若全部租户已成功，跳过该版本。
   - 对「待执行租户」依次执行正向脚本；每成功一台写日志成功。
   - **任一租户失败**：对本轮启动中已成功执行的全部正向脚本（含其他 serviceCode/更早版本）按**逆序**执行回滚；日志标为失败/已回滚；**后续全部中止**（含其他 serviceCode）。
3. 新租户 `initDatabase`：`tenant-init.sql` 成功后，仅对该租户执行其 serviceCode 下全部 pending 正向脚本；失败则对该租户按逆序回滚本轮已执行脚本并标记 init 失败。


### 脚本内容

- 允许 DDL + 初始化数据（INSERT 等）。
- 幂等依赖「主库成功日志」；回滚脚本由研发保证可撤销本次正向变更。

## 8. 验收要点（摘要，细节见 ACCEPTANCE.md）

- 启动后 pending 脚本自动打到各启用租户库；成功写入主库日志；再次启动跳过已成功。
- 某租户正向失败时，同版本其他已成功租户被回滚，主库有失败/回滚记录。
- 缺少配对回滚脚本时迁移拒绝执行并有明确日志。
- 新租户 init 后 schema 与同 service 已迁移租户一致（在 migrate 全成功前提下）。
- 本期无 HTTP API / 无前端 / 无权限码。

## 9. 开放问题（确认前必须清空或标延期）

| # | 问题 | 结论 | 确认人 |
|---|------|------|--------|
| 1 | 触发时机 | **启动自动**（另：新租户 init 后补跑） | 用户 2026-08-25 |
| 2 | 执行记录 | **主库统一日志** `saas_schema_migrate_log` | 用户 2026-08-25 |
| 3 | 失败策略 | **一租户失败 → 同版本已成功租户全部回滚**；需配对回滚脚本；同 serviceCode 后续版本中止 | 用户 2026-08-25 |
| 4 | 脚本内容 | **允许 DDL + 初始化数据** | 用户 2026-08-25 |
| 5 | 目录划分 | **按 serviceCode 分目录** | 用户 2026-08-25 |
| 6 | 日志查询接口与权限码 | **本期不做** | 用户 2026-08-25 |
| 7 | 多 serviceCode 时：一个 service 迁移失败是否阻断其他 service | **直接阻断**；本轮任一失败则对本轮已成功执行的全部（跨 serviceCode/版本）按逆序回滚 | 用户 2026-08-25 |

## 确认记录

- [x] 需求卡片已与用户对齐，可进入任务拆分  
- 确认备注：开放问题 1–7 已全部确认；可编码。
