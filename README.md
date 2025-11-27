# Sky Test Automation Framework 
A scalable Python-based test automation framework for the Data QA team to validate ETL pipelines, UDM transformations, data quality rules, and end-to-end data integrity.

A comprehensive, production-ready **Python-based test automation framework** with enterprise-grade utilities for test automation, data validation, and reporting.

## ✨ Quick Overview

This framework provides **7 core utility classes** for:
- ✅ Configuration management (multi-environment)
- ✅ Test logging with execution reports
- ✅ Multi-format data comparison (JSON, CSV, XML)
- ✅ Advanced data validation (7 rule types)
- ✅ Test categorization with JIRA tracking
- ✅ Professional report generation (HTML, JSON)
- ✅ Intelligent test data generation

## 🎯 Key Features

| Feature | Details |
|---------|---------|
| **7 Core Utilities** | ConfigManager, LoggerManager, DataComparator, DataValidator, TestMarker, ReportGenerator, DataMocker |
| **50+ Methods** | Comprehensive functionality across all utilities |
| **Multi-Format Support** | JSON, CSV, XML data comparison and validation |
| **JIRA Integration** | Track tests with JIRA IDs and run by marker |
| **Environment Config** | Dev/Prod configuration management |
| **Report Generation** | Professional HTML and JSON reports |
| **Data Validation** | Null check, type, schema, conditional, range, enum, pattern |
| **Test Categorization** | Smoke, regression, sanity, integration, unit |
| **PyCharm Ready** | Full IDE integration and support |

## 📦 What's Included

```
sky-tests-automation/
├── utilities/              ← 7 core utility classes (~1,450 lines)
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
├── test-scripts/           ← Your test cases
│   └── example_test_user_registration.py
└── reports/                ← Generated logs & reports
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Test Case
```bash
python GenerateTestCaseFolder.py my_test_case
```

### 3. Write Test Using Utilities
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

## 📚 Documentation

Start with **`INDEX.md`** for navigation guide to all documentation.

| Document | Purpose |
|----------|---------|
| **INDEX.md** | 📍 Navigation guide - START HERE |
| **GETTING_STARTED.md** | Setup and quick start (10 min read) |
| **QUICK_REFERENCE.md** | Code snippets and commands |
| **UTILITIES_GUIDE.md** | Detailed documentation for each utility |
| **ARCHITECTURE.md** | System design and diagrams |
| **FRAMEWORK_SUMMARY.md** | Requirements verification |
| **DELIVERY_SUMMARY.md** | Project completion overview |

## 🔧 7 Core Utilities

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

## ✅ All 10 Requirements Implemented

✅ Utilities and Tests in different folders
✅ Configurations for general setup
✅ Expected results & logs with comparison
✅ Null check, schema, conditional fields
✅ Per-test-case folder structure
✅ Python and PyCharm only
✅ Organization standards
✅ Reports and full execution logs
✅ Markers for JIRA IDs
✅ Data Mocker for test data

## 💡 Common Commands

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

## 🎓 Learning Path (30 minutes)

1. Install: `pip install -r requirements.txt` (1 min)
2. Read: `GETTING_STARTED.md` (10 min)
3. Review: `ARCHITECTURE.md` (10 min)
4. Study: `example_test_user_registration.py` (5 min)
5. Try: `pytest -v` (4 min)

## 📊 Framework Statistics

- **Utility Classes**: 7
- **Core Methods**: 50+
- **Utility Code**: ~1,450 lines
- **Documentation**: ~1,500 lines
- **Total Implementation**: ~2,950 lines

## 🔐 Production Ready

✅ All 10 requirements implemented
✅ Comprehensive documentation
✅ Example test provided
✅ Best practices applied
✅ Enterprise-grade utilities

## 🚀 Get Started

1. **Read**: `INDEX.md` (navigation guide)
2. **Install**: `pip install -r requirements.txt`
3. **Learn**: `GETTING_STARTED.md`
4. **Create**: `python GenerateTestCaseFolder.py first_test`
5. **Run**: `pytest -v -m smoke`

---

**Happy Testing! 🎉**
*Production Ready - November 15, 2025*
