---
title: Web and Power Platform delivery
---

GitHub Pages, TypeScript/WASM demos, Streamlit, and Power Platform are delivery
surfaces over the shared calculator contract. They do not own calculator math.

Rules:

- GitHub Pages stays static-first and synthetic/demo-only.
- TypeScript/WASM can support browser demos, but only with committed fixtures
  and shared contract metadata.
- Streamlit is a Python-hosted analyst surface for local or demo workflows.
- Power Platform remains orchestration-only through a secure service boundary
  or custom connector.
- Real-data workflows stay outside browser-hosted demo shells.

For Power Platform deployments, use the NSW readiness templates and managed
promotion runbooks under:

- `power-platform/deployment/nsw-deployment-readiness-template.md`
- `power-platform/deployment/nsw-managed-solution-promotion-runbook.md`
- `power-platform/evidence/nsw-operational-readiness-bundle-template.json`

NSW production deployment readiness is not yet claimed. Deployments remain
`blocked` until tenant credentials, managed import evidence, and rollback
verification are present.

See the canonical source in [ADR 0005](../../../../../docs/adr/0005-web-and-power-platform-delivery.md).
