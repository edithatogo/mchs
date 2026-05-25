from __future__ import annotations

# ruff: noqa: E501
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "power-platform" / "evidence"
CANVAS_APP_PUBLICATION = EVIDENCE / "canvas-app-publication-20260520.json"
CONNECTION_REFERENCES = (
    ROOT / "power-platform" / "solution" / "connection-references.json"
)
FLOW_SMOKE_TEMPLATE = EVIDENCE / "flow-smoke-evidence-template.json"
FLOW_SMOKE_EVIDENCE = EVIDENCE / "power-automate-flow-smoke-20260521.json"
POWERAPP_RUNTIME_LAUNCH = EVIDENCE / "powerapp-runtime-launch-20260525.json"
TENANT_CLI_OBSERVATION = EVIDENCE / "tenant-cli-observation-20260525.json"
FLOW_ROOT = ROOT / "power-platform" / "flows"
REQUIRED_MONITORING_FIELDS = (
    ("monitoring", "owner"),
    ("monitoring", "failureMetrics"),
    ("dlp", "policyId"),
    ("dlp", "policyName"),
    ("dlp", "policyClassification"),
    ("dlp", "policyCaptureState"),
    ("connectorPolicy", "policyId"),
    ("connectorPolicy", "policyName"),
    ("connectorPolicy", "connectorAllowState"),
    ("support", "owner"),
    ("support", "escalationOwner"),
    ("support", "escalationPath"),
    ("support", "escalationContact"),
)
EXPECTED_FAILURE_METRIC_FIELDS = (
    "connectorFailures",
    "flowRunFailures",
    "serviceBoundaryHealth",
    "appHealthMetrics",
    "correlationIdsWithoutPatientData",
)
EXPECTED_SUPPORT_DIAGNOSTIC_FIELDS = (
    "solutionVersion",
    "environmentId",
    "connectorOperation",
    "correlationId",
    "sanitizedPayloadHash",
)
GUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{12}$"
)


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _require_false(data: dict, key: str, path: Path) -> None:
    if data["claimBoundary"].get(key) is not False:
        raise SystemExit(f"{path}: {key} must remain false until live evidence exists")


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def _require_path(data: dict, path: tuple[str, ...], label: str, source: Path) -> None:
    cursor: object = data
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            joined = ".".join(path)
            raise SystemExit(f"{source}: missing required {label} field {joined}")
        cursor = cursor[key]
    if cursor in (None, "", [], {}):
        joined = ".".join(path)
        raise SystemExit(f"{source}: {label} field {joined} must be populated")


def _require_list_contains(
    data: dict,
    key: str,
    required_values: list[str],
    source: Path,
    label: str,
) -> None:
    value = data.get(key)
    _require(isinstance(value, list), f"{source}: {label} must be a list")
    for required in required_values:
        _require(
            required in value,
            f"{source}: missing required {label} entry {required}",
        )


def _require_exact_keys(
    data: dict,
    path: tuple[str, ...],
    expected: tuple[str, ...],
    label: str,
    source: Path,
) -> None:
    cursor: object = data
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            joined = ".".join(path)
            raise SystemExit(f"{source}: missing required {label} field {joined}")
        cursor = cursor[key]
    _require(
        isinstance(cursor, dict),
        f"{source}: {label} field {'.'.join(path)} must be an object",
    )
    actual = set(cursor)
    expected_set = set(expected)
    _require(
        actual == expected_set,
        (
            f"{source}: {label} field {'.'.join(path)} must contain exactly "
            f"{sorted(expected_set)}"
        ),
    )


def _require_exact_list(
    data: dict,
    path: tuple[str, ...],
    expected: tuple[str, ...],
    label: str,
    source: Path,
) -> None:
    cursor: object = data
    for key in path:
        if not isinstance(cursor, dict) or key not in cursor:
            joined = ".".join(path)
            raise SystemExit(f"{source}: missing required {label} field {joined}")
        cursor = cursor[key]
    _require(
        isinstance(cursor, list),
        f"{source}: {label} field {'.'.join(path)} must be a list",
    )
    _require(
        cursor == list(expected),
        (f"{source}: {label} field {'.'.join(path)} must equal {list(expected)!r}"),
    )


def _load_connection_reference() -> dict:
    data = _json(CONNECTION_REFERENCES)
    refs = {ref["name"]: ref for ref in data["connectionReferences"]}
    _require(
        "mchs_service_boundary" in refs,
        "missing mchs_service_boundary connection reference",
    )
    connection_reference = refs["mchs_service_boundary"]
    _require(
        connection_reference["api"] == "mchs-service-boundary",
        "mchs_service_boundary must bind the mchs-service-boundary api",
    )
    return connection_reference


def _validate_flow_files(
    expected_connection_reference: str,
) -> dict[str, dict[str, object]]:
    flows: dict[str, dict[str, object]] = {}
    for flow_path in sorted(FLOW_ROOT.glob("*/flow.json")):
        flow = _json(flow_path)
        logical_name = flow.get("name")
        _require(bool(logical_name), f"{flow_path}: missing flow name")
        _require(bool(flow.get("operation")), f"{flow_path}: missing operation")
        _require(
            flow.get("connectionReference") == expected_connection_reference,
            (
                f"{flow_path}: connectionReference must remain "
                f"{expected_connection_reference}"
            ),
        )
        _require(bool(flow.get("trigger")), f"{flow_path}: missing trigger")
        _require(
            flow.get("storesPatientData") is False,
            f"{flow_path}: storesPatientData must remain false",
        )
        _require(
            flow.get("containsFormulaLogic") is False,
            f"{flow_path}: containsFormulaLogic must remain false",
        )
        flows[logical_name] = {
            "path": flow_path,
            "operation": flow["operation"],
        }
    _require(flows, "no Power Automate flow metadata found under power-platform/flows")
    return flows


def _expected_flow_required_evidence(logical_name: str) -> list[str]:
    evidence_map = {
        "mchs-validate-input": [
            "flowId",
            "runId",
            "connectionReferenceId",
            "correlationId",
            "connectionReference",
            "sanitizedPayloadHash",
            "successfulResponseForSyntheticInput",
        ],
        "mchs-calculate-request": [
            "flowId",
            "runId",
            "connectionReference",
            "connectionReferenceId",
            "connectorLatencySummary",
            "correlationId",
        ],
        "mchs-evidence-export": [
            "flowId",
            "runId",
            "connectionReference",
            "connectionReferenceId",
            "bundleScopeAndId",
        ],
        "mchs-deployment-smoke": [
            "flowId",
            "runId",
            "connectionReference",
            "connectionReferenceId",
            "deploymentProfile",
        ],
    }
    _require(
        logical_name in evidence_map,
        f"unsupported flow logical name: {logical_name}",
    )
    return evidence_map[logical_name]


def _validate_flow_smoke_contract(
    data: dict,
    path: Path,
    expected_connection_reference: str,
    expected_connection_reference_id: str,
    flow_metadata: dict[str, dict[str, object]],
    require_empty_runs: bool,
) -> None:
    flow_files = {
        logical_name: metadata["path"].relative_to(ROOT).as_posix()
        for logical_name, metadata in flow_metadata.items()
    }
    flow_operations = {
        logical_name: metadata["operation"]
        for logical_name, metadata in flow_metadata.items()
    }
    _require(
        data["claimBoundary"].get("flowSmokePassed") is False,
        (
            f"{path}: flowSmokePassed must remain false until "
            "real NSW run evidence exists"
        ),
    )
    _require(
        data["claimBoundary"].get("productionReadinessClaimed") is False,
        (
            f"{path}: productionReadinessClaimed must remain false until "
            "real NSW run evidence exists"
        ),
    )
    entries = data.get("realNswRunEvidence", [])
    _require(entries, f"{path}: missing realNswRunEvidence template")
    _require(
        {entry["flowLogicalName"] for entry in entries} == set(flow_metadata),
        f"{path}: realNswRunEvidence must cover every flow logical name",
    )
    checklist = {
        item["flowLogicalName"]: item for item in data.get("flowSmokeChecklist", [])
    }
    _require(
        set(checklist) == set(flow_metadata),
        f"{path}: flowSmokeChecklist must cover every flow logical name",
    )
    if "requiredFlows" in data:
        _require(
            {Path(item["flowFile"]).parent.name for item in checklist.values()}
            == set(data["requiredFlows"]),
            f"{path}: requiredFlows must match the declared flow files",
        )
    for item in checklist.values():
        _require(
            item["status"] == "blocked",
            f"{path}: {item['flowLogicalName']} must remain blocked",
        )
        _require(
            item["flowFile"] == flow_files[item["flowLogicalName"]],
            (
                f"{path}: {item['flowLogicalName']} flowFile must match "
                "the source-controlled flow"
            ),
        )
        _require(
            item.get("operation") == flow_operations[item["flowLogicalName"]],
            (
                f"{path}: {item['flowLogicalName']} operation must match "
                "the source-controlled flow metadata"
            ),
        )
        _require(
            item["requiredEvidence"]
            == _expected_flow_required_evidence(item["flowLogicalName"]),
            (
                f"{path}: {item['flowLogicalName']} requiredEvidence must "
                "match the stricter flow smoke contract"
            ),
        )
    for entry in entries:
        logical_name = entry["flowLogicalName"]
        _require(
            entry["flowFile"] == flow_files[logical_name],
            f"{path}: flowFile mismatch for {logical_name}",
        )
        _require(
            entry.get("operation") == flow_operations[logical_name],
            f"{path}: operation mismatch for {logical_name}",
        )
        _require(
            entry["connectionReference"] == expected_connection_reference,
            f"{path}: connectionReference must remain {expected_connection_reference}",
        )
        _require(
            entry["connectionReferenceId"] == expected_connection_reference_id,
            (
                f"{path}: connectionReferenceId must remain "
                f"{expected_connection_reference_id}"
            ),
        )
        if require_empty_runs:
            _require(
                entry["flowId"] is None,
                f"{path}: flowId must remain null until real NSW evidence exists",
            )
            _require(
                entry["runId"] is None,
                f"{path}: runId must remain null until real NSW evidence exists",
            )
            _require(
                entry["runStatus"] is None,
                (f"{path}: runStatus must remain null until real NSW evidence exists"),
            )
            _require(
                entry["runUrl"] is None,
                f"{path}: runUrl must remain null until real NSW evidence exists",
            )
        else:
            _require(
                bool(entry["flowId"]) and GUID_RE.match(entry["flowId"]) is not None,
                f"{path}: flowId must be a GUID when real NSW run evidence exists",
            )
            _require(
                bool(entry["runId"]),
                f"{path}: runId must be present when real NSW run evidence exists",
            )
            _require(
                entry["runStatus"] == "succeeded",
                (
                    f"{path}: runStatus must be succeeded when "
                    "real NSW run evidence exists"
                ),
            )
        _require(
            logical_name in checklist,
            f"{path}: missing checklist entry for {logical_name}",
        )
    if require_empty_runs:
        _require(
            not data.get("runs"),
            f"{path}: runs must remain empty until real NSW run evidence exists",
        )
        _require(
            not data.get("results", {}).get("successfulRunIds"),
            (
                f"{path}: successfulRunIds must remain empty until "
                "real NSW run evidence exists"
            ),
        )
        _require(
            not data.get("results", {}).get("failedRunIds"),
            (
                f"{path}: failedRunIds must remain empty until "
                "real NSW run evidence exists"
            ),
        )


def _validate_powerapp_runtime_launch(
    data: dict,
    path: Path,
    publication: dict,
    deployment: dict,
) -> None:
    _require(
        data["evidenceType"] == "power_platform_powerapp_runtime_launch_attempt",
        f"{path}: unexpected evidenceType",
    )
    _require(
        data["status"].startswith("blocked"),
        f"{path}: status must remain blocked until app runtime is reached",
    )
    _require(
        data["targetEnvironment"]["environmentId"] == deployment["environmentId"],
        f"{path}: target environment must match deployment-status environmentId",
    )
    optimized = publication["optimizedPublication"]
    _require(
        data["targetApp"]["appId"] == optimized["appId"],
        f"{path}: target app must match optimized publication appId",
    )
    _require(
        data["targetApp"]["playUrl"] == optimized["playUrl"],
        f"{path}: target playUrl must match optimized publication playUrl",
    )
    runtime_state = data["observedRuntimeState"]
    screenshot = ROOT / runtime_state["screenshot"]
    _require(
        screenshot.is_file() and screenshot.stat().st_size > 0,
        f"{path}: runtime screenshot is missing or empty: {screenshot}",
    )
    _require(
        runtime_state["finalTitle"] == "Sign in to your account",
        f"{path}: blocked launch evidence must capture the sign-in title",
    )
    _require(
        runtime_state["finalUrlHost"] == "login.microsoftonline.com",
        f"{path}: blocked launch evidence must capture Microsoft sign-in host",
    )
    for claim in (
        "appRuntimeReached",
        "connectorBackedScreenExecuted",
        "serviceBoundaryExecutionObserved",
        "runtimeSmokePassed",
        "productionReadinessClaimed",
    ):
        _require_false(data, claim, path)


def _validate_tenant_cli_observation(
    data: dict,
    path: Path,
    deployment: dict,
    expected_connector_id: str,
) -> None:
    _require(
        data["evidenceType"] == "power_platform_tenant_cli_observation",
        f"{path}: unexpected evidenceType",
    )
    _require(
        data["status"] == "blocked_with_connector_definition_observed",
        f"{path}: tenant CLI observation must stay blocked",
    )
    _require(
        data["targetEnvironment"]["environmentId"] == deployment["environmentId"],
        f"{path}: target environment must match deployment-status environmentId",
    )
    _require(
        data["targetEnvironment"]["environmentUrl"] == deployment["environmentUrl"],
        f"{path}: target environment URL must match deployment-status environmentUrl",
    )
    _require(
        data["targetEnvironment"]["activeInPac"] is True,
        f"{path}: target environment must be marked active in PAC",
    )
    _require(
        data["claimBoundary"]["targetEnvironmentAccessConfirmed"] is True,
        f"{path}: target environment access claim must be explicit",
    )
    connector = data["connectorObservation"]
    _require(
        connector["customConnectorDefinitionObserved"] is True,
        f"{path}: custom connector definition must be observed",
    )
    _require(
        data["claimBoundary"]["customConnectorDefinitionObserved"] is True,
        f"{path}: custom connector definition claim must be explicit",
    )
    _require(
        connector["connectorId"] == expected_connector_id,
        f"{path}: connector id must match the expected service-boundary connector",
    )
    _require(
        connector["displayName"] == "MCHS Service Boundary",
        f"{path}: connector display name must remain explicit",
    )
    _require(
        connector["matchesExpectedServiceBoundaryConnector"] is True,
        f"{path}: connector must match the expected service-boundary connector",
    )
    _require(
        connector["connectorType"] == "CustomConnector",
        f"{path}: connector type must be CustomConnector",
    )
    _require(
        connector["customConnectorConnectionObserved"] is False,
        f"{path}: custom connector connection must remain false until observed",
    )
    _require(
        data["connectionObservation"]["targetEnvironmentDataverseConnectionObserved"]
        is True,
        f"{path}: target environment Dataverse connection must be observed",
    )
    _require(
        data["connectionObservation"]["serviceBoundaryConnectionReferenceResolved"]
        is False,
        f"{path}: connection reference must remain unresolved",
    )
    _require(
        data["dlpObservation"]["policyInventoryVisible"] is True,
        f"{path}: DLP policy inventory visibility must be recorded",
    )
    _require(
        data["dlpObservation"]["targetEnvironmentPolicyIdentified"] is False,
        f"{path}: target DLP policy must remain unidentified until captured",
    )
    _require(
        data["dlpObservation"]["serviceBoundaryConnectorPolicyIdentified"] is False,
        f"{path}: service-boundary connector policy must remain unidentified",
    )
    _require(
        data["flowObservation"]["flowRunEvidenceCaptured"] is False,
        f"{path}: flow run evidence must remain false until captured",
    )
    for claim in (
        "customConnectorConnectionObserved",
        "serviceBoundaryEndpointConfigured",
        "serviceBoundaryExecutionObserved",
        "flowSmokePassed",
        "dlpCompatible",
        "monitoringOperational",
        "runtimeSmokePassed",
        "productionReadinessClaimed",
    ):
        _require_false(data, claim, path)


def main() -> int:
    publication = _json(CANVAS_APP_PUBLICATION)
    deployment = _json(EVIDENCE / "deployment-status.json")
    bundle = _json(EVIDENCE / "nsw-operational-readiness-bundle-template.json")
    runtime = _json(EVIDENCE / "runtime-smoke-evidence-template.json")
    powerapp_runtime_launch = _json(POWERAPP_RUNTIME_LAUNCH)
    tenant_cli_observation = _json(TENANT_CLI_OBSERVATION)
    connections = _json(EVIDENCE / "connection-reference-evidence-template.json")
    endpoint = _json(EVIDENCE / "service-boundary-endpoint-template.json")
    monitoring = _json(EVIDENCE / "monitoring-dlp-evidence-template.json")
    flow_smoke_template = _json(FLOW_SMOKE_TEMPLATE)
    flow_smoke_evidence = _json(FLOW_SMOKE_EVIDENCE)
    connection_reference = _load_connection_reference()
    required_ref_map = {
        ref["name"]: ref for ref in _json(CONNECTION_REFERENCES)["connectionReferences"]
    }
    required_connection = required_ref_map["mchs_service_boundary"]
    flow_paths = _validate_flow_files(connection_reference["name"])

    _require(
        publication["claimBoundary"].get("appPublished") is True,
        "canvas app publication evidence must remain published",
    )
    _require(
        publication["claimBoundary"].get("appLaunchSmokePassed") is True,
        "canvas app publication evidence must keep launch smoke passed",
    )
    _require(
        publication["claimBoundary"].get("visualFunctionOptimized") is True,
        "canvas app publication evidence must keep visual optimization recorded",
    )
    _require(
        publication["claimBoundary"].get("serviceBoundaryExecutionProven")
        in (False, True),
        "canvas app publication evidence must keep service-boundary execution as a boolean claim",
    )
    if publication["claimBoundary"].get("productionReadinessClaimed") is True:
        _require(
            publication["claimBoundary"].get("appPublished") is True,
            "canvas app publication production readiness claim requires published app evidence",
        )
        _require(
            publication["claimBoundary"].get("appLaunchSmokePassed") is True,
            "canvas app publication production readiness claim requires launch smoke evidence",
        )
        _require(
            publication["claimBoundary"].get("visualFunctionOptimized") is True,
            "canvas app publication production readiness claim requires visual optimization evidence",
        )
        _require(
            publication["claimBoundary"].get("serviceBoundaryExecutionProven") is True,
            "canvas app publication production readiness claim requires service-boundary execution evidence",
        )
        _require(
            publication["visualReview"].get("optimizedArtifactPublished") is True,
            "canvas app publication production readiness claim requires optimized artifact publication evidence",
        )
    _require(
        publication["claimBoundary"].get("productionReadinessClaimed") in (False, True),
        "canvas app publication evidence production readiness claim must be boolean",
    )
    _validate_powerapp_runtime_launch(
        powerapp_runtime_launch,
        POWERAPP_RUNTIME_LAUNCH,
        publication,
        deployment,
    )
    expected_connector = next(
        ref["connectorId"]
        for ref in connections["requiredConnectionReferences"]
        if ref["logicalName"] == "mchs_service_boundary"
    )
    _validate_tenant_cli_observation(
        tenant_cli_observation,
        TENANT_CLI_OBSERVATION,
        deployment,
        expected_connector,
    )
    _require_list_contains(
        publication,
        "requiredEvidence",
        [
            "appId",
            "playUrl",
            "optimizedPublication.appId",
            "optimizedPublication.playUrl",
            "visualReview.viewedInTenant",
            "visualReview.optimizedArtifactPublished",
        ],
        CANVAS_APP_PUBLICATION,
        "publication required evidence",
    )
    _require(
        bool(publication["optimizedPublication"].get("appId")),
        "canvas app publication evidence must keep the optimized app id explicit",
    )
    _require(
        bool(publication["optimizedPublication"].get("playUrl")),
        "canvas app publication evidence must keep the optimized play URL explicit",
    )

    if not deployment["managedSolutionImported"]:
        raise SystemExit("managed solution import evidence is required")
    if deployment["productionReadinessClaimed"]:
        _require(
            deployment["managedSolutionImported"] is True
            and deployment["customConnectorRegistered"] is True
            and deployment["canvasAppPublished"] is True
            and deployment["optimizedCanvasAppPublished"] is True
            and deployment["operationPageSourceUxComplete"] is True
            and deployment.get("operationPagesPublishedToTenant") is True
            and not deployment.get("missing"),
            "deployment status production readiness claim requires completed deployment evidence",
        )
        _require(
            deployment["repoHealth"]["score"] >= 9.9,
            "deployment status production readiness claim requires repo-health evidence at 9.9",
        )

    known_limitations = "\n".join(bundle["known_limitations"])
    for blocker in [
        "service_boundary_production_endpoint_missing",
        "connection_reference_values_missing",
        "real_dataverse_app_component_smoke_missing",
        "real_power_automate_flow_component_smoke_missing",
    ]:
        if blocker not in known_limitations:
            raise SystemExit(f"missing operational blocker: {blocker}")

    if bundle["governance"]["runtime_production_readiness_claim"]:
        _require(
            deployment["productionReadinessClaimed"] is True,
            "readiness bundle runtime production readiness claim requires deployment evidence",
        )
        _require(
            runtime["claimBoundary"].get("productionReadinessClaimed") is True,
            "readiness bundle runtime production readiness claim requires runtime evidence",
        )
        _require(
            connections["claimBoundary"].get("productionReadinessClaimed") is True,
            "readiness bundle runtime production readiness claim requires connection evidence",
        )
        _require(
            endpoint["claimBoundary"].get("productionReadinessClaimed") is True,
            "readiness bundle runtime production readiness claim requires endpoint evidence",
        )
        _require(
            monitoring["claimBoundary"].get("productionReadinessClaimed") is True,
            "readiness bundle runtime production readiness claim requires monitoring evidence",
        )
    _require(
        runtime["claimBoundary"].get("runtimeSmokePassed") in (False, True),
        f"{EVIDENCE}: runtime smoke claim must be boolean",
    )
    if runtime["claimBoundary"].get("productionReadinessClaimed") is True:
        _require(
            runtime["claimBoundary"].get("runtimeSmokePassed") is True,
            f"{EVIDENCE}: runtime production readiness claim requires runtime smoke evidence",
        )
        _require_path(
            runtime,
            ("serviceBoundary", "productionEndpoint"),
            "runtime production readiness evidence",
            EVIDENCE,
        )
        _require(
            bool(runtime.get("connectionReferences", {}).get("configured")),
            f"{EVIDENCE}: runtime production readiness claim requires configured connection references",
        )
        _require(
            runtime.get("flowSmoke", {}).get("status")
            != "blocked_missing_real_flow_component",
            f"{EVIDENCE}: runtime production readiness claim requires flow smoke evidence",
        )
    _require(
        runtime["claimBoundary"].get("productionReadinessClaimed") in (False, True),
        f"{EVIDENCE}: runtime production readiness claim must be boolean",
    )
    _require(
        connections["claimBoundary"].get("connectionsConfigured") in (False, True),
        f"{EVIDENCE}: connection readiness claim must be boolean",
    )
    if connections["claimBoundary"].get("productionReadinessClaimed") is True:
        _require(
            connections["claimBoundary"].get("connectionsConfigured") is True,
            f"{EVIDENCE}: connection readiness claim requires configured connections",
        )
        _require(
            bool(connections.get("requiredEvidence")),
            f"{EVIDENCE}: connection readiness claim requires required evidence entries",
        )
        _require(
            connections.get("pacObservedConnections", {}).get(
                "customConnectorConnectionFound"
            )
            is True,
            f"{EVIDENCE}: connection readiness claim requires observed custom connector evidence",
        )
        _require(
            bool(
                connections.get("pacObservedConnections", {}).get(
                    "customConnectorConnectionId"
                )
            ),
            f"{EVIDENCE}: connection readiness claim requires a custom connector connection id",
        )
    _require(
        connections["claimBoundary"].get("productionReadinessClaimed") in (False, True),
        f"{EVIDENCE}: connection readiness claim must be boolean",
    )
    if not endpoint["status"].startswith("blocked"):
        raise SystemExit("service boundary endpoint template must remain blocked")
    _require(
        endpoint["claimBoundary"].get("endpointConfigured") in (False, True),
        f"{EVIDENCE}: endpointConfigured claim must be boolean",
    )
    _require(
        endpoint["claimBoundary"].get("endpointValidated") in (False, True),
        f"{EVIDENCE}: endpointValidated claim must be boolean",
    )
    if endpoint["claimBoundary"].get("productionReadinessClaimed") is True:
        _require(
            endpoint["claimBoundary"].get("endpointConfigured") is True,
            f"{EVIDENCE}: endpoint production readiness claim requires endpoint configuration evidence",
        )
        _require(
            endpoint["claimBoundary"].get("endpointValidated") is True,
            f"{EVIDENCE}: endpoint production readiness claim requires validated endpoint evidence",
        )
        _require_path(
            endpoint,
            ("serviceBoundary", "httpsBaseUrl"),
            "endpoint production readiness evidence",
            EVIDENCE,
        )
        _require(
            endpoint["serviceBoundary"].get("publiclyReachableFromPowerPlatform")
            is True,
            f"{EVIDENCE}: endpoint production readiness claim requires public reachability evidence",
        )
        _require(
            endpoint["serviceBoundary"].get("tlsTrusted") is True,
            f"{EVIDENCE}: endpoint production readiness claim requires trusted TLS evidence",
        )
        _require(
            endpoint["validation"].get("endpointSyntaxValidated") is True
            and endpoint["validation"].get("healthzProbed") is True
            and endpoint["validation"].get("serverCardProbed") is True,
            f"{EVIDENCE}: endpoint production readiness claim requires probe evidence",
        )
    _require(
        endpoint["claimBoundary"].get("productionReadinessClaimed") in (False, True),
        f"{EVIDENCE}: endpoint production readiness claim must be boolean",
    )
    for path in REQUIRED_MONITORING_FIELDS:
        _require_path(monitoring, path, "monitoring evidence", EVIDENCE)
    for path in (
        ("monitoring", "failureMetrics", "connectorFailures"),
        ("monitoring", "failureMetrics", "flowRunFailures"),
        ("monitoring", "failureMetrics", "serviceBoundaryHealth"),
        ("monitoring", "failureMetrics", "appHealthMetrics"),
        ("monitoring", "failureMetrics", "correlationIdsWithoutPatientData"),
    ):
        _require_path(monitoring, path, "failure metric", EVIDENCE)
    _require_exact_keys(
        monitoring,
        ("monitoring", "failureMetrics"),
        EXPECTED_FAILURE_METRIC_FIELDS,
        "failure metrics",
        EVIDENCE,
    )
    _require_exact_list(
        monitoring,
        ("support", "requiredDiagnosticFields"),
        EXPECTED_SUPPORT_DIAGNOSTIC_FIELDS,
        "support diagnostic fields",
        EVIDENCE,
    )
    _require(
        monitoring["claimBoundary"].get("monitoringConfigured") in (False, True),
        f"{EVIDENCE}: monitoringConfigured claim must be boolean",
    )
    _require(
        monitoring["claimBoundary"].get("dlpEvidenceCaptured") in (False, True),
        f"{EVIDENCE}: dlpEvidenceCaptured claim must be boolean",
    )
    if monitoring["claimBoundary"].get("productionReadinessClaimed") is True:
        _require(
            monitoring["claimBoundary"].get("monitoringConfigured") is True,
            f"{EVIDENCE}: monitoring production readiness claim requires monitoring configuration evidence",
        )
        _require(
            monitoring["claimBoundary"].get("dlpEvidenceCaptured") is True,
            f"{EVIDENCE}: monitoring production readiness claim requires DLP capture evidence",
        )
        _require(
            monitoring["status"] != "blocked_pending_tenant_policy_capture",
            f"{EVIDENCE}: monitoring production readiness claim requires non-blocked monitoring status",
        )
        _require(
            all(
                item.get("status")
                not in {
                    "blocked_pending_owner_capture",
                    "blocked_pending_metrics_capture",
                    "blocked_pending_policy_capture",
                    "blocked_pending_escalation_capture",
                }
                for item in monitoring.get("capturedEvidence", [])
            ),
            f"{EVIDENCE}: monitoring production readiness claim requires captured evidence to be resolved",
        )
    _require(
        monitoring["claimBoundary"].get("productionReadinessClaimed") in (False, True),
        f"{EVIDENCE}: monitoring production readiness claim must be boolean",
    )
    _require(
        flow_smoke_template["connectionReference"]["connectionConfigured"] is False,
        "flow smoke template must keep the service boundary connection unconfigured",
    )
    _require(
        flow_smoke_template["connectionReference"]["logicalName"]
        == required_connection["name"],
        "flow smoke template must bind the declared logical connection reference",
    )
    _require(
        endpoint["serviceBoundary"]["logicalConnectionReference"]
        == "mchs_service_boundary",
        "service boundary endpoint must remain bound to mchs_service_boundary",
    )
    required_connections = {
        item["logicalName"]: item
        for item in connections["requiredConnectionReferences"]
    }
    _require(
        "mchs_service_boundary" in required_connections,
        "connection reference evidence must include mchs_service_boundary",
    )
    evidence_connection = required_connections["mchs_service_boundary"]
    _require(
        evidence_connection["logicalName"] == required_connection["name"],
        (
            "connection reference evidence must track the "
            "mchs_service_boundary logical name"
        ),
    )
    _require(
        flow_smoke_template["connectionReference"]["connectorId"]
        == evidence_connection["connectorId"],
        "connection reference evidence must track the published connector id",
    )
    _require(
        evidence_connection["valueStatus"] == "missing",
        (
            "connection reference evidence must stay missing until "
            "a real NSW binding exists"
        ),
    )
    _require(
        connections.get("requiredEvidence")
        and isinstance(connections["requiredEvidence"], list),
        "connection reference evidence must declare required evidence entries",
    )
    _require_list_contains(
        connections,
        "requiredEvidence",
        [
            "environmentId",
            "requiredConnectionReferences[].connectorId",
            "requiredConnectionReferences[].baseUrlEnvironmentVariable",
            "requiredConnectionReferences[].valueStatus",
            "environmentVariables[].logicalName",
            "pacObservedConnections.checkedWithPacConnectionList",
            "pacObservedConnections.customConnectorConnectionFound",
            "pacObservedConnections.customConnectorConnectionId",
            "pacObservedConnections.customConnectorApiId",
            "pacObservedConnector.checkedWithPacConnectorList",
            "pacObservedConnector.connectorId",
            "pacObservedConnector.status",
        ],
        EVIDENCE / "connection-reference-evidence-template.json",
        "connection reference required evidence",
    )
    _require(
        connections["pacObservedConnections"].get("customConnectorConnectionId")
        is None,
        (
            "connection reference evidence must keep the connection id absent "
            "until binding exists"
        ),
    )
    _require(
        connections["pacObservedConnections"]["customConnectorConnectionFound"]
        is False,
        "connection reference evidence must keep PAC connection observations blocked",
    )
    _require(
        connections["environmentId"] == deployment["environmentId"],
        "connection reference evidence must stay bound to the deployment environment",
    )
    for env_var in connections["environmentVariables"]:
        _require(
            env_var["valueStatus"] in {"missing", "template"},
            (
                "connection reference environment variables must remain "
                "missing or template"
            ),
        )
    for path, data in (
        (FLOW_SMOKE_TEMPLATE, flow_smoke_template),
        (FLOW_SMOKE_EVIDENCE, flow_smoke_evidence),
    ):
        real_claimed = data["claimBoundary"].get("flowSmokePassed") is True
        if real_claimed:
            _require(
                not data["status"].startswith("blocked"),
                (
                    f"{path}: status must stop being blocked once "
                    "real NSW run evidence exists"
                ),
            )
        else:
            _require(
                data["status"].startswith("blocked"),
                (
                    f"{path}: status must remain blocked until "
                    "real NSW run evidence exists"
                ),
            )
        _validate_flow_smoke_contract(
            data,
            path,
            connection_reference["name"],
            evidence_connection["connectorId"],
            flow_paths,
            require_empty_runs=not real_claimed,
        )

    print("Power Platform operational evidence contracts passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
