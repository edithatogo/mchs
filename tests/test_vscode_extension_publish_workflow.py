from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish-vscode-extension.yml"


def test_vscode_extension_publish_workflow_is_fail_closed() -> None:
    text = WORKFLOW.read_text()

    assert "workflow_dispatch:" in text
    assert "dry_run:" in text
    assert "default: true" in text
    assert "OVSX_PAT: ${{ secrets.OVSX_PAT }}" in text
    assert "VSCE_PAT: ${{ secrets.VSCE_PAT }}" in text
    assert "Missing required secret: OVSX_PAT" in text
    assert "Missing required secret: VSCE_PAT" in text


def test_vscode_extension_publish_workflow_packages_before_publish() -> None:
    text = WORKFLOW.read_text()

    package_step = text.index("Package VSIX")
    openvsx_step = text.index("Publish to Open VSX")
    marketplace_step = text.index("Publish to Visual Studio Marketplace")

    assert package_step < openvsx_step
    assert package_step < marketplace_step
    assert "vsce package --no-dependencies --out mchs-tools.vsix" in text
    assert "ovsx publish mchs-tools.vsix --pat" in text
    assert "vsce publish --packagePath mchs-tools.vsix --pat" in text
