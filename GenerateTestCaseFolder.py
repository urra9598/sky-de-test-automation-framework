import os
import sys
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def sanitize_name(test_case_name):
    """Sanitize test case name to be filesystem-safe."""
    test_case_name = test_case_name.replace(" ", "_")
    sanitized = re.sub(r'[^A-Za-z0-9_]', '', test_case_name)
    return sanitized

def create_test_case(test_case_name, base_dir=None):
    """Create test case folder structure."""
    if base_dir is None:
        base_dir = os.getenv("SKY_TESTS_DIR", "sky-tests-automation")
    
    test_case_dir = os.path.join(base_dir, "test-scripts", test_case_name)
    expected_dir = os.path.join(test_case_dir, "expected-result")
    logs_dir = os.path.join(test_case_dir, "logs")

    # Check if folder already exists
    if os.path.exists(test_case_dir):
        logger.error(f"Test case '{test_case_name}' already exists at {test_case_dir}")
        return False

    try:
        # Create new directories
        os.makedirs(expected_dir)
        os.makedirs(logs_dir)

        # Create test script file
        test_script_path = os.path.join(test_case_dir, f"{test_case_name}.py")
        sample_content = f"""# Auto-generated Test Case: {test_case_name}

def {test_case_name}():
    \"\"\"Test case implementation.\"\"\"
    # TODO: Add test logic
    assert True

if __name__ == "__main__":
    {test_case_name}()
"""
        with open(test_script_path, "w") as f:
            f.write(sample_content)

        logger.info(f"✅ Test case folder created: {test_case_dir}")
        logger.info(f"✅ Test script created: {test_script_path}")
        logger.info("✅ Expected-result & logs folders created.")
        return True

    except OSError as e:
        logger.error(f"Failed to create test case: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python GenerateTestCaseFolder.py <test-case-name>")
        sys.exit(1)

    original_name = sys.argv[1]
    sanitized_name = sanitize_name(original_name)

    if not sanitized_name:
        logger.error("Test case name is invalid after sanitization.")
        sys.exit(1)

    if sanitized_name != original_name:
        logger.warning(f"Name '{original_name}' was sanitized to '{sanitized_name}'")

    success = create_test_case(sanitized_name)
    sys.exit(0 if success else 1)