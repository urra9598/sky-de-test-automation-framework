# Sky Test Automation Framework - Complete Utility Suite


### 1. **ConfigManager** (`utilities/config_manager.py`)
**Purpose**: Centralized configuration and environment management

**Features**:
- Singleton pattern for single instance
- Loads environment-specific JSON configs
- Environment variable support via `TEST_ENV`
- Runtime configuration updates
- Config reloading


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


---

### 5. **TestMarker** (`utilities/markers.py`)
**Purpose**: Pytest markers for test categorization and JIRA tracking

**Features**:
- **Test Categories**: smoke, regression, sanity, integration, unit
- **JIRA Tracking**: Tag tests with JIRA IDs (e.g., JIRA-1234)
- **Combined Markers**: Multiple markers on single test
- **Parametrization**: Data-driven test support
- **Skip/XFail**: Skip or mark tests as expected to fail
- **Custom Markers**: Extensible marker system

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
│   ├── config_manager.py      # Configuration management
│   ├── logger_manager.py      # Test logging & reports
│   ├── data_comparator.py     # Multi-format comparison
│   ├── validator.py           # Data validation
│   ├── markers.py             # Pytest markers + JIRA
│   ├── report_generator.py    # Report generation
│   └── data_mocker.py         # Test data generation
│
└── reports/
    ├── latest_execution_logs/ # Test logs (recreated each run)
    ├── test_report_*.html     # HTML reports
    └── test_report_*.json     # JSON reports
```

---


## Getting Started

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

##  Key Features

 **Modular Design** - Independent, reusable utilities
 **Comprehensive Logging** - File + console with structured output
 **Multi-Format Support** - JSON, CSV, XML comparison
 **Data Validation** - Null, type, schema, conditional, range, enum, pattern
 **Test Categorization** - Markers with JIRA tracking
 **Report Generation** - HTML & JSON with statistics
 **Data Generation** - Template-based mock data
 **PyCharm Native** - Full IDE support
 **Best Practices** - Type hints, docstrings, patterns
 **Extensible** - Easy to add new validators, comparators, markers

