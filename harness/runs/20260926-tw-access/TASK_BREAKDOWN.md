# 任务拆分 TASK_BREAKDOWN

> 落盘：`.cursor/harness/runs/20260926-tw-access/TASK_BREAKDOWN.md`

## 状态总览

| 区 | 状态 |
|----|------|
| A 模块骨架 | ✅ |
| B EMQX 回调 | ✅ |
| C Kafka/下行 | ✅ |
| D 测试 | ✅ 部分 |
| E 文档/网关 | ✅ |

## A. 模块骨架

- [x] A1 父 POM 增加 `mall-tw-access`
- [x] A2 `pom.xml` / Application / Properties / Config
- [x] A3 `application.yaml` / `bootstrap.yaml` / logback

## B. EMQX

- [x] B1 Auth + MallTwDeviceClient（含 dev-bypass）
- [x] B2 ACL + DeviceSessionCache
- [x] B3 Webhook → Redis online
- [x] B4 Sa-Token 放行 `/emqx/**`

## C. 桥接与下行

- [x] C1 GPS bridge → Kafka
- [x] C2 MQTT publish API（EMQX API Key）

## D. 测试

- [x] D1 JUnit：`EmqxAuthServiceAclTest`
- [x] D2 Python：`test_emqx_auth_ok.py` / `test_emqx_auth_ng_empty.py`
- [x] D3 Python：`test_bridge_gps_ok.py`

## E. 文档

- [x] E1 README
- [x] E2 `docs/nacos/gateway-tw-access-route.yaml`
- [x] E3 `docs/nacos/mall-tw-access-emqx.md`
