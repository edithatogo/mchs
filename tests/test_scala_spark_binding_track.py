from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
TRACK = ROOT / "conductor" / "archive" / "scala_spark_binding_20260513"
TRACKS_REGISTRY = ROOT / "conductor" / "tracks.md"
FIXTURE_ROOT = Path(__file__).resolve().parent / "fixtures" / "scala_spark_binding"
CONTRACT_BUNDLE = FIXTURE_ROOT / "contract_bundle.json"
CONTRACT_ROOT = ROOT / "contracts" / "scala-spark-binding"
LIVE_CONTRACT = CONTRACT_ROOT / "scala-spark-binding.contract.json"
LIVE_SCHEMA = CONTRACT_ROOT / "scala-spark-binding.schema.json"
LIVE_EXAMPLES = CONTRACT_ROOT / "examples"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    payload = json.loads(_read_text(path))
    assert isinstance(payload, dict)
    return payload


def _as_mapping(value: object) -> dict[str, Any]:
    assert isinstance(value, dict)
    return cast(dict[str, Any], value)


def _squash(text: str) -> str:
    return " ".join(text.split())


def test_scala_spark_binding_track_metadata_docs_and_contract_bundle_are_conservative():
    for path in [
        TRACK / "spec.md",
        TRACK / "plan.md",
        TRACK / "index.md",
        TRACK / "metadata.json",
        TRACKS_REGISTRY,
        CONTRACT_BUNDLE,
        LIVE_CONTRACT,
        LIVE_SCHEMA,
        LIVE_EXAMPLES / "parquet-file.pass.json",
        LIVE_EXAMPLES / "service.pass.json",
        LIVE_EXAMPLES / "sql-boundary.pass.json",
        LIVE_EXAMPLES / "binding.fail.json",
        LIVE_EXAMPLES / "diagnostics.fail.json",
        ROOT / "bindings" / "scala-spark" / "build.sbt",
        ROOT
        / "bindings"
        / "scala-spark"
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "BoundaryModels.scala",
        ROOT
        / "bindings"
        / "scala-spark"
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "ParquetFileExchangeAdapter.scala",
        ROOT
        / "bindings"
        / "scala-spark"
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "ServiceFallbackAdapter.scala",
        ROOT
        / "bindings"
        / "scala-spark"
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "SparkSqlBoundaryAdapter.scala",
    ]:
        assert path.exists(), path

    metadata = _load_json(TRACK / "metadata.json")
    spec = _read_text(TRACK / "spec.md")
    plan = _read_text(TRACK / "plan.md")
    index = _read_text(TRACK / "index.md")
    tracks = _read_text(TRACKS_REGISTRY)
    bundle = _load_json(CONTRACT_BUNDLE)
    live_contract = _load_json(LIVE_CONTRACT)
    parquet_pass = _load_json(LIVE_EXAMPLES / "parquet-file.pass.json")
    service_pass = _load_json(LIVE_EXAMPLES / "service.pass.json")
    sql_pass = _load_json(LIVE_EXAMPLES / "sql-boundary.pass.json")
    binding_fail = _load_json(LIVE_EXAMPLES / "binding.fail.json")

    assert metadata["track_id"] == "scala_spark_binding_20260513"
    assert metadata["type"] == "feature"
    assert metadata["status"] == "completed"
    assert metadata["track_class"] == "binding"
    assert metadata["current_state"] == "complete-with-gaps"
    assert metadata["primary_contract"] == (
        "contracts/scala-spark-binding/scala-spark-binding.contract.json"
    )
    assert metadata["publication_status"] == "not-applicable"
    assert metadata["completion_evidence"] == ["docs", "workflows", "tests"]
    assert "Scala/Spark roadmap" in str(metadata["description"])

    for phrase in [
        "Define a Scala/Spark integration roadmap for enterprise lakehouse, Spark SQL,",
        "Scala/Spark must consume the shared",
        "calculator contract through Arrow/Parquet, service, or SQL/DuckDB boundaries and",
        "Select initial DataFrame/file/service strategy.",
        "Define Spark version, schema, and package gating constraints.",
        "Add Scala/Spark examples and shared-fixture validation.",
        "Validate diagnostics and provenance against the shared contract.",
        "Document lakehouse deployment patterns.",
        "Formula logic remains single-sourced outside Scala/Spark adapters.",
        "must not duplicate formula logic.",
    ]:
        assert phrase in spec or phrase in plan

    for phrase in [
        "Define Scala/Spark Arrow/Parquet and Spark SQL contract boundaries.",
        "Document lakehouse deployment patterns.",
    ]:
        assert phrase in plan

    assert "Track scala_spark_binding_20260513 Context" in index
    assert "Scala/Spark Binding" in tracks
    assert "audience/owner evidence gate" in tracks
    assert (
        "Scala/Spark Binding"
        in tracks
    )

    bundle_map = _as_mapping(bundle)
    diagnostics = _as_mapping(bundle_map["diagnostics"])
    provenance = _as_mapping(bundle_map["provenance"])
    spark_module = _as_mapping(bundle_map["spark_module"])

    assert bundle_map["schema_version"] == "1.0"
    assert bundle_map["binding_id"] == "scala_spark_binding_20260513"
    assert bundle_map["surface"] == "scala_spark"
    assert bundle_map["initial_strategy"] == "parquet-arrow file exchange"
    assert bundle_map["fallback_strategy"] == "service boundary"
    assert bundle_map["formula_logic_location"] == "rust core"
    assert bundle_map["spark_module_status"] == "future-only"
    assert diagnostics["format"] == "json"
    assert diagnostics["includes"] == [
        "contract_id",
        "fixture_id",
        "validation_status",
        "strategy",
        "fallback",
    ]
    assert provenance["checksum_algorithm"] == "sha256"
    assert provenance["preserve_fields"] == [
        "source_basis",
        "fixture_id",
        "notes",
    ]
    assert spark_module["status"] == "future-only"
    assert spark_module["release_gate"] == "contract and parity stable"
    assert live_contract["schema_version"] == "1.0"
    assert live_contract["privacy"]["classification"] == "synthetic"
    assert live_contract["privacy"]["contains_phi"] is False
    priorities = {
        mode["mode"]: mode["priority"] for mode in live_contract["transport_modes"]
    }
    assert priorities == {
        "file-exchange": "primary",
        "sql-boundary": "primary",
        "service": "fallback",
    }
    parquet_checks = parquet_pass["response"]["diagnostics"]["checks"]
    assert {check["status"] for check in parquet_checks} == {"pass"}
    assert service_pass["response"]["mode"] == "service"
    assert sql_pass["response"]["mode"] == "sql-boundary"
    assert "fail" in {
        check["status"]
        for check in binding_fail["response"]["diagnostics"]["checks"]
    }
    readiness = {
        item["id"]: item["state"] for item in live_contract["module_readiness"]
    }
    assert readiness["scala_spark_transport_adapter"] == "adapter_ready"
    assert readiness["file_exchange_boundary"] == "ready"
    assert readiness["sql_boundary"] == "ready"
    assert readiness["service_fallback_boundary"] == "ready"


def test_scala_spark_binding_preserves_provenance_without_formula_logic():
    bundle = _load_json(CONTRACT_BUNDLE)
    diagnostics = _as_mapping(bundle["diagnostics"])
    provenance = _as_mapping(bundle["provenance"])
    spark_module = _as_mapping(bundle["spark_module"])

    assert bundle["formula_logic_location"] == "rust core"
    assert "scala" not in str(bundle["formula_logic_location"]).lower()
    assert "spark" not in str(bundle["formula_logic_location"]).lower()
    assert diagnostics["format"] == "json"
    assert provenance["checksum_algorithm"] == "sha256"
    assert spark_module["status"] == "future-only"
    assert "publication" not in str(spark_module["status"]).lower()


def test_scala_spark_binding_if_a_scaffold_exists_it_stays_thin_and_non_formula():
    scaffold_root = ROOT / "bindings" / "scala-spark"
    assert scaffold_root.exists(), scaffold_root

    scaffold_text = _squash(
        " ".join(
            _read_text(path)
            for path in scaffold_root.rglob("*")
            if path.is_file()
            and "bin" not in path.parts
            and "vendor" not in path.parts
            and "node_modules" not in path.parts
            and "target" not in path.parts
            and path.suffix
            in {".md", ".txt", ".json", ".scala", ".sbt", ".yaml", ".yml"}
        )
    ).lower()

    for forbidden in [
        "formula logic",
        "reimplement formula",
        "duplicate formulas",
        "spark module publication",
        "publication-ready",
        "production-ready",
        "unsupportedoperationexception",
        "scaffold placeholder",
    ]:
        assert forbidden not in scaffold_text


def test_scala_spark_binding_scaffold_has_concrete_transport_boundaries():
    scaffold_root = ROOT / "bindings" / "scala-spark"
    boundary_models = _read_text(
        scaffold_root
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "BoundaryModels.scala"
    )
    parquet_adapter = _read_text(
        scaffold_root
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "ParquetFileExchangeAdapter.scala"
    )
    service_adapter = _read_text(
        scaffold_root
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "ServiceFallbackAdapter.scala"
    )
    sql_adapter = _read_text(
        scaffold_root
        / "src"
        / "main"
        / "scala"
        / "mchs"
        / "spark"
        / "adapter"
        / "SparkSqlBoundaryAdapter.scala"
    )

    for phrase in [
        "final case class ScalaSparkBindingRequest",
        "final case class ScalaSparkServiceRequest",
        "final case class ScalaSparkServiceResponse",
        "def requireSparkSqlIdentifier",
        "def requireHttpUrl",
    ]:
        assert phrase in boundary_models

    assert "spark.read.parquet(normalizedPath)" in parquet_adapter
    assert "createOrReplaceTempView(normalizedViewName)" in parquet_adapter
    assert "BoundaryValidation.requireSparkSqlIdentifier" in parquet_adapter

    for phrase in [
        "java.net.http.{HttpClient, HttpRequest, HttpResponse}",
        "def execute(request: ScalaSparkServiceRequest)",
        "HttpRequest.BodyPublishers.ofString(validated.payloadJson)",
        "X-MCHS-Calculator-Id",
        "X-MCHS-Pricing-Year",
        "def jsonEnvelope(request: ScalaSparkBindingRequest)",
    ]:
        assert phrase in service_adapter

    assert "def registerParquetView(path: String, viewName: String)" in sql_adapter
    assert "def query(sqlText: String): DataFrame" in sql_adapter
