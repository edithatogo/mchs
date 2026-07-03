package mchs.spark.adapter

final case class ScalaSparkBindingRequest(
    schemaVersion: String,
    calculatorId: String,
    pricingYear: String,
    inputSchemaVersion: String,
    outputSchemaVersion: String,
    correlationId: Option[String],
    fixtureGate: String,
    metadata: Map[String, String] = Map.empty
) {
  def validate(): ScalaSparkBindingRequest = {
    BoundaryValidation.requireNonBlank(schemaVersion, "schemaVersion")
    BoundaryValidation.requireNonBlank(calculatorId, "calculatorId")
    BoundaryValidation.requireNonBlank(pricingYear, "pricingYear")
    BoundaryValidation.requireNonBlank(inputSchemaVersion, "inputSchemaVersion")
    BoundaryValidation.requireNonBlank(outputSchemaVersion, "outputSchemaVersion")
    BoundaryValidation.requireNonBlank(fixtureGate, "fixtureGate")
    correlationId.foreach(BoundaryValidation.requireNonBlank(_, "correlationId"))
    this
  }
}

final case class ScalaSparkServiceRequest(
    binding: ScalaSparkBindingRequest,
    serviceUrl: String,
    payloadJson: String
) {
  def validate(): ScalaSparkServiceRequest = {
    binding.validate()
    BoundaryValidation.requireHttpUrl(serviceUrl, "serviceUrl")
    BoundaryValidation.requireNonBlank(payloadJson, "payloadJson")
    this
  }
}

final case class ScalaSparkServiceResponse(
    statusCode: Int,
    body: String,
    correlationId: Option[String]
) {
  def isSuccess: Boolean = statusCode >= 200 && statusCode < 300
}

object BoundaryValidation {
  private val SparkIdentifier = "^[A-Za-z_][A-Za-z0-9_]*$".r

  def requireNonBlank(value: String, fieldName: String): String = {
    val normalized = Option(value).map(_.trim).getOrElse("")
    require(normalized.nonEmpty, s"$fieldName must be provided")
    normalized
  }

  def requireSparkSqlIdentifier(value: String, fieldName: String): String = {
    val normalized = requireNonBlank(value, fieldName)
    require(
      SparkIdentifier.pattern.matcher(normalized).matches(),
      s"$fieldName must be a simple Spark SQL identifier"
    )
    normalized
  }

  def requireHttpUrl(value: String, fieldName: String): String = {
    val normalized = requireNonBlank(value, fieldName)
    require(
      normalized.startsWith("http://") || normalized.startsWith("https://"),
      s"$fieldName must start with http:// or https://"
    )
    normalized
  }
}
