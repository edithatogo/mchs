# Swift Package Index Public Probe Checklist

This checklist records the completed follow-up evidence for `MCHSBind@0.1.0` after the upstream PackageList submission was merged.

## Inputs

- Package: `MCHSBind`
- Version: `0.1.0`
- Local surface: `bindings/swift/Package.swift`
- Public repository: `https://github.com/edithatogo/mchs-swift.git`
- GitHub release: `https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0`

## Completed steps

1. Confirmed the PackageList issue remains closed as completed.
2. Confirmed PackageList PR `https://github.com/SwiftPackageIndex/PackageList/pull/13999` merged at `2026-06-12T12:02:16Z`.
3. Probed the public Swift Package Index page for `https://swiftpackageindex.com/edithatogo/mchs-swift`.
4. Verified the page exposes package name `MCHSBind`, repository `edithatogo/mchs-swift`, stable version `v0.1.0`, the SPM manifest snippet using `from: "0.1.0"`, and the GitHub release link.
5. Recorded the HTTP status and page evidence in the track metadata, spec, runbook, and registry contract.

## Evidence to record

- Public probe URL and response status: `https://swiftpackageindex.com/edithatogo/mchs-swift` returned HTTP 200 on 2026-06-12.
- Previous pending-publication probes were treated as unresolved while the page returned `403/404`-style inaccessible or missing states; the current HTTP 200 probe supersedes those blockers.
- Version evidence: page includes stable `v0.1.0` and a SwiftPM manifest snippet with `from: "0.1.0"`.
- Package evidence: page title and package heading identify `MCHSBind`; canonical links identify `edithatogo/mchs-swift`.
- Release evidence: page links to `https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0`.

## Completion rule

The public Swift Package Index page exposes version `0.1.0`, so this checklist is complete.
