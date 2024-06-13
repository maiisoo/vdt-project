import requests
import json
import config
from extract_sql import *

OPENROUTER_API_KEY = config.API_KEY


def generate_prompt_sql(input, context):
    return f"""You are a powerful text-to-SQL model. Your job is to answer questions about a database. You are given 
    a question and context regarding one or more tables. 

  You must output only the SQL query that answers the question.
  
  ### Input:
  {input}
  
  ### Context:
  {context}
  """


def gen_sql_query(question, context):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        },
        data=json.dumps({
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "user", "content": generate_prompt_sql(question, context)}
            ]
        })
    )

    response_json = json.loads(response.text)  # Assuming response is the response object
    raw_query = response_json["choices"][0]["message"]["content"]
    query = extract_sql(raw_query)

    print(query)

    return query



