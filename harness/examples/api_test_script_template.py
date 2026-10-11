#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：Controller API 正例脚本骨架。
复制到 {域}-startup/src/test/python/{资源}/ 后改名 test_{动作}_ok.py，并改 URL 与断言。
反例请用同目录 api_test_script_ng_template.py。

环境变量：
  BASE_URL  网关或服务根地址，如 https://api.example.com
  TOKEN     可选，完整 Authorization 头值，如 Bearer eyJ...

退出码：0 成功；1 业务/断言失败；2 配置或依赖缺失
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

    token = os.environ.get("TOKEN", "")
    headers = {"Authorization": token} if token else {}
    # TODO: 改成真实接口
    url = f"{base}/sys/open/client/page"
    resp = requests.post(
        url,
        json={"current": 1, "size": 10, "filter": {}},
        headers=headers,
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"FAIL http={resp.status_code} body={resp.text[:500]}")
        return 1
    body = resp.json()
    if body.get("code") != 200:
        print(f"FAIL bizCode={body.get('code')} msg={body.get('msg')}")
        return 1
    print("PASS ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
