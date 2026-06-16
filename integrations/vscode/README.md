# MCHS Tools

MCHS Tools is a lightweight VS Code helper for the repository's registry-gate workflow. The `0.1.1` extension publication is verified on Visual Studio Marketplace and Open VSX; the canonical `0.1.0` publication remains available through Open VSX.

## Commands

- `MCHS: Show Registry Status` reads `contracts/language-registry-submissions/language-registry-submissions.contract.json` from the open MCHS workspace and shows the VS Code/Open VSX gate status in an output channel.
- `MCHS: Open Language Registry Contract` opens the checked-in registry submission contract.
- `MCHS: Open External Gate Roadmap` opens `docs/roadmaps/language-registry-external-gates.md`.
- `MCHS: Copy Open VSX Publish Command` copies the gated `ovsx publish` command for the local `.vsix` artifact.

## Publication Gates

The package is published on Visual Studio Marketplace as `edithatogo.mchs-tools@0.1.1`. Open VSX also exposes `edithatogo.mchs-tools@0.1.0`; its latest public version is `0.1.1`.

The local package metadata and copied publish command target `0.1.1`. The prepared local Marketplace-sync artifact is `mchs-tools-0.1.1.vsix`; the public Marketplace Gallery API also reports `0.1.1`, so latest-version synchronization is complete.
