import openai

openai.api_key = 'YOUR_API_KEY'

PROMPT_HEADER = '''
I will prompt you with a job description contained within ```, and I want your help to extract specific useful technical skills: 
 
1. Make the skills as concise as possible, maybe even as keywords. Be as economic as possible.
2. Avoid paragraphs of text or long sentences. 
3. Avoid redundant text.
4. Have each skill be as specific as possible. I am looking for specific languages, tools, or algorithms to practice.
5. Please provide one skill per line, with no other extra text. Your answer should be in the following format:
"
Skill1
Skill2
Skill3
...
"

Please keep these rules in mind when categorizing the job description. Let's begin!:\n
'''

job_description = '''Summary
Posted: Aug 14, 2023
Weekly Hours: 40
Role Number: 200496347
Imagine what you can do here. Apple is a place where extraordinary people gather to do their lives best work. Together we create products and experiences people once couldn’t have imagined, and now, can’t imagine living without. It’s the diversity of those people and their ideas that inspires the innovation that runs through everything we do.
Key Qualifications
Master’s degree or foreign equivalent in Computer Science, Software Engineering, Electrical Engineering, Information Technology or related field and 2 years of experience in the job offered or related occupation. Alternatively, employer will accept a Bachelor’s degree or foreign equivalent in Computer Science, Software Engineering, Electrical Engineering, Information Technology or related field and 5 years of progressive, post-baccalaureate experience in the job offered or related occupation.
1 year of experience with each of the following skills is required:
ETL, BI and Data analytics
Apache Hadoop, Apache Hive, Apache Sqoop or Apache Spark
Extract data and implement data pipelines & SQL friendly data structures
Apache AVRO, Apache Parquet and common methods in data transformation
Dependency driven job schedulers
Teradata or ANSI SQL
Description
Multiple positions available in Cary, North Carolina. Translate business requirements by business team into data and engineering specifications. Build scalable data sets based on engineering specifications from the available raw data. Work with engineering and business partners to define and implement the data engagement relationships required with partners. Understand and Identify server APIs that needs to be instrumented for data analytics and reporting and align the server events for execution in already established data pipelines. Analyze complex data sets, identify and formulate correlational rules between heterogenous sources for effective analytics and reporting. Process, clean and validate the integrity of data used for analysis. Develop Python and Shell Scripts for data ingestion from external data sources for business insights. Work hand in hand with the DevOps team and develop monitoring and alerting scripts on various data pipelines and jobs. Mentor a team of hardworking engineers. 40 hours/week.
Education & Experience
Additional Requirements'''


def form_prompt(job_description):
    prompt = PROMPT_HEADER
    prompt += '```' + job_description + '```'
    return prompt


def prompt_chatgpt(job_description):
    prompt = form_prompt(job_description)

    messages = [
        {"role": "system", "content" : "You’re a kind helpful assistant"}
    ]

    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    chat_response = response.choices[0].message.content

    return chat_response


def main():
    response = prompt_chatgpt(job_description)
    print(response)


if __name__ == '__main__':
    main()