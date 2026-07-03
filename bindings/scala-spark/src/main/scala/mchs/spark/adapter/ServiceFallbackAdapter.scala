package mchs.spark.adapter

import java.net.URI
import java.net.http.{HttpClient, HttpRequest, HttpResponse}
import java.time.Duration

import scala.concurrent.{ExecutionContext, Future}

/**
 * ServiceFallbackAdapter provides an HTTP/REST fallback path for callers
 * that need online request/response behaviour with the shared calculator
 * backend.
 *
 * This adapter is transport-only. It does not perform any calculation,
 * expression evaluation, or data transformation. Calculator rules must
 * stay single-sourced in the shared core.
 *
 * @param client   JDK HTTP client used for service fallback requests
 * @param timeout  per-request timeout
 */
class ServiceFallbackAdapter(
    client: HttpClient = HttpClient.newHttpClient(),
    timeout: Duration = Duration.ofSeconds(30)
)(implicit ec: ExecutionContext) {

  /**
   * Executes a service-bound request against the shared calculator backend.
   * The payload is passed through as JSON so Spark callers do not need a
   * Scala copy of the calculator schema.
   *
   * @param request versioned service-bound request envelope
   * @return        future containing status code, response body, and trace id
   */
  def execute(request: ScalaSparkServiceRequest): Future[ScalaSparkServiceResponse] = {
    val validated = request.validate()
    val httpRequest = HttpRequest
      .newBuilder(URI.create(validated.serviceUrl))
      .timeout(timeout)
      .header("Content-Type", "application/json")
      .header("Accept", "application/json")
      .header("X-MCHS-Calculator-Id", validated.binding.calculatorId)
      .header("X-MCHS-Pricing-Year", validated.binding.pricingYear)
      .headers(correlationHeader(validated.binding): _*)
      .POST(HttpRequest.BodyPublishers.ofString(validated.payloadJson))
      .build()

    Future {
      val response = client.send(httpRequest, HttpResponse.BodyHandlers.ofString())
      ScalaSparkServiceResponse(
        statusCode = response.statusCode(),
        body = response.body(),
        correlationId = validated.binding.correlationId
      )
    }
  }

  /**
   * Convenience path for existing callers that already hold a JSON request
   * body and service URL outside the typed envelope.
   */
  def executeJson(
      serviceUrl: String,
      calculatorId: String,
      pricingYear: String,
      correlationId: String,
      payloadJson: String
  ): Future[String] = {
    val binding = ScalaSparkBindingRequest(
      schemaVersion = "1.0",
      calculatorId = calculatorId,
      pricingYear = pricingYear,
      inputSchemaVersion = "1.0",
      outputSchemaVersion = "1.0",
      correlationId = Some(correlationId),
      fixtureGate = "caller_supplied"
    )
    execute(
      ScalaSparkServiceRequest(
        binding = binding,
        serviceUrl = serviceUrl,
        payloadJson = payloadJson
      )
    ).map(_.body)
  }

  private def correlationHeader(binding: ScalaSparkBindingRequest): Seq[String] = {
    binding.correlationId match {
      case Some(value) => Seq("X-Correlation-Id", value)
      case None        => Seq.empty
    }
  }
}

object ServiceFallbackAdapter {
  def jsonEnvelope(request: ScalaSparkBindingRequest): String = {
    val validated = request.validate()
    val fields = Seq(
      "schema_version" -> validated.schemaVersion,
      "calculator_id" -> validated.calculatorId,
      "pricing_year" -> validated.pricingYear,
      "input_schema_version" -> validated.inputSchemaVersion,
      "output_schema_version" -> validated.outputSchemaVersion,
      "fixture_gate" -> validated.fixtureGate
    ) ++ validated.correlationId.map("correlation_id" -> _).toSeq

    val metadataJson = validated.metadata.toSeq
      .sortBy(_._1)
      .map { case (key, value) =>
        s""""${escapeJson(key)}":"${escapeJson(value)}""""
      }
      .mkString("{", ",", "}")

    val fieldJson = fields
      .map { case (key, value) =>
        s""""${escapeJson(key)}":"${escapeJson(value)}""""
      }
      .mkString(",")

    s"{$fieldJson,\"metadata\":$metadataJson}"
  }

  private def escapeJson(value: String): String = {
    value.flatMap {
      case '"'  => "\\\""
      case '\\' => "\\\\"
      case '\b' => "\\b"
      case '\f' => "\\f"
      case '\n' => "\\n"
      case '\r' => "\\r"
      case '\t' => "\\t"
      case char if char.isControl =>
        "\\u%04x".format(char.toInt)
      case char => char.toString
    }
  }
}
