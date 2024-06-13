import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from datetime import date, timedelta, datetime
import time
import csv

# Path to the Chromedriver
path = "/Volumes/NithinSameer/College/GRA/TamilMatrimony/chrome-mac-arm64/chromedriver.app"

# Configure WebDriver
options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('start-maximized')
# options.add_argument('disable-infobars')
# options.add_argument('--disable-extensions')
# options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Initialize WebDriver
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

#open linkedin website
driver.get("https://www.linkedin.com/jobs/")

#entering the email
email_input = driver.find_element(By.ID, "session_key")
email_input.send_keys("email")

#entering the password
password_input = driver.find_element(By.ID, "session_password")
password_input.send_keys("password")

#clicking the sign in button
sign_in_button = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-btn--full-width")
sign_in_button.click()

#searching for the data analyst job
# Use a CSS selector that matches the input field regardless of the changing part of the ID
skill_input = driver.find_element(By.CSS_SELECTOR, "[id^='jobs-search-box-keyword-id-ember']")
skill_input.send_keys("Data Analyst")
skill_input.send_keys(Keys.ENTER)

current_url = driver.current_url

# #selecting for jobs posted in the last 24 hours
# try:
#     # Wait for the dropdown button to be present and visible
#     dropdown_button = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "searchFilter_timePostedRange"))
#     )

#     # Click on the dropdown button
#     dropdown_button.click()
#     time.sleep(1)

#     # Wait for the "24 hours" option to be present and visible
#     option_24_hours = WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "search-reusables_select-input"))
#     )

#     # Click on the "24 hours" option
#     option_24_hours.click()

# except:
#     print("Dropdown button or '24 hours' option not found.")


#wait for the page to load
#time.sleep(5)

#close the driver
#driver.quit()
