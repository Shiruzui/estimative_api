import uuid
from flask import Flask, make_response, request, jsonify
from database import Database
from messages import INDEX_MESSAGE
from utils import process_request

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def default():
    return jsonify({"message": INDEX_MESSAGE})


@app.route('/estimative', methods=['GET'])
def get_all_estimatives():
    db = Database("db/results.json")
    estimatives = [value for key, value in db.items()]
    return (
        jsonify(estimatives)
        if estimatives
        else (jsonify({"message": "Estimativas não encontrada."}), 400)
    )


@app.route('/estimative/<calc_uuid>', methods=['GET'])
def get_estimative(calc_uuid):
    db = Database("db/results.json")
    estimative = db.get(calc_uuid)
    return (
        jsonify(estimative)
        if estimative
        else make_response(
            jsonify({"message": "Estimativa não encontrada"}), 404
        )
    )


@app.route('/estimative', methods=['POST'])
def calculate():
    data = request.get_json()
    response_payload, error_message, status_code = process_request(data)

    if error_message:
        return jsonify(error_message), status_code

    return jsonify(response_payload), 201


@app.route('/estimative/<calc_uuid>', methods=['PUT'])
def update_estimative(calc_uuid):
    data = request.get_json()
    db = Database("db/results.json")
    if not db.get(calc_uuid):
        return make_response(jsonify({"message": "Estimativa não encontrada"}), 404)

    response_payload, error_message, status_code = process_request(
        data, calc_uuid, is_update=True)

    if error_message:
        return jsonify(error_message), status_code

    return jsonify(response_payload), 200


if __name__ == '__main__':
    app.run(debug=True)
