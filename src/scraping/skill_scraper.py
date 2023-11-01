import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def get_authorization():
    payload = f'client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials&scope=emsi_open'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    response = requests.request("POST", 'https://auth.emsicloud.com/connect/token', data=payload, headers=headers)
    access_token = response.json().get("access_token")

    return access_token


def extract_job_skills(job_desc, access_token):
    # Get skills from API request
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    payload = {
        'text': job_desc,
        'confidenceThreshold': 0.6
    }
    response = requests.post('https://emsiservices.com/skills/versions/latest/extract?language=en', json=payload, headers=headers)

    # Extract skills from json response
    if response.status_code == 200:
        data = response.json()
        skills = [item['skill']['name'] for item in data['data']]
    else:
        print('Error extracting skills. Status code:', response.status_code)

    return skills


def extract_all_skills(data_fn, output_fn):
    access_token = get_authorization()

    job_data = pd.read_csv(data_fn)
    extracted_skills = []

    for desc in job_data['Description']:
        skills = extract_job_skills(desc, access_token)
        extracted_skills.extend(skills)

    # Create a DataFrame to count the skills
    skills_df = pd.DataFrame({'Skill': extracted_skills})
    skills_counts = skills_df['Skill'].value_counts().reset_index()
    skills_counts.columns = ['Skill', 'Count']

    skills_counts.to_csv(output_fn, index=False)

    return skills_counts