# 验收对照 VERIFY — §9 T1～T9（后端）

> 落盘：`.cursor/harness/runs/20260922-tw-telemetry/VERIFY_T1_T9.md`  
> Python 脚本均在 `yz-mall/mall-tw/src/test/python/tw_telemetry/`，**单文件独立运行**。  
> 默认 `BASE_URL=http://127.0.0.1:5005`；网关则改端口。

## 环境变量

```text
BASE_URL   服务根地址（必填）
TOKEN      Authorization 完整值，如 Bearer xxx（需鉴权的接口）
TW_TEST_VIN  测试 VIN
```

## T1～T9 映射

| 编号 | 场景 | 怎么验 | 期望 |
|------|------|--------|------|
| T1 | 持续上报 | Kafka 投 `tw-telemetry-raw`，或 `python test_raw_ingest_ok.py` 多次 | Redis + MySQL latest 更新；CH 开时有明细（需 flush/等定时刷盘） |
| T2 | 查最新位置 | `python test_latest_ok.py` 或下方 curl latest | 与最后上报一致 |
| T3 | Redis miss 回源 | 删 `tw:gps:latest:{vin}` 后再 GET latest | 回源 MySQL 并回填 Redis |
| T4 | 轨迹时间窗 | `python test_track_ok.py`（先灌点） | `points` 按时间升序；可空 |
| T5 | 超大时间窗 | `python test_track_ng_window.py` | 业务拒绝 `code=1` |
| T6 | 授权无 scope2 | 用「仅查看、无位置」授权账号调 latest/track | `无权查看该车辆位置`（`code=1`）；运营账号跳过 |
| T7 | 非法 lat/lng | `python test_raw_ingest_ng_bad_coord.py` | 不写三端；业务拒绝 |
| T8 | 批量监控 | `python test_batch_ok.py`；超限 `test_batch_ng_over_limit.py` | ≤200 成功；>200 拒绝 |
| T9 | CH 不可用 | `clickhouse.enabled=false` 或停 CH 后 `raw/ingest` | latest 仍成功；轨迹 API 提示未启用或查空 |

## curl 速查（Git Bash / 单引号）

### 模拟上报（T1 / 对齐 Kafka Value）

```bash
curl -X POST "$BASE_URL/tw/telemetry/dev/raw/ingest" \
  -H "Content-Type: application/json" \
  -H "Authorization: $TOKEN" \
  -d '{"vin":"TESTVIN001","lng":116.397128,"lat":39.916527,"speed":36.5,"heading":90.0,"gpsTime":"2026-09-25T10:00:01.000+08:00","soc":78.5,"signalLevel":4}'
```

### 最新位置（T2）

```bash
curl -G "$BASE_URL/tw/telemetry/latest" \
  -H "Authorization: $TOKEN" \
  --data-urlencode "vin=TESTVIN001"
```

### 批量（T8）

```bash
curl -X POST "$BASE_URL/tw/telemetry/latest/batch" \
  -H "Content-Type: application/json" \
  -H "Authorization: $TOKEN" \
  -d '{"vins":["TESTVIN001"]}'
```

### 轨迹（T4）

```bash
curl -X POST "$BASE_URL/tw/telemetry/track" \
  -H "Content-Type: application/json" \
  -H "Authorization: $TOKEN" \
  -d '{"vin":"TESTVIN001","startTime":"2026-09-25 00:00:00","endTime":"2026-09-25 23:59:59","maxPoints":2000}'
```

### 超时间窗（T5）

```bash
curl -X POST "$BASE_URL/tw/telemetry/track" \
  -H "Content-Type: application/json" \
  -H "Authorization: $TOKEN" \
  -d '{"vin":"TESTVIN001","startTime":"2026-09-01 00:00:00","endTime":"2026-09-03 00:00:01"}'
```

### Extend 最新位置

```bash
curl -G "$BASE_URL/extend/tw/telemetry/latest/TESTVIN001" \
  -H "Authorization: $TOKEN"
```

### 非法坐标（T7）

```bash
curl -X POST "$BASE_URL/tw/telemetry/dev/raw/ingest" \
  -H "Content-Type: application/json" \
  -H "Authorization: $TOKEN" \
  -d '{"vin":"TESTVIN001","lng":200,"lat":39.9,"gpsTime":"2026-09-25 10:00:00"}'
```

## 仓库脚本一览

| 脚本 | 对应 |
|------|------|
| `test_raw_ingest_ok.py` | T1 |
| `test_raw_ingest_ng_bad_coord.py` | T7 |
| `test_latest_ok.py` | T2 |
| `test_latest_ng_no_token.py` / `test_latest_ng_missing_param.py` | 鉴权/参数 |
| `test_batch_ok.py` / `test_batch_ng_over_limit.py` / `test_batch_ng_no_token.py` | T8 |
| `test_track_ok.py` / `test_track_ng_window.py` / `test_track_ng_no_token.py` | T4 / T5 |
| `test_extend_latest_ok.py` | Extend |

T3 / T6 / T9 以手工 + curl 为主（依赖 Redis/账号/CH 开关）。
