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
    'database': 'ndma_prompt'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get('prompt')
    sql, result_text = prompt_to_sql(prompt)

    if not sql:
        return jsonify({
            'result': result_text,
            'sql': '',
            'suggestions': get_suggestions(prompt)
        })

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            result_text = str(result[0][0]) if len(result[0]) == 1 else str(result[0])
    except Exception as e:
        result_text = f"Error running query: {e}"
    finally:
        cursor.close()
        conn.close()

    return jsonify({
        'result': result_text,
        'sql': sql,
        'suggestions': get_suggestions(prompt)
    })

if __name__ == '__main__':
    app.run(debug=True)
