"""DevFlow report formatters."""

import json

from .audit import Check, summarize


def render_json(checks: list[Check]) -> str:
    return json.dumps(summarize(checks), indent=2)


def render_markdown(checks: list[Check], target: str) -> str:
    counts = summarize(checks)["summary"]
    lines = [
        f"# DevFlow audit: `{target}`", "",
        "**Summary:** {} passed, {} warnings, {} failed".format(
            counts["pass"], counts["warn"], counts["fail"]),
        "", "| Status | Check | Finding | Recommendation |",
        "|---|---|---|---|",
    ]
    for check in checks:
        message = check.message.replace("|", r"\|")
        recommendation = check.recommendation.replace("|", r"\|")
        lines.append(f"| {check.status.upper()} | {check.name} | {message} | {recommendation} |")
    return "\n".join(lines) + "\n"
