# 功能管道 PIPELINE

## 阶段与门控

| 阶段 | 名称 | 落盘产物 | 进入下一阶段的门控 |
|------|------|----------|-------------------|
| 1 | 需求确认与梳理 | `FEATURE_CARD.md` | 用户确认卡片内容 |
| 2 | 任务拆分 | `TASK_BREAKDOWN.md` | 用户确认任务清单与顺序 |
| 3 | 代码开发 | 代码 + 勾选任务项 | 任务项完成或明确延期 |
| 4 | 测试验证 | Java `src/test/java` + **Python API 脚本** `src/test/python` + ACCEPTANCE | L1/L2 通过或记录豁免；Python 脚本具备上传定时平台条件 |
| 5 | 问题修复 | 更新 NOTES + 重跑失败测试 | 失败项清零或豁免说明 |
| 6 | 代码检查 | Review 结论写入 `ACCEPTANCE.md` | 「必须修改」为空；用户认可 |

```text
需求确认 → 任务拆分 → 代码开发 → 测试验证 ⇄ 问题修复 → 代码检查 → 交付
                ↑_______________|（未确认不得跳阶段）
```

## 禁止事项

- 禁止未创建 `runs/{feature}/` 目录就开始大范围改码  
- 禁止用对话摘要代替 `FEATURE_CARD` / `TASK_BREAKDOWN` / `ACCEPTANCE`  
- 禁止未获用户明确要求时 `git commit` / `git push`  
- 禁止把测试堆进单一巨型测试工程；按模块小文件放置（见 `TEST_CONVENTION.md`）  
- **Controller HTTP API 的定时验证脚本必须用 Python**，并考虑上传定时任务平台每日执行  
- **Python API 脚本必须同时有正例与反例**，禁止只写成功路径  

## 编排时复用的现有能力

| 阶段 | Skills / Rules |
|------|----------------|
| 建表 | `design-mysql-table`、`mysql-schema` |
| 后端 CRUD | `scaffold-java-crud`、`java-api-layer` |
| 前端 | `frontend-vue-template`、`frontend-ts-api-format` |
| 审查 | `review-java-change`、`change-discipline` |
| 常驻 | `yz-mall-overview`、`git-no-push`、`agent-communication` |

## Agent 每阶段结束动作

1. 更新对应落盘文件中的勾选状态  
2. 用简短中文向用户汇报本阶段结论  
3. **询问是否进入下一阶段**（阶段 1、2、6 必须等人确认）
