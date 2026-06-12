# conda-forge Review Checklist

This checklist captures the maintainer follow-up required for `nwau-py==0.2.2` after the staged-recipes submission is open.

## Inputs

- Package: `nwau-py`
- Version: `0.2.2`
- Source surface: `pyproject.toml`
- Staged-recipes PR: `https://github.com/conda-forge/staged-recipes/pull/33452`
- Current branch: `edithatogo/staged-recipes:add-nwau-py-0.2.2`

## Required steps

1. Monitor the staged-recipes PR for maintainer comments or bot feedback.
2. Keep the recipe aligned with the checked-in `packaging/conda-forge/meta.yaml`.
3. Re-run or reference the staged-recipes validation jobs after each change.
4. Apply any requested recipe fixes, then push the updated branch.
5. Record the merge or feedstock publication evidence once the PR is accepted.
6. Verify the feedstock and package page expose version `0.2.2`.

## Evidence to record

- PR comments or maintainer requests
- Updated branch head SHA
- Check results from staged-recipes CI
- Merge commit or feedstock URL
- Public conda-forge package page for `nwau-py==0.2.2`

## Completion rule

Do not mark the track complete until the staged-recipes PR is merged and the resulting feedstock publicly exposes `0.2.2`.
