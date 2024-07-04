from flask import Flask, request, render_template, redirect, url_for
import logging
import csv
import os
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, ExperienceLevelFilters

app = Flask(__name__)

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)

# List to store job data
jobs = []

# Fired once for each successfully processed job
def on_data(data: EventData):
    job_type = 'Full-time' if 'Full-time' in data.insights else 'Internship' if 'Internship' in data.insights else 'Unknown'
    
    salary = 'Not specified'
    for insight in data.insights:
        if 'salary' in insight.lower():
            salary = insight
            break

    jobs.append({
        'title': data.title,
        'company': data.company,
        'location': data.place,
        'date': data.date,
        'link': data.link
    })
    print('[ON_DATA]', data.title, data.company, data.company_link, data.date, data.link, data.insights, len(data.description))

# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))

def on_error(error):
    print('[ON_ERROR]', error)

def on_end():
    print('[ON_END]')
    # Save the collected job data to a CSV file
    if jobs:
        keys = jobs[0].keys()
        output_dir = 'data'  # Save to the data directory
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        output_file_path = os.path.join(output_dir, 'jobs.csv')
        with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            dict_writer = csv.DictWriter(output_file, keys, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\")
            dict_writer.writeheader()
            dict_writer.writerows(jobs)
        print(f"Saved jobs to {output_file_path}")

scraper = LinkedinScraper(
    chrome_executable_path=None,  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_binary_location=None,  # Custom path to Chrome/Chromium binary (e.g. /foo/bar/chrome-mac/Chromium.app/Contents/MacOS/Chromium)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=0.5,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=40  # Page load timeout (in seconds)    
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    query = request.form['query']
    experience = request.form['experience']
    location = request.form['location']

    # Map experience input to LinkedinScraper's filters
    experience_map = {
        'intern': ExperienceLevelFilters.INTERNSHIP,
        'entry_level': ExperienceLevelFilters.ENTRY_LEVEL,
        'associate': ExperienceLevelFilters.ASSOCIATE,
        'mid_senior': ExperienceLevelFilters.MID_SENIOR,
        'director': ExperienceLevelFilters.DIRECTOR
    }

    queries = [
        Query(
            query=query,
            options=QueryOptions(
                locations=[location],
                apply_link=True,
                limit=30,
                filters=QueryFilters(
                    relevance=RelevanceFilters.RECENT,
                    time=TimeFilters.MONTH,
                    experience=[experience_map[experience]]
                )
            )
        ),
    ]

    scraper.run(queries)
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)
