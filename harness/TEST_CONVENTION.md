# 模块级小测试约定 TEST_CONVENTION

> **不做大型测试中台。** 测试按模块拆成小文件，放在与 `main` 同级的 `test` 目录，可独立运行，需要时再聚合。

## 分层分工（重要）

| 层级 | 技术 | 落盘 | 用途 |
|------|------|------|------|
| Service / 领域逻辑 | Java + JUnit5（可 Mockito） | `{module}/src/test/java/...` | 本地/CI 单测 |
| **Controller API 接口** | **Python 脚本** | `{startup模块}/src/test/python/...` | **本地冒烟 + 上传定时任务平台每日验证** |
| 前端 | 手测 README / 日后 vitest | 功能目录 `tests/` | 页面与纯逻辑 |

**硬性约定：Controller 层对外 HTTP API 的自动化验证脚本必须用 Python**，不得用 Java/`RestAssured` 等替代「可上传定时平台」的那一份。

---

## 1. 后端 Service 单测（Java）

### 落盘位置

```text
{module}/
├── src/main/java/...
└── src/test/java/...     ← 与 main 同级
    └── com/yz/mall/{域}/...
        ├── XxxServiceSaveTest.java
        └── XxxServicePageTest.java
```

参考：`mall-sys-core/src/test/java/com/yz/mall/sys/service/SysDictionaryServiceTest.java`

> Controller 的 HTTP 契约验证走第 2 节 Python，**不要**再写 Java `XxxControllerSmokeTest` 充当定时平台脚本。

### 编写原则

| 原则 | 说明 |
|------|------|
| 小而独立 | 单个类聚焦一个聚合行为 |
| 可单跑 | 优先 Mockito，弱依赖全套中间件 |
| 命名 | `{被测类}{场景}Test` |
| 展示名 | `@DisplayName("中文场景")` |

### 单跑 / 聚合跑

```bash
mvn -pl mall-admin/mall-sys-core -Dtest=SysOpenClientServiceSaveTest test
mvn -pl mall-admin/mall-sys-core -am test
```

---

## 2. Controller API 接口测试（Python，定时平台）

### 为何用 Python

脚本需**上传到定时任务平台**，按天定时对线上/预发环境做接口验证。Python 脚本体积小、依赖少、平台易调度，与模块内 Java 单测职责分离。

### 落盘位置

放在提供该 Controller 的 **startup 模块** 下，与 `main` 同级：

```text
{域}-startup/
├── src/main/java/.../controller/XxxController.java
└── src/test/
    ├── java/...                    # （可选）其它 Java 测试
    └── python/
        ├── README.md               # 本模块 API 脚本说明、定时平台上传注意
        ├── requirements.txt        # 仅列脚本依赖（如 requests）
        └── {资源或控制器短名}/
            ├── test_page_ok.py           # 正例：合法请求应成功
            ├── test_page_ng_no_token.py  # 反例：缺鉴权应被拒绝
            ├── test_page_ng_bad_param.py # 反例：非法参数应业务失败
            ├── test_add_ok.py
            ├── test_add_ng_*.py
            └── _common.py                # 可选：读环境变量、鉴权头、断言封装
```

示例（开放客户端）：

```text
mall-sys-startup/src/test/python/sys_open_client/
  test_page_ok.py
  test_page_ng_no_token.py
  test_get_detail_ok.py
  test_get_detail_ng_not_found.py
  test_server_public_key_ok.py
  _common.py
```

### 正例与反例（硬性）

每个对外 HTTP 接口（或 FEATURE_CARD 中的每个关键 API 验收点）**至少**各有：

| 类型 | 命名建议 | 脚本 `PASS` 含义 |
|------|----------|------------------|
| **正例** | `test_{动作}_ok.py` | 合法请求得到预期成功（通常 HTTP 200 且业务 `code==200`，关键字段存在） |
| **反例** | `test_{动作}_ng_{原因}.py` | 非法/越权/缺参等请求被**正确拒绝**（得到约定的业务/框架错误码），而不是误成功 |

### 响应码口径（业务码会持续增加）

详见 **`RESPONSE_CODE.md`**。摘要：

| 断言对象 | 真相源 | 说明 |
|----------|--------|------|
| 成功 | `CodeEnum.SUCCESS` → `200` | 正例 |
| 鉴权/通用框架错误 | `CodeEnum`（如 `50000`） | 相对稳定，可写死在脚本 |
| **业务域错误** | `sys_dictionary` 中 `RESPONSE-CODE`（`ancestor_id=1995060920724340736`）的 `dictionary_key` | **持续增长**；脚本只引用当次期望码，Harness **禁止**抄一份全量码表 |

反例常见覆盖（按接口选，不必每个都写全）：

- 无 Token / 无效 Token（框架码 `50000`/`50001` 等）  
- 缺必填参数、类型错误（框架 `30001` 或业务字典码，以卡片为准）  
- 无权限、不存在的 id（框架码或业务字典码）  
- 写接口重复/非法状态（优先业务字典码）  

约定：

1. **一小文件一场景**（正例、反例分开文件），便于定时平台按文件调度与失败定位  
2. 反例脚本退出码语义与正例相同：`0` = 断言符合预期（含「应失败且已失败」），非 `0` = 未按预期拒绝或环境异常  
3. 文件头注释标明：接口路径、正/反例、对应验收 Gx/Tx、**期望 code**（框架枚举值或字典 `dictionary_key`）  
4. 禁止只写正例就勾选 ACCEPTANCE L2-b 完成  
5. 新业务错误码：先入 `RESPONSE-CODE` 字典，再写反例脚本  

### 编写原则（面向定时平台）

| 原则 | 说明 |
|------|------|
| 一小文件一场景 | 正例、反例各一文件；便于平台配置与失败定位 |
| 可独立执行 | `python test_xxx_ok.py` 即可；退出码 `0` 成功，非 `0` 失败 |
| **单文件自包含** | **禁止**依赖同目录其它 `.py`（如 `_common`）或额外配置文件；环境变量注入即可跑 |
| 配置全走环境变量 | `BASE_URL`、`TOKEN`（或平台注入的鉴权）；**禁止**脚本内写死密钥/账号密码 |
| 依赖最小化 | 默认 `requests`；`requirements.txt` 写清版本范围 |
| 输出可读 | print 关键断言结果；失败时打印 status/body 摘要（勿打全量敏感信息） |
| 幂等友好 | 定时任务每日跑；写操作正例注意清理或可重复数据策略，并在 README 注明 |
| 不进巨型中台仓 | 脚本跟 startup 模块走，上传平台时按文件挑选 |

### 推荐脚本骨架

正例见 `.cursor/harness/examples/api_test_script_template.py`；反例见同目录 `api_test_script_ng_template.py`。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API: POST /sys/open/client/page — 正例 — 对应验收 Gx/Tx"""
import os
import sys
import requests

BASE_URL = os.environ["BASE_URL"].rstrip("/")
TOKEN = os.environ.get("TOKEN", "")

def main() -> int:
    url = f"{BASE_URL}/sys/open/client/page"
    headers = {"Authorization": TOKEN} if TOKEN else {}
    resp = requests.post(url, json={"current": 1, "size": 10, "filter": {}}, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"FAIL status={resp.status_code} body={resp.text[:500]}")
        return 1
    data = resp.json()
    if data.get("code") != 200:
        print(f"FAIL business code={data.get('code')} msg={data.get('msg')}")
        return 1
    print("PASS ok")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

反例（期望未授权被拒绝；若意外成功则 FAIL）：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""API: POST /sys/open/client/page — 反例(无Token) — 对应验收 Gx/Tx"""
import os
import sys
import requests

BASE_URL = os.environ["BASE_URL"].rstrip("/")

def main() -> int:
    url = f"{BASE_URL}/sys/open/client/page"
    resp = requests.post(url, json={"current": 1, "size": 10, "filter": {}}, headers={}, timeout=30)
    # 期望业务码：写死本次场景的字典 dictionary_key（业务码持续增长，勿在 Harness 抄全表）
    # 期望框架码：可用 CodeEnum，如 50000 未登录
    expect_code = int(os.environ.get("EXPECT_CODE", "50000"))
    try:
        data = resp.json()
    except Exception:
        data = {}
    code = data.get("code")
    if code == expect_code:
        print(f"PASS ng: rejected bizCode={code} msg={data.get('msg')}")
        return 0
    if resp.status_code in (401, 403) and expect_code in (50000, 50001, 50002, 50003):
        print(f"PASS ng: rejected http={resp.status_code} (auth)")
        return 0

    print(f"FAIL ng: expected code={expect_code}, got http={resp.status_code} body={resp.text[:500]}")
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

### 本地单跑

```bash
cd yz-mall/mall-admin/mall-sys-startup/src/test/python
pip install -r requirements.txt
export BASE_URL=https://your-env.example
export TOKEN='Bearer xxx'
python sys_open_client/test_page_ok.py
# 鉴权反例（框架码）
EXPECT_CODE=50000 python sys_open_client/test_page_ng_no_token.py
# 业务反例（字典 dictionary_key，随 RESPONSE-CODE 持续增加）
# EXPECT_CODE=20002 TOKEN='Bearer xxx' python sys_open_client/test_add_ng_dup_key.py
```

### 上传定时任务平台

1. 以**单个 `.py` 文件**（及如需的 `_common.py`）为上传单元；**正例与反例分别建任务或同组挂多个文件**  
2. 在平台配置同样的环境变量：`BASE_URL`、`TOKEN` 等（反例脚本通常不依赖有效 TOKEN，仍可注入以免平台缺省报错）  
3. 启动命令示例：`python test_page_ok.py` / `python test_page_ng_no_token.py`  
4. 在模块 `src/test/python/README.md` 与功能 `ACCEPTANCE.md` 记录：**脚本路径、正/反例类型、平台任务名、调度周期（每日）**  

聚合：需要时在平台建「任务组」挂多个小脚本，或本地用 shell 循环调用多个文件——**仍不是测试中台工程**。

### 与 Harness 的关系

- `TASK_BREAKDOWN` D 区：分别列出 Java 单测类名 + **Python 正例/反例脚本相对路径**  
- `ACCEPTANCE` L2-b：每行标注 `ok` / `ng`；Python 表增加「是否已上传定时平台」勾选；缺反例不得标 L2-b 完成  

---

## 3. 前端（yz-mall-web-admin-pc）

```text
src/views/{模块}/{feature}/tests/
  README.md           # 手测步骤
  xxx.spec.ts         # 引入 vitest 后再加
```

L1 仍以 eslint / vue-tsc 为主。

---

## 4. 跨模块清单（可选）

`runs/{feature}/SMOKE.md` 只罗列要跑的项，例如：

```text
java:mall-sys-core:SysOpenClientServiceSaveTest
python:mall-sys-startup/src/test/python/sys_open_client/test_page_ok.py
python:mall-sys-startup/src/test/python/sys_open_client/test_page_ng_no_token.py
python:mall-sys-startup/src/test/python/sys_open_client/test_get_detail_ok.py
python:mall-sys-startup/src/test/python/sys_open_client/test_get_detail_ng_not_found.py
```

---

## 5. Agent 生成测试时的检查清单

- [ ] Service 单测在模块 `src/test/java`  
- [ ] **Controller API 验证为 Python**，落在对应 `*-startup/src/test/python/`  
- [ ] **每个关键接口同时有正例（`*_ok.py`）与反例（`*_ng_*.py`）**  
- [ ] **业务反例期望码来自字典 `dictionary_key` 或卡片已写明码；未在 Harness 维护全量码表**  
- [ ] 反例的 PASS =「按预期被拒绝」，不是误当成成功  
- [ ] Python 脚本可 `python xxx.py` 单跑，退出码语义正确  
- [ ] 鉴权与地址仅环境变量；无密钥入库  
- [ ] ACCEPTANCE 写明单跑命令与 ok/ng 类型；定时平台上传项已列出（或标「待上传」）  
- [ ] 与 FEATURE_CARD 的 Gx/Tx 可追溯（文件头注释）
