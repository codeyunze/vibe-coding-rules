---
name: scaffold-java-crud
description: 按 yz-mall 五层模块与现有风格脚手架生成 Java CRUD（含可选 Extend/Feign）。在用户要求新增业务接口、增删改查、仿照字典/商品模块生成代码时使用。
---

# 脚手架生成 Java CRUD

## 何时使用

用户要「新增某某管理」「仿 SysDictionary/PmsProduct 做 CRUD」「补 Controller/Service/Extend」时使用。

## 落盘位置（按域五层）

| 产物 | 模块 | 包/命名 |
|------|------|---------|
| Entity / Mapper /（常含）DTO·VO | `{域}-dao` | `Xxx` / `XxxMapper` / `XxxAddDto`… |
| Service / Impl | `{域}-core` | `XxxService` / `XxxServiceImpl` |
| 对外 Controller | `{域}-startup` | `XxxController` |
| 跨服务（可选） | interface + core/feign + startup/extend | `ExtendXxx*` |

参考：

- 对外：`PmsProductController`、`SysDictionaryController`
- 跨服务：`ExtendPmsStockController`、`ExtendPmsStockFeign`
- 基类：`ApiController`、`Result`、`ResultTable`、`PageFilter`

## 实现约束

1. Controller 继承 `ApiController`；`Result` / `Result<ResultTable<>>`
2. `@Valid` + `PageFilter`；权限 `api:{域}:{资源}:{动作}`
3. Service 对齐 MyBatis-Plus `IService`/`ServiceImpl`；ID 用雪花
4. `@TableLogic` 与表 `invalid` 语义一致
5. 需要跨服务时才生成 `Extend*`；否则不要过度设计
6. **只生成任务需要的文件**

## 工作流

```
- [ ] 确认域模块与包名（sys/pms/oms…）
- [ ] 确认表结构；新建表走 design-mysql-table 规范
- [ ] dao：Entity/Mapper/DTO/VO
- [ ] core：Service 接口与实现
- [ ] startup：Controller（add/update/delete/page/get）
- [ ] 如需跨服务：interface + ExtendController + Feign 双实现
- [ ] 核对权限码、路径前缀、校验注解
```

## 路径示例

```text
POST   /pms/product/add
POST   /pms/product/page
DELETE /pms/product/delete/{id}
POST   /extend/pms/stock/...    # 仅跨服务
```
