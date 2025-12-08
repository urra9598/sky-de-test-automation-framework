
"""
Configuration Manager Utility - Manages application configurations from environment variables and config files.

Handles:
- Environment variable management
- Configuration file loading (.properties, JSON)
- Environment-specific configurations
"""

import os
import json
import logging
from typing import Any, Dict
from pathlib import Path
from threading import Lock

logger = logging.getLogger(__name__)

class ConfigManager:
    """Thread-safe Singleton for managing application configurations."""

    _instance = None
    _lock = Lock()
    _config: Dict[str, Any] = {}

    def __new__(cls):
        """Ensure only one instance (Singleton)."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration manager."""
        if not self._config:  # Load only once
            self._load_config()

    def _load_config(self):
        """Load configuration from environment variables, JSON file, properties file, and defaults."""
        with self._lock:
            # Start with environment variables
            self._config.update(os.environ)

            # Determine environment (default: dev)
            self.environment = os.getenv("TEST_ENV", "dev")

            # Load JSON config file (if exists)
            json_config_file = os.getenv("CONFIG_JSON", f"config.{self.environment}.json")
            if Path(json_config_file).is_file():
                try:
                    with open(json_config_file, "r") as f:
                        json_config = json.load(f)
                        self._config.update(json_config)
                    logger.info(f"✅ JSON config loaded from {json_config_file}")
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️ Invalid JSON in {json_config_file}: {e}")

            # Load properties file (if exists)
            properties_file = os.getenv("CONFIG_PROPERTIES", "config.properties")
            if Path(properties_file).is_file():
                props = self._load_properties(properties_file)
                self._config.update(props)
                logger.info(f"✅ Properties loaded from {properties_file}")
            else:
                logger.warning(f"⚠️ Properties file not found: {properties_file}")

            # Apply fallback defaults for missing keys
            defaults = self._get_default_config()
            for key, value in defaults.items():
                self._config.setdefault(key, value)

            logger.debug(f"Final configuration: {self._config}")

    def _load_properties(self, file_path: str) -> Dict[str, str]:
        """Load key-value pairs from .properties file."""
        props = {}
        try:
            with open(file_path) as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key, value = line.split("=", 1)
                        props[key.strip()] = value.strip()
        except IOError as e:
            logger.error(f"Failed to read properties file: {e}")
        return props

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "environment": self.environment,
            "test_timeout": 300,
            "log_level": "INFO",
            "report_format": ["html", "json"],
            "data_formats": ["json", "csv", "xml"],
            "enable_screenshots": True,
            "retry_count": 3,
            "reports_dir": "reports",
            "log_retention": 10,
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key (supports dot notation)."""
        if "." in key:
            keys = key.split(".")
            value = self._config
            for k in keys:
                value = value.get(k, {}) if isinstance(value, dict) else {}
            return value if value != {} else default
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """Set configuration value."""
        with self._lock:
            self._config[key] = value
            logger.debug(f"Configuration set: {key} = {value}")

    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary."""
        return self._config.copy()

    def reload(self):
        """Reload configuration from files and env vars."""
        with self._lock:
            self._config.clear()
            self._load_config()
            logger.info("✅ Configuration reloaded")


# Singleton instance
config = ConfigManager()
