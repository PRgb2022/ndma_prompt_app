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
    'database': 'ndma'  # Make sure this matches your actual database name
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    prompt = data.get('prompt')
    sql, summary = prompt_to_sql(prompt)

    if not sql:
        return jsonify({
            'result': summary or "Sorry, I didn't understand that.",
            'sql': '',
            'suggestions': get_suggestions(prompt),
            'chart': None
        })

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        result_text = str(result)

        # Prepare chart data if the result is grouped (like alert counts)
        result_data = []
        labels = []

        if result and isinstance(result[0], tuple) and len(result[0]) == 2:
            for row in result:
                labels.append(str(row[0]))
                result_data.append(row[1])
            result_text = "\n".join(f"{row[0]}: {row[1]}" for row in result)

        return jsonify({
            'result': result_text,
            'sql': sql,
            'suggestions': get_suggestions(prompt),
            'chart': {
                'data': result_data,
                'labels': labels,
                'title': summary
            } if result_data and labels else None
        })

    except Exception as e:
        return jsonify({
            'result': f"Error running query: {e}",
            'sql': sql,
            'suggestions': get_suggestions(prompt),
            'chart': None
        })
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
