from flask import Flask, render_template, request, jsonify
import mysql.connector
import openai
import os
from dotenv import load_dotenv
from sql_generator import prompt_to_sql, get_suggestions

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Prajwal.sql@25",  # update if your MySQL has a password
        database="ndma"
    )

def generate_sql_with_openai(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Convert the user's natural language prompt into a SQL query for a MySQL database containing an 'alerts' table with columns like state_name, area_description, event_type, severity, effectiveTime, etc."},
                {"role": "user", "content": prompt}
            ]
        )
        sql = response.choices[0].message.content.strip()
        return sql
    except Exception as e:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    sql_query, description = prompt_to_sql(prompt)

    if not sql_query:
        # Try OpenAI fallback if hardcoded logic fails
        sql_query = generate_sql_with_openai(prompt)
        description = "Generated using OpenAI" if sql_query else None

    if not sql_query:
        return jsonify({'error': description or 'Unable to generate SQL for the given prompt'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        conn.close()

        suggestions = get_suggestions(prompt)

        return jsonify({
            'results': results,
            'columns': column_names,
            'sql': sql_query,
            'description': description,
            'suggestions': suggestions
        })

    except Exception as e:
        return jsonify({'error': f'Error running query: {str(e)}'}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

