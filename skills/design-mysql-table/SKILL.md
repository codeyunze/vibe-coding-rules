---
name: design-mysql-table
description: 按 yz-mall 规范设计 MySQL 表结构并输出建表 SQL（含基础字段、COMMENT、索引）。在用户要求建表、改表、设计库表、写 DDL、评估索引时使用。
---

# 设计 MySQL 表结构

## 何时使用

用户给出业务字段、实体概念，或要求「建表 / DDL / 索引设计」时执行本技能。

## 输出要求

1. 先用 2～4 句说明表职责、主查询场景、关键约束
2. 给出完整 `CREATE TABLE`（可含必要索引）
3. 每个字段必须有 `COMMENT`；表必须有表级 `COMMENT`
4. 说明建议索引及原因（针对预计查询，不堆砌）

## 基础字段（无特别要求必须包含）

```sql
`id`          bigint   NOT NULL COMMENT '主键标识',
`create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
`update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
`invalid`     bigint   NOT NULL DEFAULT 0 COMMENT '数据是否有效：0数据有效',
PRIMARY KEY (`id`)
```

## 设计步骤

1. **澄清**：主键策略（默认 `bigint`）、是否逻辑删除（默认 `invalid`）、唯一业务键、预估查询
2. **对齐存量**：若改已有表，先查 `docs/sql` 或模块内 SQL/Entity，字段命名与该表历史风格一致；**新建表**用上述基础字段
3. **选型**：金额用 `decimal`；状态用 `tinyint`/`int` 并在 COMMENT 写枚举含义；长文本 `varchar` 设合理长度，超长用 `text` 并评估是否拆表
4. **索引**：
   - 等值过滤 → 单列或联合索引
   - 列表「状态 + 时间排序」→ `(status, create_time)` 类联合索引
   - 唯一约束 → `UNIQUE KEY`，并说明与 `invalid` 的共存策略
5. **输出 SQL 模板**：

```sql
CREATE TABLE `表名` (
  `id` bigint NOT NULL COMMENT '主键标识',
  -- 业务字段...
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `invalid` bigint NOT NULL DEFAULT 0 COMMENT '数据是否有效：0数据有效',
  PRIMARY KEY (`id`),
  KEY `idx_xxx` (`col1`, `col2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='表中文说明';
```

## 禁止

- 缺少 COMMENT
- 无依据的冗余索引、前缀过长索引
- 在 DDL 中写入真实密码或环境相关连接信息
