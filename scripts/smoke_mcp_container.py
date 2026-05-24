"""Smoke-test a containerized stdio MCP server."""

from __future__ import annotations

import json
import shutil
import subprocess  # nosec B404 - intentional Docker smoke-test harness.
import sys


def main() -> int:
    """Run initialize and tools/list against a Docker image command."""
    image = sys.argv[1] if len(sys.argv) > 1 else "mchs-mcp:local"
    docker = shutil.which("docker")
    if docker is None:
        raise RuntimeError("docker executable not found")
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    ]
    proc = subprocess.run(  # nosec B603 - command is fixed; image is explicit CLI input.
        [docker, "run", "--rm", "-i", image],
        input="".join(json.dumps(request) + "\n" for request in requests),
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        return proc.returncode
    lines = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
    if len(lines) != 2:
        raise AssertionError(f"expected 2 JSON-RPC responses, got {len(lines)}")
    if lines[0]["result"]["serverInfo"]["name"] != "mchs":
        raise AssertionError("unexpected server name")
    tool_names = {tool["name"] for tool in lines[1]["result"]["tools"]}
    if "mchs.list_calculators" not in tool_names:
        raise AssertionError("mchs.list_calculators missing from container tools")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
