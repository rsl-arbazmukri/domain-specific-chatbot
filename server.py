from flask import Flask, request
import json
from main import Main

app = Flask(__name__)


def extract_response(json_str: str):
    """Extracting user question and id from the request."""
    question = ""
    userId = ""
    json_from_response = json.loads(json_str)
    if "question" in json_from_response:
        question = json_from_response["question"]
    if "userId" in json_from_response:
        userId = json_from_response["userId"]
    return question, userId


@app.route('/test', methods=['GET'])
def test():
    return "Server running at: http://localhost:5000/"


@app.route('/chat', methods=['POST'])
def chat():
    question, userId = extract_response(json.dumps(request.get_json()))
    return Main().start_chat(question, userId)


if __name__ == '__main__':
    app.run()
