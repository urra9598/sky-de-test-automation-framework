"""
Utilities Documentation and Guide

Sky Test Automation Framework - Utility Classes
"""

# ============================================================================
# UTILITIES OVERVIEW
# ============================================================================
"""
The utilities package provides comprehensive functionality for test automation:

1. ConfigManager       - Configuration and environment management
2. LoggerManager       - Test execution logging and reporting
3. DataComparator      - Data comparison (JSON, CSV, XML)
4. DataValidator       - Data validation and schema checking
5. TestMarker          - Pytest markers for test categorization
6. ReportGenerator     - Test execution report generation
7. DataMocker          - Test data generation

"""

# ============================================================================
# 1. CONFIG MANAGER
# ============================================================================
"""
Usage: Configuration Management

from utilities.config_manager import config

# Get configuration values
env = config.get('environment')
timeout = config.get('test_timeout')
api_url = config.get('api.base_url')  # Supports nested keys with dot notation

# Get with default
log_level = config.get('log_level', 'INFO')

# Set configuration value
config.set('custom_key', 'custom_value')

# Get all configuration
all_config = config.get_all()

# Reload configuration
config.reload()

Configuration file: sky-tests-automation/config/config.{environment}.json
Environment: Set via TEST_ENV environment variable (default: 'dev')
"""

# ============================================================================
# 2. LOGGER MANAGER
# ============================================================================
"""
Usage: Test Execution Logging

from utilities.logger_manager import LoggerManager

# Initialize logger for test case
logger_manager = LoggerManager('test_case_name')
logger = logger_manager.logger

# Log messages
logger.info('Test started')
logger.debug('Debug information')
logger.warning('Warning message')
logger.error('Error message', exception=error_obj)

# Log test results with expected vs actual
logger_manager.log_result(
    expected={'status': 'success'},
    actual={'status': 'success'},
    validation_errors=['Error 1', 'Error 2']
)

# Save execution report
logger_manager.save_execution_report(
    status='PASSED',
    failure_reason=None
)

# Get log directory
log_dir = logger_manager.get_log_directory()

Output: sky-tests-automation/reports/latest_execution_logs/{test_case_name}/
Files: execution_*.log, execution_report_*.json
"""

# ============================================================================
# 3. DATA COMPARATOR
# ============================================================================
"""
Usage: Comparing Test Results

from utilities.data_comparator import DataComparator

# Compare JSON objects
expected = {'user_id': 1, 'name': 'John'}
actual = {'user_id': 1, 'name': 'John'}
is_equal, differences = DataComparator.compare_json(expected, actual)

# Compare files (auto-detects format: JSON, CSV, XML)
is_equal, differences = DataComparator.compare_files(
    'expected.json',
    'actual.json'
)

# Load data from file
data = DataComparator.load_data('data.json')

# Validate data against schema
schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'string'},
        'email': {'type': 'string'}
    },
    'required': ['id', 'email']
}
is_valid, errors = DataComparator.validate_schema(data, schema)

Supported formats: JSON, CSV, XML, XSD
Output: List of differences or validation errors with detailed paths
"""

# ============================================================================
# 4. DATA VALIDATOR
# ============================================================================
"""
Usage: Data Validation

from utilities.validator import DataValidator

data = {
    'email': 'test@example.com',
    'age': 25,
    'status': 'active'
}

# Validate not null/empty
errors = DataValidator.validate_not_null(data, ['email', 'age'])

# Validate types
errors = DataValidator.validate_type(data, {
    'age': int,
    'email': str
})

# Validate conditional: if status='active', then registration_date must exist
errors = DataValidator.validate_conditional(
    data,
    condition_field='status',
    condition_value='active',
    required_fields=['registration_date']
)

# Validate numeric range
errors = DataValidator.validate_range(data, {
    'age': (18, 100)
})

# Validate enum values
errors = DataValidator.validate_enum(data, {
    'status': ['active', 'inactive', 'pending']
})

# Validate regex pattern
errors = DataValidator.validate_pattern(data, {
    'email': r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'
})

# Validate with custom function
def validate_age(value):
    return None if value >= 18 else "Age must be 18 or older"

errors = DataValidator.validate_custom(data, {
    'age': validate_age
})

# Validate all rules at once
validation_rules = {
    'not_null': ['email', 'age'],
    'types': {'age': int, 'email': str},
    'ranges': {'age': (18, 100)},
    'enums': {'status': ['active', 'inactive']},
    'patterns': {'email': r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'}
}
is_valid, all_errors = DataValidator.validate_all(data, validation_rules)
"""

# ============================================================================
# 5. TEST MARKER
# ============================================================================
"""
Usage: Test Categorization with Markers

from utilities.markers import TestMarker
import pytest

class TestMyFeature:
    
    @TestMarker.smoke()
    def test_basic_functionality(self):
        pass
    
    @TestMarker.regression()
    def test_existing_feature(self):
        pass
    
    @TestMarker.jira('SKY-1234')
    def test_jira_tracked(self):
        pass
    
    @TestMarker.jira_with_category('SKY-1234', 'smoke')
    def test_combined_markers(self):
        pass
    
    @TestMarker.parametrize('input,expected', [(1, 2), (2, 4)])
    def test_parametrized(self, input, expected):
        pass
    
    @TestMarker.skip_test('Not ready')
    def test_skipped(self):
        pass
    
    @TestMarker.xfail('Known issue SKY-5678')
    def test_expected_to_fail(self):
        pass

# Run specific markers
# pytest -m smoke (run smoke tests)
# pytest -m regression (run regression tests)
# pytest -m "smoke and regression" (run both)
# pytest -m jira (run JIRA-tracked tests)

Available Markers:
- smoke: Quick validation tests
- regression: Regression test suite
- sanity: Sanity check tests
- integration: Integration tests
- unit: Unit tests
- jira: JIRA issue reference
- data_driven: Data-driven tests
"""

# ============================================================================
# 6. REPORT GENERATOR
# ============================================================================
"""
Usage: Test Execution Reports

from utilities.report_generator import ReportGenerator

# Initialize report generator
report_gen = ReportGenerator()

# Add test results
report_gen.add_test_result(
    test_name='test_login',
    status='PASSED',
    duration=2.5,
    expected={'result': 'success'},
    actual={'result': 'success'},
    errors=[],
    jira_id='SKY-1234'
)

report_gen.add_test_result(
    test_name='test_logout',
    status='FAILED',
    duration=1.2,
    errors=['Connection timeout'],
    jira_id='SKY-1235'
)

# Generate reports
json_report_path = report_gen.generate_json_report()
html_report_path = report_gen.generate_html_report()

Output:
- JSON: sky-tests-automation/reports/test_report_YYYYMMDD_HHMMSS.json
- HTML: sky-tests-automation/reports/test_report_YYYYMMDD_HHMMSS.html

Report includes:
- Summary statistics (pass rate, total/passed/failed/skipped counts)
- Duration metrics
- JIRA ID references
- Detailed error messages
- Execution timestamp
"""

# ============================================================================
# 7. DATA MOCKER
# ============================================================================
"""
Usage: Test Data Generation

from utilities.data_mocker import DataMocker

# Generate random strings
random_str = DataMocker.generate_string(10, 'alpha')
random_alphanum = DataMocker.generate_string(15, 'alphanumeric')

# Generate email
email = DataMocker.generate_email()

# Generate phone
phone = DataMocker.generate_phone()

# Generate date
date = DataMocker.generate_date()  # Default: within last year

# Generate number
number = DataMocker.generate_number(1, 100, decimal_places=2)

# Generate UUID
uuid = DataMocker.generate_uuid()

# Generate from template
template = {
    'first_name': {'type': 'string', 'length': 10},
    'email': {'type': 'email'},
    'age': {'type': 'number', 'min': 18, 'max': 65},
    'status': {'type': 'enum', 'values': ['active', 'inactive']},
    'created_date': {'type': 'date'},
    'address': {
        'type': 'object',
        'properties': {
            'street': {'type': 'string', 'length': 20},
            'city': {'type': 'string', 'length': 15}
        }
    },
    'tags': {
        'type': 'array',
        'items': {'type': 'string', 'length': 5},
        'count': 3
    }
}

# Generate single record
user_data = DataMocker.generate_data_from_template(template)

# Generate multiple records
batch_data = DataMocker.generate_batch_data(template, count=10)

# Generate from JSON schema file
data = DataMocker.generate_from_json_schema('schema.json')

Supported Types:
- string: Random string (alpha, alphanumeric, numeric, or custom charset)
- email: Random email address
- phone: Random phone number
- number: Random numeric value
- date: Random date within range
- enum: Random value from list
- uuid: UUID v4
- credit_card: Mock credit card number
- object: Nested object
- array: Array of items
"""

# ============================================================================
# COMPLETE EXAMPLE
# ============================================================================
"""
from utilities.markers import TestMarker
from utilities.config_manager import config
from utilities.logger_manager import LoggerManager
from utilities.data_mocker import DataMocker
from utilities.data_comparator import DataComparator
from utilities.validator import DataValidator
from utilities.report_generator import ReportGenerator


class TestCompleteExample:
    
    @TestMarker.jira('SKY-1000')
    @TestMarker.smoke()
    def test_user_registration(self):
        # Setup
        logger_manager = LoggerManager('test_user_registration')
        logger = logger_manager.logger
        
        # Get configuration
        api_url = config.get('api.base_url')
        
        # Generate test data
        user_template = {
            'email': {'type': 'email'},
            'first_name': {'type': 'string', 'length': 10},
            'age': {'type': 'number', 'min': 18, 'max': 65}
        }
        user_data = DataMocker.generate_data_from_template(user_template)
        logger.info(f'Generated user data: {user_data}')
        
        # Validate data
        validation_rules = {
            'not_null': ['email', 'first_name'],
            'patterns': {'email': r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'},
            'ranges': {'age': (18, 100)}
        }
        is_valid, errors = DataValidator.validate_all(user_data, validation_rules)
        logger.info(f'Data validation: {"PASSED" if is_valid else "FAILED"}')
        
        # Expected result
        expected = {'success': True, 'user_id': 'USR-1'}
        
        # Actual result (from API call)
        actual = {'success': True, 'user_id': 'USR-1'}
        
        # Compare results
        is_equal, differences = DataComparator.compare_json(expected, actual)
        logger_manager.log_result(expected, actual, differences)
        
        # Generate report
        report_gen = ReportGenerator()
        report_gen.add_test_result(
            test_name='test_user_registration',
            status='PASSED' if is_equal else 'FAILED',
            duration=2.5,
            expected=expected,
            actual=actual,
            errors=differences,
            jira_id='SKY-1000'
        )
        report_gen.generate_html_report()
        
        # Assert
        assert is_equal and is_valid


# Run with: pytest path/to/test.py -v -m smoke --jira SKY-1000
"""
