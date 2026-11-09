"""Repository readiness checks."""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Union


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    message: str
    recommendation: str = ""


def audit_repository(path: Union[str, Path]) -> List[Check]:
    """Check common maintenance files in a repository directory."""
    root = Path(path).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {root}")

    checks = []

    def add(name, exists, message, recommendation, missing_status="warn"):
        checks.append(Check(
            name=name,
            status="pass" if exists else missing_status,
            message=message if exists else f"{name} is missing.",
            recommendation="" if exists else recommendation,
        ))

    add("README.md", (root / "README.md").is_file(),
        "Project overview found.", "Add a README explaining installation and usage.", "fail")

    license_names = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")
    add("LICENSE", any((root / name).is_file() for name in license_names),
        "License file found.", "Add an appropriate open-source license.")

    add("CONTRIBUTING.md", (root / "CONTRIBUTING.md").is_file(),
        "Contribution guidance found.", "Explain how to report issues, run tests, and submit pull requests.")

    has_tests = (root / "tests").is_dir() or (root / "test").is_dir()
    add("tests/", has_tests, "Test directory found.", "Add automated tests for important behavior.")

    workflows = root / ".github" / "workflows"
    has_ci = workflows.is_dir() and any(
        item.is_file() and item.suffix.lower() in (".yml", ".yaml")
        for item in workflows.iterdir()
    )
    add("CI workflow", has_ci, "GitHub Actions workflow found.",
        "Add a workflow that runs tests on pushes and pull requests.")

    add(".gitignore", (root / ".gitignore").is_file(),
        ".gitignore found.", "Ignore caches, virtual environments, build output, and local secrets.")

    has_packaging = (root / "pyproject.toml").is_file() or (root / "setup.py").is_file()
    add("Python packaging", has_packaging, "Python packaging metadata found.",
        "Add pyproject.toml or setup.py if this is a Python project.")
    return checks


def summarize(checks: List[Check]) -> Dict[str, object]:
    counts = {status: sum(check.status == status for check in checks)
              for status in ("pass", "warn", "fail")}
    return {"summary": counts, "checks": [asdict(check) for check in checks]}
