package io.github.edithatogo.mchs

import kotlin.io.path.createTempFile
import kotlin.io.path.exists
import kotlin.test.Test
import kotlin.test.assertContains
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertTrue

class ContractBoundaryTest {
    @Test
    fun exposesConcreteMavenAndContractBoundaryMetadata() {
        val metadata = ContractBoundary.metadata()

        assertEquals("io.github.edithatogo:mchs-jvm-bindings:0.1.0", metadata.packageCoordinate)
        assertEquals("1.0", metadata.contractVersion)
        assertContains(metadata.supportedCalculators, "acute")
        assertContains(metadata.publicContractFields, "calculator_id")
        assertEquals(
            setOf(TransportMode.CLI_FILE, TransportMode.SERVICE_HTTP),
            metadata.transports.map { it.mode }.toSet(),
        )
        assertContains(metadata.formulaLogicPolicy, "shared core")
    }

    @Test
    fun validatesFileBoundaryAndDelegatesExecution() {
        val input = createTempFile(prefix = "mchs-jvm-input", suffix = ".json")
        val output = input.parent.resolve("nested").resolve("response.json")
        val adapter = JvmFileBoundaryAdapter()

        val response = adapter.execute(
            JvmBindingRequest(
                calculatorId = "acute",
                pricingYear = "2026-27",
                inputPath = input,
                outputPath = output,
            ),
        )

        assertTrue(output.parent.exists())
        assertTrue(response.success)
        assertEquals("boundary_validated_pending_shared_core_execution", response.status)
        assertEquals(DiagnosticSeverity.INFO, response.diagnostics.single().severity)
        assertContains(response.warnings.single(), "shared core")
    }

    @Test
    fun rejectsUnsupportedCalculatorBeforeSharedCoreExecution() {
        val input = createTempFile(prefix = "mchs-jvm-input", suffix = ".json")
        val adapter = JvmFileBoundaryAdapter()

        val error = assertFailsWith<BoundaryValidationException> {
            adapter.execute(
                JvmBindingRequest(
                    calculatorId = "private_calculator",
                    pricingYear = "2026-27",
                    inputPath = input,
                    outputPath = input.parent.resolve("response.json"),
                ),
            )
        }

        assertContains(error.message.orEmpty(), "Unsupported calculator_id")
    }
}
