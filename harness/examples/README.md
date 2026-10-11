# Harness 示例说明（非业务可执行代码）

完整可运行测试请落在各业务模块的 `src/test` 下；本目录仅提供约定示例。

## 1. Service 单测（Java）

```text
yz-mall/mall-admin/mall-sys-core/src/test/java/com/yz/mall/sys/service/
  SysOpenClientServiceSaveTest.java
```

```bash
cd yz-mall
mvn -pl mall-admin/mall-sys-core -Dtest=SysOpenClientServiceSaveTest test
```

## 2. Controller API（Python → 定时任务平台）

**每个接口至少：1 个正例 + 1 个反例**（分文件）。

```text
yz-mall/mall-admin/mall-sys-startup/src/test/python/
  requirements.txt
  sys_open_client/
    test_page_ok.py
    test_page_ng_no_token.py
    test_get_detail_ok.py
    test_get_detail_ng_not_found.py
```

骨架模板：

| 类型 | 文件 |
|------|------|
| 正例 | `api_test_script_template.py` → 复制为 `test_{动作}_ok.py` |
| 反例 | `api_test_script_ng_template.py` → 复制为 `test_{动作}_ng_{原因}.py` |

```bash
cd yz-mall/mall-admin/mall-sys-startup/src/test/python
pip install -r requirements.txt
BASE_URL=https://env.example TOKEN='Bearer xxx' python sys_open_client/test_page_ok.py
BASE_URL=https://env.example python sys_open_client/test_page_ng_no_token.py
```

会手动上传定时平台：以单个 `.py`为单元；正例、反例分别调度或同组挂多个文件，配置相同环境变量，每日执行。

## 3. 前端手测备忘

```text
yz-mall-web-admin-pc/src/views/system/openclient/tests/README.md
```
