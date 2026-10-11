#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：Controller API 反例脚本骨架。
复制到 {域}-startup/src/test/python/{资源}/ 后改名 test_{动作}_ng_{原因}.py。

PASS 含义：请求被正确拒绝（Result.code 等于期望码），不是业务成功。
期望码：
  - 框架级：CodeEnum（如 50000 未登录）
  - 业务级：sys_dictionary RESPONSE-CODE 的 dictionary_key（会持续增加，见 .cursor/harness/RESPONSE_CODE.md）
环境变量：
  BASE_URL     网关或服务根地址
  EXPECT_CODE  期望业务/框架 code（默认 50000）；业务反例改为字典 key，如 20002
  TOKEN        可选

退出码：0 符合预期拒绝；1 未按预期拒绝；2 配置或依赖缺失
"""
from __future__ import annotations

import os
import sys


def main() -> int:
    try:
        import requests
    except ImportError:
        print("FAIL: please pip install requests")
        return 2

    base = os.environ.get("BASE_URL", "").rstrip("/")
    if not base:
        print("FAIL: BASE_URL is required")
        return 2

    expect_code = int(os.environ.get("EXPECT_CODE", "50000"))
    # TODO: 改成真实接口；无 Token 场景不要带 Authorization
    url = f"{base}/sys/open/client/page"
    headers = {}
    token = os.environ.get("TOKEN", "")
    if token:
        headers["Authorization"] = token

    resp = requests.post(url, json={"current": 1, "size": 10, "filter": {}}, headers=headers, timeout=30)

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
