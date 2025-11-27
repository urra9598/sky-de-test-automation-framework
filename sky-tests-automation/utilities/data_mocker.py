"""
Data Mocker Utility

Handles:
- Test data generation using LLM (placeholder for future integration)
- Mock data creation for various scenarios
- Data template management
"""

import json
import random
import string
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class DataMocker:
    """Generates mock test data for various scenarios."""

    @staticmethod
    def generate_string(length: int = 10, pattern: str = "alpha") -> str:
        """
        Generate random string.

        Args:
            length: String length
            pattern: 'alpha', 'alphanumeric', 'numeric', or custom charset

        Returns:
            Generated string
        """
        if pattern == "alpha":
            charset = string.ascii_letters
        elif pattern == "alphanumeric":
            charset = string.ascii_letters + string.digits
        elif pattern == "numeric":
            charset = string.digits
        else:
            charset = pattern

        return "".join(random.choice(charset) for _ in range(length))

    @staticmethod
    def generate_email() -> str:
        """Generate random email address."""
        username = DataMocker.generate_string(10, "alpha")
        domain = DataMocker.generate_string(8, "alpha")
        return f"{username}@{domain}.com"

    @staticmethod
    def generate_phone() -> str:
        """Generate random phone number."""
        return "+1" + "".join(random.choices(string.digits, k=10))

    @staticmethod
    def generate_date(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        date_format: str = "%Y-%m-%d"
    ) -> str:
        """
        Generate random date within range.

        Args:
            start_date: Start date (default: 1 year ago)
            end_date: End date (default: today)
            date_format: Date format string

        Returns:
            Generated date string
        """
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        time_delta = end_date - start_date
        random_days = random.randint(0, time_delta.days)
        random_date = start_date + timedelta(days=random_days)
        
        return random_date.strftime(date_format)

    @staticmethod
    def generate_number(
        min_value: int = 0,
        max_value: int = 1000,
        decimal_places: int = 0
    ) -> float:
        """
        Generate random number.

        Args:
            min_value: Minimum value
            max_value: Maximum value
            decimal_places: Number of decimal places

        Returns:
            Generated number
        """
        value = random.uniform(min_value, max_value)
        if decimal_places == 0:
            return int(value)
        return round(value, decimal_places)

    @staticmethod
    def generate_uuid() -> str:
        """Generate UUID v4."""
        import uuid
        return str(uuid.uuid4())

    @staticmethod
    def generate_credit_card() -> str:
        """Generate mock credit card number (non-valid)."""
        return "".join(random.choices(string.digits, k=16))

    @staticmethod
    def generate_data_from_template(template: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate data from template specification.

        Args:
            template: Template dictionary with field definitions
                Example:
                {
                    "name": {"type": "string", "length": 10},
                    "email": {"type": "email"},
                    "age": {"type": "number", "min": 18, "max": 65},
                    "status": {"type": "enum", "values": ["active", "inactive"]},
                    "created_date": {"type": "date"}
                }

        Returns:
            Generated data dictionary
        """
        generated_data = {}

        for field, spec in template.items():
            field_type = spec.get("type", "string")

            if field_type == "string":
                length = spec.get("length", 10)
                pattern = spec.get("pattern", "alpha")
                generated_data[field] = DataMocker.generate_string(length, pattern)

            elif field_type == "email":
                generated_data[field] = DataMocker.generate_email()

            elif field_type == "phone":
                generated_data[field] = DataMocker.generate_phone()

            elif field_type == "number":
                min_val = spec.get("min", 0)
                max_val = spec.get("max", 1000)
                decimal = spec.get("decimal_places", 0)
                generated_data[field] = DataMocker.generate_number(min_val, max_val, decimal)

            elif field_type == "date":
                date_format = spec.get("format", "%Y-%m-%d")
                generated_data[field] = DataMocker.generate_date(date_format=date_format)

            elif field_type == "enum":
                values = spec.get("values", [])
                generated_data[field] = random.choice(values) if values else None

            elif field_type == "uuid":
                generated_data[field] = DataMocker.generate_uuid()

            elif field_type == "credit_card":
                generated_data[field] = DataMocker.generate_credit_card()

            elif field_type == "object":
                nested_template = spec.get("properties", {})
                generated_data[field] = DataMocker.generate_data_from_template(nested_template)

            elif field_type == "array":
                item_template = spec.get("items", {})
                count = spec.get("count", 1)
                generated_data[field] = [
                    DataMocker.generate_data_from_template(item_template) for _ in range(count)
                ]

        return generated_data

    @staticmethod
    def generate_batch_data(template: Dict[str, Any], count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate multiple records from template.

        Args:
            template: Data template
            count: Number of records to generate

        Returns:
            List of generated data records
        """
        return [DataMocker.generate_data_from_template(template) for _ in range(count)]

    @staticmethod
    def generate_from_json_schema(schema_file: str) -> Dict[str, Any]:
        """
        Generate data from JSON schema file.

        Args:
            schema_file: Path to JSON schema file

        Returns:
            Generated data matching schema
        """
        try:
            with open(schema_file, "r") as f:
                schema = json.load(f)
            
            template = DataMocker._convert_schema_to_template(schema.get("properties", {}))
            return DataMocker.generate_data_from_template(template)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error reading schema file {schema_file}: {e}")
            raise

    @staticmethod
    def _convert_schema_to_template(properties: Dict[str, Any]) -> Dict[str, Any]:
        """Convert JSON schema properties to template format."""
        template = {}

        for field_name, field_schema in properties.items():
            field_type = field_schema.get("type", "string")

            if field_type == "string":
                template[field_name] = {
                    "type": "string",
                    "length": field_schema.get("maxLength", 10)
                }

            elif field_type == "integer":
                template[field_name] = {
                    "type": "number",
                    "min": field_schema.get("minimum", 0),
                    "max": field_schema.get("maximum", 1000),
                    "decimal_places": 0
                }

            elif field_type == "number":
                template[field_name] = {
                    "type": "number",
                    "min": field_schema.get("minimum", 0),
                    "max": field_schema.get("maximum", 1000),
                    "decimal_places": 2
                }

            elif field_type == "object":
                template[field_name] = {
                    "type": "object",
                    "properties": DataMocker._convert_schema_to_template(field_schema.get("properties", {}))
                }

            elif field_type == "array":
                items_schema = field_schema.get("items", {})
                template[field_name] = {
                    "type": "array",
                    "items": DataMocker._convert_schema_to_template(items_schema.get("properties", {})),
                    "count": 1
                }

        return template
