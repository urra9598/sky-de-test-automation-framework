# Repository Structure Guide

This document explains the organization and purpose of each folder and key file in the `sky-de-test-automation-framework` project.

## Root Level Files & Folders

### `/reports/`
**Central repository for all test execution reports and logs.**

- **Purpose:** Contains all generated test reports, execution logs, and rotated historical logs
- **Contents:**
  - `latest_execution_logs.log` - The most recent test execution report (JSON format)
  - `log_<YYYYMMDD_HHMMSS>.log` - Rotated older logs (kept according to retention policy, default: 10 most recent)
  - `test_report_<YYYYMMDD_HHMMSS>.json` - JSON format test report
  - `test_report_<YYYYMMDD_HHMMSS>.html` - HTML format test report (viewable in browser)
- **Location:** At repo root (not inside test code) to keep reports separate from source code
- **Auto-created:** Yes, runners will create if it doesn't exist

### `/sky-tests-automation/`
**Main test automation framework package directory.**

Contains the core framework code, configurations, utilities, and test-case definitions.

---

## `/sky-tests-automation/` Structure

### `/sky-tests-automation/config/`
**Configuration files for different environments.**

- **Purpose:** Store environment-specific configuration settings
- **Files:**
  - `config.dev.json` - Development environment config (local testing)
  - `config.prod.json` - Production environment config (integration/staging)
- **Usage:** Loaded by `ConfigManager` based on `TEST_ENV` environment variable (default: dev)
- **Keys available:**
  - `environment` - Environment name
  - `test_timeout` - Test timeout in seconds
  - `log_level` - Logging level (INFO, DEBUG, etc.)
  - `report_format` - Report formats to generate (html, json)
  - `data_formats` - Supported data formats (json, csv, xml)
  - `enable_screenshots` - Whether to capture screenshots (boolean)
  - `retry_count` - Number of retries for failed tests
  - `reports_dir` - Directory for reports (default: "reports")
  - `log_retention` - Number of rotated logs to keep (default: 10)

### `/sky-tests-automation/utilities/`
**Reusable utility modules for test automation.**

Core framework components that are imported and used by all test-case runners.

#### Files in `/sky-tests-automation/utilities/`

**`__init__.py`**
- Package initialization file
- Re-exports commonly used functions for easier imports

**`config_manager.py`**
- **Class:** `ConfigManager` (Singleton pattern)
- **Purpose:** Centralized configuration management
- **Key Methods:**
  - `get(key, default=None)` - Get config value (supports dot notation for nested keys)
  - `set(key, value)` - Set config value
  - `get_all()` - Get entire config dictionary
  - `reload()` - Reload config from files
- **Usage:** `from utilities.config_manager import config; value = config.get("test_timeout")`

**`logger_manager.py`**
- **Class:** `LoggerManager`
- **Purpose:** Per-test case logging and execution report tracking
- **Key Methods:**
  - `log_info(message)` - Log info level message
  - `log_error(message, exception=None)` - Log error with optional exception details
  - `log_result(expected, actual, validation_errors)` - Log test result comparison
  - `save_execution_report(status="PASSED", failure_reason=None)` - Save execution report (also sends to central reports folder)
- **Behavior:** Automatically calls `save_execution_report` to update the central `latest_execution_logs.log`

**`execution_log_manager.py`**
- **Purpose:** Central execution log rotation and retention management
- **Key Functions:**
  - `save_execution_report(report, logs_dir=None, log_name='latest_execution_logs.log', as_json=True, timestamp_fmt='%Y%m%d_%H%M%S')` - Save and rotate logs
  - `read_latest_report(logs_dir=None, log_name='latest_execution_logs.log')` - Read the latest execution report
- **Auto-rotation:** When a new report is saved, previous `latest_execution_logs.log` is renamed to `log_<timestamp>.log`
- **Retention Policy:** Keeps only N most recent rotated logs (configurable via `log_retention` config, default: 10)
- **Reports Directory:** Defaults to `repo_root/reports/`

**`data_mocker.py`**
- **Class:** `DataMocker`
- **Purpose:** Generate synthetic test data
- **Key Methods:**
  - `generate_string(length=10)` - Generate random string
  - `generate_email()` - Generate random email
  - `generate_phone()` - Generate random phone number
  - `generate_date()` - Generate random date
  - `generate_number(min=0, max=100)` - Generate random number
  - `generate_uuid()` - Generate random UUID
  - `generate_from_template(template)` - Generate data from template dict
  - `generate_batch_data(template, count)` - Generate multiple records from template
  - `generate_from_json_schema(schema_file)` - Generate data matching JSON schema
- **Usage:** Create mock records for testing without using real data

**`data_comparator.py`**
- **Class:** `DataComparator`
- **Purpose:** Compare and validate test data
- **Key Methods:**
  - `load_data(file_path)` - Load data from JSON/CSV/XML files
  - `compare_json(expected, actual)` - Deep comparison of JSON data
  - `compare_files(file1, file2)` - Compare two data files
  - `validate_schema(record, schema)` - Validate a record against JSON schema
  - `_compare_recursive(expected, actual)` - Recursive comparison helper
- **Usage:** Validate generated mock data against expected schemas

**`validator.py`**
- **Class:** `DataValidator`
- **Purpose:** Perform various data validation checks
- **Key Methods:**
  - `validate_not_null(value)` - Check value is not null
  - `validate_type(value, expected_type)` - Check value is of expected type
  - `validate_conditional(value, condition)` - Validate conditional rules
  - `validate_range(value, min, max)` - Validate numeric range
  - `validate_enum(value, allowed_values)` - Validate against allowed values
  - `validate_pattern(value, regex_pattern)` - Validate against regex pattern
  - `validate_custom(value, custom_func)` - Validate with custom function
  - `validate_all(value, rules)` - Run multiple validations
- **Usage:** Apply business logic validation rules to test data

**`report_generator.py`**
- **Class:** `ReportGenerator`
- **Purpose:** Generate test execution reports in multiple formats
- **Key Methods:**
  - `add_test_result(test_name, status, duration, expected, actual, errors, jira_id)` - Add a test result
  - `generate_json_report()` - Generate JSON format report
  - `generate_html_report()` - Generate HTML format report
- **Reports Generated:**
  - JSON report with detailed test results, execution summary, timestamps
  - HTML report with visual formatting, pass/fail summary, details per test
- **Location:** Reports saved to configured `reports_dir` (default: `repo_root/reports/`)

**`markers.py`**
- **Class:** `TestMarker`
- **Purpose:** Pytest markers for test categorization and JIRA integration
- **Key Methods:**
  - `jira(jira_id)` - Mark test with JIRA ticket ID
  - `smoke()` - Mark as smoke test
  - `regression()` - Mark as regression test
  - `parametrization()` - Helper for parametrized tests
- **Usage:** `@TestMarker.jira("JIRA-123")` or `@pytest.mark.smoke`
- **Benefits:** Allows filtering tests by type, linking to JIRA issues

### `/sky-tests-automation/test-scripts/`
**Container directory for all test-case implementations.**

Each subdirectory is a self-contained test-case with its own schema, runner, and expected results.

**General Structure of Each Test-Case:**
```
test-case-name/
├── <schema-file>.json              # Test data schema (e.g., customer_schema.json)
├── <runner-script>.py              # Executable test runner (e.g., schemavalidation.py)
├── expected-result/
│   └── expected_records.json       # Expected test output/records
└── <testcase>_summary.json         # Per-test-case execution summary
```

#### Example Test-Case: `/sky-tests-automation/test-scripts/schema_check/`
**Purpose:** Validate customer data against a JSON schema.

- **`customer_schema.json`**
  - JSON Schema file defining the structure and rules for customer data
  - Used by `DataMocker` to generate valid test records
  - Used by `DataComparator` to validate records

- **`schemavalidation.py`**
  - Executable test runner for the schema_check test-case
  - Workflow:
    1. Loads customer_schema.json
    2. Generates N mock customer records using DataMocker
    3. Validates each record against the schema using DataComparator
    4. Saves expected records to expected-result/expected_records.json
    5. Generates global reports (JSON/HTML) in repo_root/reports/
    6. Saves per-test-case summary to schema_validation_summary.json
    7. Updates central latest_execution_logs.log with execution details
  - **Run:** `python3 schemavalidation.py` (from schema_check directory)

- **`expected-result/expected_records.json`**
  - Contains the N mock records generated and validated in the last test run
  - Used for regression testing (comparing future runs against this baseline)
  - Overwritten each test run with new expected data

- **`schema_validation_summary.json`**
  - Per-test-case summary (separate from central reports)
  - Contains: test_case name, num_records, passed/failed counts, duration, individual result details

#### Example Test-Case: `/sky-tests-automation/test-scripts/nullcheck/`
**Purpose:** Validate data for null/missing field checks.**

- **`nullcheck_schema.json`** (or similar)
  - Defines what fields must not be null

- **`nullcheck.py`**
  - Executable test runner for nullcheck validation
  - Similar structure to schemavalidation.py but with null-check specific logic

- **`expected-result/`**
  - Expected records for null-check validation

---

## File Descriptions

### Root Level Files

**`requirements.txt`**
- Python package dependencies for the project
- Includes: pytest, pytest-html, jsonschema, pandas, Jinja2, black, flake8, mypy, pylint, pyflakes
- Install: `pip install -r requirements.txt`

**`pytest.ini`**
- Pytest configuration file
- Defines test discovery patterns, markers, and output options

**`.gitignore`**
- Git ignore patterns to exclude files from version control
- Typically excludes: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `reports/` (optional)

**`README.md`**
- Project overview and quick start guide

**`GETTING_STARTED.md`**
- Detailed getting started guide with setup instructions

**`UTILITIES_GUIDE.md`**
- Comprehensive guide to using the utility modules

**`ARCHITECTURE.md`**
- Architecture and design decisions documentation

**`QUICK_REFERENCE.md`**
- Quick reference for common tasks and commands

**`FRAMEWORK_SUMMARY.md`**
- High-level framework summary and features

**`DELIVERY_SUMMARY.md`**
- Delivery information and checklist

**`COMPLETION_REPORT.md`**
- Project completion report

---

## Workflow Summary

### To Create a New Test-Case:

1. Create a new folder under `sky-tests-automation/test-scripts/`
   ```
   mkdir sky-tests-automation/test-scripts/my_new_test
   ```

2. Create the schema file (e.g., `my_schema.json`)
   ```
   sky-tests-automation/test-scripts/my_new_test/my_schema.json
   ```

3. Create the test runner script (e.g., `my_test.py`)
   - Import utilities: `from utilities.data_mocker import DataMocker`
   - Use `_resolve_reports_dir()` to get central reports directory
   - Generate data, validate, save results

4. Create expected-result folder
   ```
   mkdir sky-tests-automation/test-scripts/my_new_test/expected-result
   ```

5. Run the test
   ```
   cd sky-tests-automation/test-scripts/my_new_test
   python3 my_test.py
   ```

6. Reports will be generated in `reports/` at repo root

### To Run an Existing Test-Case:

```bash
cd sky-tests-automation/test-scripts/schema_check
python3 schemavalidation.py
```

### To View Reports:

- **Latest execution log:** `reports/latest_execution_logs.log` (JSON)
- **HTML report:** `reports/test_report_YYYYMMDD_HHMMSS.html` (open in browser)
- **JSON report:** `reports/test_report_YYYYMMDD_HHMMSS.json` (machine-readable)

### Log Rotation:

Each time a test runs, the old `latest_execution_logs.log` is automatically rotated to `log_<YYYYMMDD_HHMMSS>.log`. The retention policy (default: 10) ensures old logs are removed to save disk space.

---

## Key Design Principles

1. **Separation of Concerns:** Test code lives in `sky-tests-automation/`, reports live at repo root
2. **Self-Contained Test-Cases:** Each test-case has its own schema, runner, and expected results
3. **Centralized Reports:** All global reports and logs go to `repo_root/reports/`
4. **Reusable Utilities:** Common functionality in `utilities/` is imported by all test-cases
5. **Configuration-Driven:** Environment-specific configs in `config/`
6. **Automatic Log Rotation:** Prevents disk space issues with historical logs
7. **No logs in test folders:** Keeps test-case directories clean and minimal

---

## Environment Variables

- **`TEST_ENV`** - Environment to load (dev, prod). Default: dev
- **`CONFIG_DIR`** - Path to config directory. Default: `sky-tests-automation/config`
- **`SKY_TESTS_DIR`** - Base directory for tests (used by GenerateTestCaseFolder.py). Default: current directory

---

## Typical Directory Tree

```
sky-de-test-automation-framework/
├── reports/                                 # Central reports (auto-created)
│   ├── latest_execution_logs.log
│   ├── log_20251115_011101.log
│   ├── test_report_20251115_014014.json
│   └── test_report_20251115_014014.html
│
├── sky-tests-automation/
│   ├── config/
│   │   ├── config.dev.json
│   │   └── config.prod.json
│   │
│   ├── utilities/
│   │   ├── __init__.py
│   │   ├── config_manager.py
│   │   ├── logger_manager.py
│   │   ├── execution_log_manager.py
│   │   ├── data_mocker.py
│   │   ├── data_comparator.py
│   │   ├── validator.py
│   │   ├── report_generator.py
│   │   ├── markers.py
│   │   └── __pycache__/
│   │
│   └── test-scripts/
│       ├── schema_check/
│       │   ├── customer_schema.json
│       │   ├── schemavalidation.py
│       │   ├── schema_validation_summary.json
│       │   └── expected-result/
│       │       └── expected_records.json
│       │
│       └── nullcheck/
│           ├── nullcheck_schema.json
│           ├── nullcheck.py
│           ├── nullcheck_summary.json
│           └── expected-result/
│               └── expected_records.json
│
├── requirements.txt
├── pytest.ini
├── README.md
└── REPOSITORY_STRUCTURE.md                  # This file
```

---

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run a specific test-case
cd sky-tests-automation/test-scripts/schema_check
python3 schemavalidation.py

# Run all tests using pytest
pytest sky-tests-automation/test-scripts/

# View HTML report (after running a test)
open reports/test_report_*.html

# List generated reports
ls -la reports/

# Check latest execution log
cat reports/latest_execution_logs.log
```

---

## Support & Questions

- See `UTILITIES_GUIDE.md` for detailed utility usage
- See `GETTING_STARTED.md` for setup and configuration
- See `ARCHITECTURE.md` for design and patterns
