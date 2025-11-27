"""
Data Validator Utility

Handles:
- Null/empty field validation
- Schema validation
- Conditional field validation (e.g., if field A has value, field B must be populated)
- Custom validation rules
"""

import logging
from typing import Any, Dict, List, Callable, Optional, Tuple

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates data against various rules and schemas."""

    @staticmethod
    def validate_not_null(data: Dict, fields: List[str]) -> List[str]:
        """
        Validate that specified fields are not null or empty.

        Args:
            data: Data to validate
            fields: List of field names to check

        Returns:
            List of validation errors
        """
        errors = []
        for field in fields:
            value = DataValidator._get_nested_value(data, field)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                errors.append(f"Field '{field}' is null or empty")
        return errors

    @staticmethod
    def validate_type(data: Dict, field_types: Dict[str, type]) -> List[str]:
        """
        Validate field types.

        Args:
            data: Data to validate
            field_types: Dict of {field_name: expected_type}

        Returns:
            List of validation errors
        """
        errors = []
        for field, expected_type in field_types.items():
            value = DataValidator._get_nested_value(data, field)
            if value is not None and not isinstance(value, expected_type):
                errors.append(f"Field '{field}' has invalid type. Expected {expected_type.__name__}, got {type(value).__name__}")
        return errors

    @staticmethod
    def validate_conditional(
        data: Dict,
        condition_field: str,
        condition_value: Any,
        required_fields: List[str]
    ) -> List[str]:
        """
        Validate that certain fields are populated if another field has a specific value.

        Args:
            data: Data to validate
            condition_field: Field to check for condition
            condition_value: Value that triggers the condition
            required_fields: Fields that must be populated when condition is met

        Returns:
            List of validation errors
        """
        errors = []
        condition_actual = DataValidator._get_nested_value(data, condition_field)
        
        if condition_actual == condition_value:
            for field in required_fields:
                value = DataValidator._get_nested_value(data, field)
                if value is None or (isinstance(value, str) and value.strip() == ""):
                    errors.append(
                        f"Field '{field}' must be populated when '{condition_field}' = '{condition_value}', "
                        f"but found: {value}"
                    )
        return errors

    @staticmethod
    def validate_multiple_conditions(
        data: Dict,
        conditions: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Validate multiple conditional rules.

        Args:
            data: Data to validate
            conditions: List of condition dictionaries with keys:
                - condition_field: Field to check
                - condition_value: Value that triggers
                - required_fields: List of fields that must be populated

        Returns:
            List of validation errors
        """
        errors = []
        for condition in conditions:
            errors.extend(DataValidator.validate_conditional(
                data,
                condition["condition_field"],
                condition["condition_value"],
                condition["required_fields"]
            ))
        return errors

    @staticmethod
    def validate_range(data: Dict, field_ranges: Dict[str, Tuple[Any, Any]]) -> List[str]:
        """
        Validate that numeric fields are within specified ranges.

        Args:
            data: Data to validate
            field_ranges: Dict of {field_name: (min_value, max_value)}

        Returns:
            List of validation errors
        """
        errors = []
        for field, (min_val, max_val) in field_ranges.items():
            value = DataValidator._get_nested_value(data, field)
            if value is not None:
                if not (min_val <= value <= max_val):
                    errors.append(f"Field '{field}' value {value} is out of range [{min_val}, {max_val}]")
        return errors

    @staticmethod
    def validate_enum(data: Dict, field_enums: Dict[str, List[Any]]) -> List[str]:
        """
        Validate that fields match allowed enum values.

        Args:
            data: Data to validate
            field_enums: Dict of {field_name: [allowed_values]}

        Returns:
            List of validation errors
        """
        errors = []
        for field, allowed_values in field_enums.items():
            value = DataValidator._get_nested_value(data, field)
            if value is not None and value not in allowed_values:
                errors.append(f"Field '{field}' has invalid value '{value}'. Allowed: {allowed_values}")
        return errors

    @staticmethod
    def validate_pattern(data: Dict, field_patterns: Dict[str, str]) -> List[str]:
        """
        Validate that fields match regex patterns.

        Args:
            data: Data to validate
            field_patterns: Dict of {field_name: regex_pattern}

        Returns:
            List of validation errors
        """
        import re
        errors = []
        for field, pattern in field_patterns.items():
            value = DataValidator._get_nested_value(data, field)
            if value is not None:
                if not re.match(pattern, str(value)):
                    errors.append(f"Field '{field}' value '{value}' does not match pattern '{pattern}'")
        return errors

    @staticmethod
    def validate_custom(data: Dict, validators: Dict[str, Callable]) -> List[str]:
        """
        Apply custom validation functions.

        Args:
            data: Data to validate
            validators: Dict of {field_name: validation_function}
                       Function should return error message or None if valid

        Returns:
            List of validation errors
        """
        errors = []
        for field, validator_func in validators.items():
            value = DataValidator._get_nested_value(data, field)
            try:
                error_message = validator_func(value)
                if error_message:
                    errors.append(f"Field '{field}': {error_message}")
            except Exception as e:
                errors.append(f"Field '{field}': Validation error - {str(e)}")
        return errors

    @staticmethod
    def validate_all(
        data: Dict,
        rules: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Apply all validation rules at once.

        Args:
            data: Data to validate
            rules: Dict containing validation rules:
                {
                    "not_null": ["field1", "field2"],
                    "types": {"field1": str, "field2": int},
                    "conditionals": [
                        {
                            "condition_field": "status",
                            "condition_value": "active",
                            "required_fields": ["activation_date"]
                        }
                    ],
                    "enums": {"status": ["active", "inactive"]},
                    "patterns": {"email": r"^[\w\.-]+@[\w\.-]+\.\w+$"}
                }

        Returns:
            Tuple of (is_valid, list of all errors)
        """
        all_errors = []

        if "not_null" in rules:
            all_errors.extend(DataValidator.validate_not_null(data, rules["not_null"]))

        if "types" in rules:
            all_errors.extend(DataValidator.validate_type(data, rules["types"]))

        if "conditionals" in rules:
            all_errors.extend(DataValidator.validate_multiple_conditions(data, rules["conditionals"]))

        if "ranges" in rules:
            all_errors.extend(DataValidator.validate_range(data, rules["ranges"]))

        if "enums" in rules:
            all_errors.extend(DataValidator.validate_enum(data, rules["enums"]))

        if "patterns" in rules:
            all_errors.extend(DataValidator.validate_pattern(data, rules["patterns"]))

        if "custom" in rules:
            all_errors.extend(DataValidator.validate_custom(data, rules["custom"]))

        return len(all_errors) == 0, all_errors

    @staticmethod
    def _get_nested_value(data: Dict, path: str) -> Any:
        """
        Get nested value using dot notation.

        Args:
            data: Dictionary to traverse
            path: Dot-separated path (e.g., 'user.profile.email')

        Returns:
            Value at path or None if not found
        """
        keys = path.split(".")
        value = data
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return None
            else:
                return None
        return value
