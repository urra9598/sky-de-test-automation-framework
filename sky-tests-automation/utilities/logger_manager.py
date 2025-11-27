"""
Logger Manager Utility

Handles:
- Structured logging setup
- Test execution logs
- Execution report generation
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from utilities.execution_log_manager import save_execution_report as save_global_execution_report
try:
    from utilities.config_manager import config as CONFIG
except Exception:
    CONFIG = None


class LoggerManager:
    """Manages test execution logging and reporting."""

    def __init__(self, test_case_name: str, base_log_dir: Optional[str] = None):
        """
        Initialize logger manager for a test case.

        Args:
            test_case_name: Name of the test case
            base_log_dir: Base directory for logs
        """
        self.test_case_name = test_case_name
        # Resolve base_log_dir from config if not provided
        if base_log_dir:
            self.base_log_dir = base_log_dir
        else:
            # Hardcoded approach: file is at repo_root/sky-tests-automation/utilities/logger_manager.py
            # parents[2] = repo_root
            # logs go to repo_root/reports/latest_execution_logs
            script_path = Path(__file__).resolve()
            repo_root = script_path.parents[2]
            reports_dir = repo_root / "reports"
            self.base_log_dir = str(reports_dir / "latest_execution_logs")

        # test-specific directory under the base log directory
        self.test_log_dir = os.path.join(self.base_log_dir, test_case_name)

        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create directories
        self._create_directories()
        
        # Initialize logger
        self.logger = self._setup_logger()
        
        # Execution metadata
        self.execution_data: Dict[str, Any] = {
            "test_case": test_case_name,
            "start_time": datetime.now().isoformat(),
            "status": "RUNNING",
            "results": {
                "expected": None,
                "actual": None,
                "comparison": None,
                "validation_errors": []
            }
        }

    def _create_directories(self):
        """Create necessary log directories."""
        Path(self.test_log_dir).mkdir(parents=True, exist_ok=True)
        logger_instance = logging.getLogger(__name__)
        logger_instance.debug(f"✅ Log directory created: {self.test_log_dir}")

    def _setup_logger(self) -> logging.Logger:
        """Setup logger with both file and console handlers."""
        logger = logging.getLogger(f"test.{self.test_case_name}")
        logger.setLevel(logging.DEBUG)

        # File handler
        log_file = os.path.join(self.test_log_dir, f"execution_{self.timestamp}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def log_info(self, message: str):
        """Log info level message."""
        self.logger.info(message)

    def log_debug(self, message: str):
        """Log debug level message."""
        self.logger.debug(message)

    def log_warning(self, message: str):
        """Log warning level message."""
        self.logger.warning(message)

    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log error level message."""
        if exception:
            self.logger.error(message, exc_info=True)
        else:
            self.logger.error(message)

    def log_result(self, expected: Any, actual: Any, validation_errors: List[str] = None):
        """
        Log test results.

        Args:
            expected: Expected result
            actual: Actual result
            validation_errors: List of validation errors
        """
        self.execution_data["results"]["expected"] = expected
        self.execution_data["results"]["actual"] = actual
        self.execution_data["results"]["validation_errors"] = validation_errors or []
        
        self.logger.info("=" * 80)
        self.logger.info("TEST RESULT COMPARISON")
        self.logger.info("=" * 80)
        self.logger.info(f"Expected: {json.dumps(expected, indent=2, default=str)}")
        self.logger.info(f"Actual: {json.dumps(actual, indent=2, default=str)}")
        
        if validation_errors:
            self.logger.error(f"Validation Errors: {len(validation_errors)}")
            for error in validation_errors:
                self.logger.error(f"  - {error}")

    def save_execution_report(self, status: str = "PASSED", failure_reason: str = None):
        """
        Save execution report as JSON.

        Args:
            status: Test status (PASSED, FAILED, SKIPPED)
            failure_reason: Reason for failure if applicable
        """
        self.execution_data["status"] = status
        self.execution_data["end_time"] = datetime.now().isoformat()
        if failure_reason:
            self.execution_data["failure_reason"] = failure_reason

        report_file = os.path.join(self.test_log_dir, f"execution_report_{self.timestamp}.json")
        
        try:
            with open(report_file, "w") as f:
                json.dump(self.execution_data, f, indent=2, default=str)
            self.logger.info(f"✅ Execution report saved: {report_file}")
        except IOError as e:
            self.logger.error(f"Failed to save execution report: {e}")

        # Also save a centralized latest execution log (rotates previous latest)
        try:
            save_global_execution_report(self.execution_data)
            self.logger.info("Saved centralized latest execution log")
        except Exception as e:
            self.logger.error(f"Failed to save centralized latest execution log: {e}")

    def get_log_directory(self) -> str:
        """Return the log directory for this test case."""
        return self.test_log_dir
