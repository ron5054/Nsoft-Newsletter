"""
Validation script to check project structure and code syntax without running the full application.
"""

import ast
import os
import sys
from pathlib import Path


def validate_python_syntax(file_path):
    """Validate Python file syntax."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def check_file_exists(file_path, description):
    """Check if a file exists and validate it."""
    if not os.path.exists(file_path):
        return False, f"Missing: {description}"
    
    if file_path.endswith('.py'):
        is_valid, error = validate_python_syntax(file_path)
        if not is_valid:
            return False, f"{description}: {error}"
    
    return True, f"[OK] {description}"


def validate_project_structure():
    """Validate the complete project structure."""
    print("LinkedIn MCP Server - Project Structure Validation")
    print("=" * 60)
    
    base_path = Path(__file__).parent
    
    # Required files and their descriptions
    required_files = [
        ("requirements.txt", "Python dependencies file"),
        ("linkedin_extractor.py", "Core extraction logic"),
        ("mcp_server.py", "MCP server implementation"),
        ("exceptions.py", "Custom exceptions module"),
        ("cli.py", "Command-line interface"),
        ("README.md", "Documentation"),
        ("setup.py", "Installation script"),
        ("test_server.py", "Test suite"),
        ("validate_structure.py", "This validation script"),
    ]
    
    all_valid = True
    
    for filename, description in required_files:
        file_path = base_path / filename
        is_valid, message = check_file_exists(str(file_path), description)
        print(message)
        if not is_valid:
            all_valid = False
    
    print("\n" + "=" * 60)
    
    if all_valid:
        print("[SUCCESS] PROJECT STRUCTURE VALIDATION PASSED!")
        print("\nNext steps to run the server:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Install Playwright: playwright install chromium")
        print("3. Run tests: python test_server.py")
        print("4. Start server: python mcp_server.py")
        print("5. Test CLI: python cli.py <linkedin-url>")
    else:
        print("[FAILED] PROJECT STRUCTURE VALIDATION FAILED!")
        print("Please ensure all required files are present and have valid syntax.")
    
    print("\n" + "=" * 60)
    
    # Check imports in main modules
    print("Checking module imports (syntax validation)...")
    
    key_modules = [
        "linkedin_extractor.py",
        "mcp_server.py", 
        "cli.py"
    ]
    
    for module in key_modules:
        file_path = base_path / module
        if file_path.exists():
            is_valid, error = validate_python_syntax(str(file_path))
            status = "[OK]" if is_valid else "[ERROR]"
            print(f"{status} {module}: {'Valid syntax' if is_valid else error}")
        else:
            print(f"[ERROR] {module}: File not found")
    
    print("\n" + "=" * 60)
    print("VALIDATION COMPLETE")
    print("=" * 60)
    
    return all_valid


if __name__ == "__main__":
    success = validate_project_structure()
    sys.exit(0 if success else 1)