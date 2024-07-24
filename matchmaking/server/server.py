import logging
from flask import Flask, request, jsonify, current_app
import json
import os

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route('/ping', methods=['GET'])
def send():
    return "pong!"


@app.get('/matchmaking/users')
def get_waiting_users():
    test_name = request.args.get('test_name')
    epoch = request.args.get('epoch')

    if test_name is None or epoch is None:
        return jsonify({"error": "Missing parameters"}), 400

    file_path = os.path.join(current_app.root_path, "tests", test_name, f"{epoch}.json")

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return jsonify(data)
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/matchmaking/match', methods=['POST'])
def log_match():
    test_name = request.args.get('test_name')
    epoch = request.args.get('epoch')

    if test_name is None or epoch is None:
        return jsonify({"error": "Missing parameters"}), 400

    file_path = os.path.join(current_app.root_path, "tests", test_name, f"test.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            epoches = json.load(file)

    new_epoch = epoches.get(epoch)

    data = request.get_json()
    logger.info(data)
    return jsonify({"epoch": new_epoch, "test_name": test_name}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
