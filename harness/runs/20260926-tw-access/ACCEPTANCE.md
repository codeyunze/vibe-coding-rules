# 验收清单 ACCEPTANCE

> 落盘：`.cursor/harness/runs/20260926-tw-access/ACCEPTANCE.md`

## L1 构建与配置

- [x] 父 POM 包含 `mall-tw-access`
- [x] 本地配置端口 5006、Topic `tw-telemetry-raw`
- [ ] 真机 `mvn -pl mall-tw-access -am package`（本机可能无 mvn）

## L2-a Service 单测

| 类 | 结果 |
|----|------|
| `com.yz.mall.tw.access.service.EmqxAuthServiceAclTest` | 待本机 mvn |

## L2-b Python API

| 脚本 | 类型 | 说明 |
|------|------|------|
| `mall-tw-access/src/test/python/tw_access/test_emqx_auth_ok.py` | ok | Auth allow（需服务 + dev-bypass） |
| `mall-tw-access/src/test/python/tw_access/test_emqx_auth_ng_empty.py` | ng | 空密码 deny |
| `mall-tw-access/src/test/python/tw_access/test_bridge_gps_ok.py` | ok | GPS 桥接返回 sent |

环境：`BASE_URL=http://127.0.0.1:5006`；定时平台：待上传。

## L3 联调（可选）

- [ ] EMQX Cloud 配 Auth/ACL/Webhook/Rule
- [ ] MQTT 发 GPS → mall-tw latest 有点

## Review

- 最小职责清晰；RocketMQ/踢线延后合理
- 密钥走环境变量
