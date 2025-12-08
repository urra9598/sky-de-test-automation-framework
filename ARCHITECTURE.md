# Sky Test Automation Framework - Architecture Overview

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Test Execution Layer                          │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Test Cases (test-scripts/)                                 │ │
│  │ - Example: test_user_registration.py                       │ │
│  │ - Markers: @smoke, @regression, @jira('SKY-1234')          │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Utilities Layer                               │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ ConfigManager (config_manager.py)                        │   │
│  │ - Load: config.{dev|prod}.json                           │   │
│  │ - Singleton pattern                                      │   │
│  │ - Nested key support (api.base_url)                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ LoggerManager (logger_manager.py)                        │   │
│  │ - Structured logging (file + console)                    │   │
│  │ - Per-test execution logs                                │   │
│  │ - JSON execution reports                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ DataMocker (data_mocker.py)                              │   │
│  │ - Generate: strings, emails, phones, dates, UUIDs        │   │
│  │ - Template-based generation                              │   │
│  │ - Batch generation                                       │   │
│  │ - JSON schema conversion                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│           │                    │                │                │
│           ▼                    ▼                ▼                │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  │ DataValidator    │  │ DataComparator   │  │ ReportGenerator  │
│  │ (validator.py)   │  │ (data_comparator │  │ (report_generat  │
│  │                  │  │ .py)             │  │ or.py)           │
│  │ - Null check     │  │                  │  │                  │
│  │ - Type check     │  │ - JSON compare   │  │ - HTML reports   │
│  │ - Schema valid   │  │ - CSV compare    │  │ - JSON reports   │
│  │ - Conditional    │  │ - XML compare    │  │ - Statistics     │
│  │ - Range check    │  │ - Deep diff      │  │ - JIRA links     │
│  │ - Enum check     │  │ - Path tracking  │  │                  │
│  │ - Pattern check  │  │ - Schema valid   │  │                  │
│  │ - Custom rules   │  │                  │  │                  │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ TestMarker (markers.py)                                  │   │
│  │ - Categories: smoke, regression, sanity, integration    │   │
│  │ - JIRA tracking: @jira('SKY-1234')                       │   │
│  │ - Parametrization: @parametrize(...)                    │   │
│  │ - Skip/XFail: @skip, @xfail                              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Configuration Layer                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ config.dev.json / config.prod.json                       │   │
│  │ - Environment settings                                   │   │
│  │ - API endpoints                                          │   │
│  │ - Database config                                        │   │
│  │ - Timeout settings                                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ pytest.ini                                               │   │
│  │ - Marker definitions                                     │   │
│  │ - Test discovery paths                                   │   │
│  │ - Report generation                                      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Output Layer                                 │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ reports/latest_execution_logs/{test_name}/              │   │
│  │ - execution_YYYYMMDD_HHMMSS.log                          │   │
│  │ - execution_report_YYYYMMDD_HHMMSS.json                 │   │
│  │ (Recreated each test run)                                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ reports/test_report_YYYYMMDD_HHMMSS.{html|json}         │   │
│  │ - Summary statistics                                     │   │
│  │ - Pass/Fail/Skip counts                                  │   │
│  │ - Test durations                                         │   │
│  │ - JIRA references                                        │   │
│  │ - Error details                                          │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Diagram

```
Test Case Execution
        │
        ▼
┌──────────────────────────────────────────────────┐
│ Test Data Generation                             │
├──────────────────────────────────────────────────┤
│ DataMocker.generate_data_from_template()         │
│   └─ Returns: Generated test data (dict)         │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│ Data Validation                                  │
├──────────────────────────────────────────────────┤
│ DataValidator.validate_all(data, rules)         │
│   ├─ Null check                                  │
│   ├─ Type validation                             │
│   ├─ Conditional validation                      │
│   ├─ Range validation                            │
│   └─ Pattern validation                          │
│   └─ Returns: (is_valid, error_list)             │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│ Test Execution                                   │
├──────────────────────────────────────────────────┤
│ Execute actual test logic                        │
│ - API calls, database operations, etc.           │
│   └─ Returns: Actual result (dict/list)          │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│ Data Comparison                                  │
├──────────────────────────────────────────────────┤
│ DataComparator.compare_json(expected, actual)   │
│   ├─ Deep comparison                             │
│   ├─ Type checking                               │
│   ├─ Value matching                              │
│   └─ Returns: (is_equal, differences)            │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│ Logging & Reporting                              │
├──────────────────────────────────────────────────┤
│ LoggerManager.log_result(expected, actual)       │
│ LoggerManager.save_execution_report(status)      │
│   └─ Output: execution_*.log, execution_report_*.json
│                                                  │
│ ReportGenerator.add_test_result(...)             │
│ ReportGenerator.generate_html_report()           │
│   └─ Output: test_report_*.html                  │
└──────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────┐
│ Reports & Logs Generated                         │
├──────────────────────────────────────────────────┤
│ Location: reports/latest_execution_logs/         │
│ Location: reports/test_report_*.html             │
└──────────────────────────────────────────────────┘
```

## 🔄 Test Case Lifecycle

```
1. Test Case Creation
   └─ GenerateTestCaseFolder.py test_name
      └─ Creates: test-scripts/{test_name}/
         ├─ test_name.py (test script)
         ├─ expected-result/ (folder)
         └─ logs/ (folder)

2. Configuration Loading
   └─ ConfigManager loads config.{env}.json
      └─ Provides: API URLs, timeouts, database settings

3. Logger Initialization
   └─ LoggerManager('test_case_name')
      └─ Creates: reports/latest_execution_logs/{test_name}/

4. Test Data Generation
   └─ DataMocker.generate_data_from_template(template)
      └─ Returns: Mock data matching template

5. Data Validation
   └─ DataValidator.validate_all(data, rules)
      └─ Returns: Validation status & errors

6. Test Execution
   └─ Run actual test logic
      └─ Generate expected & actual results

7. Result Comparison
   └─ DataComparator.compare_json(expected, actual)
      └─ Returns: Comparison results & differences

8. Logging & Reporting
   └─ LoggerManager.log_result(expected, actual)
      └─ Outputs: execution_*.log

9. Report Generation
   └─ ReportGenerator.generate_html_report()
      └─ Outputs: test_report_*.html

10. Assertion & Completion
    └─ Assert comparison results
       └─ Save execution report
```

## 🎯 Usage Patterns

### Pattern 1: Simple Validation Test
```python
@TestMarker.jira('SKY-100')
def test_data_validation():
    data = DataMocker.generate_data_from_template(template)
    is_valid, errors = DataValidator.validate_all(data, rules)
    assert is_valid
```

### Pattern 2: API Response Test
```python
@TestMarker.jira('SKY-200')
@TestMarker.smoke()
def test_api_response():
    logger_mgr = LoggerManager('test_api_response')
    
    # Generate request
    request_data = DataMocker.generate_data_from_template(template)
    
    # Execute API
    response = api_client.post('/endpoint', request_data)
    
    # Compare
    is_equal, diffs = DataComparator.compare_json(
        expected_response, response
    )
    
    # Log
    logger_mgr.log_result(expected_response, response, diffs)
    assert is_equal
```

### Pattern 3: Conditional Field Test
```python
@TestMarker.jira('SKY-300')
def test_conditional_fields():
    data = {'status': 'active', 'email': 'test@example.com'}
    
    # Rule: If status='active', must have activation_date
    rules = {
        'conditionals': [{
            'condition_field': 'status',
            'condition_value': 'active',
            'required_fields': ['activation_date']
        }]
    }
    
    is_valid, errors = DataValidator.validate_all(data, rules)
    assert not is_valid  # Should fail - missing activation_date
```

### Pattern 4: Multi-Format Comparison
```python
@TestMarker.jira('SKY-400')
def test_multi_format():
    # Compare CSV files
    is_equal, diffs = DataComparator.compare_files(
        'expected.csv',
        'actual.csv'
    )
    assert is_equal
```

---

## 📈 Scalability & Extensibility

### Adding New Validators
```python
# In validator.py
@staticmethod
def validate_custom_rule(data, rule_config):
    # Implementation
    pass
```

### Adding New Data Generators
```python
# In data_mocker.py
@staticmethod
def generate_custom_format():
    # Implementation
    pass
```

### Adding New Markers
```python
# In markers.py
@staticmethod
def custom_marker():
    return pytest.mark.custom_marker
```

---

## 🔐 Best Practices Implemented

✅ **Singleton Pattern**: ConfigManager ensures single config instance
✅ **Separation of Concerns**: Each utility has single responsibility
✅ **Type Hints**: Full type annotations throughout
✅ **Comprehensive Logging**: All operations logged
✅ **Error Handling**: Graceful exception handling
✅ **Reusability**: Utilities can be used independently
✅ **Extensibility**: Easy to add new functionality
✅ **Documentation**: Detailed docstrings
✅ **DRY Principle**: No code duplication
✅ **Consistent Naming**: Clear, consistent naming conventions
