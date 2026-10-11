# 响应码断言口径 RESPONSE_CODE

> API 正/反例脚本断言业务 `Result.code` 时以本文为准。  
> **业务响应码会持续增加，Harness 禁止维护一份「完整码表副本」作为真相源。**

## 双源模型

| 来源 | 用途 | 是否会持续增长 | Harness 怎么用 |
|------|------|----------------|----------------|
| `CodeEnum`（`mall-base`） | 框架级：成功、鉴权、通用参数/系统异常等 | 较少、相对稳定 | 正例成功码、鉴权/通用反例可直接写枚举值 |
| `sys_dictionary`（`RESPONSE-CODE`） | **业务域响应码** | **会持续增加** | 业务反例只引用字典中的 `dictionary_key`；不在 Harness 文档里抄全表 |

### 字典定位（活数据源）

| 项 | 值 |
|----|-----|
| 根 `dictionary_key` | `RESPONSE-CODE` |
| 根 id / 子项 `ancestor_id` | `1995060920724340736` |
| 码值字段 | 子项 `dictionary_key`（如 `20001`） |
| 文案字段 | 子项 `dictionary_value` |

查询有效业务码（开发/写脚本前可查库，**勿把结果永久写死进约定文档**）：

```sql
SELECT dictionary_key, dictionary_value, sort_order
FROM sys_dictionary
WHERE ancestor_id = 1995060920724340736
  AND invalid = 0
ORDER BY sort_order, id;
```

### 框架级常用码（相对稳定，可写进脚本）

来自 `com.yz.mall.base.enums.CodeEnum`，节选：

| code | 含义 | 典型场景 |
|------|------|----------|
| `200` | 成功 | 正例 |
| `50000` | 请登录系统 | 无 Token |
| `50001` | 无效令牌 | 非法 Token |
| `50002` | 登录已过期 | Token 过期 |
| `50003` | 没有操作权限 | 无权限 |
| `30001` | 参数异常 | 缺参/非法参数（若业务未单独挂字典码） |
| `30003` | 数据不存在 | 通用不存在（若业务未单独挂字典码） |

业务域专属错误（如字典 `20001`/`20002`/…）以 **RESPONSE-CODE 字典当时库内数据** 为准。

## 脚本与落盘约定

1. **正例**：断言 `code == 200`（除非卡片明确约定其它成功语义）。  
2. **鉴权反例**：优先断言 `CodeEnum` 鉴权段（`50000`~`50005`）；若网关先返回 HTTP 401/403，以实际联调结果写进该脚本文件头，并在 ACCEPTANCE 注明。  
3. **业务反例**：文件头写明期望 `dictionary_key`（如 `EXPECT_CODE=20002`），脚本断言 `Result.code` 等于该值；**不要**在 Harness 模板里枚举「全部业务码」。  
4. **FEATURE_CARD / TASK / ACCEPTANCE**：接口或反例行填写「期望 code = 字典 key」，新增业务码时先入 `sys_dictionary`，再写脚本。  
5. 字典新增码后：只更新对应功能的脚本与验收行，**不必**改本文件码表（本文件无全量码表）。

## Agent 检查清单

- [ ] 未在 `.cursor/harness/` 维护完整业务码副本  
- [ ] 业务反例期望码来自字典 `dictionary_key`（或卡片已写明的字典码）  
- [ ] 鉴权/成功等框架码来自 `CodeEnum`  
- [ ] 新业务错误已先落入 `RESPONSE-CODE` 再写 API 反例
