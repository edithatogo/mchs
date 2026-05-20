# GitHub live-gate operator runbook

This runbook covers the current GitHub live-gate workflows in
`microcosting_healthservices/.github/workflows/` and the evidence language in
`docs/roadmaps/release/evidence-bundle-format.md`,
`docs-site/src/content/docs/governance/release-policy.md`, and
`docs-site/src/content/docs/governance/pricing-year-validation-gates.mdx`.

## Scope

Use this guide when you need to trigger or publish one of the repository's
manual GitHub release gates:

- `release.yml`
- `publish.yml`
- `publish-mcp-registry.yml`
- `release-rust.yml`
- `slow-validation.yml`
- `release-drafter.yml`

## Secret and input map

The current workflows do not require stored NSW secrets in the repository.
They rely on GitHub-provided tokens and on operator-supplied dispatch inputs.

| Workflow item | Source in workflow | NSW value to supply | Notes |
| --- | --- | --- | --- |
| `GITHUB_TOKEN` | GitHub Actions secret context | None | GitHub injects this automatically. Do not store it in a file. |
| `GH_TOKEN` | GitHub Actions secret context | None | Used only for `gh` CLI steps in `publish.yml`; GitHub injects the same automatic token. |
| `workflow_dispatch.tag` | Manual dispatch input | Release tag such as `v0.0.0` | Required for `publish.yml`, `publish-mcp-registry.yml`, and `release-rust.yml`. |
| `workflow_dispatch` on `release.yml` | Manual dispatch, no extra input | None | The workflow can be started manually, but the normal release path is the `v*` tag push. |
| `workflow_dispatch` on `slow-validation.yml` | Manual dispatch, no extra input | None | No secrets and no inputs are required. |
| `id-token` permission | GitHub Actions permission | None | Required for OIDC-backed publishing steps; not a stored secret. |
| `attestations` permission | GitHub Actions permission | None | Required for release attestation steps; not a stored secret. |

## Dispatch checklist

1. Confirm the workflow name and the trigger path you intend to use.
2. Confirm the release tag or branch ref is correct before dispatching.
3. For tag-based workflows, use a signed `v*` tag when that is part of the release policy.
4. For manual dispatches that accept `tag`, supply the exact tag string and do not improvise a branch name.
5. Do not create repo secrets for `GITHUB_TOKEN` or `GH_TOKEN`; GitHub supplies those values automatically at runtime.
6. Keep any future NSW-owned secret names out of source control and record them only in repository secret settings, not in this repo.

## Workflow-specific notes

### `release.yml`

- Manual dispatch is allowed.
- Tag pushes matching `v*` are the normal release path.
- The workflow uses GitHub release publishing and attestations, but no custom secrets.

### `publish.yml`

- Manual dispatch accepts an optional `tag`.
- Release events publish from the tagged release automatically.
- `gh release download` and attestation verification both use the built-in GitHub token.

### `publish-mcp-registry.yml`

- Manual dispatch requires a `tag`.
- The workflow waits for the published package to appear on PyPI before registry publication.
- Authentication to the registry is done through GitHub OIDC, not a stored secret.

### `release-rust.yml`

- Manual dispatch requires a `tag`.
- The workflow produces the release evidence bundle and attaches artifacts.
- The only auth surfaces are GitHub permissions and OIDC-backed attestations.

### `slow-validation.yml`

- Manual dispatch has no inputs.
- No secrets are required.
- Use this workflow for property, mutation, and profiling checks only.

## Sanitized operator reminder

- Keep tags, approvals, and workflow names in the operator checklist.
- Keep secrets out of the repo.
- If a future live-gate adds a real repository secret, document the name here and store the value only in GitHub secret settings.
