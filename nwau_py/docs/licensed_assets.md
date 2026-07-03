# Licensed Asset Registry

The repository keeps licensed IHACPA, ICD-10-AM, ACHI, ACS, mapping, and
grouper assets out of version control. Public metadata can be committed, but
restricted content stays in ignored local storage under
`archive/ihacpa/raw/`.

## Registry workflow

Use the `licensed-assets` CLI group to manage the local-only manifest:

```bash
python -m nwau_py.cli.main licensed-assets register --help
python -m nwau_py.cli.main licensed-assets validate --help
python -m nwau_py.cli.main licensed-assets doctor --help
python -m nwau_py.cli.main licensed-assets audit --help
```

The manifest is a JSON file at
`archive/ihacpa/raw/licensed-assets.manifest.json`. It is intentionally kept
under the ignored raw-asset tree so it does not become a tracked repository
artifact.

## Status vocabulary

- `validated`: the manifest is structurally valid and the required local assets
  are present.
- `blocked_licensed`: the manifest is missing, invalid, or the required local
  assets are absent.

## Guard behavior

The audit script and CLI guard reject committed files that look like restricted
licensed assets, including common office, archive, and statistical bundle
extensions. They do not inspect or expose restricted contents.

The command-line audit entry point is `scripts/validate_licensed_assets.py`.

