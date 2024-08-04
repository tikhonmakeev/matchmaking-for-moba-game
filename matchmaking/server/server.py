import csv
import json
import logging
import os

from flask import Flask, request, jsonify

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

    file_path = os.path.join(app.root_path, 'secret_tests', test_name, f"{epoch}.json")

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
    if epoch == "last":
        return jsonify({"Nostradamus": "No... no... no..."}), 400

    file_path = os.path.join(app.root_path, 'secret_tests', test_name, f"test.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            epoches = json.load(file)

    new_epoch = epoches.get(epoch)
    last_epoch = epoches.get("last")

    data = request.get_json()

    with open(os.path.join('/matchmaking/server/secret_tests/logs', 'result.csv'), 'a', newline='') as csvfile:
        result_writer = csv.writer(csvfile, delimiter=' ',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for match in data:
            for team in match.get("teams"):
                for user in team.get("users"):
                    result_writer.writerow(
                        [
                            test_name, epoch, match.get("match_id"), team.get("side"), user.get("id"),
                            user.get("role")
                        ]

                    )

    return jsonify({"new_epoch": new_epoch, "is_last_epoch": (last_epoch == new_epoch)}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
