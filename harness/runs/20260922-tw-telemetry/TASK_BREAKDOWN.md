# 任务拆分 TASK_BREAKDOWN

> 落盘：`.cursor/harness/runs/20260922-tw-telemetry/TASK_BREAKDOWN.md`  
> 对照设计文档 §12 实现节点。

## 依赖顺序

`节点0 DDL/配置 → 节点1 Latest 写读 → 节点2 API → 节点3 CH轨迹 → 节点4 Kafka → 节点5 验收`

## 任务清单

### 节点 0～4

- [x] 见前序（仓库侧已完成）

### 节点 5 — 验收收口

- [x] 权限/菜单文本 `mall-tw/src/main/resources/db/tw_telemetry_permissions.txt`
- [x] §9 T1～T9 对照 + curl：`VERIFY_T1_T9.md`
- [x] Python 正反例单文件独立可跑（无 `_common`）
- [x] ACCEPTANCE / 设计文档 §10 / §12 节点 5 收口

### C. 前端

- [ ] 本轮 n/a（实时监控 / 轨迹查询页另开）

### 环境待办（非代码）

- [ ] ClickHouse 容器 init 确认
- [ ] 真 Kafka / access 上行联调
- [ ] mall-sys 录入权限码与角色勾选

## 当前状态

| 节点 | 状态 |
|------|------|
| 0～5 | **仓库侧全部完成** |
| 前端 / access 联调 | 另开 |
