# Managed Solution Promotion

MCHS Power Platform promotion uses unmanaged source in development and managed
solution artifacts downstream. Promotions require solution checker output,
approval, import logs, and smoke evidence.

## Environments

- Development: source authoring and unmanaged export.
- Test: managed import and smoke validation.
- Production/NSW: managed import only after approval.

## Rollback

Rollback requires a previous managed solution artifact, version record, import
output, and post-rollback smoke evidence.
