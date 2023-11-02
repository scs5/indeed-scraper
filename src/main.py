from scraping.web_scraper import *
from scraping.skill_scraper import *
from analysis.visualization import *
from categorization.categorizer import *
from utils import *

# Indeed search terms
KEYWORDS = 'Machine Learning Engineer, Data Scientist'
LOCATION = 'Raleigh, NC'

# Data output filenames
SCRAPED_DATA_OUTPUT_FN = './data/scraped_job_data.csv'
CURATED_DATA_OUTPUT_FN = './data/curated_job_data.csv'
SKILL_COUNTS_OUTPUT_FN = './data/skill_counts.csv'
SKILL_TYPES_OUTPUT_FN = './data/skill_types.csv'
SKILL_CATEGORIES_OUTPUT_FN = './data/skill_categories.csv'
COMBINED_SKILL_DATA_FN = './data/combined_skill_data.csv'
KNOWN_SKILLS_DATA_FN = './data/known_skills.csv'

# Visualization output filenames
SKILL_COUNT_BARPLOT_FN = './figures/skill_counts.png'
SKILL_TYPE_PIECHART_FN = './figures/skill_types.png'
SKILL_CATEGORY_PIECHART_FN = './figures/skill_categories.png'
KNOWN_SKILL_BARPLOT_FN = './figures/known_skills.png'


def curate_data():
    # Scrape data
    job_data = scrape_job_data(KEYWORDS, LOCATION)

    # Remove duplicate jobs
    job_data = remove_duplicates(SCRAPED_DATA_OUTPUT_FN)

    # Save to csv
    job_data.to_csv(SCRAPED_DATA_OUTPUT_FN, index=False)


def visualize_data():
    visualize_skill_counts(COMBINED_SKILL_DATA_FN, SKILL_COUNT_BARPLOT_FN)
    visualize_hard_vs_soft(COMBINED_SKILL_DATA_FN, SKILL_TYPE_PIECHART_FN)
    visualize_category_pie(COMBINED_SKILL_DATA_FN, SKILL_CATEGORY_PIECHART_FN)
    visualize_known_skills(KNOWN_SKILLS_DATA_FN, KNOWN_SKILL_BARPLOT_FN)

 
def main():
    #curate_data()
    #skill_counts = extract_all_skills(CURATED_DATA_OUTPUT_FN, SKILL_COUNTS_OUTPUT_FN)

    #find_skill_info(SKILL_COUNTS_OUTPUT_FN, SKILL_TYPES_OUTPUT_FN, info='Type')
    #find_skill_info(SKILL_COUNTS_OUTPUT_FN, SKILL_CATEGORIES_OUTPUT_FN, info='Category')
    #combine_skill_info(SKILL_TYPES_OUTPUT_FN, SKILL_CATEGORIES_OUTPUT_FN, COMBINED_SKILL_DATA_FN)

    visualize_data()


if __name__ == '__main__':
    main()