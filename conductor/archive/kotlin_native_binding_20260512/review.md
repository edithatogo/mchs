# Review: Kotlin/Native Binding

## Findings

1. Resolved - The track metadata points to the live synthetic contract bundle
   at `contracts/kotlin-native-binding/kotlin-native-binding.contract.json`.
2. Resolved - The track includes fixture-backed tests, live contract examples,
   and a Kotlin/Native file-boundary adapter.
3. Resolved - The roadmap and governance docs choose Kotlin/Native over C ABI
   plus Arrow/Parquet file interop, with service fallback. Java/JVM integration
   is deferred outside this track.

## Blockers

- None for the Kotlin-first roadmap/prototype scope.

## Changed files

- `microcosting_healthservices/conductor/archive/kotlin_native_binding_20260512/review.md`

## Validation

- The initial review was document-only; the integration pass adds contract,
  fixture, Kotlin adapter, Starlight, JSON, and focused test validation.

## Risks

- The Kotlin adapter is transport-only and does not invoke a real calculator
  backend yet.
- Kotlin/Native artifact publication remains gated until reproducible packaging
  and native runtime matrices exist.
- Formula behavior remains owned by the shared core; Kotlin/Native stays an
  adapter surface.
