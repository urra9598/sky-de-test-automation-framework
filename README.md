# Sky Test Automation Framework 
A scalable Python-based test automation framework for the Data QA team to validate ETL pipelines, UDM transformations, data quality rules, and end-to-end data integrity.

A comprehensive, production-ready **Python-based test automation framework** with enterprise-grade utilities for test automation, data validation, and reporting.

## ✨ Quick Overview

This framework consists the following utility classes:
- Configuration management (multi-environment)
- Test logging with execution reports
- Multi-format data comparison (JSON, CSV, XML)
- Advanced data validation (7 rule types)
- Test categorization with JIRA tracking
- Professional report generation (HTML, JSON)
- Intelligent test data generation

## Key Features

| Feature | Details |
|---------|---------|
| **Utilities** | ConfigManager, LoggerManager, DataComparator, DataValidator, TestMarker, ReportGenerator, DataMocker |
| **Multi-Format Support** | JSON, CSV, XML data comparison and validation |
| **JIRA Integration** | Track tests with JIRA IDs and run by marker |
| **Environment Config** | Dev/Prod configuration management |
| **Report Generation** | Professional HTML and JSON reports |
| **Test Categorization** | Smoke, regression, sanity, integration, unit |
| **PyCharm Ready** | Full IDE integration and support |

## Framework Structure

```
sky-tests-automation/
├── utilities/              ← Utility classes
│   ├── config_manager.py
│   ├── logger_manager.py
│   ├── data_comparator.py
│   ├── validator.py
│   ├── markers.py
│   ├── report_generator.py
│   └── data_mocker.py
├── config/                 ← Environment-specific configs
│   ├── config.dev.json
│   └── config.prod.json
├── test-scripts/           ← Test cases
│   └── example_test_user_registration.py
└── reports/                ← Generated logs & reports
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Test Case - Automatic tests generator
```bash
python GenerateTestCaseFolder.py my_test_case
```

### 3. Write Tests Using Utilities
```python
from utilities.markers import TestMarker
from utilities.logger_manager import LoggerManager
from utilities.data_mocker import DataMocker
from utilities.validator import DataValidator

@TestMarker.jira('SKY-1234')
@TestMarker.smoke()
def test_my_feature():
    logger_mgr = LoggerManager('test_my_feature')
    
    # Generate test data
    data = DataMocker.generate_data_from_template({
        'email': {'type': 'email'},
        'age': {'type': 'number', 'min': 18, 'max': 100}
    })
    
    # Validate data
    is_valid, errors = DataValidator.validate_all(data, {
        'not_null': ['email'],
        'patterns': {'email': r'^[\w\.-]+@[\w\.-]+\.\w+$'}
    })
    
    # Log & report
    logger_mgr.save_execution_report(status='PASSED' if is_valid else 'FAILED')
    assert is_valid
```

### 4. Run Tests
```bash
pytest -v -m smoke
```

### 5. View Reports
```
Location: sky-tests-automation/reports/test_report_*.html
```

## Documentation

### 1. ConfigManager
```python
from utilities.config_manager import config
api_url = config.get('api.base_url')
```

### 2. LoggerManager
```python
logger_mgr = LoggerManager('test_name')
logger_mgr.save_execution_report(status='PASSED')
```

### 3. DataComparator
```python
is_equal, diffs = DataComparator.compare_json(expected, actual)
```

### 4. DataValidator
```python
is_valid, errors = DataValidator.validate_all(data, rules)
```

### 5. TestMarker
```python
@TestMarker.jira('SKY-1234')
@TestMarker.smoke()
def test_something():
    pass
```

### 6. ReportGenerator
```python
report_gen = ReportGenerator()
report_gen.generate_html_report()
```

### 7. DataMocker
```python
data = DataMocker.generate_data_from_template(template)
```


## Sample Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Create test case
python GenerateTestCaseFolder.py test_name

# Run all tests
pytest -v

# Run smoke tests
pytest -m smoke

# Run JIRA-tracked tests
pytest -k "SKY-1234"

# Generate report
pytest --html=report.html --self-contained-html
```


## Get Started

1. **Read**: `README.md` (navigation guide)
2. **Install**: `pip install -r requirements.txt`
3. **Learn**: `GETTING_STARTED.md`
4. **Create**: `python GenerateTestCaseFolder.py first_test`
5. **Run**: `pytest -v -m smoke`
