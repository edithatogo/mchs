package mchs.spark.adapter

import org.apache.spark.sql.{DataFrame, SparkSession}

/**
 * ParquetFileExchangeAdapter loads pre-computed calculator outputs
 * stored as Parquet datasets and exposes them as Spark DataFrames.
 *
 * This adapter is transport-only. It does not perform any calculation,
 * expression evaluation, or data transformation. Calculator rules must
 * stay single-sourced in the shared core.
 *
 * @param spark the active SparkSession (implicit or explicit)
 */
class ParquetFileExchangeAdapter(implicit spark: SparkSession) {

  /**
   * Loads a Parquet dataset from the given path and returns it as a DataFrame.
   *
   * @param path  file-system or object-store path to the Parquet data
   * @return      Spark DataFrame with the Parquet schema inferred
   */
  def load(path: String): DataFrame = {
    val normalizedPath = BoundaryValidation.requireNonBlank(path, "path")
    spark.read.parquet(normalizedPath)
  }

  /**
   * Loads a Parquet dataset and registers it as a temporary view for
   * Spark SQL queries.
   *
   * @param path      file-system or object-store path to the Parquet data
   * @param viewName  name of the temporary view
   * @return          Spark DataFrame backing the registered view
   */
  def loadAsView(path: String, viewName: String): DataFrame = {
    val normalizedViewName =
      BoundaryValidation.requireSparkSqlIdentifier(viewName, "viewName")
    val df = load(path)
    df.createOrReplaceTempView(normalizedViewName)
    df
  }
}
