# Release Boundary Control Plane

## Purpose

Release status is governed per package surface. Public docs, README tables,
Conductor metadata, and registry reports must not claim publication, support, or
readiness unless the package surface registry records matching evidence.

## Boundary Fields

Each package surface records:

- release target;
- release workflow or manual submission path;
- version source;
- registry state;
- immutable evidence paths or public URLs;
- external gate class;
- support status;
- claim boundary.

## Registry States

- `not_applicable`: no registry publication applies.
- `prepared`: local package artifacts or manifests exist, but no submission is
  complete.
- `submitted`: submission is external and waiting on a maintainer, account,
  reviewer, scheduler, propagation, or registry action.
- `published_verified`: public registry evidence exists.
- `blocked`: a named external or local blocker prevents submission or proof.

## Claim Rules

- Publication claims require immutable evidence.
- Submitted or blocked states must name the remaining external gate.
- Local readiness and registry publication are separate claims.
- A package can be implemented and still unpublished.
- A registry can be submitted and still not publicly installable.
- Adapter surfaces must describe support scope without duplicating formula
  behavior.

## Validation

`scripts/validate_repository_topology.py` validates the static release boundary
fields. Live registry proof remains in registry-specific validation scripts.
