import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load API keys stored in .env file
load_dotenv()
CLIENT_ID = os.getenv('LIGHTCAST_CLIENT_ID')
CLIENT_SECRET = os.getenv('LIGHTCAST_CLIENT_SECRET')


def get_authorization():
    """Obtains an access token for authorization from the Lightcast API.

    Returns:
        access_token (str): The access token for authentication.
    """
    # Create reqest string
    payload = f'client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&grant_type=client_credentials&scope=emsi_open'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    # Request access token
    response = requests.request("POST", 'https://auth.emsicloud.com/connect/token', data=payload, headers=headers)
    access_token = response.json().get("access_token")

    return access_token


def extract_job_skills(job_desc, access_token):
    """Extracts skills from a job description using the Lightcast API.

    Args:
        job_desc (str): The job description text.
        access_token (str): The access token obtained for authorization.

    Returns:
        skills (list): A list of extracted skills from the job description.
    """
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
    """Extracts skills from a file containing job descriptions and saves skills and their counts to an output file.

    Args:
        data_fn (str): The filename of the CSV file containing job descriptions.
        output_fn (str): The filename for the output CSV file.

    Returns:
        skills_counts (pandas.DataFrame): A DataFrame containing skill counts.
    """
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

    # Save and return skills and their counts
    skills_counts.to_csv(output_fn, index=False)
    return skills_counts