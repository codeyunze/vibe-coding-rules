# 需求卡片 FEATURE_CARD

> 落盘：`.cursor/harness/runs/20260926-tw-access/FEATURE_CARD.md`

## 元信息

| 项 | 内容 |
|----|------|
| 功能短名（slug） | `tw-access` |
| 创建日期 | 2026-09-26 |
| 设计文档路径 | `yz-mall/docs/prepare/功能模块规划.md` §3.3；遥测设计中的 access 边界 |
| 后端仓库/模块 | `yz-mall` / `mall-tw-access`（独立进程，端口 5006） |
| 前端仓库 | 无 |
| 负责人确认 | ☑ 用户要求「实现 tw-access 模块」 |

## 1. 目标（做什么）

- G1：EMQX HTTP Auth / ACL（本 VIN Topic 命名空间）
- G2：Webhook 上下线 → Redis `tw:online:{vin}`
- G3：上行 GPS Rule HTTP → Kafka `tw-telemetry-raw`
- G4：下行 MQTT 发布代理（EMQX HTTP API）
- G5：开发旁路鉴权，便于无终端表联调

## 2. 非目标（明确不做）

- 轨迹/最新位置消费（mall-tw）
- RocketMQ 在线事件、ACK→MQ（本轮延后）
- 踢连接 / 凭证缓存失效（终端重置联调延后）
- 管理端页面

## 3. 角色与权限

| 角色 | 能力 | 权限码（拟定） |
|------|------|----------------|
| EMQX | `/emqx/**` 免登录 | — |
| 内部服务 | 下行发布 | `api:tw:access:publish`（代码内注释，可开） |

## 4. 数据与表

本模块无新表；读写 Redis 在线键。

## 5. 后端接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/emqx/auth` | CONNECT 鉴权 |
| POST | `/emqx/acl` | Topic ACL |
| POST | `/emqx/webhook` | 上下线 |
| POST | `/emqx/bridge/gps` | GPS→Kafka |
| POST | `/tw/access/mqtt/publish` | 下行发布 |

## 6. 前端页面

无。

## 7. 跨服务 / 消息 / 缓存

- 调 mall-tw：`/extend/tw/device/verify`、`.../bound-vin`
- 生产 Kafka：`tw-telemetry-raw`
- Redis：`tw:online:{vin}`
- Topic：`tsp/{vin}/up/gps`、`tsp/{vin}/down/cmd`

## 8. 验收要点（摘要）

见 `ACCEPTANCE.md`。

## 9. 开放问题

| # | 问题 | 结论 |
|---|------|------|
| 1 | 端口 | 5006（与 mall-tw 5005 相邻） |
| 2 | RocketMQ 上下线事件 | 本轮不做 |
| 3 | 正式鉴权 | `dev-bypass=false` + mall-tw 设备表 |

## 确认记录

- [x] 模块骨架与核心接口已实现
