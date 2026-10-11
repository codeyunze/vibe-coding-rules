# NOTES — tw-telemetry 节点 0

## 环境

- MySQL MCP 只读，无法在本机代执行 `CREATE TABLE tw_gps_latest`。
- ClickHouse 通过 `docs/docker/docker-compose.yml` 服务 `clickhouse` 引入；首次 `docker compose up -d clickhouse` 后检查 init 是否执行。

## 启用 ClickHouse（后续节点）

1. 在 `mall-tw/pom.xml` 增加依赖（父 POM 已管理版本）：

```xml
<dependency>
    <groupId>com.clickhouse</groupId>
    <artifactId>clickhouse-jdbc</artifactId>
    <classifier>all</classifier>
</dependency>
```

2. 配置：

```yaml
tw:
  telemetry:
    clickhouse:
      enabled: true
      password: ${CLICKHOUSE_PASSWORD}
```

> 注意：默认不把 clickhouse-jdbc 放进 classpath。驱动会经 SPI 注册到 DriverManager，
> 与 dynamic-datasource 初始化冲突时会出现 `Could not initialize class com.clickhouse.jdbc.ClickHouseDriver`。

## Kafka

节点 0 仅配置占位，未引入 `spring-kafka` 依赖，避免自动装配连不上 Broker。节点 4 再加依赖与消费者。
