# vcpkg / ConanCenter Upstream PR Checklist

This checklist captures historical upstream review evidence for `nwau-c-abi@0.1.0`. The vcpkg / ConanCenter surface is deprecated and cancelled as of 2026-07-03.

## Inputs

- Package: `nwau-c-abi`
- Version: `0.1.0`
- Local preview surfaces:
  - `packaging/vcpkg/ports/nwau-c-abi/vcpkg.json`
  - `packaging/vcpkg/ports/nwau-c-abi/portfile.cmake`
  - `packaging/conan/conanfile.py`

## vcpkg outcome

1. PR `https://github.com/microsoft/vcpkg/pull/51965` was opened and later closed unmerged on 2026-05-26.
2. Actionable quality feedback was addressed in fork commit `58ff86fe`.
3. The remaining blocker is upstream policy, not local packaging readiness: vcpkg maintainers stated that vcpkg does not currently support building Rust libraries.
4. Keep the overlay install as local/private preview evidence only.
5. Revisit vcpkg only if upstream Rust-library support appears or the C ABI distribution is redesigned to avoid requiring vcpkg to build Rust code.

## ConanCenter historical steps

1. Fork `conan-io/conan-center-index`.
2. Add the `nwau-c-abi` recipe in the ConanCenter recipe layout expected by the repository.
3. Include a `conandata.yml` file.
   - ConanCenter treats `conandata.yml` as mandatory for its recipe format.
   - Put source and patch metadata there rather than hardcoding it in the recipe when possible.
4. Keep the recipe aligned with the validated local preview.
   - `conan inspect packaging/conan/conanfile.py` should continue to parse successfully.
   - `conan create packaging/conan --build=missing` should remain the local proof of buildability.
5. Run the ConanCenter validation path required by the fork.
6. Open a PR to `conan-io/conan-center-index`.
7. Record the PR URL, branch, validation result, and any maintainer requests in the track evidence.
8. Current PR: `https://github.com/conan-io/conan-center-index/pull/30262`.
9. Latest pushed fix: `c635b0f9d2f1619d9149e4fa964185658c063f5d` fixed test-package portability.
10. CLA/recheck gate resolved on 2026-06-12: live GitHub check shows `license/cla` success.
11. Latest live probe on 2026-06-25: PR 30262 remains open, `mergedAt=null`, `draft=False`, `mergeable=MERGEABLE`, `mergeStateStatus=BLOCKED`, `reviewDecision=REVIEW_REQUIRED`, `license/cla` success, and `Job scheduler` `ACTION_REQUIRED`; no new actionable comments appear after the 2026-06-12 author follow-up.
12. Cancelled state: PR 30262 is retained as historical evidence only; no further job scheduler, maintainer review, merge, or publication monitoring is planned unless a new track re-charters the surface.

## Completion rule

Do not mark the track complete as a publication track. The surface is deprecated and cancelled; historical evidence is retained only, and no public vcpkg or ConanCenter publication is claimed.
