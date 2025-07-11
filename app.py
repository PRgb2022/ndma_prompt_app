from flask import Flask, render_template, request, jsonify
import mysql.connector
from sql_generator import prompt_to_sql, get_suggestions

app = Flask(__name__)

# Database config
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

    if not sql:
        return jsonify({
            'result': [],
            'sql': '',
            'suggestions': get_suggestions(prompt),
            'chart': None
        })

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns, row)) for row in result]

        chart_labels, chart_data = [], []
        if rows and len(rows[0]) == 2:
            chart_labels = [str(r[columns[0]]) for r in rows]
            chart_data = [r[columns[1]] for r in rows]

    except Exception as e:
        return jsonify({
            'result': [],
            'sql': sql,
            'suggestions': get_suggestions(prompt),
            'chart': None,
            'error': str(e)
        })
    finally:
        cursor.close()
        conn.close()

    return jsonify({
        'result': rows,
        'sql': sql,
        'suggestions': get_suggestions(prompt),
        'chart': {
            'labels': chart_labels,
            'data': chart_data,
            'title': summary
        } if chart_data else None
    })

if __name__ == '__main__':
    app.run(debug=True)
