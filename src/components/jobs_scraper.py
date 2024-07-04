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
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# Open LinkedIn website
driver.get("https://www.linkedin.com/jobs/")

# Enter email
email_input = driver.find_element(By.ID, "session_key")
email_input.send_keys("")

# Enter password
password_input = driver.find_element(By.ID, "session_password")
password_input.send_keys("")

# Click the sign-in button
sign_in_button = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-btn--full-width")
sign_in_button.click()

# Searching for the data analyst job
skill_input = driver.find_element(By.CSS_SELECTOR, "[id^='jobs-search-box-keyword-id-ember']")
skill_input.send_keys("Data Analyst")
skill_input.send_keys(Keys.ENTER)

# Wait for the filters to be present and visible
wait = WebDriverWait(driver, 10)

# Open "Date posted" filter dropdown
try:
    date_posted_button = wait.until(EC.element_to_be_clickable((By.ID, "searchFilter_timePostedRange")))
    print("Date posted filter button found.")
    date_posted_button.click()
    time.sleep(2)  # Adding sleep to see if the element becomes available

    # Try locating the "Past 24 hours" option using a more robust selector
    past_24_hours_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='timePostedRange-r86400']/following-sibling::label")))
    print("Past 24 hours option found.")
    past_24_hours_option.click()

    # Click the "Show results" button to apply the filter
    show_results_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Apply current filter to show results')]")))
    show_results_button.click()
    
except TimeoutException:
    print("Date posted filter options not found.")
except NoSuchElementException as e:
    print(f"An element was not found: {e}")

# Wait for the page to load
time.sleep(5)

# Close the driver
driver.quit()
