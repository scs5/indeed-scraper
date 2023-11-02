import openai
import os
import pandas as pd
from dotenv import load_dotenv
from io import StringIO
import numpy as np

load_dotenv()
openai.api_key = os.getenv('CHATGPT_SECRET')

SKILL_TYPE_PROMPT_HEADER = '''
I am going to give you a list of skills and their counts.
Determine their type as a hard or soft, then add that to the csv.
Return the updated csv with labels Skill, Type, and Count.
Do not respond with any other text, just the csv.\n
'''

SKILL_CATEGORY_PROMPT_HEADER = '''
I am going to give you a list of skills and their counts.
Categorize them as one of the following:
- Machine Learning Algorithms/Models
- Data Analytics & Visualization
- Programming Languages
- Data Management
- Cloud and Infrastructure
- Business and Communication
- Mathematics and Statistics
- Tools and Libraries
- Problem Solving and Research
- Other
Then add the category to the csv.
If multiple categories apply to the skill, choose the one that is most closely related.
Return the updated csv with labels Skill, Category, and Count.
Do not respond with any other text, just the csv:\n
'''


def find_skill_info(data_fn, output_fn, info='Type', batch_size=200):
    """Finds skill information (Type or Category) using ChatGPT and updates a CSV file.

    Args:
        data_fn (str): The filename of the CSV file containing skill data.
        output_fn (str): The filename for saving the updated CSV file.
        info (str): Information to find ('Type' or 'Category'). Defaults to 'Type'.
        batch_size (int): Batch size for processing skills. Defaults to 200.
    """
    # Set up data
    skill_data = pd.read_csv(data_fn)
    combined_data = pd.DataFrame(columns=['Skill', info, 'Count'])

    # Iterate through skills in batches
    num_rows = len(skill_data)
    number_of_batches = (num_rows + batch_size - 1) // batch_size
    print('Finding Skill ' + info + 's...')
    for i in range(0, num_rows, batch_size):
        print('Processing Batch', str(int(np.ceil(i / batch_size + 1))) + '/' + str(number_of_batches))
        batch = skill_data.iloc[i:i+batch_size]
        batch_csv = batch.to_csv(index=False)
        
        # Prompt ChatGPT for skill types
        if info == 'Type':
            prompt = SKILL_TYPE_PROMPT_HEADER + batch_csv
        elif info == 'Category':
            prompt = SKILL_CATEGORY_PROMPT_HEADER + batch_csv
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        
        # Extract the CSV response
        response = response.choices[0].message.content
        batch_data_with_type = pd.read_csv(StringIO(response))

        # Append the batch data to the combined_data DataFrame
        combined_data = pd.concat([combined_data, batch_data_with_type], ignore_index=True)

    # Write the combined DataFrame to a CSV file
    combined_data.to_csv(output_fn, index=False)


def combine_skill_info(skill_type_fn, skill_category_fn, output_fn):
    """Combines skill information from two CSV files into one and updates a CSV file.

    Args:
        skill_type_fn (str): The filename of the CSV file containing skill type data.
        skill_category_fn (str): The filename of the CSV file containing skill category data.
        output_fn (str): The filename for saving the updated CSV file.
    """
    # Read the CSV files into Pandas DataFrames
    skill_type_df = pd.read_csv(skill_type_fn)
    skill_category_df = pd.read_csv(skill_category_fn)

    # Merge the DataFrames on the "Skill" column
    merged_df = pd.merge(skill_type_df, skill_category_df, on="Skill", how="inner")

    # Rename the columns for clarity
    merged_df.rename(columns={"Type_x": "Type", "Category_y": "Category", "Count_x": "Count"}, inplace=True)

    # Select the desired columns
    merged_df = merged_df[["Skill", "Type", "Category", "Count"]]

    # Write the merged dataFrame to the output CSV file
    merged_df.to_csv(output_fn, index=False)