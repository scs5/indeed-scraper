# Job Skills Mining and Analysis
## Table of Contents
1. [Overview](#overview)
    - [Key Objectives](#key-objectives)
    - [Technologies Used](#technologies-used)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Results](#results)
6. [Challenges](#challenges)
7. [Lessons Learned](#lessons-learned)
8. [Acknowledgments](#acknowledgments)

## Overview
This project aims to automate the process of extracting skills from job listings on Indeed, categorizing these skills, and performing data analysis on the extracted skills and their respective categories.

### Key Objectives
1. **Web Scraping Indeed:** I start by scraping job listings from the Indeed job board using a selenium webdriver.
2. **Skills Extraction with Lightcast API:** Next, I utilize the Lightcast API to extract skills from the job descriptions. Lightcast is a service that helps identify and extract specific skills and keywords from text, which is particularly useful for job-related data.
3. **Skills Categorization with ChatGPT API:** After extracting skills, I employ the ChatGPT API to automatically categorize these skills. This categorization step helps organize the skills into broader skill categories or domains, making it easier to analyze and interpret the data.
4. **Data Analysis:** Finally, I conduct data analysis to gain insights into the skills demand within the job market.

### Technologies Used
#### Web Scraping:
- **Selenium:** Selenium is a powerful web automation tool that allows you to interact with web pages and automate various tasks, including web scraping. In this project, I used Selenium to control the web browser and navigate the Indeed website.
#### APIs:
- **ChatGPT API:** This API from OpenAI allows you to interact with the ChatGPT model programmatically, providing prompts and receiving responses for various natural language processing tasks, such as categorization.
- **Lightcast API:** Lightcast is a service that specializes in natural language processing and information extraction. It helps identify and extract specific skills mentioned within job descriptions.
  
**Other:** matplotlib, seaborn, numpy, pandas

## Project Structure
```
.
├── data                       # Data storage
├── figures                    # Data visualizations
├── src
│   ├── analysis
|   |   └── visualization.py   # Generates data visualizations
|   |
│   ├── categorization
|   |   └── categorizer.py     # Categories skills
|   |
|   └── scraping
|   |   ├── skill_scraper.py   # Extracts skills from job descriptions
|   |   └── web_scraper.py     # Scrapes Indeed for job postings
|   |
|   ├── main.py                # Main project script
|   └── utils.py               # Utility functions
|
├── .env                       # API keys
├── .gitignore
├── README.md
└── requirements.txt           # Project dependencies
```

## Installation
`pip install -r requirements.txt`

## Usage
Run `main.py`, uncommenting the functions you wish to call (scraping data, exctracting skills, or visualizing the data).<br>
You will have to change `SKILL_CATEGORY_PROMPT_HEADER` in `categorizer.py` to accomodate your own self-made categories.

## Results
I began by searching for positions similar to 'Machine Learning Engineer' and 'Data Scientist' in my area. I gathered data from around 150 job postings, filtering out duplicates and positions that didn't align with my goals. After this manual curation, I narrowed it down to 50 relevant job listings.
From these job descriptions, I extracted the most frequently mentioned skills and visualized them in a bar plot below.
![counts](./figures/skill_counts.png)

Many of these skills were quite broad. My main aim with this project was to identify specific, learnable skills that I needed to focus on. I created a plot highlighting the top 50 skills, color-coded to indicate my proficiency in each.
![known](./figures/known_skills.png)
**Skills I know:** Python, SQL, R, NLP, Sckikit-learn, APIs, Java, C++, Linux, Git, Pandas, Agile, ...<br>
**Skills I need to practice:** PyTorch, JavaSCript, LLM, Unit Testing, Computer Vision, C, Keras, Data Warehousing, React, Artificial NNs<br>
**Skills I need to learn:** AWS, Apache Spark, DevOps, Azure, Tableau, MLOps, Docker, Kubernetes, Cloud Computing, ETL, Nvidia CUDA<br><br>

I then organized these skills using ChatGPT, categorizing them into "hard" vs. "soft" skills and placing them in broader skill categories specific to my field.
![categories](./figures/skill_categories.png)
![types](./figures/skill_types.png)

## Challenges
- While scraping data from Indeed, I encountered security measures that triggered captchas, requiring me to implement random waiting times between actions to simulate human-like behavior.
- Crafting effective prompts for ChatGPT proved to be more challenging than expected. Ensuring clarity and specificity in the prompts is crucial to minimize response variability and prevent data formatting issues.
- ChatGPT's API performance is a bit sluggish for regular users, leading to longer category generation times. Additionally, server overloads may occasionally disrupt the process.

## Lessons Learned
- It's advisable to explore existing APIs before resorting to web scraping. I later discovered that Indeed offers its own API, although I couldn't actually use it due to significant restrictions. Nevertheless, it could have simplified the project considerably if I had been able to use it.
- Avoid hardcoding API keys directly into your code. I made the mistake of inadvertently committing my API keys in the early stages of development. To fix this, I securely stored them in a .env file, which is loaded into the main files while keeping it excluded from version control.

## Acknowledgments
- [Lightcast's](https://lightcast.io/) API
- [OpenAI's](https://openai.com/blog/chatgpt) ChatGPT API
