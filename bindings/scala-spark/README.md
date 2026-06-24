# Scala/Spark bindings adapter

This directory contains a synthetic, non-published Scala/Spark module used as a
transport binding surface for lakehouse and distributed costing-study workflows.

Scope:

- Parquet/Arrow file-exchange adapter for Spark DataFrame batch consumption
- Spark SQL boundary support for analytical queries against pre-computed outputs
- Service fallback adapter for online request/response behaviour over HTTP

Out of scope:

- Formula parsing
- Formula evaluation
- Calculator logic of any kind
- Spark UDFs, custom aggregators, or Catalyst extensions
- Repo-wide build or release wiring

## Layout

- `src/main/scala/mchs/spark/adapter/`: Parquet/Arrow adapter and service
  fallback adapters
- `build.sbt`: Minimal build configuration for Spark SQL consumers

## Usage

```scala
import mchs.spark.adapter.{ParquetFileExchangeAdapter, SparkSqlBoundaryAdapter}

val adapter = new ParquetFileExchangeAdapter()
adapter.loadAsView("s3://shared-core-outputs/2026/nwau/", "nwau_2026")

val sqlBoundary = new SparkSqlBoundaryAdapter()
spark.sql("SELECT * FROM nwau_2026 WHERE drg_code LIKE 'A%'").show()
```

The adapter only loads and exposes pre-computed Parquet datasets as Spark
DataFrames. It does not compute formula results or mutate calculator logic.

```scala
import mchs.spark.adapter.{
  ScalaSparkBindingRequest,
  ScalaSparkServiceRequest,
  ServiceFallbackAdapter
}

import scala.concurrent.ExecutionContext.Implicits.global

val binding = ScalaSparkBindingRequest(
  schemaVersion = "1.0",
  calculatorId = "acute",
  pricingYear = "2025",
  inputSchemaVersion = "1.0",
  outputSchemaVersion = "1.0",
  correlationId = Some("spark-job-001"),
  fixtureGate = "caller_supplied"
)

val payload = ServiceFallbackAdapter.jsonEnvelope(binding)
val service = new ServiceFallbackAdapter()
service.execute(
  ScalaSparkServiceRequest(
    binding = binding,
    serviceUrl = "https://calculator.local/v1/execute",
    payloadJson = payload
  )
)
```
