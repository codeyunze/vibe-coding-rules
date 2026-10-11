# 任务拆分 TASK_BREAKDOWN

> 复制到 `.cursor/harness/runs/{yyyyMMdd-slug}/TASK_BREAKDOWN.md` 后填写。  
> **开发进度只更新本文件勾选，不靠聊天列表记忆。**

## 依赖顺序（强制）

建议顺序：`DDL → 后端 dao/core/startup → 网关/配置 → 前端 api/views/router → Java 单测 + Python API 脚本 → Review`

## 任务清单

### A. 数据

- [ ] A1 DDL 编写并落到约定路径
- [ ] A2 （可选）本地/环境执行 DDL；只读库则记录「待 DBA」

### B. 后端（yz-mall）

- [ ] B1 Entity / Mapper / DTO / VO（`*-dao`）
- [ ] B2 Service / Impl（`*-core`）
- [ ] B3 Controller / 权限注解（`*-startup`）
- [ ] B4 （可选）Extend / Feign
- [ ] B5 配置项 / 环境变量占位（禁止硬编码密钥）
- [ ] B6 网关或 Nacos 路由样例（若 path 可能冲突）

### C. 前端（yz-mall-web-admin-pc）

- [ ] C1 `api/*.ts` 路径与类型
- [ ] C2 页面 `views/...` + hook
- [ ] C3 路由（独立父 path，避免抢动态菜单前缀）
- [ ] C4 eslint / prettier / vue-tsc 无新增报错

### D. 测试（模块内小文件）

- [ ] D1 后端 Service：对应模块 `src/test/java/...` 可单跑 JUnit 小测试
- [ ] D2 后端 Controller API：**Python** 脚本落到 `*-startup/src/test/python/...`；**每个关键接口须有正例 `*_ok.py` + 反例 `*_ng_*.py`**（可单跑；供定时任务平台每日验证）
- [ ] D3 前端：（若需要）功能目录 `tests/` 手测说明或小 spec
- [ ] D4 本机执行 D1/D2（含正例与反例）并记录到 ACCEPTANCE；D2 注明是否已上传定时平台（或待上传）

### E. 检查与收尾

- [ ] E1 跑 `review-java-change`（或等价审查）并回写 ACCEPTANCE
- [ ] E2 更新设计文档勾选（若文档有交付清单）
- [ ] E3 （仅用户明确要求时）commit；禁止擅自 push

## 任务明细（可增行）

| ID | 描述 | 仓库 | 路径/模块 | 依赖 | 状态 |
|----|------|------|-----------|------|------|
| A1 | | yz-mall | | - | todo |
| B1 | | yz-mall | | A1 | todo |
| C1 | | yz-mall-web-admin-pc | | B3 | todo |

状态取值：`todo` / `doing` / `done` / `blocked` / `deferred`

## 阻塞项

| ID | 原因 | 需要谁 | 状态 |
|----|------|--------|------|
| | | | |

## 确认记录

- [ ] 任务拆分已与用户对齐，可开始编码  
- 确认备注：
