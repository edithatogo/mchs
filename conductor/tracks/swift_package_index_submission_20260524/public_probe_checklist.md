# Swift Package Index Public Probe Checklist

This checklist captures the follow-up steps required to finish `MCHSBind@0.1.0` once the upstream submission is already complete.

## Inputs

- Package: `MCHSBind`
- Version: `0.1.0`
- Local surface: `bindings/swift/Package.swift`
- Public repository: `https://github.com/edithatogo/mchs-swift.git`
- GitHub release: `https://github.com/edithatogo/mchs-swift/releases/tag/v0.1.0`

## Required steps

1. Confirm the PackageList issue remains closed as completed.
2. Probe the public Swift Package Index page for `https://swiftpackageindex.com/edithatogo/mchs-swift`.
3. Verify the page exposes package name `MCHSBind` and version `0.1.0`.
4. Record the HTTP status, page contents, or screenshot evidence from the public probe.
5. If the page still returns 403/404 or otherwise hides the package version, record that as the current blocker rather than claiming publication.

## Evidence to record

- Public probe URL and response status
- Version evidence for `0.1.0`
- Screenshot or page extract showing the package entry
- Any Cloudflare or access-blocking response that prevents version visibility

## Completion rule

Do not mark the track complete until the public Swift Package Index page exposes version `0.1.0` or the registry provides accepted-review evidence that makes the version visible.
