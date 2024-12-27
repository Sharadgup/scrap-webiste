from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

# Setup the Selenium Grid URL
selenium_grid_url = "http://localhost:4444/wd/hub"

# Setup Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Create WebDriver object and connect to the grid
driver = webdriver.Remote(
    command_executor=selenium_grid_url,
    options=options
)

# Run a test: Open a page and get the title
driver.get("https://www.instagram.com/jun.amaki/")
title = driver.title

# Log the result in JSON format
result = {
    "test_case": "Page Title Test",
    "url": driver.current_url,
    "title": title
}

# Output the result as JSON
print(json.dumps(result, indent=4))

driver.quit()
