from __future__ import annotations

import argparse
import json
from typing import Any

from .mcp_adapter import (
    list_baselines,
    package_metadata,
    simulate_batch,
    simulate_one,
    symbolic_report,
)


def create_server() -> Any:
    """Create a FastMCP stdio server exposing the packaged QRC APIs."""
    from mcp.server.fastmcp import FastMCP

    app = FastMCP("qrc-ising-core")

    @app.resource("qrc://metadata")
    def resource_metadata() -> str:
        return json.dumps(package_metadata(), sort_keys=True)

    @app.resource("qrc://baselines")
    def resource_baselines() -> str:
        return json.dumps({"baselines": list_baselines()}, sort_keys=True)

    @app.tool()
    def get_baselines() -> dict[str, list[str]]:
        """List supported parity baselines for QRC/QELM/classical comparisons."""
        return {"baselines": list_baselines()}

    @app.tool()
    def simulate_qrc_scenario(params: dict[str, Any]) -> dict[str, Any]:
        """Simulate one scenario and return accuracy/error/fidelity-style metrics."""
        return simulate_one(params)

    @app.tool()
    def simulate_qrc_batch(params: dict[str, Any]) -> list[dict[str, Any]]:
        """Simulate a grid over tier/noise/shots to inspect robustness frontiers."""
        return simulate_batch(params)

    @app.tool()
    def run_qrc_symbolic_checks() -> dict[str, bool]:
        """Execute FC1/FC2/FC3 symbolic checks used in theorem-assumption audits."""
        return symbolic_report()

    @app.prompt()
    def parity_audit_prompt() -> str:
        """Prompt scaffold for parity and leakage audits in QRC evaluations."""
        return (
            "Audit parity constraints before claiming quantum advantage: "
            "check fold-local PCA, matched observable budget, matched readout class, "
            "and fixed split seeds."
        )

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="qrc-ising-core MCP server")
    parser.add_argument("--transport", default="stdio", choices=["stdio"])
    args = parser.parse_args()

    app = create_server()
    app.run(transport=args.transport)


if __name__ == "__main__":
    main()
