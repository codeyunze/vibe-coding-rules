# 验收清单 ACCEPTANCE

> 复制到 `.cursor/harness/runs/{yyyyMMdd-slug}/ACCEPTANCE.md` 后填写。  
> **功能是否「完成」以本文件为准；对话中的「好了」不能替代勾选。**

## 功能验收（对照 FEATURE_CARD 目标）

| ID | 验收项 | 结果 | 证据（路径/命令/截图说明） |
|----|--------|------|----------------------------|
| G1 | | ☐ pass / ☐ fail / ☐ n/a | |
| G2 | | ☐ pass / ☐ fail / ☐ n/a | |

## 静态检查 L1

| 项 | 命令或操作 | 结果 |
|----|------------|------|
| 后端编译（相关模块） | `mvn -pl … -am -DskipTests compile` | ☐ |
| 前端 eslint（改动文件） | `npx eslint …` | ☐ |
| 前端 vue-tsc（若改 TS/Vue） | `npx vue-tsc --noEmit` | ☐ |

## 模块小测试 L2

### L2-a Java（Service 等）

| 测试类（模块 src/test/java） | 单跑命令 | 结果 |
|------------------------------|----------|------|
| | `mvn -pl … -Dtest=… test` | ☐ |

### L2-b Python（Controller API，定时平台）

> **硬性**：每个关键接口须同时有正例（`ok`）与反例（`ng`）；缺反例不得将本表标为完成。

| 脚本路径（*-startup/src/test/python） | 类型 | 单跑命令 | 本地结果 | 已上传定时平台 | 平台任务名/周期 |
|----------------------------------------|------|----------|----------|----------------|-----------------|
| | ok / ng | `BASE_URL=… TOKEN=… python …/test_xxx_ok.py` | ☐ | ☐ 是 / ☐ 待上传 | 每日 |
| | ok / ng | `BASE_URL=… python …/test_xxx_ng_….py` | ☐ | ☐ 是 / ☐ 待上传 | 每日 |

```text
# Java 示例
mvn -pl mall-admin/mall-sys-core -Dtest=SysOpenClientServiceSaveTest test

# Python API 示例（正例 + 反例；环境变量由本地或定时平台注入）
cd mall-admin/mall-sys-startup/src/test/python
pip install -r requirements.txt
BASE_URL=https://env.example TOKEN='Bearer xxx' python sys_open_client/test_page_ok.py
BASE_URL=https://env.example python sys_open_client/test_page_ng_no_token.py
```

## 场景验收 L3（摘自设计文档用例）

| 用例 ID | 场景 | 期望 | 结果 |
|---------|------|------|------|
| T1 | | | ☐ |
| T2 | | | ☐ |

## 代码检查（Review）

| 项 | 结果 |
|----|------|
| review-java-change / 人工或 Agent 审查 | ☐ 通过 / ☐ 有条件通过 / ☐ 不通过 |
| 「必须修改」是否已清零 | ☐ |
| 前端路由是否与动态菜单冲突 | ☐ |
| 权限码、密钥、SQL 安全项 | ☐ |

审查摘要（可贴要点，详细可另开 NOTES.md）：

```text

```

## 残留风险与豁免

| 项 | 原因 | 是否接受 |
|----|------|----------|
| | | ☐ |

## 最终确认

- [ ] 验收清单已更新，可视为本功能开发闭环完成（不含未授权的 push）  
- 确认人 / 日期：
