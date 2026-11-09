import json
import pytest
from devflow.audit import audit_repository, summarize
from devflow.report import render_json, render_markdown


def make_complete_repo(root):
    (root / "README.md").write_text("# Demo\n", encoding="utf-8")
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (root / "CONTRIBUTING.md").write_text("Contribute\n", encoding="utf-8")
    (root / ".gitignore").write_text("__pycache__/\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\n", encoding="utf-8")
    (root / "tests").mkdir()
    workflows = root / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "ci.yml").write_text("name: CI\n", encoding="utf-8")


def test_complete_repository_passes_all_checks(tmp_path):
    make_complete_repo(tmp_path)
    checks = audit_repository(tmp_path)
    assert len(checks) == 7
    assert all(check.status == "pass" for check in checks)
    assert summarize(checks)["summary"]["pass"] == 7


def test_missing_readme_is_a_failure(tmp_path):
    checks = audit_repository(tmp_path)
    readme = next(check for check in checks if check.name == "README.md")
    assert readme.status == "fail"
    assert readme.recommendation


def test_nonexistent_path_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        audit_repository(tmp_path / "missing")


def test_json_report_is_valid(tmp_path):
    assert "summary" in json.loads(render_json(audit_repository(tmp_path)))


def test_markdown_report_has_table(tmp_path):
    report = render_markdown(audit_repository(tmp_path), "sample")
    assert "| Status | Check |" in report
