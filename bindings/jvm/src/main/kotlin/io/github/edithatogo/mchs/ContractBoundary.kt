package io.github.edithatogo.mchs

import java.nio.file.Files
import java.nio.file.Path

object ContractBoundary {
    const val groupId: String = "io.github.edithatogo"
    const val artifactId: String = "mchs-jvm-bindings"
    const val version: String = "0.1.0"
    const val packageName: String = "$groupId:$artifactId"
    const val packageCoordinate: String = "$packageName:$version"
    const val bindingContractVersion: String = "1.0"
    const val formulaLogicPolicy: String =
        "Formula logic is delegated to the shared core; the JVM binding owns typed contracts, validation, and transport metadata only."

    val supportedCalculators: Set<String> = setOf(
        "acute",
        "adjust",
        "community_mh",
        "ed",
        "mh",
        "outpatients",
        "subacute",
    )

    val publicContractFields: List<String> = listOf(
        "schema_version",
        "calculator_id",
        "pricing_year",
        "input_schema_version",
        "output_schema_version",
        "required_input_columns",
        "required_output_columns",
    )

    fun metadata(): BindingBoundaryMetadata = BindingBoundaryMetadata(
        packageCoordinate = packageCoordinate,
        contractVersion = bindingContractVersion,
        formulaLogicPolicy = formulaLogicPolicy,
        supportedCalculators = supportedCalculators.toList(),
        publicContractFields = publicContractFields,
        transports = listOf(
            TransportBoundary(
                mode = TransportMode.CLI_FILE,
                role = "primary-local",
                notes = "Validated request/response file handoff for local shared-core execution.",
            ),
            TransportBoundary(
                mode = TransportMode.SERVICE_HTTP,
                role = "fallback",
                notes = "HTTP/JSON handoff for hosted shared-core execution when configured by the caller.",
            ),
        ),
    )
}

enum class TransportMode {
    CLI_FILE,
    SERVICE_HTTP,
}

data class TransportBoundary(
    val mode: TransportMode,
    val role: String,
    val notes: String,
)

data class BindingBoundaryMetadata(
    val packageCoordinate: String,
    val contractVersion: String,
    val formulaLogicPolicy: String,
    val supportedCalculators: List<String>,
    val publicContractFields: List<String>,
    val transports: List<TransportBoundary>,
)

data class JvmBindingRequest(
    val calculatorId: String,
    val pricingYear: String,
    val inputPath: Path,
    val outputPath: Path,
    val transportMode: TransportMode = TransportMode.CLI_FILE,
    val correlationId: String? = null,
    val metadata: Map<String, String> = emptyMap(),
)

data class JvmBindingResponse(
    val success: Boolean,
    val status: String,
    val calculatorId: String,
    val pricingYear: String,
    val inputPath: Path,
    val outputPath: Path,
    val transportMode: TransportMode,
    val diagnostics: List<BindingDiagnostic>,
    val warnings: List<String> = emptyList(),
)

data class BindingDiagnostic(
    val code: String,
    val severity: DiagnosticSeverity,
    val message: String,
)

enum class DiagnosticSeverity {
    INFO,
    WARNING,
    ERROR,
}

interface SharedCoreAdapter {
    fun execute(request: JvmBindingRequest): JvmBindingResponse
}

class BoundaryValidationException(message: String) : IllegalArgumentException(message)

class JvmFileBoundaryAdapter(
    private val sharedCoreAdapter: SharedCoreAdapter = MetadataOnlySharedCoreAdapter(),
) {
    fun execute(request: JvmBindingRequest): JvmBindingResponse {
        validate(request)
        return sharedCoreAdapter.execute(request)
    }

    fun validate(request: JvmBindingRequest) {
        if (request.calculatorId !in ContractBoundary.supportedCalculators) {
            throw BoundaryValidationException("Unsupported calculator_id: ${request.calculatorId}")
        }

        if (request.pricingYear.isBlank()) {
            throw BoundaryValidationException("pricing_year must not be blank")
        }

        if (!Files.isRegularFile(request.inputPath)) {
            throw BoundaryValidationException("input_path must reference an existing file: ${request.inputPath}")
        }

        val parent = request.outputPath.parent
        if (parent != null && !Files.exists(parent)) {
            Files.createDirectories(parent)
        }

        if (parent != null && !Files.isDirectory(parent)) {
            throw BoundaryValidationException("output_path parent is not a directory: $parent")
        }
    }
}

class MetadataOnlySharedCoreAdapter : SharedCoreAdapter {
    override fun execute(request: JvmBindingRequest): JvmBindingResponse = JvmBindingResponse(
        success = true,
        status = "boundary_validated_pending_shared_core_execution",
        calculatorId = request.calculatorId,
        pricingYear = request.pricingYear,
        inputPath = request.inputPath,
        outputPath = request.outputPath,
        transportMode = request.transportMode,
        diagnostics = listOf(
            BindingDiagnostic(
                code = "JVM-BINDING-001",
                severity = DiagnosticSeverity.INFO,
                message = "JVM binding validated the file/service boundary and delegated formula execution to the shared core adapter.",
            ),
        ),
        warnings = listOf(ContractBoundary.formulaLogicPolicy),
    )
}
