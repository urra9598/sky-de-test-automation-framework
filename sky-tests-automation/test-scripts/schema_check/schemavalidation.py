"""
Schema validation test-case runner for the `schema_check` test case.

This script will:
- Load the JSON schema `customer_schema.json` (from this test-case folder)
- Generate a small batch of mock records using `DataMocker.generate_from_json_schema`
- Validate each record with `DataComparator.validate_schema`
- Save the expected records under `expected-result/expected_records.json`
- Generate global JSON/HTML reports in the central `reports/` folder at repo root

Run:
    python schemavalidation.py

"""
import json
import os
import sys
from time import perf_counter
from pathlib import Path

# Ensure utilities are importable
# This file: sky-tests-automation/test-scripts/schema_check/schemavalidation.py
# Utilities: sky-tests-automation/utilities
# So we need to go up 2 levels (./../..) to reach sky-tests-automation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from utilities.data_mocker import DataMocker
from utilities.data_comparator import DataComparator
from utilities.report_generator import ReportGenerator
from utilities.execution_log_manager import save_execution_report
from utilities.config_manager import config as CONFIG

# Paths within this test-case folder
BASE_DIR = os.path.dirname(__file__)
SCHEMA_FILE = os.path.join(BASE_DIR, "customer_schema.json")
EXPECTED_DIR = os.path.join(BASE_DIR, "expected-result")
EXPECTED_FILE = os.path.join(EXPECTED_DIR, "expected_records.json")


def _resolve_reports_dir() -> Path:
    """Return the absolute path to the reports directory at repo root.
    
    This script is at: repo_root/sky-tests-automation/test-scripts/schema_check/schemavalidation.py
    parents[3] = repo_root
    reports_dir = repo_root / "reports"  (at repo root, not inside sky-tests-automation)
    """
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[3]
    reports_dir = repo_root / "reports"
    return reports_dir


REPORTS_DIR = _resolve_reports_dir()
NUM_RECORDS = 5


def ensure_dirs():
    os.makedirs(EXPECTED_DIR, exist_ok=True)


def main():
    print("Running schema validation test-case: schema_check")
    ensure_dirs()

    if not os.path.exists(SCHEMA_FILE):
        print(f"Schema file not found at {SCHEMA_FILE}")
        return 2

    try:
        with open(SCHEMA_FILE, "r") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"Failed to read schema: {e}")
        return 2

    report = ReportGenerator(report_dir=str(REPORTS_DIR))

    records = []
    results = []
    total_start = perf_counter()

    for i in range(NUM_RECORDS):
        rec_start = perf_counter()
        try:
            record = DataMocker.generate_from_json_schema(SCHEMA_FILE)
        except Exception as e:
            print(f"Failed to generate mock record: {e}")
            return 2

        is_valid, errors = DataComparator.validate_schema(record, schema)
        duration = perf_counter() - rec_start

        records.append(record)
        results.append({
            "index": i,
            "valid": is_valid,
            "errors": errors,
            "duration_seconds": round(duration, 3)
        })

        status = "PASSED" if is_valid else "FAILED"
        report.add_test_result(
            test_name=f"schema_check_record_{i}",
            status=status,
            duration=duration,
            expected=schema,
            actual=record,
            errors=errors,
            jira_id=None
        )

        print(f"Record {i}: {status} (errors: {len(errors) if errors else 0})")

    total_duration = perf_counter() - total_start

    # Save expected records (these are considered the expected output for the test-case)
    try:
        with open(EXPECTED_FILE, "w") as ef:
            json.dump(records, ef, indent=2, default=str)
        print(f"Saved expected records to {EXPECTED_FILE}")
    except Exception as e:
        print(f"Failed to save expected records: {e}")

    # Build a human-readable log with expected & actual (expected are the records we generated)
    log_entries = [
        "SCHEMA VALIDATION TEST-CASE: schema_check",
        f"Schema: {SCHEMA_FILE}",
        f"Records generated: {len(records)}",
        f"Total duration: {round(total_duration,3)}s",
        "",
    ]

    for r, res in zip(records, results):
        log_entries.append("---")
        log_entries.append(f"Index: {res['index']}")
        log_entries.append(f"Valid: {res['valid']}")
        log_entries.append(f"Duration: {res['duration_seconds']}s")
        log_entries.append("Expected (sample):")
        log_entries.append(json.dumps(r, indent=2, default=str))
        if res['errors']:
            log_entries.append("Errors:")
            for e in res['errors']:
                log_entries.append(f" - {e}")
        log_entries.append("")

    log_content = "\n".join(log_entries)

    # Also write global reports
    try:
        json_report = report.generate_json_report()
        html_report = report.generate_html_report()
        print(f"Reports generated: {json_report}, {html_report}")
    except Exception as e:
        print(f"Failed to generate global reports: {e}")

    # Save a small summary inside the test-case folder
    summary = {
        "test_case": "schema_check",
        "schema_file": SCHEMA_FILE,
        "num_records": len(records),
        "passed": sum(1 for r in results if r['valid']),
        "failed": sum(1 for r in results if not r['valid']),
        "total_duration_seconds": round(total_duration, 3),
        "results": results
    }

    summary_file = os.path.join(BASE_DIR, "schema_validation_summary.json")
    try:
        with open(summary_file, "w") as sf:
            json.dump(summary, sf, indent=2, default=str)
        print(f"Saved per-test summary: {summary_file}")
    except Exception as e:
        print(f"Failed to save per-test summary: {e}")

    # Save the test-case summary as the latest execution log (rotates previous latest)
    # This sends the summary + log content to the central reports folder
    try:
        latest_payload = {
            "per_test_summary": summary,
            "human_readable_log": log_content,
        }
        save_execution_report(latest_payload)
        print("Saved latest execution log to reports/latest_execution_logs.log")
    except Exception as e:
        print(f"Failed to save latest execution log: {e}")

    print("Schema check test-case finished.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
