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
    print("Show results button found.")
    show_results_button.click()
    
except TimeoutException:
    print("Date posted filter options not found.")
except NoSuchElementException as e:
    print(f"An element was not found: {e}")

# Wait for the page to load
time.sleep(5)

# Open "Experience level" filter dropdown
try:
    experience_level_button = wait.until(EC.element_to_be_clickable((By.ID, "searchFilter_experience")))
    print("Experience level filter button found.")
    experience_level_button.click()
    time.sleep(2)  # Adding sleep to see if the element becomes available

    # Select "Internship" option
    internship_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='experience-1']/following-sibling::label")))
    print("Internship option found.")
    internship_option.click()

    # Select "Entry level" option
    entry_level_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='experience-2']/following-sibling::label")))
    print("Entry level option found.")
    entry_level_option.click()

    # Click the "Show results" button to apply the filter
    show_results_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[3]/div[4]/section/div/section/div/div/div/ul/li[4]/div/div/div/div[1]/div/form/fieldset/div[2]/button[2]')))
    print("Show results button for experience level found.")
    show_results_button.click()
    
except TimeoutException:
    print("Experience level filter options not found.")
except NoSuchElementException as e:
    print(f"An element was not found: {e}")

# Wait for the page to load
time.sleep(5)

job_listings = []

# Wait for the job cards to be present
time.sleep(5)

job_cards = driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")

for job_card in job_cards:
    try:
        job_title_element = job_card.find_element(By.CSS_SELECTOR, "a.job-card-list__title")
        company_element = job_card.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle span.job-card-container__primary-description")
        location_element = job_card.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__caption ul li")

        job_title = job_title_element.text if job_title_element else "N/A"
        company = company_element.text if company_element else "N/A"
        location = location_element.text if location_element else "N/A"
        job_url = job_title_element.get_attribute("href") if job_title_element else "N/A"
        
        job_listings.append({
            "Job Title": job_title,
            "Company": company,
            "Location": location,
            "URL": job_url
        })
    except NoSuchElementException as e:
        print(f"An element was not found: {e}")
        continue

# Convert to DataFrame and save to CSV
df = pd.DataFrame(job_listings)
df.to_csv("linkedin_job_listings.csv", index=False)

# Close the driver
driver.quit()
