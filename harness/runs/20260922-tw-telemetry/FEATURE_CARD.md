# 需求卡片 FEATURE_CARD

> 落盘：`.cursor/harness/runs/20260922-tw-telemetry/FEATURE_CARD.md`

## 元信息

| 项 | 内容 |
|----|------|
| 功能短名（slug） | `tw-telemetry` |
| 创建日期 | 2026-09-22 |
| 设计文档路径 | `yz-mall/docs/prepare/功能模块设计-遥测与轨迹.md` |
| 后端仓库/模块 | `yz-mall` / `mall-tw`（合入，不独立服务） |
| 前端仓库 | `yz-mall-web-admin-pc`（本轮不做页面） |
| 负责人确认 | ☑ 实现节点已写入设计文档 §12，用户要求从节点 0 开始 |

## 1. 目标（做什么）

- G1：消费 Kafka `tw-telemetry-raw`，解析校验 GPS
- G2：Redis + MySQL `tw_gps_latest` 最新位置
- G3：ClickHouse `tw_gps_track` 批量轨迹
- G4～G6：latest / batch / track API + 折线
- G7：非法坐标轻量去噪
- 按 §12 节点 0～5 增量交付

## 2. 非目标（明确不做）

- tw-access / EMQX / Kafka 生产
- 管理端地图页（前端另开）
- MySQL 轨迹分表、围栏、在线状态写入
- 独立进程 `tw-telemetry`

## 3. 角色与权限

| 角色 | 能力 | 权限码（拟定） |
|------|------|----------------|
| 运营/管理员/监控 | 最新位置、轨迹、批量 | `api:tw:telemetry:latest` / `track` / `latest:batch` |
| 车主/授权用户 | 己车且 scope≥2 | 同上 + access/check |

## 4. 数据与表

| 表名 | 变更类型 | DDL 落盘路径 |
|------|----------|--------------|
| `tw_gps_latest` | 新建 MySQL | `mall-tw/src/main/resources/db/tw_gps_latest.sql` |
| `tw_gps_track` | 新建 ClickHouse | `mall-tw/src/main/resources/db/clickhouse/tw_gps_track.sql` |

## 5. 后端接口

| 方法 | 路径 | 说明 | 权限码 | 正例 | 反例 |
|------|------|------|--------|------|------|
| GET | `/tw/telemetry/latest` | 最新位置 | `api:tw:telemetry:latest` | 200 | 无权 |
| POST | `/tw/telemetry/latest/batch` | 批量最新 | `api:tw:telemetry:latest:batch` | 200 | 超限 |
| POST | `/tw/telemetry/track` | 轨迹 | `api:tw:telemetry:track` | 200 | 时间窗过大 |
| GET | `/extend/tw/telemetry/latest/{vin}` | Extend | — | 200 | — |

网关：`/tw/telemetry/**`、`/extend/tw/telemetry/**` → `lb://mall-tw`

## 6. 前端页面

本轮不做（节点 0～5 仅后端）。

## 7. 跨服务 / 消息 / 缓存

- Kafka Topic `tw-telemetry-raw`，组 `tw-telemetry-gps`
- Redis `tw:gps:latest:{vin}`
- ClickHouse 批量写；配置开关默认关闭，保证无 CH/Kafka 时也能启动

## 8. 验收要点（摘要）

见设计文档 §9 / §12；节点 0～5 仓库侧已完成。验收对照：`VERIFY_T1_T9.md`。

## 9. 开放问题

| # | 问题 | 结论 | 确认人 |
|---|------|------|--------|
| 1 | 是否独立 telemetry 服务 | 合入 mall-tw | 用户 |
| 2 | 节点 4 是否必须真 Kafka | 可用 `dev/raw/ingest`；真 Broker 开 `kafka.enabled` | 设计 §12.3 |

## 确认记录

- [x] 节点 0～5 仓库侧交付（权限文本 + T1～T9 清单 + Harness 收口）
- 遗留：前端地图页；access 上行 Topic 联调；环境侧 CH/Kafka/权限录入
