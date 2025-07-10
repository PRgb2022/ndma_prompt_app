from flask import Flask, render_template, request, jsonify
import mysql.connector
from sql_generator import prompt_to_sql, get_suggestions

app = Flask(__name__)

# DB Config
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'Prajwal.sql@25',
    'database': 'ndma'  
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get('prompt')

    sql, summary = prompt_to_sql(prompt)

    # Debug print to terminal
    print("Prompt received:", prompt)
    print("SQL generated:", sql)

    if not sql:
        return jsonify({
            'result': "Sorry, I couldn't understand the prompt.",
            'sql': '',
            'suggestions': get_suggestions(prompt)
        })

    result_text = ""
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        if result:
            result_text = str(result[0][0]) if len(result[0]) == 1 else str(result[0])
        else:
            result_text = "No results found."

    except Exception as e:
        result_text = f"Error running query: {e}"
        sql = ""

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

    return jsonify({
        'result': result_text,
        'sql': sql,
        'suggestions': get_suggestions(prompt)
    })

if __name__ == '__main__':
    app.run(debug=True)
