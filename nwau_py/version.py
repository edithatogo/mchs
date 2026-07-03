"""Runtime package version helpers."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

_DISTRIBUTION_NAME = "nwau_py"
_FALLBACK_VERSION = "0.0.0+local"


def get_version() -> str:
    """Return the installed or source-tree package version."""
    try:
        return version(_DISTRIBUTION_NAME)
    except PackageNotFoundError:
        pass

    try:
        from setuptools_scm import get_version as get_scm_version
    except ImportError:
        return _FALLBACK_VERSION

    try:
        return get_scm_version(
            root="..",
            relative_to=__file__,
            fallback_version=_FALLBACK_VERSION,
        )
    except (LookupError, OSError):
        return _FALLBACK_VERSION


__version__ = get_version()
