# Specification: GitHub Pages Public Demo Readiness

## Goal

Document a static-hostable, demo-only web app posture that demonstrates calculator workflows using synthetic fixtures and the public calculator contract, while keeping all real-data workflows outside GitHub Pages behind a secure service boundary.

## Requirements

- The app must be safe for GitHub Pages static hosting.
- GitHub Pages must be demo-only and must not require, encourage, or accept real patient data.
- Calculator capability metadata and the public API contract should drive UI options, form validation, and available calculator/year combinations.
- The app should use golden fixtures or sample datasets for demonstrations.
- Any future real-data workflow must be routed through a documented secured service boundary, not through the Pages-hosted demo.
- Demo data, fixture packs, and UI examples must be traceable back to the shared golden-fixture contract.

## Acceptance Criteria

- A public demo architecture is documented before UI implementation.
- Privacy and data-governance warnings are embedded in workflow design, not bolted on later.
- The app can be deployed to GitHub Pages without server dependencies for demo use.
- The real-data path is explicitly documented as a separate, secured service boundary and is not presented as a GitHub Pages capability.
- The demo UI can be driven from public contract metadata and shared golden fixtures.
