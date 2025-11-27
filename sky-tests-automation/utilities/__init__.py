"""
Utilities Package for Sky Test Automation Framework

This package contains all utility modules for:
- Configuration management
- Logging and reporting
- Data comparison and validation
- Test data generation
- Environment management
"""

__version__ = "1.0.0"
__author__ = "Test Automation Team"

# Re-export commonly used utilities
from .execution_log_manager import (
	save_execution_report,
	read_latest_report,
)
