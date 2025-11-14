import os
import sys
import re

def sanitize_name(test_case_name):
    # Replace spaces with underscore
    test_case_name = test_case_name.replace(" ", "_")
    # Remove all characters except letters, numbers, and underscore
    sanitized = re.sub(r'[^A-Za-z0-9_]', '', test_case_name)
    return sanitized

def create_test_case(test_case_name):
    base_dir = "sky-tests-automation"

    # Paths
    test_case_dir = os.path.join(base_dir, "test-scripts", test_case_name)
    expected_dir = os.path.join(test_case_dir, "expected-result")
    logs_dir = os.path.join(test_case_dir, "logs")

    # Check if folder already exists
    if os.path.exists(test_case_dir):
        print(f"ERROR: Test case '{test_case_name}' already exists at {test_case_dir}")
        sys.exit(1)

    # Create new directories
    os.makedirs(expected_dir)
    os.makedirs(logs_dir)

    # Create test script file
    test_script_path = os.path.join(test_case_dir, f"{test_case_name}.py")
    sample_content = f"""# Auto-generated Test Case: {test_case_name}
def {test_case_name}():
    # TODO: Add test logic
    assert True
"""

    with open(test_script_path, "w") as f:
        f.write(sample_content)

    print(f"✅ Test case folder created: {test_case_dir}")
    print(f"✅ Test script created: {test_script_path}")
    print("✅ Expected-result & logs folders created.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR: Usage: provide <test-case-name> in run configuration")
        sys.exit(1)

    original_name = sys.argv[1]
    sanitized_name = sanitize_name(original_name)

    if sanitized_name != original_name:
        print(f"⚠️ Name '{original_name}' was sanitized to '{sanitized_name}'")

    if not sanitized_name:
        print("ERROR: Test case name is invalid after sanitization.")
        sys.exit(1)

    create_test_case(sanitized_name)