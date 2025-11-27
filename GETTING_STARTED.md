# Sky Test Automation Framework - Complete Utility Suite

## 📋 Overview

I've created a comprehensive test automation framework with **7 core utility classes** that address all your requirements. The framework is production-ready and follows industry best practices.

---

## 🎯 Core Utilities Created

### 1. **ConfigManager** (`utilities/config_manager.py`)
**Purpose**: Centralized configuration and environment management

**Features**:
- Singleton pattern for single instance
- Loads environment-specific JSON configs
- Supports dot notation for nested keys (`api.base_url`)
- Environment variable support via `TEST_ENV`
- Runtime configuration updates
- Config reloading

**Example**:
```python
from utilities.config_manager import config

env = config.get('environment')
api_url = config.get('api.base_url')
config.set('custom_key', 'value')
```

---

### 2. **LoggerManager** (`utilities/logger_manager.py`)
**Purpose**: Structured logging with execution reports

**Features**:
- Per-test-case logging with timestamp
- Both file and console output
- Logs expected vs actual results
- JSON execution reports with metadata
- Validation error tracking
- Organized directory structure per test

**Output Location**: `reports/latest_execution_logs/{test_name}/`
**Files**: `execution_*.log`, `execution_report_*.json`

**Example**:
```python
from utilities.logger_manager import LoggerManager

logger_mgr = LoggerManager('test_case_name')
logger = logger_mgr.logger

logger.info('Test started')
logger_mgr.log_result(expected, actual, errors)
logger_mgr.save_execution_report(status='PASSED')
```

---

### 3. **DataComparator** (`utilities/data_comparator.py`)
**Purpose**: Multi-format data comparison and validation

**Features**:
- Compares JSON objects with detailed diff reporting
- Loads and compares CSV, XML files
- Deep recursive comparison with path tracking
- Schema validation against JSON schemas
- Supports nested structures and arrays
- Comprehensive error reporting

**Supported Formats**: JSON, CSV, XML, XSD

**Example**:
```python
from utilities.data_comparator import DataComparator

# Compare JSON
is_equal, differences = DataComparator.compare_json(expected, actual)

# Compare files
is_equal, differences = DataComparator.compare_files('expected.json', 'actual.json')

# Validate against schema
is_valid, errors = DataComparator.validate_schema(data, schema)
```

---

### 4. **DataValidator** (`utilities/validator.py`)
**Purpose**: Comprehensive data validation with multiple rules

**Features**:
- **Null Check**: Validate required fields are populated
- **Type Validation**: Verify correct data types
- **Conditional Validation**: If field A = X, then field B must be populated
- **Range Validation**: Numeric value bounds checking
- **Enum Validation**: Allowed values checking
- **Pattern Validation**: Regex pattern matching
- **Custom Validators**: User-defined validation functions
- **Batch Validation**: Apply multiple rules at once

**Example**:
```python
from utilities.validator import DataValidator

data = {'email': 'test@example.com', 'age': 25, 'status': 'active'}

# Null check
errors = DataValidator.validate_not_null(data, ['email', 'age'])

# Conditional: if status='active', registration_date must exist
errors = DataValidator.validate_conditional(
    data, 'status', 'active', ['registration_date']
)

# All rules at once
rules = {
    'not_null': ['email'],
    'patterns': {'email': r'^[\w\.-]+@[\w\.-]+\.\w+$'},
    'ranges': {'age': (18, 100)},
    'enums': {'status': ['active', 'inactive']}
}
is_valid, all_errors = DataValidator.validate_all(data, rules)
```

---

### 5. **TestMarker** (`utilities/markers.py`)
**Purpose**: Pytest markers for test categorization and JIRA tracking

**Features**:
- **Test Categories**: smoke, regression, sanity, integration, unit
- **JIRA Tracking**: Tag tests with JIRA IDs (e.g., SKY-1234)
- **Combined Markers**: Multiple markers on single test
- **Parametrization**: Data-driven test support
- **Skip/XFail**: Skip or mark tests as expected to fail
- **Custom Markers**: Extensible marker system

**Example**:
```python
from utilities.markers import TestMarker

class TestMyFeature:
    @TestMarker.jira('SKY-1234')
    @TestMarker.smoke()
    def test_login(self):
        pass
    
    @TestMarker.parametrize('email,expected', [
        ('valid@test.com', True),
        ('invalid-email', False)
    ])
    def test_email_validation(self, email, expected):
        pass
```

**Run by Marker**:
```bash
pytest -m smoke              # Run smoke tests
pytest -m "jira and smoke"   # Run JIRA-tracked smoke tests
pytest -k "SKY-1234"         # Run specific JIRA ID
```

---

### 6. **ReportGenerator** (`utilities/report_generator.py`)
**Purpose**: Test execution report generation

**Features**:
- Generates HTML and JSON reports
- Summary statistics (pass rate, counts, duration)
- Per-test details with errors
- JIRA ID references
- Execution timestamps
- Professional HTML formatting

**Output Location**: `reports/test_report_{timestamp}.{html|json}`

**Example**:
```python
from utilities.report_generator import ReportGenerator

report_gen = ReportGenerator()

report_gen.add_test_result(
    test_name='test_login',
    status='PASSED',
    duration=2.5,
    expected={'result': 'success'},
    actual={'result': 'success'},
    jira_id='SKY-1234'
)

report_gen.generate_html_report()
report_gen.generate_json_report()
```

---

### 7. **DataMocker** (`utilities/data_mocker.py`)
**Purpose**: Generate test data from templates (LLM-ready)

**Features**:
- Generate random: strings, emails, phones, dates, numbers, UUIDs
- Template-based bulk generation
- JSON schema to data conversion
- Configurable patterns (alpha, alphanumeric, numeric)
- Nested objects and arrays support
- Batch data generation
- Custom field generators

**Example**:
```python
from utilities.data_mocker import DataMocker

# Generate single record
template = {
    'email': {'type': 'email'},
    'age': {'type': 'number', 'min': 18, 'max': 65},
    'status': {'type': 'enum', 'values': ['active', 'inactive']},
    'created_date': {'type': 'date'}
}
user_data = DataMocker.generate_data_from_template(template)

# Generate batch
batch = DataMocker.generate_batch_data(template, count=10)

# Generate from JSON schema
data = DataMocker.generate_from_json_schema('schema.json')
```

---

## 📁 Project Structure

```
sky-tests-automation/
├── config/
│   ├── config.dev.json        # Dev environment config
│   └── config.prod.json       # Prod environment config
│
├── test-scripts/
│   ├── nullcheck/             # Example test case
│   ├── example_test_user_registration.py
│   └── ... (other test cases)
│
├── utilities/
│   ├── __init__.py
│   ├── config_manager.py      ✅ Configuration management
│   ├── logger_manager.py      ✅ Test logging & reports
│   ├── data_comparator.py     ✅ Multi-format comparison
│   ├── validator.py           ✅ Data validation
│   ├── markers.py             ✅ Pytest markers + JIRA
│   ├── report_generator.py    ✅ Report generation
│   └── data_mocker.py         ✅ Test data generation
│
└── reports/
    ├── latest_execution_logs/ # Test logs (recreated each run)
    ├── test_report_*.html     # HTML reports
    └── test_report_*.json     # JSON reports
```

---

## ✅ Requirements Checklist

| # | Requirement | Status | Implementation |
|---|---|---|---|
| 1 | Utilities & Tests in different folders | ✅ | `utilities/` vs `test-scripts/` |
| 2 | Configurations in separate folder | ✅ | `config/` with env-specific files |
| 3 | Expected results & logs with comparison | ✅ | LoggerManager + DataComparator |
| 4 | Null check, schema, conditional fields | ✅ | DataValidator with all checks |
| 5 | Per-test folder structure | ✅ | LoggerManager creates per-test logs |
| 6 | Python & PyCharm only | ✅ | Pure Python, pytest native |
| 7 | Organization standards | ✅ | Type hints, docstrings, patterns |
| 8 | Reports in framework folder | ✅ | `reports/` with HTML & JSON |
| 9 | JIRA markers for test tags | ✅ | TestMarker with JIRA support |
| 10 | Data Mocker for test data | ✅ | DataMocker with templates |

---

## 📚 Documentation Files

1. **`FRAMEWORK_SUMMARY.md`** - Complete framework overview with all requirements
2. **`UTILITIES_GUIDE.md`** - Detailed usage guide for each utility
3. **`pytest.ini`** - Pytest configuration with markers
4. **`example_test_user_registration.py`** - Complete example using all utilities

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install pytest pytest-html
```

### 2. Create a New Test Case
```bash
python GenerateTestCaseFolder.py my_new_test
```

### 3. Write Your Test
```python
from utilities.markers import TestMarker
from utilities.logger_manager import LoggerManager
from utilities.data_mocker import DataMocker
from utilities.validator import DataValidator

class TestMyFeature:
    @TestMarker.jira('SKY-1234')
    @TestMarker.smoke()
    def test_something(self):
        logger_mgr = LoggerManager('test_something')
        
        # Generate test data
        data = DataMocker.generate_data_from_template({...})
        
        # Validate data
        is_valid, errors = DataValidator.validate_all(data, rules)
        
        # Log results
        logger_mgr.log_result(expected, actual, errors)
        logger_mgr.save_execution_report('PASSED')
```

### 4. Run Tests
```bash
# All tests
pytest

# By marker
pytest -m smoke

# By JIRA
pytest -k "SKY-1234"

# Generate reports
pytest --html=report.html
```

### 5. Check Results
- **Logs**: `sky-tests-automation/reports/latest_execution_logs/`
- **Reports**: `sky-tests-automation/reports/test_report_*.html`

---

## 🔧 Configuration

### Environment Variables
```bash
export TEST_ENV=dev      # or prod
export CONFIG_DIR=sky-tests-automation/config
```

### Config Files
**`config.dev.json`** / **`config.prod.json`**:
```json
{
  "environment": "dev",
  "test_timeout": 300,
  "log_level": "DEBUG",
  "api": {
    "base_url": "http://localhost:8080",
    "timeout": 30
  }
}
```

---

## 💡 Key Features

✅ **Modular Design** - Independent, reusable utilities
✅ **Comprehensive Logging** - File + console with structured output
✅ **Multi-Format Support** - JSON, CSV, XML comparison
✅ **Data Validation** - Null, type, schema, conditional, range, enum, pattern
✅ **Test Categorization** - Markers with JIRA tracking
✅ **Report Generation** - HTML & JSON with statistics
✅ **Data Generation** - Template-based mock data (LLM-ready)
✅ **PyCharm Native** - Full IDE support
✅ **Best Practices** - Type hints, docstrings, patterns
✅ **Extensible** - Easy to add new validators, comparators, markers

---

## 📞 Next Steps

1. **Review** `FRAMEWORK_SUMMARY.md` and `UTILITIES_GUIDE.md`
2. **Study** `example_test_user_registration.py` for complete usage
3. **Create** your first test case with `GenerateTestCaseFolder.py`
4. **Run** tests with pytest markers
5. **Check** reports in `reports/` folder

All utilities are production-ready and follow industry best practices! 🎉
