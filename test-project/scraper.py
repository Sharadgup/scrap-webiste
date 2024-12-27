from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Use Dockerized Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Connect to the remote WebDriver
driver = webdriver.Remote(
    command_executor='http://172.17.0.2:4444',
    options=options
)

# Example usage
driver.get("https://www.instagram.com/jun.amaki/")
print(driver.page_source)
driver.quit()
