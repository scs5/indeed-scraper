from scraping.web_scraper import *
from scraping.skill_scraper import *
from analysis.visualization import *

KEYWORDS = 'Machine Learning Engineer, Data Scientist'
LOCATION = 'Raleigh, NC'

SCRAPED_DATA_OUTPUT_FN = './data/scraped_job_data.csv'
CURATED_DATA_OUTPUT_FN = './data/curated_job_data.csv'
SKILL_COUNTS_OUTPUT_FN = './data/skill_counts.csv'

def main():
def curate_data():
    # Scrape data
    job_data = scrape_job_data(KEYWORDS, LOCATION)

    # Remove duplicate jobs
    job_data = remove_duplicates(SCRAPED_DATA_OUTPUT_FN)

    # Save to csv
    job_data.to_csv(SCRAPED_DATA_OUTPUT_FN, index=False)

 
def main():
    #curate_data()


if __name__ == '__main__':
    main()