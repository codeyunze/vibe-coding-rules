---
name: yz-mall-feature-pipeline
description: >-
  yz-mall 与 yz-mall-web-admin-pc 功能开发流水线（Harness）。
  强制将需求卡片、任务清单、验收清单落盘到 .cursor/harness/runs/；
  Service 用模块 src/test/java 小单测；Controller API 用 Python 脚本
  （可上传定时任务平台每日验证）。
  在用户要求按设计文档开发功能、走功能管道、开 feature harness、
  需求确认落盘、任务拆分落盘、或端到端交付某模块时使用。
---

# yz-mall 功能开发管道

## 何时使用

- 「按 `docs/prepare/功能模块设计-xxx.md` 开发」
- 「开一条 feature harness / 功能管道」
- 「先需求确认并落盘，再拆任务」
- 需要同时改 `yz-mall` + `yz-mall-web-admin-pc` 并闭环验收

## 硬性规则（用户明确要求，必须遵守）

1. **不要只靠 Chat 记忆**——需求卡片、任务清单、验收清单必须落盘  
2. 落盘根目录：`.cursor/harness/runs/{yyyyMMdd-slug}/`  
3. 模板来源：`.cursor/harness/FEATURE_CARD.md`、`TASK_BREAKDOWN.md`、`ACCEPTANCE.md`  
4. 阶段顺序与门控：读 `.cursor/harness/PIPELINE.md`  
5. 测试约定：读 `.cursor/harness/TEST_CONVENTION.md`  
   - Service：各模块 **`src/test/java`**，JUnit 小文件，可 `mvn -Dtest=类名`  
   - **Controller API：必须用 Python**，落在 **`*-startup/src/test/python/`**，可 `python xxx.py` 单跑  
   - **每个关键接口必须同时有正例（`*_ok.py`）与反例（`*_ng_*.py`）**；反例 PASS = 按预期被拒绝  
   - 业务错误码查 `sys_dictionary` 的 `RESPONSE-CODE`（见 `.cursor/harness/RESPONSE_CODE.md`），**禁止**在 Harness 维护全量码表；新码先入字典再写脚本  
   - Python 脚本需可**上传定时任务平台做每日验证**（环境变量注入 BASE_URL/TOKEN，退出码 0/非0）  
   - **不要**搭建大型测试中台  

未创建 runs 目录、未完成阶段 1/2 的用户确认前，**禁止**大范围编写业务代码。

## 启动步骤

### 0. 读取规范

1. `.cursor/harness/README.md`、`PIPELINE.md`、`TEST_CONVENTION.md`  
2. 相关设计文档（用户给出的路径）  
3. 现有同域实现（对照改，禁止另起风格）  

### 1. 创建本次落盘目录

```text
.cursor/harness/runs/{yyyyMMdd-slug}/
├── FEATURE_CARD.md
├── TASK_BREAKDOWN.md
├── ACCEPTANCE.md
└── NOTES.md          # 可选
```

从 `.cursor/harness/` 复制三份模板后填写，**写文件，不要只在回复里贴一整份代替落盘**。

向用户汇报目录路径，并确认 slug 命名。

### 2. 阶段 1 — 需求确认

- 填写 `FEATURE_CARD.md`（目标/非目标/表/接口/页面/权限/开放问题）  
- 缺信息则提问；开放问题清空或标延期  
- **停下来等用户确认**卡片后再进入阶段 2  

### 3. 阶段 2 — 任务拆分

- 填写 `TASK_BREAKDOWN.md`，按 DDL → BE → FE → 测试 → Review 排序  
- D 区写清：  
  - Java 单测类全名（`src/test/java`）  
  - **Python API 正例与反例脚本相对路径**（`*-startup/src/test/python/.../*_ok.py` 与 `*_ng_*.py`）  
- **停下来等用户确认**任务清单后再编码  

### 4. 阶段 3 — 代码开发

按任务项最小改动实现；优先复用：

| 场景 | Skill |
|------|--------|
| 建表 | `design-mysql-table` |
| 后端 CRUD | `scaffold-java-crud` |
| 审查准备 | 对照 `review-java-change` 清单自检 |

前端注意：静态路由勿抢后端动态菜单父 path（如 `/system`）。  
每完成若干任务项，**回写** `TASK_BREAKDOWN.md` 勾选与状态列。

### 5. 阶段 4 — 测试验证

1. Service：模块 `src/test/java/...` 小 JUnit  
2. **Controller：`*-startup/src/test/python/...` 小 Python 脚本**（正例参考 `examples/api_test_script_template.py`，反例参考 `examples/api_test_script_ng_template.py`）  
3. 单跑并写入 `ACCEPTANCE.md` L2-a / L2-b（L2-b 每行标注 ok/ng）；缺反例不得勾完成；勾选「是否已上传定时平台」或标「待上传」  
4. 勾选 L1、L3  

```bash
# Java
mvn -pl mall-admin/mall-sys-core -Dtest=YourSmallTest test

# Python API（正例 + 反例）
cd mall-admin/mall-sys-startup/src/test/python
BASE_URL=... TOKEN='Bearer ...' python your_api/test_page_ok.py
BASE_URL=... python your_api/test_page_ng_no_token.py
```

### 6. 阶段 5 — 问题修复

失败则最小修复 → 重跑失败项（含对应 Python 脚本）→ 更新 ACCEPTANCE；禁止无关重构。

### 7. 阶段 6 — 代码检查

1. 使用 `review-java-change`（Java/SQL）并对前端做路由/权限/格式检查  
2. 确认 Python API 脚本无硬编码密钥、可独立上传平台  
3. 结论写入 `ACCEPTANCE.md`；「必须修改」清零后请用户最终确认  

默认 **不** commit / push；仅当用户明确要求时再提交。

## 回复风格

- 使用简体中文  
- 每阶段结束：说明落盘路径 + 本阶段结论 + 是否等待确认  
- 引用代码用 `startLine:endLine:path`  

## 检查清单（Agent 自检）

- [ ] `runs/{slug}/` 下三份核心 md 已存在且内容非空模板  
- [ ] 阶段 1、2、6 有用户确认迹象再继续  
- [ ] Service 测在 `src/test/java`；Controller API 测为 Python 且在 `src/test/python`  
- [ ] 每个关键 API 同时有 `*_ok.py` 与 `*_ng_*.py`  
- [ ] ACCEPTANCE L2-b 含 ok/ng 类型与定时平台上传状态  
- [ ] ACCEPTANCE 能回答「怎样算做完」
