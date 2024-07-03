import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    return driver

def wait_and_click(driver, by, value, timeout=30):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(1)
        element.click()
        logging.debug(f"Successfully clicked element: {value}")
    except Exception as e:
        logging.error(f"Error clicking element {value}: {str(e)}")
        raise

def login(driver, email, password):
    driver.get("https://www.linkedin.com/jobs/")
    logging.info("Navigated to LinkedIn Jobs page")
    
    email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "session_key")))
    email_input.send_keys(email)
    logging.debug("Entered email")
    
    password_input = driver.find_element(By.ID, "session_password")
    password_input.send_keys(password)
    logging.debug("Entered password")
    
    sign_in_button = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-btn--full-width")
    sign_in_button.click()
    logging.info("Clicked sign in button")
    
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='jobs-search-box-keyword-id-ember']")))
    logging.info("Successfully logged in")

def search_jobs(driver, job_title):
    skill_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='jobs-search-box-keyword-id-ember']")))
    skill_input.clear()
    skill_input.send_keys(job_title)
    skill_input.send_keys(Keys.ENTER)
    logging.info(f"Searched for job: {job_title}")
    time.sleep(10)  # Wait for search results to load

def apply_filters(driver):
    try:
        # Wait for the filters to load
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "search-reusables__filter-list")))
        logging.debug("Filters loaded")

        # Click on "Date posted" filter
        date_posted_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='searchFilter_timePostedRange']"))
        )
        date_posted_button.click()
        logging.debug("Clicked Date posted filter")

        # Select "Past 24 hours"
        past_24_hours = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='timePostedRange-r86400']"))
        )
        past_24_hours.click()
        logging.debug("Selected Past 24 hours")

        # Apply the date filter
        show_results_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button--primary') and contains(., 'Show')]"))
        )
        show_results_button.click()
        logging.debug("Applied date filter")

        time.sleep(5)

        # Click on "Experience level" filter
        experience_level_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='searchFilter_experience']"))
        )
        experience_level_button.click()
        logging.debug("Clicked Experience level filter")

        # Select "Entry level"
        entry_level = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='experience-2']"))
        )
        entry_level.click()
        logging.debug("Selected Entry level")

        # Apply the experience level filter
        show_results_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'artdeco-button--primary') and contains(., 'Show')]"))
        )
        show_results_button.click()
        logging.debug("Applied experience level filter")

        time.sleep(5)
        logging.info("All filters applied successfully")
    except Exception as e:
        logging.error(f"Error applying filters: {str(e)}")
        raise

def scrape_job_listings(driver):
    job_listings = []
    try:
        job_cards = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "job-card-container")))
        logging.info(f"Found {len(job_cards)} job cards")
        
        for index, card in enumerate(job_cards):
            try:
                title = WebDriverWait(card, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "job-card-list__title"))).text
                company = card.find_element(By.CLASS_NAME, "job-card-container__company-name").text
                location = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
                link = card.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
                
                job_listings.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Link": link
                })
                logging.debug(f"Scraped job {index + 1}: {title} at {company}")
            except (NoSuchElementException, TimeoutException) as e:
                logging.warning(f"Skipping job card {index + 1} due to error: {str(e)}")
    except Exception as e:
        logging.error(f"Error scraping job listings: {str(e)}")
    
    logging.info(f"Successfully scraped {len(job_listings)} job listings")
    return job_listings

def main():
    driver = setup_driver()
    try:
        login(driver, "ynsameer@gmail.com", "Nitins@meer02")
        search_jobs(driver, "Data Analyst")
        apply_filters(driver)
        job_listings = scrape_job_listings(driver)
        
        for job in job_listings:
            logging.info(job)
        
        input("Press Enter to close the browser...")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()