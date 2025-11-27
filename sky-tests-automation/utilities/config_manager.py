"""
Configuration Manager Utility

Handles:
- Environment variable management
- Configuration file loading (YAML, JSON)
- Environment-specific configurations
"""

import os
import json
import logging
from typing import Any, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configurations from environment variables and config files."""

    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        """Singleton pattern to ensure only one instance."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration manager."""
        if not self._config:
            self._load_config()

    def _load_config(self):
        """Load configuration from environment variables and config files."""
        # Get environment
        self.environment = os.getenv("TEST_ENV", "dev")
        
        # Load base configuration
        config_dir = os.getenv("CONFIG_DIR", "sky-tests-automation/config")
        config_file = os.path.join(config_dir, f"config.{self.environment}.json")
        
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    self._config = json.load(f)
                logger.info(f"✅ Configuration loaded from {config_file}")
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"⚠️ Failed to load config file {config_file}: {e}")
                self._config = {}
        else:
            logger.info(f"ℹ️ Config file not found: {config_file}. Using defaults.")
            self._config = self._get_default_config()

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
            # Location where global reports and execution logs are stored (at repo root)
            "reports_dir": "reports",
            # How many rotated logs to keep (older ones will be removed)
            "log_retention": 10,
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key: Configuration key (supports dot notation: 'database.host')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        if "." in key:
            # Handle nested keys like 'database.host'
            keys = key.split(".")
            value = self._config
            for k in keys:
                value = value.get(k, {}) if isinstance(value, dict) else {}
            return value if value != {} else default
        
        return self._config.get(key, default)

    def set(self, key: str, value: Any):
        """
        Set configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        logger.debug(f"Configuration set: {key} = {value}")

    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration dictionary."""
        return self._config.copy()

    def reload(self):
        """Reload configuration from files."""
        self._config = {}
        self._load_config()
        logger.info("✅ Configuration reloaded")


# Singleton instance
config = ConfigManager()
