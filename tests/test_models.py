import pytest
from miner.models import Finding, Repository, Summary

def test_finding_model():
    finding = Finding(
        rule_id="py/sql-injection",
        severity="error",
        message="Possible SQL injection vulnerability",
        file="app/views.py",
        start_line=15
    )
    assert finding.rule_id == "py/sql-injection"
    assert finding.start_line == 15

def test_summary_model():
    summary = Summary(
        repositories=10,
        analyzed=8,
        failed=1,
        unsupported=1,
        findings=5
    )
    assert summary.repositories == 10
    assert summary.findings == 5

def test_repository_model():
    repo = Repository(
        name="test-repo",
        url="https://github.com/test/test-repo",
        status="analyzed",
        languages=["python"],
        findings=[]
    )
    assert repo.name == "test-repo"
    assert repo.status == "analyzed"