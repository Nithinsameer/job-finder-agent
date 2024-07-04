import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def fetch_job_details(url):
    driver = None
    try:
        print(f"Starting to fetch job details from: {url}")
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        
        print("Navigating to the URL...")
        driver.get(url)
        
        print("Waiting for the job description to load...")
        wait = WebDriverWait(driver, 10)
        description_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "description__text--rich")))
        print("Job description element found!")
        
        print("Getting page source...")
        page_source = driver.page_source
        
        print("Parsing HTML with BeautifulSoup...")
        soup = BeautifulSoup(page_source, 'html.parser')
        
        print("Finding job description div...")
        job_description = soup.find('div', class_='description__text--rich')
        
        if job_description:
            print("Job description found. Extracting sections...")
            sections = {
                'responsibilities': [],
                'qualifications': [],
                'preferred qualifications': [],
                'miscellaneous': []
            }
            current_section = 'miscellaneous'
            for element in job_description.find_all(['strong', 'ul', 'p']):
                if element.name == 'strong':
                    text = element.text.strip(':').lower()
                    if 'responsibilit' in text:
                        current_section = 'responsibilities'
                    elif 'qualificat' in text or 'requirements' in text:
                        current_section = 'qualifications'
                    elif 'preferred' in text:
                        current_section = 'preferred qualifications'
                    else:
                        current_section = 'miscellaneous'
                    sections[current_section].append(f"{element.text.strip()}")
                    print(f"Found section: {current_section}")
                elif element.name in ['ul', 'p']:
                    if element.name == 'ul':
                        items = [f"- {li.text.strip()}" for li in element.find_all('li')]
                    else:
                        items = [element.text.strip()]
                    sections[current_section].extend(items)
                    print(f"Added {len(items)} items to {current_section}")
                    #print(f"Items: {items}")  # Print items for debugging
            
            print("Formatting output...")
            job_details = {}
            print(f"sections: {sections}")
            # for section, items in sections.items():
            #     print(f"the items: /n {items}")
                # if items:
                #     job_details[section] = "\n".join(items)
            
            print("Job details fetched successfully!")
            return sections
        else:
            print("Job description div not found!")
            return {"error": "Job description not found"}
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"error": f"Error fetching job details: {str(e)}"}
    finally:
        if driver:
            print("Closing the browser...")
            driver.quit()

# Read the CSV file
print("Reading CSV file...")
df = pd.read_csv('data/jobs.csv')

# Add new columns for each section
for section in ['responsibilities', 'qualifications', 'preferred qualifications', 'miscellaneous']:
    df[section] = ''

# Iterate through each row
for index, row in df.iterrows():
    url = row['job_url']
    print(f"\nProcessing job {index + 1}/{len(df)}: {url}")
    
    # Fetch job details
    job_details = fetch_job_details(url)
    
    # Update the DataFrame
    for section, content in job_details.items():
        df.at[index, section] = content
    
    # Add a random delay to avoid overwhelming the servers
    delay = random.uniform(1, 3)
    print(f"Waiting for {delay:.2f} seconds before next request...")
    time.sleep(delay)

# Save the updated DataFrame back to CSV
print("\nSaving results to CSV...")
df.to_csv('jobs_with_details_v2.csv', index=False)

print("Job details fetching completed. Results saved to 'jobs_with_details.csv'")