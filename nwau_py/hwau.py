"""HWAU/NWAU terminology compatibility helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

__all__ = ["normalize_hwau_result"]


def normalize_hwau_result(result: Mapping[str, Any]) -> dict[str, Any]:
    """Return a result payload with generic HWAU and compatible NWAU aliases.

    ``hwau`` is the generic library field. ``nwau`` is retained for Australian
    National Weighted Activity Unit source terminology and existing clients.
    If both aliases are present, they must carry the same value.
    """

    normalized = dict(result)
    has_hwau = "hwau" in normalized
    has_nwau = "nwau" in normalized

    if has_hwau and has_nwau and normalized["hwau"] != normalized["nwau"]:
        raise ValueError("conflicting HWAU/NWAU aliases in result payload")
    if has_hwau and not has_nwau:
        normalized["nwau"] = normalized["hwau"]
    if has_nwau and not has_hwau:
        normalized["hwau"] = normalized["nwau"]
    return normalized
