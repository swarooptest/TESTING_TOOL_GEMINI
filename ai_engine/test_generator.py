import os
import re
import ast

GENERATED_TEST_DIR = "tests/generated"

class TestGenerator:
    def __init__(self):
        os.makedirs(GENERATED_TEST_DIR, exist_ok=True)

    def clean_generated_code(self, code):
        """Clean and fix AI-generated code to ensure it's valid Python."""
        lines = code.splitlines()
        cleaned_lines = []
        in_code_block = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip markdown code blocks
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            
            # Skip documentation/instruction lines
            if any(marker in stripped.lower() for marker in [
                "before running:", "install", "download", "replace", "adjust", 
                "run the test:", "remember to", "this improved", "to run"
            ]):
                continue
            
            # Keep empty lines and comments
            if not stripped or stripped.startswith("#"):
                cleaned_lines.append(line)
                continue
            
            # Keep Python code lines
            if re.match(r'^\s*(from|import|def|class|@|if|elif|else|try|except|finally|for|while|with|return|yield|assert|break|continue|pass|raise|del|global|nonlocal)', line):
                # Fix common AI-generated issues
                fixed_line = line
                
                # Uncomment commented fixtures and important code
                if re.match(r'^\s*#\s*@pytest\.fixture', line):
                    fixed_line = re.sub(r'^\s*#\s*', '', line)
                elif re.match(r'^\s*#\s*(def|class|try|except|if|else|return|yield)', line):
                    fixed_line = re.sub(r'^\s*#\s*', '', line)
                
                cleaned_lines.append(fixed_line)
                continue
            
            # Keep variable assignments and expressions
            if re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\s*=', line) or re.match(r'^\s*[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z_]', line):
                cleaned_lines.append(line)
                continue
            
            # Comment out everything else
            cleaned_lines.append("# " + line)
        
        return "\n".join(cleaned_lines)
    
    def validate_python_syntax(self, code):
        """Check if the code has valid Python syntax and common runtime issues."""
        try:
            # Parse syntax
            ast.parse(code)
            
            # Check for common undefined variable issues
            undefined_vars = ['service=service', 'driver = webdriver.Chrome(service=service)']
            for var_issue in undefined_vars:
                if var_issue in code:
                    return False, f"Undefined variable detected: {var_issue}"
            
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def create_fallback_test(self):
        """Create a simple fallback test if generated code fails."""
        return '''import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
LOGIN_URL = "https://www.saucedemo.com/"
TIMEOUT_SECONDS = 10

@pytest.fixture
def driver():
    """Setup and teardown for the WebDriver."""
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()

def test_basic_login(driver):
    """Basic login test."""
    driver.get(LOGIN_URL)
    
    # Find and fill username
    username_field = WebDriverWait(driver, TIMEOUT_SECONDS).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    username_field.send_keys(USERNAME)
    
    # Find and fill password
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(PASSWORD)
    
    # Click login button
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    
    # Verify successful login
    inventory = WebDriverWait(driver, TIMEOUT_SECONDS).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
    )
    assert inventory.is_displayed(), "Login failed"
    print("Test passed successfully!")
'''

    def save_test(self, code, filename="test_generated_login.py"):
        print("[System] Saving generated test...")
        
        # Clean the generated code
        cleaned_code = self.clean_generated_code(code)
        
        # Validate syntax
        is_valid, error = self.validate_python_syntax(cleaned_code)
        
        if not is_valid:
            print(f"[Warning] Generated code has syntax errors: {error}")
            print("[System] Using fallback test instead...")
            cleaned_code = self.create_fallback_test()
        
        file_path = os.path.join(GENERATED_TEST_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)
        
        print(f"[System] Test saved to: {file_path}")
        return file_path
