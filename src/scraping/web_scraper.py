# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Webdriver
import chromedriver_autoinstaller

# Other
import time
import pandas as pd
import random
import re

def generate_indeed_url(keywords, location):
    """Generates an Indeed job search URL based on keywords and location.

    Args:
        keywords (str): The search keyword or job title.
        location (str): The location for the job search.

    Returns:
        url (str): Indeed job search URL.
    """
    # Encode spaces and commas
    keywords = keywords.replace(' ', '+')
    keywords = keywords.replace(',', '%2C')
    location = location.replace(' ', '+')
    location = location.replace(',', '%2C')

    # Construct job search URL
    url = 'https://www.indeed.com/jobs?q=' + keywords + '&l=' + location
    return url


def load_webdriver():
    """Loads a WebDriver for web scraping.

    Returns:
        driver (webdriver.Chrome): WebDriver instance.
    """
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    return driver


def find_num_jobs(driver):
    """Finds the total number of job listings on the current Indeed search page.

    Args:
        driver (webdriver.Chrome): WebDriver instance.

    Returns:
        num_jobs (int): Total number of job listings.
    """
    # Find job count element and convert to integer
    jobs_num = driver.find_element(By.CLASS_NAME, "jobsearch-JobCountAndSortPane-jobCount").get_attribute("innerText")
    jobs_num = jobs_num.replace(' jobs', '')
    if ',' in jobs_num and (jobs_num := jobs_num.replace(',', '')).isdigit():
        jobs_num = int(jobs_num)

    return int(jobs_num)


def scrape_job_data(keywords, location):
    """Scrapes job data from the Indeed search results page.

    Args:
        driver (webdriver.Chrome): WebDriver instance.

    Returns:
        job_data (pd.DataFrame): Pandas DataFrame containing job data.
    """
    # Generate URL for Indeed job search
    url = generate_indeed_url(keywords, location)
    print('Scraping from:', url)

    # Load webdriver
    driver = load_webdriver()
    driver.get(url)

    # Wait for page to load
    time.sleep(1)
    driver.refresh()
    time.sleep(2)

    # Data storage
    job_data = pd.DataFrame(columns=['Title', 'Link', 'ID', 'Date', 'Description'])
    job_title_list = []
    job_link_list = []
    job_id_list = []
    job_date_list = []
    job_description_list = []

    num_jobs_scraped = 0
    num_jobs = find_num_jobs(driver)

    while num_jobs_scraped < num_jobs:
        # Find job entries on search page
        job_page = driver.find_element(By.ID, "mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME, "job_seen_beacon")
        num_jobs_scraped = num_jobs_scraped + len(jobs)

        for job_entry in jobs:
            # Extract job title
            job_title = job_entry.find_element(By.CLASS_NAME, "jobTitle")
            job_title_list.append(job_title.text)

            # Extract job link and ID
            job_link_list.append(job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("href"))
            job_id_list.append(job_title.find_element(By.CSS_SELECTOR, "a").get_attribute("id"))

            # Extract and reformat posted date
            job_date = job_entry.find_element(By.CLASS_NAME, "date").text
            pattern = r"Posted (\d+ (?:second|minute|hour|day|week|month|year)s? ago)"
            matches = re.findall(pattern, job_date)
            job_date = matches[0] if matches else None
            job_date_list.append(job_date)

            # Extract job description
            job_title.click()
            time.sleep(3 + random.random())
            try:
                job_description_list.append(driver.find_element(By.ID, "jobDescriptionText").text)
            except:
                job_description_list.append(None)

        # Wait random amount to simulate human-like behavior
        time.sleep(random.random())

        # Go to the next page (only if it exists)
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
            next_button.click()
        except NoSuchElementException:
            break

        # Wait for the next page to load
        time.sleep(1 + random.random())

    # Load data into a DataFrame
    job_data['Title'] = job_title_list
    job_data['Link'] = job_link_list
    job_data['ID'] = job_id_list
    job_data['Date'] = job_date_list
    job_data['Description'] = job_description_list

    return job_data