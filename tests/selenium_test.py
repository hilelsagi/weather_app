import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    """Setup and teardown for headless Chrome WebDriver"""
    service = Service()
    driver = webdriver.Chrome(service=service)
    driver.get("http://16.171.205.23:5000/")
    yield driver
    driver.quit()

def test_valid_city(driver):
    """Test entering a valid city and checking for weather data."""
    wait = WebDriverWait(driver, 5)
    city_input = wait.until(EC.presence_of_element_located((By.NAME, "city")))
    city_input.send_keys("Paris")
    city_input.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Weather for" in page_text, "Weather data is not displayed for a valid city"

def test_invalid_city(driver):
    """Test entering an invalid city and checking for error message."""
    wait = WebDriverWait(driver, 5)
    city_input = wait.until(EC.presence_of_element_located((By.NAME, "city")))
    city_input.clear()
    city_input.send_keys("InvalidCity1234")
    city_input.send_keys(Keys.RETURN)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    page_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Invalid city data: No results found." in page_text, "Error message not found!"

def test_404_page(driver):
    """Test navigating to a non-existent page and checking for a 404 message."""
    driver.get("http://16.171.205.23:5000/nonexistentpage")
    error_text = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    ).text
    assert "404" in error_text or "Not Found" in error_text, "404 page does not display expected message"
