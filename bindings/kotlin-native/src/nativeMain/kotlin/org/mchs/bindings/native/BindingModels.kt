package org.mchs.bindings.native

data class BindingMetadata(
    val correlationId: String,
    val source: String,
    val transport: String,
)

data class BindingRequest(
    val schemaVersion: String,
    val calculatorId: String,
    val pricingYear: String,
    val inputPath: String,
    val outputPath: String,
    val metadata: BindingMetadata,
)

data class BindingResponse(
    val status: BindingStatus,
    val message: String,
    val diagnostics: List<String>,
    val metadata: BindingMetadata,
)

enum class BindingStatus {
    ENVELOPE_VALIDATED,
    BLOCKED,
}
