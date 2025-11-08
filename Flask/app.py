from flask import Flask, request, render_template, jsonify
from datetime import datetime
from dotenv import load_dotenv
import os
import pymongo
import json
import hashlib

load_dotenv()

# DB connection
mongo_uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(mongo_uri)
db = client.test
collection = db['flask']
todo_collection = db['todo']

app = Flask(__name__)
@app.route("/")
def hello_world():
    day_of_week = datetime.today().strftime('%A')
    return render_template("index.html", day_of_week=day_of_week)

@app.route("/submit", methods=['POST'])
def submit():
    print('taking input from user')
    form_data = dict(request.form)
    collection.insert_one(form_data)

    return 'Data submitted successfully'

@app.route("/view")
def view():
    data = list(collection.find())
    for i in data:
        del i["_id"]

    return data

@app.route('/todo')
def todoRoute():
    return render_template('form.html')

@app.route('/submittodoitem', methods=['POST'])
def todo():
    random_bytes = os.urandom(16)  # 128-bit random value
    hash_value = hashlib.sha256(random_bytes).hexdigest()
    todo_data = dict(request.form)
    todo_data['hash'] = hash_value
    todo_collection.insert_one(todo_data)
    return f'Todo saved successfully. id: {hash_value}'

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

@app.route('/api', methods=['GET'])
def get_data():
    """Read data from JSON file and return it as a response."""
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format in data file"}), 500

@app.route("/api/<name>")
def dynamic_route(name):
    result = "<p>Hello " +name+ "</p>"
    return result

@app.route("/query-params")
def query_param():
    name = request.values.get("user")
    result = "<p>Hello " +name+ "</p>"
    return result



if __name__ == '__main__':
    app.run(debug=True)
