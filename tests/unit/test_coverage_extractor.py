from src.analyzers.coverage_parser import parse_jacoco_coverage, parse_pytest_coverage


def test_pytest_coverage():
    log = "TOTAL                                       15      0   100%"
    assert parse_pytest_coverage(log) == 100.0

def test_jacoco_coverage():
    xml = '<counter type="INSTRUCTION" missed="20" covered="80"/>'
    assert parse_jacoco_coverage(xml) == 80.0
