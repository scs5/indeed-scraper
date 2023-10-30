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
    """Generates an Indeed URL.

    Args:
        keywords (str): The search keyword or job title.
        location (str): The location for the job search.

    Returns:
        url (string): Indeed job search URL
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
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    return driver


def find_num_jobs(driver):
    # Find job count element and convert to integer
    jobs_num = driver.find_element(By.CLASS_NAME,"jobsearch-JobCountAndSortPane-jobCount").get_attribute("innerText")
    jobs_num = jobs_num.replace(' jobs','')

    if ',' in jobs_num and (jobs_num := jobs_num.replace(',', '')).isdigit():
        jobs_num = int(jobs_num)

    return int(jobs_num)


def scrape_job_data(driver):
    
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
        job_page = driver.find_element(By.ID,"mosaic-jobResults")
        jobs = job_page.find_elements(By.CLASS_NAME,"job_seen_beacon")
        num_jobs_scraped = num_jobs_scraped + len(jobs)
        
        for job_entry in jobs: 
            # Extract job title
            job_title = job_entry.find_element(By.CLASS_NAME,"jobTitle")
            job_title_list.append(job_title.text)

            # Extract job link and ID
            job_link_list.append(job_title.find_element(By.CSS_SELECTOR,"a").get_attribute("href"))
            job_id_list.append(job_title.find_element(By.CSS_SELECTOR,"a").get_attribute("id"))

            # Extract and reformat posted date
            job_date = job_entry.find_element(By.CLASS_NAME,"date").text
            pattern = r"Posted (\d+ (?:second|minute|hour|day|week|month|year)s? ago)"
            matches = re.findall(pattern, job_date)
            job_date = matches[0] if matches else None
            job_date_list.append(job_date)

            # Extract job description
            job_title.click()
            time.sleep(3 + random.random())
            try: 
                job_description_list.append(driver.find_element(By.ID,"jobDescriptionText").text)
            except: 
                job_description_list.append(None)
        
        # Wait random amount to simulate human-like behavior
        time.sleep(random.random())
        
        # Go to next page (only if it exists)
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
            next_button.click()
        except NoSuchElementException:
            break

        # Wait for next page to load
        time.sleep(1 + random.random())

    # Load data into dataframe
    job_data['Title'] = job_title_list
    job_data['Link'] = job_link_list
    job_data['ID'] = job_id_list
    job_data['Date'] = job_date_list
    job_data['Description'] = job_description_list

    job_data.to_csv('./data/scraped_job_data.csv', index=False)


if __name__ == '__main__':
    url = generate_indeed_url('Machine Learning Engineer', 'Raleigh, NC')
    print(url)

    driver = load_webdriver()
    driver.get(url)

    scrape_job_data(driver)