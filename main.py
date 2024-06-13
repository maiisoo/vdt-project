from flask import Flask, request, jsonify
from flask_cors import CORS

from metadata.get_schema import get_schema
from nl2sql.exec_query import execute_query
from nl2sql.gen_query import gen_sql_query

app = Flask(__name__)
CORS(app)


@app.route('/gen_query', methods=['POST'])
def generate_query():
    data = request.get_json()
    schema = get_schema("./metadata/metadata.txt")
    question = data.get('question')

    query = gen_sql_query(question, schema)

    if not query:
        return jsonify({"error": "No query generated"}), 400

    print(query)

    return jsonify({"query": query}), 200


@app.route('/exec_query', methods=['POST'])
def exec_query():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        result = execute_query(query)
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
