package io.github.edithatogo.mchs;

/**
 * Minimal JVM binding marker for MCHS/NWAU interoperability.
 *
 * <p>This package intentionally does not duplicate calculator formula logic.
 * It provides a stable artifact coordinate and documentation surface for future
 * JVM adapters around the repository's contract, CLI, or service boundaries.</p>
 */
public final class MchsBinding {
    public static final String VERSION = "0.1.0";

    private MchsBinding() {
    }

    public static String registryStatusContractPath() {
        return "contracts/language-registry-submissions/language-registry-submissions.contract.json";
    }
}
