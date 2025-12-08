"""
Run schema validation using the utilities in the framework.
- Loads JSON schema from `customer_schema.json` (BigQuery fields mapped to JSON types)
- Generates mock data using `DataMocker.generate_from_json_schema`
- Validates generated records using `DataComparator.validate_schema`
- Produces a small JSON/HTML report via `ReportGenerator`

Run:
    python run_schema_validation.py

"""
import json
import os
import sys
from time import perf_counter
from pathlib import Path

# Make sure the utilities package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utilities.config_manager import config as CONFIG

from utilities.data_mocker import DataMocker
from utilities.data_comparator import DataComparator
from utilities.report_generator import ReportGenerator
from utilities.execution_log_manager import save_execution_report

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "customer_schema.json")
NUM_RECORDS = 5


def _resolve_reports_dir() -> Path:
    """Return the absolute path to the reports directory at repo root.
    
    This script is at: repo_root/sky-tests-automation/test-scripts/run_schema_validation.py
    parents[2] = repo_root
    reports_dir = repo_root / "reports"  (at repo root, not inside sky-tests-automation)
    """
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[2]
    reports_dir = repo_root / "reports"
    return reports_dir


def main():
    print("Schema validation runner starting...")

    if not os.path.exists(SCHEMA_FILE):
        print(f"Schema file not found: {SCHEMA_FILE}")
        return 2

    try:
        with open(SCHEMA_FILE, "r") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"Failed to read schema: {e}")
        return 2

    reports_dir = _resolve_reports_dir()
    report = ReportGenerator(report_dir=str(reports_dir))

    # Generate and validate records
    total_start = perf_counter()
    passed = 0
    failed = 0
    details = []

    for i in range(NUM_RECORDS):
        rec_start = perf_counter()
        # Generate a mock record from JSON schema
        try:
            record = DataMocker.generate_from_json_schema(SCHEMA_FILE)
        except Exception as e:
            print(f"Failed to generate record from schema: {e}")
            return 2

        # Validate generated record against schema
        try:
            is_valid, errors = DataComparator.validate_schema(record, schema)
        except Exception as e:
            is_valid = False
            errors = [f"Validation exception: {e}"]

        duration = perf_counter() - rec_start
        status = "PASSED" if is_valid else "FAILED"
        if is_valid:
            passed += 1
        else:
            failed += 1

        details.append({
            "index": i,
            "status": status,
            "duration_seconds": round(duration, 3),
            "errors": errors,
            "record": record
        })

        # Add result to report generator
        report.add_test_result(
            test_name=f"schema_validation_record_{i}",
            status=status,
            duration=duration,
            expected=schema,
            actual=record,
            errors=errors,
            jira_id=None
        )

        print(f"Record {i}: {status} (errors: {len(errors) if errors else 0})")

    total_duration = perf_counter() - total_start

    # Write final reports
    json_report = report.generate_json_report()
    html_report = report.generate_html_report()

    summary = {
        "schema_file": SCHEMA_FILE,
        "num_records": NUM_RECORDS,
        "passed": passed,
        "failed": failed,
        "total_duration_seconds": round(total_duration, 3),
        "details": details,
        "json_report": json_report,
        "html_report": html_report
    }

    summary_file = str(reports_dir / "schema_validation_summary.json")
    try:
        with open(summary_file, "w") as sf:
            json.dump(summary, sf, indent=2, default=str)
        print(f"Summary saved: {summary_file}")
    except Exception as e:
        print(f"Failed to save summary: {e}")

    # Save as the latest execution log (rotates previous latest)
    try:
        save_execution_report(summary)
        print("Saved latest execution log to sky-tests-automation/reports/latest_execution_logs.log")
    except Exception as e:
        print(f"Failed to save latest execution log: {e}")

    print("Schema validation runner finished.")
    print(f"Passed: {passed}, Failed: {failed}, Reports: {json_report}, {html_report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
