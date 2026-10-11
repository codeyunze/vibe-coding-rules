# yz-mall 功能开发 Harness

本目录是 **Agent 开发流水线的落盘约定**，解决「只靠 Chat 记忆会丢上下文」的问题。

## 原则（必须遵守）

1. **卡片 / 任务清单 / 验收清单必须落盘**，不得只写在对话里  
2. 未落盘、未获用户确认，不得进入下一阶段写业务代码  
3. 测试按模块拆小文件（`src/test` 与 `src/main` 同级）：Service 用 Java 单测；**Controller API 用 Python 脚本**（可上传定时任务平台每日验证）  
4. **API 脚本必须同时覆盖正例与反例**（`*_ok.py` / `*_ng_*.py`）  
5. **业务响应码以字典 `RESPONSE-CODE` 为活数据源**（会持续增加），Harness 不维护全量码表副本；见 `RESPONSE_CODE.md`  
6. 不做大型测试中台；需要时再单跑或按清单聚合  

## 目录结构

```text
.cursor/harness/
├── README.md                 # 本说明
├── PIPELINE.md               # 阶段顺序与门控
├── FEATURE_CARD.md           # 需求卡片模板
├── TASK_BREAKDOWN.md         # 任务拆分模板
├── ACCEPTANCE.md             # 验收清单模板
├── TEST_CONVENTION.md        # 模块级小测试约定
├── RESPONSE_CODE.md          # 响应码断言口径（业务码以字典为准，持续增长）
└── runs/                     # 每次功能开发的实际落盘区（按功能一份）
    └── .gitkeep
```

## 一次功能开发怎么落盘

在 `runs/` 下新建目录（建议命名：`yyyyMMdd-短横线slug`）：

```text
.cursor/harness/runs/20260820-sys-open-client/
├── FEATURE_CARD.md      # 从模板复制后填写
├── TASK_BREAKDOWN.md
├── ACCEPTANCE.md
└── NOTES.md             # 可选：联调备注、阻塞项
```

入口 Skill：`.cursor/skills/yz-mall-feature-pipeline/SKILL.md`  
触发词示例：「按某某设计文档走功能管道」「开一条 feature harness」「需求确认并落盘」
