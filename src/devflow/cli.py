"""DevFlow command-line interface."""

import argparse
import sys
from pathlib import Path

from .audit import audit_repository, summarize
from .report import render_json, render_markdown


def build_parser():
    parser = argparse.ArgumentParser(
        prog="devflow", description="Audit a repository for common maintenance basics.")
    parser.add_argument("path", nargs="?", default=".",
                        help="Repository directory to audit (default: current directory).")
    parser.add_argument("--format", choices=("text", "json", "markdown"),
                        default="text", help="Report format (default: text).")
    parser.add_argument("--output", help="Write the report to this file.")
    return parser


def main():
    args = build_parser().parse_args()
    try:
        checks = audit_repository(args.path)
    except (OSError, ValueError) as exc:
        print(f"devflow: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        output = render_json(checks)
    elif args.format == "markdown":
        output = render_markdown(checks, str(Path(args.path)))
    else:
        counts = summarize(checks)["summary"]
        lines = [f"DevFlow repository audit: {args.path}"]
        for check in checks:
            lines.append(f"{check.status.upper():<4} {check.name:<20} {check.message}")
            if check.recommendation:
                lines.append(f"     Recommendation: {check.recommendation}")
        lines.extend(["", "Summary: {} passed, {} warnings, {} failed".format(
            counts["pass"], counts["warn"], counts["fail"])])
        output = "\n".join(lines) + "\n"

    if args.output:
        try:
            Path(args.output).write_text(output, encoding="utf-8")
        except OSError as exc:
            print(f"devflow: could not write report: {exc}", file=sys.stderr)
            return 2
    else:
        print(output, end="")
    return 1 if any(check.status == "fail" for check in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
