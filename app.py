from flask import Flask, render_template, request, jsonify
import mysql.connector
from sql_generator import prompt_to_sql, get_suggestions

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # update this if your MySQL has a password
        database="ndma"  # make sure this is your actual DB name
    )

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
    app.run(debug=True)
