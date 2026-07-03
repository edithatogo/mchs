package org.mchs.bindings.native

interface NativeBindingClient {
    fun execute(request: BindingRequest): BindingResponse
}

class FileBoundaryNativeBindingClient : NativeBindingClient {
    override fun execute(request: BindingRequest): BindingResponse {
        val diagnostics = validate(request)
        val status =
            if (diagnostics.isEmpty()) {
                BindingStatus.ENVELOPE_VALIDATED
            } else {
                BindingStatus.BLOCKED
            }

        return BindingResponse(
            status = status,
            message =
                if (status == BindingStatus.ENVELOPE_VALIDATED) {
                    "Kotlin/Native request envelope is valid for caller-owned shared-core execution."
                } else {
                    "Kotlin/Native request is blocked at the adapter boundary."
                },
            diagnostics =
                diagnostics.ifEmpty {
                    listOf(
                        "Formula logic remains in the Rust core or approved service.",
                        "Paths are envelope-validated only; canonicalize them within the caller-owned execution root before invoking the shared-core CLI or C ABI.",
                    )
                },
            metadata = BindingMetadata(
                correlationId = request.metadata.correlationId,
                source = "validated-boundary",
                transport = "kotlin-native-file-boundary",
            ),
        )
    }

    private fun validate(request: BindingRequest): List<String> =
        buildList {
            if (request.schemaVersion.isBlank()) {
                add("schemaVersion is required.")
            }
            if (request.calculatorId != "nwau") {
                add("calculatorId must be nwau.")
            }
            if (request.pricingYear.isBlank()) {
                add("pricingYear is required.")
            }
            if (request.inputPath.isBlank()) {
                add("inputPath is required for file-boundary execution.")
            } else if (isUnsafePath(request.inputPath)) {
                add("inputPath must be relative and must not contain parent traversal.")
            }
            if (request.outputPath.isBlank()) {
                add("outputPath is required for file-boundary execution.")
            } else if (isUnsafePath(request.outputPath)) {
                add("outputPath must be relative and must not contain parent traversal.")
            }
            if (request.metadata.correlationId.isBlank()) {
                add("metadata.correlationId is required.")
            }
        }

    private fun isUnsafePath(path: String): Boolean {
        val normalized = path.replace('\\', '/')
        return normalized.startsWith("/") ||
            normalized.startsWith("~/") ||
            normalized.contains(":") ||
            normalized.split("/").any { it == ".." }
    }
}
