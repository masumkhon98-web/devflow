"""DevFlow report formatters."""

import json
from typing import List

from .audit import Check, summarize


def render_json(checks: List[Check]) -> str:
    return json.dumps(summarize(checks), indent=2)


def render_markdown(checks: List[Check], target: str) -> str:
    counts = summarize(checks)["summary"]
    lines = [
        f"# DevFlow audit: `{target}`", "",
        "**Summary:** {0} passed, {1} warnings, {2} failed".format(
            counts["pass"], counts["warn"], counts["fail"]),
        "", "| Status | Check | Finding | Recommendation |",
        "|---|---|---|---|",
    ]
    for check in checks:
        message = check.message.replace("|", r"\|")
        recommendation = check.recommendation.replace("|", r"\|")
        lines.append(f"| {check.status.upper()} | {check.name} | {message} | {recommendation} |")
    return "\n".join(lines) + "\n"
