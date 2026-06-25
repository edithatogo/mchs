# Review: VS Code/Open VSX Extension Submission

## Status

Reviewed on 2026-06-25. Archive eligible as a published-verified registry
track.

## Scope Reviewed

- Open VSX API exposes namespace `edithatogo`, extension `mchs-tools`, latest
  version `0.1.1`, and versions `0.1.0`, `0.1.1`, and `latest`.
- Visual Studio Marketplace Gallery API exposes public extension
  `edithatogo.mchs-tools` version `0.1.1`.
- Track evidence records package artifacts, marketplace sync artifact, publisher
  identifiers, VSIX checksums, and token cleanup.
- README registry status was corrected from prepared/not-published to published.

## Findings

- No Open VSX or Marketplace publication blocker remains for `0.1.1`.
- Future extension releases require new API evidence and token cleanup.
- This track proves extension publication only; it does not expand calculator
  runtime support.

## Validation

- `python` Open VSX API probe for `https://open-vsx.org/api/edithatogo/mchs-tools`
- `python` Visual Studio Marketplace Gallery `extensionquery` probe
- `uv run pytest tests/test_vscode_openvsx_extension_surface.py tests/test_remaining_language_registry_submission_tracks.py -k "vscode or external_submission_runbook_matches_current_go_and_swift_states or external_only_runbook_has_exact_next_action_checklists"`
- `python scripts/validate_language_registry_submission_tracks.py`
- `python conductor/scripts/stub_detector.py --root . --json`
