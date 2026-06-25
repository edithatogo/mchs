import Foundation
import MCHSBind

func require(_ condition: @autoclosure () -> Bool, _ message: String) {
    if !condition() {
        fatalError(message)
    }
}

let temporaryDirectory = URL(fileURLWithPath: NSTemporaryDirectory())
    .appendingPathComponent(UUID().uuidString, isDirectory: true)
try FileManager.default.createDirectory(
    at: temporaryDirectory,
    withIntermediateDirectories: true
)
defer { try? FileManager.default.removeItem(at: temporaryDirectory) }

let input = temporaryDirectory.appendingPathComponent("input.csv")
let output = temporaryDirectory.appendingPathComponent("output.csv")
try "DRG,LOS\nA01A,1\n".write(to: input, atomically: true, encoding: .utf8)

let fileRequest = SwiftBindingRequest(
    calculatorId: "acute",
    pricingYear: "2025",
    inputSchemaVersion: "1.0",
    outputSchemaVersion: "1.0",
    mode: "file-exchange",
    inputPath: input.path,
    outputPath: output.path,
    fixtureGate: "synthetic_only_examples"
)

let fileAdapter = FileBoundaryBindingAdapter(validationDate: { "2026-05-26" })
let fileResponse = try await fileAdapter.execute(request: fileRequest)
require(!fileResponse.success, "file boundary validation should not claim calculator execution")
require(fileResponse.status == "boundary_validated", "file boundary response should report validation-only status")
require(fileResponse.outputPath == output.path, "file boundary output path should echo")
require(fileResponse.diagnostics.summary.passed == 3, "file boundary diagnostics should pass path checks")
require(fileResponse.diagnostics.summary.blocked == 1, "file boundary diagnostics should block calculator-result claims")

let cliRequest = SwiftBindingRequest(
    calculatorId: "outpatients",
    pricingYear: "2025",
    inputSchemaVersion: "1.0",
    outputSchemaVersion: "1.0",
    mode: "cli",
    inputPath: input.path,
    outputPath: output.path,
    metadata: ["params_path": "tests/data/2025"],
    fixtureGate: "synthetic_only_examples"
)

let defaultArguments = CLIProcessBindingAdapter.defaultArguments(
    request: cliRequest,
    inputPath: input.path,
    outputPath: output.path
)
require(defaultArguments.first == "non-admitted", "outpatients should map to non-admitted CLI command")
require(defaultArguments.suffix(2) == ["--params", "tests/data/2025"], "params metadata should be passed through")

#if os(macOS)
let cliAdapter = CLIProcessBindingAdapter(
    commandBuilder: { request in
        CLIInvocation(
            executablePath: "/bin/sh",
            arguments: ["-c", "printf 'ok\\n' > '\(request.outputPath ?? "")'"]
        )
    },
    validationDate: { "2026-05-26" }
)
let cliResponse = try await cliAdapter.execute(request: cliRequest)
require(cliResponse.success, "cli response should pass")
require(cliResponse.mode == "cli", "cli response should report cli mode")
let cliOutput = try String(contentsOf: output, encoding: .utf8)
require(cliOutput == "ok\n", "cli process should write output")
#endif

print("swift binding smoke passed")
