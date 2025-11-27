# Sky Test Automation Framework - Quick Reference

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Your First Test Case
```bash
python GenerateTestCaseFolder.py my_first_test
```

### 3. Run Tests
```bash
pytest -v -m smoke
```

### 4. View Reports
```
Open: sky-tests-automation/reports/test_report_*.html
```

---

## 📝 Common Code Snippets

### Initialize Test with Logging
```python
from utilities.logger_manager import LoggerManager

logger_mgr = LoggerManager('my_test_name')
logger = logger_mgr.logger

logger.info('Starting test')
# ... test logic ...
logger_mgr.save_execution_report(status='PASSED')
```

### Generate Test Data
```python
from utilities.data_mocker import DataMocker

template = {
    'email': {'type': 'email'},
    'age': {'type': 'number', 'min': 18, 'max': 100},
    'name': {'type': 'string', 'length': 15}
}

data = DataMocker.generate_data_from_template(template)
```

### Validate Data
```python
from utilities.validator import DataValidator

rules = {
    'not_null': ['email', 'name'],
    'patterns': {'email': r'^[\w\.-]+@[\w\.-]+\.\w+$'},
    'ranges': {'age': (18, 100)}
}

is_valid, errors = DataValidator.validate_all(data, rules)
assert is_valid, f"Validation failed: {errors}"
```

### Compare Results
```python
from utilities.data_comparator import DataComparator

is_equal, differences = DataComparator.compare_json(
    expected={'status': 'success'},
    actual={'status': 'success'}
)

assert is_equal, f"Results don't match: {differences}"
```

### Add Test Markers
```python
from utilities.markers import TestMarker

@TestMarker.jira('SKY-1234')
@TestMarker.smoke()
def test_my_feature():
    pass
```

### Generate Report
```python
from utilities.report_generator import ReportGenerator

report_gen = ReportGenerator()
report_gen.add_test_result(
    test_name='test_login',
    status='PASSED',
    duration=2.5,
    jira_id='SKY-1234'
)
report_gen.generate_html_report()
```

### Load Configuration
```python
from utilities.config_manager import config

api_url = config.get('api.base_url')
timeout = config.get('test_timeout', 300)
```

---

## 🏷️ Pytest Marker Commands

```bash
# Run smoke tests
pytest -m smoke

# Run regression tests
pytest -m regression

# Run JIRA-tracked tests
pytest -m jira

# Run tests for specific JIRA
pytest -k "SKY-1234"

# Run smoke AND regression
pytest -m "smoke and regression"

# Run smoke OR integration
pytest -m "smoke or integration"

# Run tests BUT NOT skipped
pytest -m "not skip"

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Generate HTML report
pytest --html=report.html --self-contained-html

# Show print statements
pytest -s

# Run specific file
pytest sky-tests-automation/test-scripts/test_file.py
```

---

## 📁 Directory Structure Quick Reference

```
├── sky-tests-automation/
│   ├── config/
│   │   ├── config.dev.json
│   │   └── config.prod.json
│   ├── test-scripts/
│   │   └── my_test_case/
│   │       ├── my_test_case.py
│   │       ├── expected-result/
│   │       └── logs/
│   ├── utilities/
│   │   ├── config_manager.py
│   │   ├── logger_manager.py
│   │   ├── data_comparator.py
│   │   ├── validator.py
│   │   ├── markers.py
│   │   ├── report_generator.py
│   │   └── data_mocker.py
│   └── reports/
│       ├── latest_execution_logs/
│       ├── test_report_*.html
│       └── test_report_*.json
├── pytest.ini
├── requirements.txt
├── GETTING_STARTED.md
├── FRAMEWORK_SUMMARY.md
├── UTILITIES_GUIDE.md
└── ARCHITECTURE.md
```

---

## ✅ Validation Rules Cheat Sheet

```python
# All validation examples
rules = {
    # Require fields to be non-empty
    'not_null': ['email', 'name'],
    
    # Check field types
    'types': {
        'age': int,
        'email': str,
        'active': bool
    },
    
    # If one field has value, another must be populated
    'conditionals': [
        {
            'condition_field': 'status',
            'condition_value': 'active',
            'required_fields': ['activation_date', 'activation_by']
        }
    ],
    
    # Numeric ranges
    'ranges': {
        'age': (18, 100),
        'score': (0, 100)
    },
    
    # Allowed values
    'enums': {
        'status': ['active', 'inactive', 'pending'],
        'priority': ['low', 'medium', 'high']
    },
    
    # Regex patterns
    'patterns': {
        'email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
        'phone': r'^\+?1?\d{9,15}$',
        'username': r'^[a-zA-Z0-9_]{3,20}$'
    },
    
    # Custom validation functions
    'custom': {
        'age': lambda x: None if x >= 18 else "Must be 18 or older"
    }
}

is_valid, errors = DataValidator.validate_all(data, rules)
```

---

## 🔧 Configuration Examples

### config.dev.json
```json
{
  "environment": "dev",
  "test_timeout": 300,
  "log_level": "DEBUG",
  "api": {
    "base_url": "http://localhost:8080",
    "timeout": 30
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "test_db"
  }
}
```

### Accessing Config
```python
from utilities.config_manager import config

env = config.get('environment')           # 'dev'
url = config.get('api.base_url')         # 'http://localhost:8080'
port = config.get('database.port')       # 5432
timeout = config.get('unknown', 100)     # 100 (default)
```

---

## 📊 Data Mocker Templates

### Simple Template
```python
template = {
    'email': {'type': 'email'},
    'age': {'type': 'number', 'min': 18, 'max': 100},
    'active': {'type': 'enum', 'values': [True, False]},
    'date': {'type': 'date'}
}
```

### Complex Template
```python
template = {
    'user': {
        'type': 'object',
        'properties': {
            'email': {'type': 'email'},
            'profile': {
                'type': 'object',
                'properties': {
                    'firstname': {'type': 'string', 'length': 10},
                    'age': {'type': 'number', 'min': 18, 'max': 100}
                }
            }
        }
    },
    'tags': {
        'type': 'array',
        'items': {'type': 'string', 'length': 5},
        'count': 3
    }
}
```

---

## 🐛 Troubleshooting

### Issue: Tests not found
**Solution**: Check `pytest.ini` and ensure test files match pattern (`test_*.py`)

### Issue: Config file not loading
**Solution**: Verify config file exists at `sky-tests-automation/config/config.{env}.json`

### Issue: Logger not creating logs
**Solution**: Ensure `reports/` directory exists or use `LoggerManager` which creates it

### Issue: Comparison failing on similar values
**Solution**: Check data types - `"123"` (string) ≠ `123` (int)

### Issue: Validation passing when should fail
**Solution**: Review `validate_all()` rules - all rules must pass

---

## 📞 Common Commands

```bash
# Install requirements
pip install -r requirements.txt

# Create new test case
python GenerateTestCaseFolder.py test_name

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run smoke tests only
pytest -m smoke

# Run specific test file
pytest sky-tests-automation/test-scripts/test_file.py

# Run and stop on first failure
pytest -x

# Generate HTML report
pytest --html=report.html --self-contained-html

# Run with coverage
pytest --cov=sky-tests-automation/utilities

# List all markers
pytest --markers

# Dry run (show what would run)
pytest --collect-only
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `GETTING_STARTED.md` | Project overview & setup |
| `FRAMEWORK_SUMMARY.md` | Requirements checklist |
| `UTILITIES_GUIDE.md` | Detailed utility documentation |
| `ARCHITECTURE.md` | System architecture & diagrams |
| `README.md` | Quick reference guide (this file) |
| `pytest.ini` | Pytest configuration |
| `requirements.txt` | Project dependencies |

---

## 🎓 Learning Path

1. **Start**: Read `GETTING_STARTED.md`
2. **Understand**: Study `ARCHITECTURE.md` 
3. **Learn**: Review `example_test_user_registration.py`
4. **Reference**: Use `UTILITIES_GUIDE.md` while coding
5. **Implement**: Create your own tests
6. **Optimize**: Check `FRAMEWORK_SUMMARY.md` for best practices

---

## 💡 Pro Tips

✅ Use `DataValidator` before executing tests to catch data issues early
✅ Always use `@TestMarker.jira()` to track tests to requirements
✅ Keep test data in `data_mocker.py` templates for consistency
✅ Use `pytest -m` to run subsets of tests by category
✅ Check reports in `reports/` folder after test runs
✅ Leverage conditional validation for complex business rules
✅ Use parametrize marker for data-driven testing
✅ Configure environment via `TEST_ENV` variable

---

## 🔗 Related Files

- Test example: `sky-tests-automation/test-scripts/example_test_user_registration.py`
- Configuration: `sky-tests-automation/config/config.{dev|prod}.json`
- Test generator: `GenerateTestCaseFolder.py`
- Pytest config: `pytest.ini`

---

## 📞 Support

For detailed information on any utility:
- See `UTILITIES_GUIDE.md` for usage examples
- See `example_test_user_registration.py` for complete implementation
- Check individual utility files for docstrings and comments

**Happy Testing! 🎉**
