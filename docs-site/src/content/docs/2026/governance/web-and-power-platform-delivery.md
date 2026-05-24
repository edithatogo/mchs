---
title: Web and Power Platform delivery
slug: 2026/governance/web-and-power-platform-delivery
---

GitHub Pages, TypeScript/WASM demos, Streamlit, and Power Platform are delivery
surfaces over the shared calculator contract. They do not own calculator math.

Rules:

* GitHub Pages stays static-first and synthetic/demo-only.
* TypeScript/WASM can support browser demos, but only with committed fixtures
  and shared contract metadata.
* Streamlit is a Python-hosted analyst surface for local or demo workflows.
* Power Platform remains orchestration-only through a secure service boundary
  or custom connector.
* Real-data workflows stay outside browser-hosted demo shells.

See the canonical source in [ADR 0005](../../../../../../docs/adr/0005-web-and-power-platform-delivery.md).
