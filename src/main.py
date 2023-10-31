from scraping.web_scraper import *
from chatgpt.chatgpt_api import *

KEYWORDS = 'Machine Learning Engineer, Data Scientist'
LOCATION = 'Raleigh, NC'

SCRAPED_DATA_OUTPUT = './data/scraped_job_data.csv'

def main():
    # Scrape data
    job_data = scrape_job_data(KEYWORDS, LOCATION)
    job_data.to_csv(SCRAPED_DATA_OUTPUT, index=False)


if __name__ == '__main__':
    main()