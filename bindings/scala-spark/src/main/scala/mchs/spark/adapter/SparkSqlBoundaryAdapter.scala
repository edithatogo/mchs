package mchs.spark.adapter

import org.apache.spark.sql.{DataFrame, SparkSession}

/**
 * SparkSqlBoundaryAdapter exposes pre-computed Parquet datasets through Spark
 * SQL views and query execution. It does not register UDFs or custom
 * aggregators.
 *
 * @param spark the active SparkSession (implicit or explicit)
 */
class SparkSqlBoundaryAdapter(implicit spark: SparkSession) {
  private val parquetAdapter = new ParquetFileExchangeAdapter()

  def registerParquetView(path: String, viewName: String): DataFrame = {
    parquetAdapter.loadAsView(path, viewName)
  }

  def query(sqlText: String): DataFrame = {
    val normalizedSql = BoundaryValidation.requireNonBlank(sqlText, "sqlText")
    spark.sql(normalizedSql)
  }
}
