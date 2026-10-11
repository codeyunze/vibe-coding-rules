# 验收清单 ACCEPTANCE

> 落盘：`.cursor/harness/runs/20260922-tw-telemetry/ACCEPTANCE.md`

## 功能验收（按节点）

| ID | 验收项 | 结果 | 证据 |
|----|--------|------|------|
| N0～N4 | 基建 / Latest / API / Track / Kafka | ☑ 仓库侧 | 设计 §12 + 代码 |
| N5-1 | 权限码文本 | ☑ | `db/tw_telemetry_permissions.txt` |
| N5-2 | T1～T9 对照 + curl | ☑ | `VERIFY_T1_T9.md` |
| N5-3 | Python 正反例独立可跑 | ☑ | `src/test/python/tw_telemetry/test_*.py` |
| N5-4 | §10 后端交付勾选 | ☑ | 设计文档 §10（前端/access 联调除外） |

## 环境联调（人工）

| 项 | 结果 |
|----|------|
| 按 VERIFY 跑通 T1～T9 | ☐ |
| ClickHouse init | ☐ |
| Kafka enabled 真消费 | ☐ |
| mall-sys 录入权限 | ☐ |

## 静态检查 L1

| 项 | 结果 |
|----|------|
| mall-tw 编译 | ☐ 待本地 Maven |

## 回归与收尾

| 项 | 结果 |
|----|------|
| 设计文档 §12 节点 0～5 | ☑ |
| TASK_BREAKDOWN 收口 | ☑ |
| 本轮后端 Harness | **完成** |
