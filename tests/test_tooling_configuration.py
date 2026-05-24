from __future__ import annotations

from pathlib import Path

try:
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    import tomli as tomllib  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
PROJECT_FILE = ROOT / "pyproject.toml"
LOCK_FILE = ROOT / "uv.lock"
CODECOV_FILE = ROOT / ".github" / "codecov.yml"
PR_CI_WORKFLOW_FILE = ROOT / ".github" / "workflows" / "pr-ci.yml"
PRE_COMMIT_FILE = ROOT / ".pre-commit-config.yaml"
SLOW_VALIDATION_WORKFLOW_FILE = ROOT / ".github" / "workflows" / "slow-validation.yml"
RELEASE_DRAFTER_FILE = ROOT / ".github" / "release-drafter.yml"
RELEASE_DRAFTER_WORKFLOW_FILE = ROOT / ".github" / "workflows" / "release-drafter.yml"
RELEASE_WORKFLOW_FILE = ROOT / ".github" / "workflows" / "release.yml"
PUBLISH_WORKFLOW_FILE = ROOT / ".github" / "workflows" / "publish.yml"
TY_FILE = ROOT / "ty.toml"
MYPY_FILE = ROOT / "mypy.ini"
ROOT_README_FILE = ROOT / "README.md"
DEVELOPMENT_FILE = ROOT / "DEVELOPMENT.md"
PACKAGE_README_FILE = ROOT / "nwau_py" / "README.md"
CONDUCTOR_WORKFLOW_FILE = ROOT / "conductor" / "workflow.md"

EXPECTED_GROUP_PACKAGES = {
    "dev": {"ruff"},
    "test": {"pytest"},
    "coverage": {"pytest-cov"},
    "typing": {"ty"},
    "property": {"hypothesis"},
    "mutation": {"mutmut"},
    "profiling": {"scalene"},
    "docs": {"vale"},
}


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_pyproject_declares_the_expected_dependency_groups():
    project = _load_toml(PROJECT_FILE)["dependency-groups"]
    assert isinstance(project, dict)

    for group_name, expected_packages in EXPECTED_GROUP_PACKAGES.items():
        group_packages = set(project[group_name])
        assert expected_packages.issubset(group_packages)


def test_pyproject_supports_python_310_through_314():
    project = _load_toml(PROJECT_FILE)["project"]
    assert isinstance(project, dict)
    assert project["requires-python"] == ">=3.10,<3.15"


def test_uv_lock_records_the_supported_python_window_and_tooling_packages():
    lock = _load_toml(LOCK_FILE)
    packages = {package["name"] for package in lock["package"]}
    resolution_markers = lock["resolution-markers"]

    assert lock["requires-python"] == ">=3.10, <3.15"
    assert EXPECTED_GROUP_PACKAGES["dev"].issubset(packages)
    assert EXPECTED_GROUP_PACKAGES["test"].issubset(packages)
    assert EXPECTED_GROUP_PACKAGES["coverage"].issubset(packages)
    assert EXPECTED_GROUP_PACKAGES["typing"].issubset(packages)
    assert EXPECTED_GROUP_PACKAGES["property"].issubset(packages)
    assert EXPECTED_GROUP_PACKAGES["mutation"].issubset(packages)
    assert EXPECTED_GROUP_PACKAGES["profiling"].issubset(packages)
    assert EXPECTED_GROUP_PACKAGES["docs"].issubset(packages)

    assert any(
        "python_full_version < '3.11'" in marker for marker in resolution_markers
    )
    assert any(
        "python_full_version >= '3.11' and python_full_version < '3.13'" in marker
        for marker in resolution_markers
    )
    assert any(
        "python_full_version == '3.13.*'" in marker for marker in resolution_markers
    )
    assert any(
        "python_full_version >= '3.14'" in marker for marker in resolution_markers
    )


def test_codecov_configuration_pins_the_current_coverage_contract():
    codecov = _read_text(CODECOV_FILE)

    assert "coverage:" in codecov
    assert "range: 80..100" in codecov
    assert "round: down" in codecov
    assert "precision: 2" in codecov


def test_ty_toml_matches_the_current_top_level_shape():
    ty_config = _load_toml(TY_FILE)

    assert set(ty_config) == {"environment", "src", "analysis"}

    environment = ty_config["environment"]
    assert isinstance(environment, dict)
    assert environment["python-version"] == "3.11"
    assert environment["root"] == [".", "./src", "./excel_calculator/src"]

    src = ty_config["src"]
    assert isinstance(src, dict)
    assert src["include"] == ["nwau_py", "src", "excel_calculator/src"]

    analysis = ty_config["analysis"]
    assert isinstance(analysis, dict)
    assert analysis["replace-imports-with-any"] == [
        "pandas.**",
        "numpy.**",
        "pyreadstat.**",
        "lightgbm.**",
    ]


def test_pr_ci_workflow_runs_the_expected_quality_and_test_sequence():
    workflow = _read_text(PR_CI_WORKFLOW_FILE)

    assert 'python-version: "3.11"' in workflow
    assert "branches:" in workflow
    assert "      - master" in workflow
    assert "      - main" not in workflow
    assert '  - "3.10"' in workflow
    assert '  - "3.14"' in workflow
    assert "run: uv sync --locked" in workflow
    assert "Phase 1 quality checks (Python 3.11)" in workflow
    assert "Phase 2 tests (Python ${{ matrix.python-version }})" in workflow
    assert "Phase 3 coverage and Codecov (Python 3.11)" in workflow
    assert "Phase 3 Rust checks" in workflow
    assert "run: uv run ruff format --check ." in workflow
    assert "run: uv run ruff check ." in workflow
    assert "run: uv run ty check" in workflow
    assert "run: uv run pytest" in workflow
    assert "cargo fmt --all --check" in workflow
    assert "cargo clippy --all-targets --all-features -- -D warnings" in workflow
    assert "cargo test" in workflow
    assert (
        "run: uv run --with pytest --with pytest-cov pytest --cov=nwau_py"
        not in workflow
    )
    assert "run: uv run pytest --cov=nwau_py --cov-report=term-missing" in workflow

    assert workflow.index("Sync environment") < workflow.index("Check formatting")
    assert workflow.index("Check formatting") < workflow.index("Run lint")
    assert workflow.index("Run lint") < workflow.index("Run type check")
    assert workflow.index("Run type check") < workflow.index("Run tests")
    assert workflow.index("Run tests") < workflow.index("Run coverage")


def test_pre_commit_configuration_matches_the_current_python_quality_gate():
    config = _read_text(PRE_COMMIT_FILE)

    assert "repo: local" in config
    assert "uv run ruff format --check ." in config
    assert "uv run ruff check ." in config
    assert "uv run ty check" in config
    assert "uv run pytest" in config
    assert "cargo fmt --manifest-path rust/Cargo.toml --all --check" in config
    assert "cargo clippy --manifest-path rust/Cargo.toml --all-targets" in config
    assert "cargo test --manifest-path rust/Cargo.toml" in config
    assert "uv run --with vale vale conductor README.md docs" in config
    assert "pre-commit/mirrors-mypy" not in config
    assert "mypy" not in config


def test_slow_validation_workflow_uses_the_expected_uv_group_commands():
    workflow = _read_text(SLOW_VALIDATION_WORKFLOW_FILE)
    scalene_command = (
        "run: mkdir -p .cache/validation/scalene && uv run scalene run --cli "
        "--outfile .cache/validation/scalene/scalene.out --html python -m pytest"
    )

    assert "schedule:" in workflow
    assert '    - cron: "0 3 * * 0"' in workflow
    assert "run: uv sync --locked --group test --group property" in workflow
    assert "run: uv sync --locked --group test --group mutation" in workflow
    assert "run: uv sync --locked --group test --group profiling" in workflow
    assert "run: uv run pytest" in workflow
    assert "run: uv run mutmut run" in workflow
    assert scalene_command in workflow

    assert workflow.index("Property checks") < workflow.index(
        "Run property-focused tests"
    )
    assert workflow.index("Mutation checks") < workflow.index("Run mutmut")
    assert workflow.index("Profiling checks") < workflow.index("Run Scalene profiling")


def test_release_drafter_configuration_defines_tagged_release_notes():
    config = _read_text(RELEASE_DRAFTER_FILE)

    assert 'name-template: "nwau_py v$RESOLVED_VERSION"' in config
    assert 'tag-template: "v$RESOLVED_VERSION"' in config
    assert "release" in config
    assert "Validation expectations" in config
    assert "skip-changelog" in config


def test_release_drafter_workflow_updates_drafts_on_master_pushes():
    workflow = _read_text(RELEASE_DRAFTER_WORKFLOW_FILE)

    assert "Release Drafter" in workflow
    assert "branches:" in workflow
    assert "      - master" in workflow
    assert "release-drafter/release-drafter@v7" in workflow
    assert "config-name: release-drafter.yml" in workflow


def test_release_workflow_builds_and_publishes_tagged_releases():
    workflow = _read_text(RELEASE_WORKFLOW_FILE)

    assert "Release" in workflow
    assert '      - "v*"' in workflow
    assert "contents: write" in workflow
    assert "uv build" in workflow
    assert "actions/upload-artifact@v6" in workflow
    assert "softprops/action-gh-release@v3" in workflow
    assert "generate_release_notes: true" in workflow


def test_publish_workflow_builds_and_pushes_the_python_distribution():
    workflow = _read_text(PUBLISH_WORKFLOW_FILE)

    assert "Publish Python package" in workflow
    assert '      - "v*"' in workflow
    assert "id-token: write" in workflow
    assert "uv build" in workflow
    assert "pypa/gh-action-pypi-publish@release/v1" in workflow


def test_conductor_workflow_documents_the_target_uv_command_sequence():
    workflow = _read_text(CONDUCTOR_WORKFLOW_FILE)
    normalized = " ".join(workflow.split())
    coverage_command = (
        "uv run pytest --cov=nwau_py --cov-report=term-missing --cov-report=xml"
    )

    assert (
        "uv sync --locked --group dev --group test --group coverage --group typing "
        "--group property --group mutation --group profiling --group docs" in workflow
    )
    assert "conductor-review" in workflow
    assert "manual verification" not in workflow.lower()
    assert "user confirmation" not in workflow.lower()
    assert "Do not pause for manual confirmation" in workflow
    assert (
        "automatically continue with the next incomplete task or next track"
        in normalized
    )
    assert "uv run ruff format --check ." in workflow
    assert "uv run ruff check ." in workflow
    assert "uv run ty check" in workflow
    assert "uv run pytest" in workflow
    assert coverage_command in workflow
    assert "cd rust && cargo fmt --all --check" in workflow
    assert (
        "cd rust && cargo clippy --all-targets --all-features -- -D warnings"
        in workflow
    )
    assert "cd rust && cargo test" in workflow
    assert "uv run vale conductor README.md docs" in workflow


def test_development_docs_pin_the_current_tooling_contract():
    development = _read_text(DEVELOPMENT_FILE)
    root_readme = _read_text(ROOT_README_FILE)
    readme = _read_text(PACKAGE_README_FILE)
    normalized_development = " ".join(development.split())
    normalized_root_readme = " ".join(root_readme.split())
    normalized_readme = " ".join(readme.split())

    assert (
        "uv sync --locked --group dev --group test --group coverage --group typing "
        "--group property --group mutation --group profiling --group docs"
        in normalized_development
    )
    assert "uv run ty check" in normalized_development
    assert "cd rust && cargo fmt --all --check" in normalized_development
    assert (
        "cd rust && cargo clippy --all-targets --all-features -- -D warnings"
        in normalized_development
    )
    assert "cd rust && cargo test" in normalized_development
    assert "uv run --with vale vale conductor README.md docs" in normalized_development
    assert (
        "Codecov consumes the XML coverage report produced in CI"
        in normalized_development
    )

    assert (
        "uv run pytest --cov=nwau_py --cov-report=term-missing "
        "--cov-report=xml --cov-fail-under=80" in normalized_root_readme
    )

    assert (
        "uv sync --locked --group dev --group test --group coverage --group typing "
        "--group property --group mutation --group profiling --group docs"
        in normalized_readme
    )
    assert "Codecov" in normalized_readme
    assert "ty" in normalized_readme
    assert "cargo fmt --all --check" in normalized_readme
    assert (
        "cargo clippy --all-targets --all-features -- -D warnings" in normalized_readme
    )
    assert "cargo test" in normalized_readme


def test_mypy_ini_documents_the_transitional_comparator_note():
    mypy = _read_text(MYPY_FILE)

    assert "Transitional comparator only" in mypy
    assert "`mypy` is not the active checker." in mypy
    assert "migration to `ty`" in mypy
