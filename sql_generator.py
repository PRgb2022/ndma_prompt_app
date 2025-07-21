import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def prompt_to_sql(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can also use "gpt-3.5-turbo" for lower cost
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts natural language questions into SQL queries for a table named 'alerts'. The table has columns: id, state_name, area_description, event_type, severity, effectiveTime."},
                {"role": "user", "content": f"Convert this prompt to a SQL query: {prompt}"}
            ],
            temperature=0.2
        )

        sql_query = response['choices'][0]['message']['content'].strip()
        return sql_query, "Generated from natural language"

    except Exception as e:
        return None, f"Error from OpenAI API: {str(e)}"

def get_suggestions(prompt):
    return [
        "Recent flood alerts in Assam",
        "Which state has most red alerts?",
        "Top districts with orange alerts",
        "List all alerts from yesterday",
        "Count alerts for each state"
    ]
