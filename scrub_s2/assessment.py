"""Read the supplied Ply export without modifying its decisions or identifiers."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def elements(node):
    yield node
    for child in node.get("children", []):
        yield from elements(child)


def component_hazards(assessment, reference):
    """Direct references only, not an automated impact assessment."""
    ids = {node["id"] for node in elements(assessment["system"])
           if node["reference"] == reference}
    if not ids:
        raise ValueError(f"Unknown assessment component: {reference}")
    matches = []
    for task in assessment["tasks"]:
        for scenario in task.get("scenarios", []):
            linked = set((scenario.get("systemElementIds") or [])
                         + (scenario.get("safetyFunctionElementIds") or []))
            if ids & linked:
                matches.append({"reference": scenario["reference"],
                                "task": task["reference"],
                                "event": scenario["eventHarm"],
                                "decision": scenario["review"]["decision"]})
    return matches


def summary():
    assessment = read_json("RA-S2-WGH-01.json")["assessment"]
    scenarios = [scenario for task in assessment["tasks"]
                 for scenario in task.get("scenarios", [])]
    return {
        "reference": assessment["reference"],
        "tasks": len(assessment["tasks"]),
        "hazards": len(scenarios),
        "components": sum(node["kind"] == "COMPONENT"
                          for node in elements(assessment["system"])),
        "pending_hazards": [s["reference"] for s in scenarios
                            if s["review"]["decision"] == "PENDING"],
        "site_release": assessment["release"]["customerSiteDecision"],
        "camera_hazards": component_hazards(assessment, "PER-01"),
    }
