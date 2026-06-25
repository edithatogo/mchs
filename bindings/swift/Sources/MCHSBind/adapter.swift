import Foundation

// MARK: - Request envelope

/// Versioned Swift request envelope that mirrors the public calculator contract
/// and adds only transport metadata.
public struct SwiftBindingRequest: Codable, Sendable {
    public var schemaVersion: String
    public var calculatorId: String
    public var pricingYear: String
    public var inputSchemaVersion: String
    public var outputSchemaVersion: String
    public var mode: String
    public var inputPath: String?
    public var outputPath: String?
    public var serviceURL: String?
    public var correlationId: String?
    public var metadata: [String: String]?
    public var fixtureGate: String

    public init(
        schemaVersion: String = "1.0",
        calculatorId: String,
        pricingYear: String,
        inputSchemaVersion: String,
        outputSchemaVersion: String,
        mode: String,
        inputPath: String? = nil,
        outputPath: String? = nil,
        serviceURL: String? = nil,
        correlationId: String? = nil,
        metadata: [String: String]? = nil,
        fixtureGate: String
    ) {
        self.schemaVersion = schemaVersion
        self.calculatorId = calculatorId
        self.pricingYear = pricingYear
        self.inputSchemaVersion = inputSchemaVersion
        self.outputSchemaVersion = outputSchemaVersion
        self.mode = mode
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.serviceURL = serviceURL
        self.correlationId = correlationId
        self.metadata = metadata
        self.fixtureGate = fixtureGate
    }

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case calculatorId = "calculator_id"
        case pricingYear = "pricing_year"
        case inputSchemaVersion = "input_schema_version"
        case outputSchemaVersion = "output_schema_version"
        case mode
        case inputPath = "input_path"
        case outputPath = "output_path"
        case serviceURL = "service_url"
        case correlationId = "correlation_id"
        case metadata
        case fixtureGate = "fixture_gate"
    }
}

// MARK: - Response envelope

/// Versioned Swift response envelope that captures success, diagnostics,
/// provenance, and transport-specific outputs.
public struct SwiftBindingResponse: Codable, Sendable {
    public var schemaVersion: String
    public var calculatorId: String
    public var pricingYear: String
    public var mode: String
    public var success: Bool
    public var status: String
    public var message: String
    public var warnings: [String]?
    public var errors: [SwiftBindingError]?
    public var diagnostics: Diagnostics
    public var provenance: Provenance
    public var serviceURL: String?
    public var outputPath: String?
    public var fixtureGateState: String
    public var moduleReadinessState: String

    public init(
        schemaVersion: String = "1.0",
        calculatorId: String,
        pricingYear: String,
        mode: String,
        success: Bool,
        status: String,
        message: String,
        warnings: [String]? = nil,
        errors: [SwiftBindingError]? = nil,
        diagnostics: Diagnostics,
        provenance: Provenance,
        serviceURL: String? = nil,
        outputPath: String? = nil,
        fixtureGateState: String,
        moduleReadinessState: String
    ) {
        self.schemaVersion = schemaVersion
        self.calculatorId = calculatorId
        self.pricingYear = pricingYear
        self.mode = mode
        self.success = success
        self.status = status
        self.message = message
        self.warnings = warnings
        self.errors = errors
        self.diagnostics = diagnostics
        self.provenance = provenance
        self.serviceURL = serviceURL
        self.outputPath = outputPath
        self.fixtureGateState = fixtureGateState
        self.moduleReadinessState = moduleReadinessState
    }

    enum CodingKeys: String, CodingKey {
        case schemaVersion = "schema_version"
        case calculatorId = "calculator_id"
        case pricingYear = "pricing_year"
        case mode
        case success
        case status
        case message
        case warnings
        case errors
        case diagnostics
        case provenance
        case serviceURL = "service_url"
        case outputPath = "output_path"
        case fixtureGateState = "fixture_gate_state"
        case moduleReadinessState = "module_readiness_state"
    }
}

// MARK: - Supporting types

public struct Diagnostics: Codable, Sendable {
    public var status: String
    public var checks: [DiagnosticCheck]
    public var summary: DiagnosticSummary
    public var notes: String?

    public init(
        status: String,
        checks: [DiagnosticCheck],
        summary: DiagnosticSummary,
        notes: String? = nil
    ) {
        self.status = status
        self.checks = checks
        self.summary = summary
        self.notes = notes
    }
}

public struct DiagnosticCheck: Codable, Sendable {
    public var id: String
    public var status: String
    public var message: String

    public init(id: String, status: String, message: String) {
        self.id = id
        self.status = status
        self.message = message
    }
}

public struct DiagnosticSummary: Codable, Sendable {
    public var passed: Int
    public var failed: Int
    public var blocked: Int

    public init(passed: Int, failed: Int, blocked: Int) {
        self.passed = passed
        self.failed = failed
        self.blocked = blocked
    }
}

public struct Provenance: Codable, Sendable {
    public var command: String
    public var bindingBundleId: String
    public var sourceManifestPath: String
    public var sourceURL: String
    public var retrievedOn: String
    public var sha256: String
    public var bytes: Int
    public var checksumAlgorithm: String

    public init(
        command: String,
        bindingBundleId: String = "swift_binding_contract_20260513",
        sourceManifestPath: String,
        sourceURL: String = "https://example.invalid/contracts/swift-binding",
        retrievedOn: String,
        sha256: String,
        bytes: Int,
        checksumAlgorithm: String = "sha256"
    ) {
        self.command = command
        self.bindingBundleId = bindingBundleId
        self.sourceManifestPath = sourceManifestPath
        self.sourceURL = sourceURL
        self.retrievedOn = retrievedOn
        self.sha256 = sha256
        self.bytes = bytes
        self.checksumAlgorithm = checksumAlgorithm
    }

    enum CodingKeys: String, CodingKey {
        case command
        case bindingBundleId = "binding_bundle_id"
        case sourceManifestPath = "source_manifest_path"
        case sourceURL = "source_url"
        case retrievedOn = "retrieved_on"
        case sha256
        case bytes
        case checksumAlgorithm = "checksum_algorithm"
    }
}

public struct SwiftBindingError: Codable, Sendable {
    public var code: String
    public var severity: String
    public var retryable: Bool
    public var condition: String
    public var message: String?

    public init(
        code: String,
        severity: String,
        retryable: Bool,
        condition: String,
        message: String? = nil
    ) {
        self.code = code
        self.severity = severity
        self.retryable = retryable
        self.condition = condition
        self.message = message
    }
}

// MARK: - Transport adapter protocol

/// Adapter defines the interop boundary used by file-exchange, CLI, service,
/// or future C ABI integration.
public protocol BindingAdapter: Sendable {
    func execute(request: SwiftBindingRequest) async throws -> SwiftBindingResponse
}

// MARK: - Concrete file boundary adapter

public enum SwiftBindingMode: String, Sendable {
    case fileExchange = "file-exchange"
    case cli
    case service
    case cABI = "c-abi"
}

public enum SwiftBindingAdapterError: Error, Equatable, LocalizedError, Sendable {
    case unsupportedMode(String)
    case missingInputPath
    case missingOutputPath
    case inputFileNotFound(String)
    case outputDirectoryNotFound(String)
    case cliProcessFailed(exitCode: Int32, stderr: String)
    case cliUnavailableOnPlatform

    public var errorDescription: String? {
        switch self {
        case .unsupportedMode(let mode):
            return "Unsupported Swift binding mode: \(mode)"
        case .missingInputPath:
            return "File-boundary requests require input_path."
        case .missingOutputPath:
            return "File-boundary requests require output_path."
        case .inputFileNotFound(let path):
            return "Input file does not exist: \(path)"
        case .outputDirectoryNotFound(let path):
            return "Output directory does not exist: \(path)"
        case .cliProcessFailed(let exitCode, let stderr):
            return "CLI process failed with exit code \(exitCode): \(stderr)"
        case .cliUnavailableOnPlatform:
            return "Foundation Process is only available for the Swift CLI adapter on supported platforms."
        }
    }
}

public struct FileBoundaryValidation: Sendable {
    public var inputPath: String
    public var outputPath: String
    public var outputDirectory: String

    public init(inputPath: String, outputPath: String, outputDirectory: String) {
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.outputDirectory = outputDirectory
    }
}

public struct FileBoundaryBindingAdapter: BindingAdapter {
    private let validationDate: @Sendable () -> String

    public init(
        validationDate: @escaping @Sendable () -> String = { FileBoundaryBindingAdapter.isoDateToday() }
    ) {
        self.validationDate = validationDate
    }

    public func execute(request: SwiftBindingRequest) async throws -> SwiftBindingResponse {
        let validation = try validate(request: request)
        return SwiftBindingResponse(
            calculatorId: request.calculatorId,
            pricingYear: request.pricingYear,
            mode: request.mode,
            success: false,
            status: "boundary_validated",
            message: "File boundary validated; execute the shared CLI or core adapter before treating this as a calculator result.",
            warnings: ["The Swift binding validates transport boundaries only; calculator logic stays in the shared core."],
            errors: [],
            diagnostics: Diagnostics(
                status: "boundary_validated",
                checks: [
                    DiagnosticCheck(id: "mode_supported", status: "pass", message: "The request uses a primary file or CLI mode."),
                    DiagnosticCheck(id: "input_file_exists", status: "pass", message: "Input file exists at \(validation.inputPath)."),
                    DiagnosticCheck(id: "output_directory_exists", status: "pass", message: "Output directory exists at \(validation.outputDirectory)."),
                    DiagnosticCheck(id: "calculator_not_executed", status: "blocked", message: "The file-boundary adapter validates handoff paths only and did not execute the shared calculator."),
                ],
                summary: DiagnosticSummary(passed: 3, failed: 0, blocked: 1),
                notes: "Swift file-boundary adapter validation."
            ),
            provenance: Provenance(
                command: "swift-binding validate-file-boundary",
                sourceManifestPath: "contracts/swift-binding/swift-binding.contract.json",
                retrievedOn: validationDate(),
                sha256: "runtime-file-boundary-validation",
                bytes: 0
            ),
            outputPath: validation.outputPath,
            fixtureGateState: "boundary_validated",
            moduleReadinessState: "transport_ready_calculator_not_executed"
        )
    }

    public func validate(request: SwiftBindingRequest) throws -> FileBoundaryValidation {
        guard request.mode == SwiftBindingMode.fileExchange.rawValue || request.mode == SwiftBindingMode.cli.rawValue else {
            throw SwiftBindingAdapterError.unsupportedMode(request.mode)
        }
        guard let inputPath = request.inputPath, !inputPath.isEmpty else {
            throw SwiftBindingAdapterError.missingInputPath
        }
        guard let outputPath = request.outputPath, !outputPath.isEmpty else {
            throw SwiftBindingAdapterError.missingOutputPath
        }
        let fileManager = FileManager.default
        guard fileManager.fileExists(atPath: inputPath) else {
            throw SwiftBindingAdapterError.inputFileNotFound(inputPath)
        }

        let outputDirectory = URL(fileURLWithPath: outputPath)
            .deletingLastPathComponent()
            .path
        var isDirectory: ObjCBool = false
        guard fileManager.fileExists(atPath: outputDirectory, isDirectory: &isDirectory), isDirectory.boolValue else {
            throw SwiftBindingAdapterError.outputDirectoryNotFound(outputDirectory)
        }

        return FileBoundaryValidation(
            inputPath: inputPath,
            outputPath: outputPath,
            outputDirectory: outputDirectory
        )
    }

    public static func isoDateToday() -> String {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withFullDate]
        return formatter.string(from: Date())
    }
}

// MARK: - Concrete CLI process adapter

public struct CLIInvocation: Sendable, Equatable {
    public var executablePath: String
    public var arguments: [String]

    public init(executablePath: String, arguments: [String]) {
        self.executablePath = executablePath
        self.arguments = arguments
    }
}

public struct CLIProcessBindingAdapter: BindingAdapter {
    public typealias CommandBuilder = @Sendable (SwiftBindingRequest) throws -> CLIInvocation

    private let commandBuilder: CommandBuilder
    private let fileBoundary: FileBoundaryBindingAdapter
    private let validationDate: @Sendable () -> String

    public init(
        commandBuilder: @escaping CommandBuilder,
        fileBoundary: FileBoundaryBindingAdapter = FileBoundaryBindingAdapter(),
        validationDate: @escaping @Sendable () -> String = { FileBoundaryBindingAdapter.isoDateToday() }
    ) {
        self.commandBuilder = commandBuilder
        self.fileBoundary = fileBoundary
        self.validationDate = validationDate
    }

    public init(
        executablePath: String,
        baseArguments: [String] = ["-m", "nwau_py.cli.main"],
        fileBoundary: FileBoundaryBindingAdapter = FileBoundaryBindingAdapter(),
        validationDate: @escaping @Sendable () -> String = { FileBoundaryBindingAdapter.isoDateToday() }
    ) {
        self.init(
            commandBuilder: { request in
                let validation = try fileBoundary.validate(request: request)
                return CLIInvocation(
                    executablePath: executablePath,
                    arguments: baseArguments + Self.defaultArguments(
                        request: request,
                        inputPath: validation.inputPath,
                        outputPath: validation.outputPath
                    )
                )
            },
            fileBoundary: fileBoundary,
            validationDate: validationDate
        )
    }

    public func execute(request: SwiftBindingRequest) async throws -> SwiftBindingResponse {
        _ = try fileBoundary.validate(request: request)
        let invocation = try commandBuilder(request)
        try run(invocation: invocation)

        return SwiftBindingResponse(
            calculatorId: request.calculatorId,
            pricingYear: request.pricingYear,
            mode: SwiftBindingMode.cli.rawValue,
            success: true,
            status: "pass",
            message: "CLI process completed through the Swift binding adapter.",
            warnings: ["The Swift adapter invoked the shared CLI and did not evaluate calculator logic."],
            errors: [],
            diagnostics: Diagnostics(
                status: "pass",
                checks: [
                    DiagnosticCheck(id: "cli_process_completed", status: "pass", message: "The CLI process exited successfully."),
                    DiagnosticCheck(id: "file_boundary_validated", status: "pass", message: "Input and output paths were validated before invocation."),
                    DiagnosticCheck(id: "no_formula_duplication", status: "pass", message: "Formula execution stayed outside Swift."),
                ],
                summary: DiagnosticSummary(passed: 3, failed: 0, blocked: 0),
                notes: invocation.arguments.joined(separator: " ")
            ),
            provenance: Provenance(
                command: ([invocation.executablePath] + invocation.arguments).joined(separator: " "),
                sourceManifestPath: "contracts/swift-binding/swift-binding.contract.json",
                retrievedOn: validationDate(),
                sha256: "runtime-cli-process-invocation",
                bytes: 0
            ),
            outputPath: request.outputPath,
            fixtureGateState: "pass",
            moduleReadinessState: "ready"
        )
    }

    public static func defaultArguments(
        request: SwiftBindingRequest,
        inputPath: String,
        outputPath: String
    ) -> [String] {
        var arguments = [
            cliCommandName(for: request.calculatorId),
            inputPath,
            "--output",
            outputPath,
            "--year",
            request.pricingYear,
        ]

        if let paramsPath = request.metadata?["params_path"], !paramsPath.isEmpty {
            arguments += ["--params", paramsPath]
        }

        return arguments
    }

    public static func cliCommandName(for calculatorId: String) -> String {
        switch calculatorId {
        case "outpatients":
            return "non-admitted"
        default:
            return calculatorId
        }
    }

    private func run(invocation: CLIInvocation) throws {
        #if os(macOS)
        let process = Process()
        process.executableURL = URL(fileURLWithPath: invocation.executablePath)
        process.arguments = invocation.arguments

        let stderr = Pipe()
        process.standardError = stderr

        try process.run()
        process.waitUntilExit()

        guard process.terminationStatus == 0 else {
            let data = stderr.fileHandleForReading.readDataToEndOfFile()
            let message = String(data: data, encoding: .utf8) ?? ""
            throw SwiftBindingAdapterError.cliProcessFailed(
                exitCode: process.terminationStatus,
                stderr: message
            )
        }
        #else
        throw SwiftBindingAdapterError.cliUnavailableOnPlatform
        #endif
    }
}
