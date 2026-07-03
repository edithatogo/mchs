package mchs.spark

/**
 * The mchs.spark.adapter package provides synthetic file-exchange and service
 * fallback adapters for Spark DataFrame consumption of pre-computed calculator
 * outputs. Calculator expressions are not evaluated here.
 *
 * = Integration modes =
 *
 *  - '''file-exchange''': Parquet/Arrow file handoff for batch lakehouse workloads.
 *  - '''sql-boundary''': Spark SQL / JDBC analytical queries against pre-computed views.
 *  - '''service''': HTTP/REST fallback for online request/response behaviour.
 *
 * = Design notes =
 *
 * All adapters are transport-only. They do not parse, evaluate, or duplicate
 * calculator formulas. Calculator rules must remain single-sourced in the
 * shared core.
 */
package object adapter {
  val BindingSchemaVersion: String = "1.0"
}
