# Power Platform SOTA and Preview Capability Roadmap

## Position

The current Power Platform surface is ALM-ready as a managed solution shell and
repo-governed subrepo boundary. It is not yet production-runtime-ready because
connection references, a production service endpoint, and app/flow smoke
evidence are still missing.

Preview or bleeding-edge capabilities must be added behind explicit feature
flags, environment eligibility checks, and rollback notes. They must not replace
the stable managed-solution import path until they are available in NSW and have
repeatable evidence.

## Stable Baseline

- Keep `pac solution pack`, `pac solution check`, and managed import as the
  reproducible release path.
- Keep Power Platform apps and flows orchestration-only.
- Keep all calculator logic behind the approved service boundary.
- Use managed solutions for target environments.
- Keep source control as the single source of truth.

## Warranted Near-Term Changes

1. Native Power Platform Pipelines integration.
   - Add `pac pipeline` discovery and deployment notes once NSW pipeline host
     configuration is available.
   - Use pipelines for environment-variable and connection-reference validation
     before deployment.
   - Keep GitHub Actions as the source-level validation gate.

2. Playwright-based Power Apps runtime smoke tests.
   - Do not build new work on deprecated Test Engine assumptions.
   - Add browser smoke coverage for app launch, connector consent surface, happy
     path calculation submission, failure handling, and evidence export.

3. Code Apps evaluation track.
   - Evaluate Power Apps code apps for the orchestration UI when the app needs
     custom React-grade UX, Entra auth, connector calls from JavaScript, and
     managed hosting.
   - Do not adopt until NSW admins enable code apps and licensing is confirmed.
   - Keep Canvas or model-driven app manifests as the stable fallback.

4. Copilot Studio real-time connector knowledge.
   - Expose the service-boundary connector as a real-time knowledge/action
     candidate for up-to-date calculation metadata and operational status.
   - Do not replicate private NSW data into Microsoft 365 Graph for this use
     case unless a separate governance decision approves it.

5. Dataverse MCP server readiness.
   - Track Dataverse MCP server configuration as an admin-enabled capability for
     developer and agent workflows.
   - Do not allow external AI clients until Managed Environment status, allowed
     clients, connector policies, and Copilot credit/billing implications are
     approved.

6. Agentic governance and observability.
   - Add evidence fields for DLP policy, connector policy, Managed Environment
     state, solution checker result, import result, app health metrics, and flow
     run outcomes.
   - Treat autonomous agents as audited actors with least-privilege roles.

## Explicit Non-Adoptions

- Do not move calculator formulas into Power Apps, flows, Dataverse plug-ins, or
  Copilot prompts.
- Do not claim production readiness from preview capability availability.
- Do not use a broken gitlink or undocumented checkout as subrepo evidence.
- Do not use Test Engine as the strategic test investment when current Microsoft
  docs mark that ALM page deprecated.

## Adoption Gates

- NSW tenant feature availability is confirmed.
- Admin opt-in and licensing are recorded.
- DLP and connector policies permit the capability.
- Managed solution import continues to pass.
- Runtime smoke evidence is attached to the deployment evidence bundle.
- Rollback is documented and tested for the affected capability.

## Microsoft Documentation Basis

- Power Platform 2026 release wave 1: Dataverse APIs, MCP servers, Python SDK,
  Work IQ, agent governance, and Copilot/Power Platform administration updates.
- Power Platform 2025 release wave 2: agent collaboration, advanced approvals,
  generative actions, Dataverse MCP server, AI-powered business logic, and
  governance administration.
- Power Apps code apps: code-first managed Power Apps hosting with Entra auth,
  connector access, managed policy support, and current limitations.
- Power Platform Pipelines: native Microsoft-supported ALM with CLI extension,
  prevalidation, connection references, environment variables, and managed
  environment support.
- Copilot Studio connector knowledge: use Power Platform connectors for
  real-time transactional knowledge and actions without data replication.
