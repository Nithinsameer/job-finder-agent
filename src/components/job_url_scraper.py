import csv
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["linkedin"],
    search_term='"Full stack developer"',
    location="United States",
    #job_type= "internship",
    results_wanted=5,
    hours_old=168, # (only Linkedin/Indeed is hour specific, others round up to days old)
    #country_indeed='USA',  # only needed for indeed / glassdoor
    
    #linkedin_fetch_description=True # get full description and direct job url for linkedin (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
jobs.to_csv("data/jobs_full_stack.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel