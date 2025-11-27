"""
Test Marker Utility

Handles:
- Pytest markers for tagging tests with JIRA IDs
- Test categorization (smoke, regression, sanity, etc.)
- Selective test execution
"""

import pytest
from typing import List, Optional


class TestMarker:
    """Defines and manages test markers for categorization and execution."""

    # Marker definitions
    @staticmethod
    def smoke():
        """Mark test as smoke test."""
        return pytest.mark.smoke

    @staticmethod
    def regression():
        """Mark test as regression test."""
        return pytest.mark.regression

    @staticmethod
    def sanity():
        """Mark test as sanity test."""
        return pytest.mark.sanity

    @staticmethod
    def integration():
        """Mark test as integration test."""
        return pytest.mark.integration

    @staticmethod
    def unit():
        """Mark test as unit test."""
        return pytest.mark.unit

    @staticmethod
    def skip_test(reason: str = ""):
        """Mark test to be skipped."""
        return pytest.mark.skip(reason=reason)

    @staticmethod
    def xfail(reason: str = ""):
        """Mark test as expected to fail."""
        return pytest.mark.xfail(reason=reason)

    @staticmethod
    def jira(jira_id: str):
        """
        Mark test with JIRA ID for traceability.

        Args:
            jira_id: JIRA issue ID (e.g., 'SKY-1234')

        Example:
            @TestMarker.jira('SKY-1234')
            def test_feature():
                pass
        """
        return pytest.mark.jira(jira_id)

    @staticmethod
    def jira_with_category(jira_id: str, category: str):
        """
        Mark test with JIRA ID and category.

        Args:
            jira_id: JIRA issue ID
            category: Test category (smoke, regression, sanity, integration, unit)
        """
        return [TestMarker.jira(jira_id), getattr(TestMarker, category)()]

    @staticmethod
    def data_driven():
        """Mark test as data-driven."""
        return pytest.mark.data_driven

    @staticmethod
    def parametrize(param_names: str, param_values: List):
        """
        Mark test for parameterization.

        Args:
            param_names: Comma-separated parameter names
            param_values: List of parameter value tuples

        Example:
            @TestMarker.parametrize("input,expected", [(1, 2), (2, 4)])
            def test_double(input, expected):
                assert input * 2 == expected
        """
        return pytest.mark.parametrize(param_names, param_values)


# pytest configuration for custom markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "sanity: mark test as sanity test")
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "jira: mark test with JIRA ID")
    config.addinivalue_line("markers", "data_driven: mark test as data-driven")
