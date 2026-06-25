# Binding Strategy: Scala/Spark Binding

## Decision

Use an Arrow/Parquet file-exchange and Spark SQL integration strategy for
Scala/Spark consumers. Spark jobs read pre-computed calculator outputs as
Parquet or Arrow datasets and express analytical queries through Spark SQL,
DataFrames, or structured streaming. No Scala formula port is created.

This follows the polyglot Rust core roadmap and reuses the CLI/file interop
contract established by the shared core for language-neutral exchange.

## Rationale

- Spark is a distributed execution engine, not a single-sourced formula host.
  Porting calculator logic to Scala would duplicate maintenance across every
  pricing year.
- Arrow and Parquet are first-class formats in the Spark ecosystem via
  `spark.read.parquet()` and Arrow-optimized columnar exchange.
- The CLI/file interop track already defines the Parquet schema, provenance,
  and fixture gates needed for Spark consumption.
- Lakehouse patterns (Delta Lake, Apache Iceberg, Apache Hudi) can ingest
  shared-core Parquet outputs without custom connectors.
- Scala/Spark build tooling is now present for the local transport adapter, but
  public module release still depends on JVM CI and owner evidence.

## Contract shape

### Integration modes

| Mode                 | Consumer               | Transport          | Notes                         |
|----------------------|------------------------|--------------------|-------------------------------|
| File exchange        | Spark DataFrame reader | Parquet / Arrow    | Primary mode; no service deps |
| SQL boundary         | Spark SQL / Thrift     | Parquet / JDBC     | Via DuckDB or service gateway |
| Service API          | Spark `http4s` client  | HTTP / REST        | Optional; for live queries    |

### Parquet schema contract

Spark reads the same Parquet schemas produced by the CLI/file interop track:

- `contract_version` — pinned calculator contract version
- `calculator_id` — public calculator identifier
- `pricing_year` — target IHACPA pricing year
- `input_schema` — structured input columns matching the calculator contract
- `output_schema` — computed output columns with diagnostic flags
- `provenance` — shared-core version, source archive hash, generation timestamp
- `fixture_gate` — declared synthetic-only or local-only gate

Spark SQL schemas are derived from the Parquet schema via schema inference or
explicit DDL matching the CLI/file contract.

### Lakehouse publication pattern

```scala
import mchs.spark.adapter.{ParquetFileExchangeAdapter, SparkSqlBoundaryAdapter}

val files = new ParquetFileExchangeAdapter()
files.loadAsView("s3://shared-core-outputs/2026/nwau/", "nwau_2026")

val sql = new SparkSqlBoundaryAdapter()
sql.query("SELECT * FROM nwau_2026 WHERE drg_code LIKE 'A%'").show()
```

## Supported calculators

All calculators exposed through the CLI/file interop track as Parquet outputs
are accessible from Spark. No Spark-specific calculator packaging is required.

## Limitations

- Spark does not execute calculator logic. All computation happens in the
  shared core before Parquet exchange.
- Streaming and microbatch workloads depend on the CLI/file output cadence.
  Real-time calculation is not supported through file exchange.
- Spark SQL cannot express calculator formulas. Complex derivations must be
  pre-computed by the shared core.
- No Scala/Spark UDFs, custom aggregators, or Catalyst extensions are
  maintained in this repository.

## Versioning

- Spark integration pins to the CLI/file interop contract version for Parquet
  schemas.
- Lakehouse table schemas declare the `contract_version` and `pricing_year`
  as partitioning or metadata columns.
- No separate Spark interop version is needed.

## Diagnostics and provenance

- Parquet outputs include full provenance metadata consumed by Spark DataFrames.
- Diagnostic columns (validation warnings, gate states, calculation errors)
  are preserved in the Parquet schema for Spark SQL filtering and alerting.
- Provenance metadata supports traceability from Spark queries back to shared
  core execution.

## Privacy and synthetic examples

- All committed Spark example manifests and test Parquet files are synthetic.
- Real IHACPA pricing data or patient-level extracts are never committed as
  Spark examples.
- The `fixture_gate` column distinguishes synthetic examples from local-only
  real data.

## When to use Scala/Spark vs. other bindings

Use Scala/Spark when:
- the consumer runs distributed or lakehouse workloads (Databricks, EMR, Synapse)
- the workflow requires Spark SQL, DataFrame, or structured streaming
- the team standardises on Parquet/Arrow columnar exchange

Prefer CLI/file interop or native bindings when:
- the consumer does not use Spark or a JVM ecosystem
- the integration is single-node or sub-second interactive
- the deployment target does not include a Spark cluster

## Readiness bar

- This track has concrete transport-boundary adapters for Parquet loading,
  Spark SQL view/query access, and HTTP service fallback.
- Integration workflows are documented and validated against shared golden
  fixtures and static Scala source checks.
- Do not promote Spark integration to release status until the CLI/file Parquet
  contract is stable and a Spark read example has been validated against
  synthetic fixtures in a JVM CI matrix.
