import pytest
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
