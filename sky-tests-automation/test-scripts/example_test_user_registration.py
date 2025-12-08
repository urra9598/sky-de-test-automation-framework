"""
Example Test: User Registration Validation
============================================

This is a comprehensive example test demonstrating the Sky Test Automation Framework.

Demonstrates:
- Using markers for test categorization and JIRA tracking
- Generating mock test data with DataMocker
- Validating data with DataValidator
- Logging and reporting with LoggerManager
- Comparing expected vs actual results with DataComparator
- Professional test reports (JSON & HTML)

Run:
    pytest example_test_user_registration.py -v
    pytest example_test_user_registration.py -m smoke
    pytest example_test_user_registration.py::test_user_email_validation -v
"""

import json
import os
import sys
from pathlib import Path

import pytest

# Ensure utilities are importable
# This file: sky-tests-automation/test-scripts/example_test_user_registration.py
# Utilities: sky-tests-automation/utilities
# So we need to go up 1 level (./..) to reach sky-tests-automation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utilities.markers import TestMarker
from utilities.logger_manager import LoggerManager
from utilities.data_mocker import DataMocker
from utilities.validator import DataValidator
from utilities.data_comparator import DataComparator
from utilities.report_generator import ReportGenerator


# ============================================================================
# TEST 1: Valid User Registration
# ============================================================================
@TestMarker.jira("SKY-1001")
@TestMarker.smoke()
@TestMarker.sanity()
def test_valid_user_registration():
    """Test that a valid user registration record passes all validations."""
    logger_mgr = LoggerManager("test_valid_user_registration")
    
    try:
        # Generate mock user data
        user_data = {
            "user_id": "USR_001",
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1-555-0123",
            "age": 28,
            "is_active": True,
            "registration_date": "2025-01-15",
            "country": "USA"
        }
        
        logger_mgr.log_info(f"Generated user data: {user_data}")
        
        # Define validation rules
        validation_rules = {
            "not_null": ["email", "first_name", "last_name", "user_id"],
            "type": {
                "age": "number",
                "is_active": "boolean",
                "email": "string"
            },
            "pattern": {
                "email": r"^[\w\.-]+@[\w\.-]+\.\w+$",
                "phone": r"^\+?1?-?\d{3}-?\d{3}-?\d{4}$"
            },
            "range": {
                "age": {"min": 18, "max": 120}
            },
            "enum": {
                "country": ["USA", "Canada", "UK", "India", "Australia"]
            }
        }
        
        # Validate data
        is_valid, validation_errors = DataValidator.validate_all(user_data, validation_rules)
        
        logger_mgr.log_result(
            expected="Valid registration with all fields correct",
            actual=f"Validation: {is_valid}, Errors: {validation_errors}",
            validation_errors=validation_errors
        )
        
        # Assert
        assert is_valid, f"Validation failed: {validation_errors}"
        logger_mgr.save_execution_report(status="PASSED", failure_reason=None)
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# TEST 2: Invalid Email Format
# ============================================================================
@TestMarker.jira("SKY-1002")
@TestMarker.sanity()
def test_invalid_email_format():
    """Test that invalid email format is caught during validation."""
    logger_mgr = LoggerManager("test_invalid_email_format")
    
    try:
        # User data with invalid email
        user_data = {
            "user_id": "USR_002",
            "email": "invalid-email-format",  # Missing @ and domain
            "first_name": "Jane",
            "last_name": "Smith",
            "age": 35
        }
        
        logger_mgr.log_info(f"Testing invalid email: {user_data['email']}")
        
        # Validation rules
        validation_rules = {
            "not_null": ["email"],
            "pattern": {
                "email": r"^[\w\.-]+@[\w\.-]+\.\w+$"
            }
        }
        
        is_valid, validation_errors = DataValidator.validate_all(user_data, validation_rules)
        
        logger_mgr.log_result(
            expected="Email validation should fail",
            actual=f"Validation result: {is_valid}, Errors: {len(validation_errors)}",
            validation_errors=validation_errors
        )
        
        # Expected: validation should fail
        assert not is_valid, "Expected validation to fail for invalid email"
        assert len(validation_errors) > 0, "Expected validation errors for invalid email"
        
        logger_mgr.save_execution_report(status="PASSED", failure_reason=None)
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# TEST 3: Null Field Detection
# ============================================================================
@TestMarker.jira("SKY-1003")
@TestMarker.sanity()
def test_null_field_detection():
    """Test that null required fields are detected."""
    logger_mgr = LoggerManager("test_null_field_detection")
    
    try:
        # User data with missing required fields
        user_data = {
            "user_id": "USR_003",
            "email": None,  # Required field is null
            "first_name": "Bob",
            "last_name": None,  # Required field is null
            "age": 42
        }
        
        logger_mgr.log_info("Testing null field detection")
        
        validation_rules = {
            "not_null": ["email", "first_name", "last_name"]
        }
        
        is_valid, validation_errors = DataValidator.validate_all(user_data, validation_rules)
        
        logger_mgr.log_result(
            expected="Validation should fail for null required fields",
            actual=f"Validation result: {is_valid}, Error count: {len(validation_errors)}",
            validation_errors=validation_errors
        )
        
        assert not is_valid, "Expected validation to fail for null fields"
        assert len(validation_errors) >= 2, "Expected at least 2 validation errors"
        
        logger_mgr.save_execution_report(status="PASSED", failure_reason=None)
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# TEST 4: Age Range Validation
# ============================================================================
@TestMarker.jira("SKY-1004")
@TestMarker.regression()
def test_age_range_validation():
    """Test that age outside valid range is rejected."""
    logger_mgr = LoggerManager("test_age_range_validation")
    
    try:
        test_cases = [
            {"age": 15, "should_pass": False, "reason": "Too young (below 18)"},
            {"age": 18, "should_pass": True, "reason": "Minimum valid age"},
            {"age": 65, "should_pass": True, "reason": "Within valid range"},
            {"age": 125, "should_pass": False, "reason": "Too old (above 120)"},
        ]
        
        all_passed = True
        
        for test_case in test_cases:
            user_data = {
                "user_id": f"USR_{test_case['age']:03d}",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "age": test_case["age"]
            }
            
            validation_rules = {
                "range": {
                    "age": {"min": 18, "max": 120}
                }
            }
            
            is_valid, errors = DataValidator.validate_all(user_data, validation_rules)
            should_pass = test_case["should_pass"]
            
            result = "PASS" if (is_valid == should_pass) else "FAIL"
            logger_mgr.log_info(
                f"Age {test_case['age']:3d} - {test_case['reason']:30s} - {result}"
            )
            
            if is_valid != should_pass:
                all_passed = False
        
        logger_mgr.save_execution_report(
            status="PASSED" if all_passed else "FAILED",
            failure_reason=None if all_passed else "Some age validations failed"
        )
        
        assert all_passed, "Not all age range tests passed"
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# TEST 5: Data Type Validation
# ============================================================================
@TestMarker.jira("SKY-1005")
@TestMarker.regression()
def test_data_type_validation():
    """Test that incorrect data types are detected."""
    logger_mgr = LoggerManager("test_data_type_validation")
    
    try:
        # User data with incorrect data types
        user_data = {
            "user_id": "USR_005",
            "email": "user@example.com",
            "first_name": "Alice",
            "last_name": "Johnson",
            "age": "thirty-five",  # Should be number, but it's string
            "is_active": "yes",    # Should be boolean, but it's string
        }
        
        logger_mgr.log_info("Testing data type validation")
        
        validation_rules = {
            "type": {
                "age": "number",
                "is_active": "boolean",
                "email": "string",
                "first_name": "string"
            }
        }
        
        is_valid, validation_errors = DataValidator.validate_all(user_data, validation_rules)
        
        logger_mgr.log_result(
            expected="Type validation should fail for incorrect types",
            actual=f"Validation result: {is_valid}, Errors: {len(validation_errors)}",
            validation_errors=validation_errors
        )
        
        assert not is_valid, "Expected validation to fail for incorrect types"
        assert len(validation_errors) >= 2, "Expected at least 2 type validation errors"
        
        logger_mgr.save_execution_report(status="PASSED", failure_reason=None)
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# TEST 6: Enum Value Validation
# ============================================================================
@TestMarker.jira("SKY-1006")
@TestMarker.sanity()
def test_enum_value_validation():
    """Test that invalid enum values are rejected."""
    logger_mgr = LoggerManager("test_enum_value_validation")
    
    try:
        # User data with invalid enum value
        user_data = {
            "user_id": "USR_006",
            "email": "user@example.com",
            "first_name": "Charlie",
            "last_name": "Brown",
            "age": 40,
            "country": "InvalidCountry"  # Not in allowed enum
        }
        
        logger_mgr.log_info(f"Testing enum validation for country: {user_data['country']}")
        
        allowed_countries = ["USA", "Canada", "UK", "India", "Australia"]
        
        validation_rules = {
            "enum": {
                "country": allowed_countries
            }
        }
        
        is_valid, validation_errors = DataValidator.validate_all(user_data, validation_rules)
        
        logger_mgr.log_result(
            expected=f"Validation should fail (country not in {allowed_countries})",
            actual=f"Validation result: {is_valid}, Errors: {validation_errors}",
            validation_errors=validation_errors
        )
        
        assert not is_valid, "Expected validation to fail for invalid enum value"
        
        logger_mgr.save_execution_report(status="PASSED", failure_reason=None)
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# TEST 7: Data Comparison
# ============================================================================
@TestMarker.jira("SKY-1007")
@TestMarker.regression()
def test_data_comparison():
    """Test comparing expected vs actual user registration data."""
    logger_mgr = LoggerManager("test_data_comparison")
    
    try:
        expected_user = {
            "user_id": "USR_007",
            "email": "expected@example.com",
            "first_name": "Diana",
            "last_name": "Prince",
            "age": 30
        }
        
        # Actual data (mostly matches, one field differs)
        actual_user = {
            "user_id": "USR_007",
            "email": "expected@example.com",
            "first_name": "Diana",
            "last_name": "Prince",
            "age": 31  # Different age
        }
        
        logger_mgr.log_info("Comparing expected vs actual user data")
        
        is_equal, diffs = DataComparator.compare_json(expected_user, actual_user)
        
        logger_mgr.log_result(
            expected="User data should match (with age difference)",
            actual=f"Comparison result: Equal={is_equal}, Differences: {diffs}",
            validation_errors=diffs if not is_equal else []
        )
        
        # We expect them NOT to be equal due to age difference
        assert not is_equal, "Expected data to differ due to age field"
        assert "age" in str(diffs), "Expected age difference to be reported"
        
        logger_mgr.save_execution_report(status="PASSED", failure_reason=None)
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# TEST 8: Mock Data Generation
# ============================================================================
@TestMarker.jira("SKY-1008")
@TestMarker.smoke()
def test_mock_data_generation():
    """Test that mock data can be generated from a template."""
    logger_mgr = LoggerManager("test_mock_data_generation")
    
    try:
        # Define a user template
        user_template = {
            "user_id": {"type": "string", "prefix": "USR_", "random": True},
            "email": {"type": "email"},
            "first_name": {"type": "string", "choices": ["John", "Jane", "Bob", "Alice"]},
            "last_name": {"type": "string", "choices": ["Smith", "Johnson", "Brown", "Wilson"]},
            "age": {"type": "number", "min": 18, "max": 75},
            "country": {"type": "string", "choices": ["USA", "Canada", "UK"]},
            "is_active": {"type": "boolean"}
        }
        
        logger_mgr.log_info("Generating mock user data from template")
        
        # Generate multiple records
        generated_users = DataMocker.generate_batch_data(user_template, num_records=5)
        
        logger_mgr.log_info(f"Generated {len(generated_users)} user records")
        
        assert len(generated_users) == 5, "Expected 5 generated records"
        
        # Validate each generated record has required fields
        for idx, user in enumerate(generated_users):
            required_fields = ["user_id", "email", "first_name", "last_name"]
            for field in required_fields:
                assert field in user, f"Record {idx} missing required field: {field}"
        
        logger_mgr.log_info(f"All {len(generated_users)} records contain required fields")
        logger_mgr.save_execution_report(status="PASSED", failure_reason=None)
        
    except Exception as e:
        logger_mgr.log_error(f"Test failed: {str(e)}")
        logger_mgr.save_execution_report(status="FAILED", failure_reason=str(e))
        raise


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Add custom markers."""
    config.addinivalue_line("markers", "smoke: Mark test as smoke test")
    config.addinivalue_line("markers", "sanity: Mark test as sanity test")
    config.addinivalue_line("markers", "regression: Mark test as regression test")
    config.addinivalue_line("markers", "jira: JIRA tracking marker")


if __name__ == "__main__":
    # Allow running this file directly with pytest
    pytest.main([__file__, "-v", "-s"])
