from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json
import requests

# Step 1: Set up Selenium WebDriver
service = Service(executable_path='/Users/daviddai/Downloads/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

# Step 2: Navigate to the URL
url = "https://seia.org/solar-state-by-state/"
# driver.get(url)


response = requests.get(url)
print(response.text)
print(response.status_code)
print(f"here\n")