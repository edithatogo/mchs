from __future__ import annotations

from pathlib import Path

import yaml
import yaml.resolver

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = [
    ROOT / ".github" / "workflows" / "docs-site.yml",
    ROOT / ".github" / "workflows" / "release-rust.yml",
]


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping_without_duplicate_keys(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[object, object]:
    seen: set[object] = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise AssertionError(f"duplicate YAML key: {key!r}")
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping_without_duplicate_keys,
)


def test_docs_and_rust_release_workflows_parse_with_unique_keys():
    for workflow in WORKFLOWS:
        parsed = yaml.load(workflow.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)

        assert isinstance(parsed, dict), workflow
        assert "name" in parsed, workflow
        assert "jobs" in parsed, workflow
        assert parsed["jobs"], workflow
