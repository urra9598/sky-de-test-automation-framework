"""
Report Generator Utility

Handles:
- Test execution report generation (HTML, JSON)
- Summary statistics
- Test result aggregation
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates comprehensive test execution reports."""

    def __init__(self, report_dir: str = "sky-tests-automation/reports"):
        """
        Initialize report generator.

        Args:
            report_dir: Base directory for reports
        """
        self.report_dir = report_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.test_results: List[Dict[str, Any]] = []
        
        # Create report directory
        Path(self.report_dir).mkdir(parents=True, exist_ok=True)

    def add_test_result(
        self,
        test_name: str,
        status: str,
        duration: float,
        expected: Any = None,
        actual: Any = None,
        errors: List[str] = None,
        jira_id: str = None
    ):
        """
        Add test result to report.

        Args:
            test_name: Test case name
            status: Test status (PASSED, FAILED, SKIPPED)
            duration: Test execution time in seconds
            expected: Expected result
            actual: Actual result
            errors: List of error messages
            jira_id: Associated JIRA ID
        """
        result = {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "expected": expected,
            "actual": actual,
            "errors": errors or [],
            "jira_id": jira_id,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        logger.debug(f"Result added: {test_name} - {status}")

    def generate_json_report(self) -> str:
        """
        Generate JSON report.

        Returns:
            Path to generated JSON report
        """
        summary = self._get_summary()
        
        report = {
            "execution_summary": summary,
            "generated_at": datetime.now().isoformat(),
            "test_results": self.test_results
        }

        report_file = os.path.join(self.report_dir, f"test_report_{self.timestamp}.json")
        
        try:
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"✅ JSON report generated: {report_file}")
            return report_file
        except IOError as e:
            logger.error(f"Failed to generate JSON report: {e}")
            raise

    def generate_html_report(self) -> str:
        """
        Generate HTML report.

        Returns:
            Path to generated HTML report
        """
        summary = self._get_summary()
        html_content = self._build_html(summary)

        report_file = os.path.join(self.report_dir, f"test_report_{self.timestamp}.html")
        
        try:
            with open(report_file, "w") as f:
                f.write(html_content)
            logger.info(f"✅ HTML report generated: {report_file}")
            return report_file
        except IOError as e:
            logger.error(f"Failed to generate HTML report: {e}")
            raise

    def _get_summary(self) -> Dict[str, Any]:
        """Calculate test execution summary statistics."""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r["status"] == "PASSED")
        failed = sum(1 for r in self.test_results if r["status"] == "FAILED")
        skipped = sum(1 for r in self.test_results if r["status"] == "SKIPPED")
        total_duration = sum(r.get("duration", 0) for r in self.test_results)

        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "pass_percentage": round((passed / total * 100) if total > 0 else 0, 2),
            "total_duration_seconds": round(total_duration, 2),
            "execution_timestamp": datetime.now().isoformat()
        }

    def _build_html(self, summary: Dict[str, Any]) -> str:
        """Build HTML report content."""
        passed_class = "success" if summary["failed"] == 0 else "danger"
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Test Execution Report</title>
    <style>
        * {{ font-family: Arial, sans-serif; }}
        body {{ margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; margin: 20px 0; }}
        .summary-card {{ padding: 15px; border-radius: 5px; text-align: center; color: white; }}
        .total {{ background-color: #5a6c7d; }}
        .passed {{ background-color: #28a745; }}
        .failed {{ background-color: #dc3545; }}
        .skipped {{ background-color: #ffc107; color: #333; }}
        .duration {{ background-color: #17a2b8; }}
        .summary-card h3 {{ margin: 0 0 10px 0; font-size: 14px; }}
        .summary-card .value {{ font-size: 24px; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background-color: #007bff; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .status-passed {{ color: #28a745; font-weight: bold; }}
        .status-failed {{ color: #dc3545; font-weight: bold; }}
        .status-skipped {{ color: #ffc107; font-weight: bold; }}
        .errors {{ background-color: #f8d7da; padding: 10px; border-radius: 3px; color: #721c24; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Execution Report</h1>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>Total Tests</h3>
                <div class="value">{summary['total_tests']}</div>
            </div>
            <div class="summary-card passed">
                <h3>Passed</h3>
                <div class="value">{summary['passed']}</div>
            </div>
            <div class="summary-card failed">
                <h3>Failed</h3>
                <div class="value">{summary['failed']}</div>
            </div>
            <div class="summary-card skipped">
                <h3>Skipped</h3>
                <div class="value">{summary['skipped']}</div>
            </div>
            <div class="summary-card duration">
                <h3>Duration (s)</h3>
                <div class="value">{summary['total_duration_seconds']}</div>
            </div>
        </div>

        <p><strong>Pass Rate:</strong> {summary['pass_percentage']}%</p>
        <p><strong>Generated:</strong> {summary['execution_timestamp']}</p>

        <h2>Test Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Test Name</th>
                    <th>Status</th>
                    <th>Duration (s)</th>
                    <th>JIRA ID</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for result in self.test_results:
            status_class = f"status-{result['status'].lower()}"
            errors_html = ""
            if result['errors']:
                errors_html = f"<div class='errors'>{'<br>'.join(result['errors'])}</div>"
            
            html += f"""
                <tr>
                    <td>{result['test_name']}</td>
                    <td><span class='{status_class}'>{result['status']}</span></td>
                    <td>{result['duration']:.2f}</td>
                    <td>{result.get('jira_id', '-')}</td>
                    <td>{errors_html}</td>
                </tr>
"""

        html += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        return html
