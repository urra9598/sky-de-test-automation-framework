"""
Data Comparator Utility

Handles:
- Comparison of JSON, CSV, XML data
- Field-level validation
- Detailed difference reporting
"""

import json
import csv
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Tuple, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class DataComparator:
    """Compares expected and actual data in multiple formats."""

    @staticmethod
    def load_data(file_path: str) -> Any:
        """
        Load data from file based on extension.

        Args:
            file_path: Path to the data file

        Returns:
            Loaded data structure
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix == ".json":
            return DataComparator._load_json(file_path)
        elif path.suffix == ".csv":
            return DataComparator._load_csv(file_path)
        elif path.suffix in [".xml", ".xsd"]:
            return DataComparator._load_xml(file_path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

    @staticmethod
    def _load_json(file_path: str) -> Dict:
        """Load JSON file."""
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            raise

    @staticmethod
    def _load_csv(file_path: str) -> List[Dict]:
        """Load CSV file as list of dictionaries."""
        try:
            with open(file_path, "r") as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            logger.error(f"Error reading CSV {file_path}: {e}")
            raise

    @staticmethod
    def _load_xml(file_path: str) -> Dict:
        """Load XML file."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return DataComparator._xml_to_dict(root)
        except ET.ParseError as e:
            logger.error(f"Invalid XML in {file_path}: {e}")
            raise

    @staticmethod
    def _xml_to_dict(element) -> Dict:
        """Convert XML element to dictionary."""
        result = {}
        for child in element:
            child_dict = DataComparator._xml_to_dict(child)
            if child.tag in result:
                if not isinstance(result[child.tag], list):
                    result[child.tag] = [result[child.tag]]
                result[child.tag].append(child_dict or child.text)
            else:
                result[child.tag] = child_dict or child.text
        return result or element.text

    @staticmethod
    def compare_json(expected: Dict, actual: Dict) -> Tuple[bool, List[str]]:
        """
        Compare two JSON objects.

        Args:
            expected: Expected JSON data
            actual: Actual JSON data

        Returns:
            Tuple of (is_equal, list of differences)
        """
        differences = []
        DataComparator._compare_recursive(expected, actual, differences)
        return len(differences) == 0, differences

    @staticmethod
    def compare_files(expected_file: str, actual_file: str) -> Tuple[bool, List[str]]:
        """
        Compare two data files.

        Args:
            expected_file: Path to expected data file
            actual_file: Path to actual data file

        Returns:
            Tuple of (is_equal, list of differences)
        """
        expected_data = DataComparator.load_data(expected_file)
        actual_data = DataComparator.load_data(actual_file)

        if isinstance(expected_data, list) and isinstance(actual_data, list):
            return DataComparator._compare_lists(expected_data, actual_data)
        elif isinstance(expected_data, dict) and isinstance(actual_data, dict):
            return DataComparator.compare_json(expected_data, actual_data)
        else:
            differences = [f"Type mismatch: expected {type(expected_data)}, got {type(actual_data)}"]
            return False, differences

    @staticmethod
    def _compare_recursive(expected: Any, actual: Any, differences: List[str], path: str = ""):
        """Recursively compare nested structures."""
        if type(expected) != type(actual):
            differences.append(f"Type mismatch at {path}: expected {type(expected).__name__}, got {type(actual).__name__}")
            return

        if isinstance(expected, dict):
            # Check for missing/extra keys
            expected_keys = set(expected.keys())
            actual_keys = set(actual.keys())
            
            missing_keys = expected_keys - actual_keys
            extra_keys = actual_keys - expected_keys
            
            for key in missing_keys:
                differences.append(f"Missing key at {path}.{key}")
            for key in extra_keys:
                differences.append(f"Extra key at {path}.{key}")

            # Compare values for common keys
            for key in expected_keys & actual_keys:
                new_path = f"{path}.{key}" if path else key
                DataComparator._compare_recursive(expected[key], actual[key], differences, new_path)

        elif isinstance(expected, list):
            if len(expected) != len(actual):
                differences.append(f"List length mismatch at {path}: expected {len(expected)}, got {len(actual)}")
                return

            for i, (exp_item, act_item) in enumerate(zip(expected, actual)):
                new_path = f"{path}[{i}]"
                DataComparator._compare_recursive(exp_item, act_item, differences, new_path)

        elif expected != actual:
            differences.append(f"Value mismatch at {path}: expected '{expected}', got '{actual}'")

    @staticmethod
    def _compare_lists(expected: List[Dict], actual: List[Dict]) -> Tuple[bool, List[str]]:
        """Compare two lists of dictionaries."""
        differences = []
        
        if len(expected) != len(actual):
            differences.append(f"List length mismatch: expected {len(expected)}, got {len(actual)}")

        for i, (exp_row, act_row) in enumerate(zip(expected, actual)):
            DataComparator._compare_recursive(exp_row, act_row, differences, f"Row[{i}]")

        return len(differences) == 0, differences

    @staticmethod
    def validate_schema(data: Dict, schema: Dict) -> Tuple[bool, List[str]]:
        """
        Validate data against a schema.

        Args:
            data: Data to validate
            schema: Schema definition

        Returns:
            Tuple of (is_valid, list of errors)
        """
        errors = []
        DataComparator._validate_recursive(data, schema, errors)
        return len(errors) == 0, errors

    @staticmethod
    def _validate_recursive(data: Any, schema: Dict, errors: List[str], path: str = ""):
        """Recursively validate data against schema."""
        if "type" not in schema:
            return

        expected_type = schema["type"]
        
        if expected_type == "object":
            if not isinstance(data, dict):
                errors.append(f"Type mismatch at {path}: expected object, got {type(data).__name__}")
                return

            required_fields = schema.get("required", [])
            properties = schema.get("properties", {})

            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {path}.{field}" if path else f"Missing required field: {field}")

            for key, value in data.items():
                if key in properties:
                    new_path = f"{path}.{key}" if path else key
                    DataComparator._validate_recursive(value, properties[key], errors, new_path)

        elif expected_type == "array":
            if not isinstance(data, list):
                errors.append(f"Type mismatch at {path}: expected array, got {type(data).__name__}")
                return

            items_schema = schema.get("items", {})
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                DataComparator._validate_recursive(item, items_schema, errors, new_path)

        elif expected_type == "string":
            if not isinstance(data, str):
                errors.append(f"Type mismatch at {path}: expected string, got {type(data).__name__}")

        elif expected_type == "number":
            if not isinstance(data, (int, float)) or isinstance(data, bool):
                errors.append(f"Type mismatch at {path}: expected number, got {type(data).__name__}")

        elif expected_type == "boolean":
            if not isinstance(data, bool):
                errors.append(f"Type mismatch at {path}: expected boolean, got {type(data).__name__}")
