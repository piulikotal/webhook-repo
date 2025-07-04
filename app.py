from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)

# MongoDB connection
client = MongoClient("mongodb+srv://Piuli:MbrGm8H1aJNrOB7J@cluster0.xof1kzt.mongodb.net/?retryWrites=true&w=majority")
db = client["webhook_db"]
collection = db["events"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events', methods=['GET'])
def get_events():
    events = list(
        collection.find({}, {'_id': 0})
        .sort("timestamp", -1)
        .limit(10)
    )
    return jsonify(events)

@app.route('/test-print')
def test_print():
    events = list(collection.find({}, {'_id': 0}))
    print("Events from DB:", events)
    return jsonify(events)


@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    event = request.headers.get('X-GitHub-Event')
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    doc = {
        "request_id": "req-" + str(uuid.uuid4()),
        "author": "",
        "action": "",
        "from_branch": "",
        "to_branch": "",
        "timestamp": timestamp
    }

    if event == "push":
        doc["author"] = data.get("pusher", {}).get("name", "Unknown")
        doc["action"] = "push"
        doc["to_branch"] = data.get("ref", "").split("/")[-1]

    elif event == "pull_request":
        action = data.get("action")
        author = data["pull_request"]["user"]["login"]
        from_branch = data["pull_request"]["head"]["ref"]
        to_branch = data["pull_request"]["base"]["ref"]

        doc["author"] = author
        doc["from_branch"] = from_branch
        doc["to_branch"] = to_branch

        if action == "opened":
            doc["action"] = "pull_request"
        elif action == "closed" and data["pull_request"].get("merged", False):
            doc["action"] = "merge"
        else:
            return jsonify({"status": "ignored", "reason": "Unsupported pull_request action"}), 200

    else:
        return jsonify({"status": "ignored", "reason": "Unsupported event type"}), 200

    collection.insert_one(doc)
    return jsonify({"status": "received", "doc": doc}), 200

# Test route to insert test data
@app.route('/test-insert')
def test_insert():
    test_doc = {
        "request_id": "req-" + str(uuid.uuid4()),
        "author": "Sohom",
        "action": "push",
        "from_branch": "",
        "to_branch": "dev",
        "timestamp": "2025-07-03T11:00:00Z"
    }
    collection.insert_one(test_doc)
    return "Inserted test data!"

# Optional: manual cleanup route
@app.route('/cleanup')
def cleanup():
    delete_result = collection.delete_many({
        "$or": [
            {"action": {"$exists": False}},
            {"author": {"$exists": False}},
            {"to_branch": {"$exists": False}},
            {"timestamp": {"$exists": False}},
            {"action": ""},
            {"author": ""},
            {"to_branch": ""}
        ]
    })
    return f"Deleted {delete_result.deleted_count} invalid documents."

if __name__ == '__main__':
    app.run(debug=True, port=5000)
