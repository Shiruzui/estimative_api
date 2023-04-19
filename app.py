import os
from flask import Flask, make_response, jsonify
from db.database import Database
from webargs.flaskparser import use_args
import logging

from my_requests.post_request import process_post_request
from validations.post_request_validations import post_request_schema
from validations.put_request_validations import put_request_schema

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def default():
    return jsonify({"message": 'Ainda não há nada aqui.'})


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
@use_args(post_request_schema, location="json")
def create_estimative(args):
    try:
        response_payload, error, status_code = process_post_request(args)
        if error:
            return jsonify(post_request_schema.error_messages), status_code
        return jsonify(response_payload), status_code
    except Exception as e:
        logging.exception("An error occurred while processing the request.")
        return str(e), 500


@app.route('/estimative/<calc_uuid>', methods=['PUT'])
@use_args(put_request_schema, location="json")
def update_estimative(args, calc_uuid):
    response_payload, error, status_code = process_post_request(
        args, calc_uuid=calc_uuid, is_update=True)
    if error:
        return jsonify(error), status_code
    return jsonify(response_payload), status_code


@app.route('/estimative/<calc_uuid>/delete', methods=['DELETE'])
def delete_estimative(calc_uuid):
    db = Database("db/results.json")
    existing_data = db.get(calc_uuid)

    if not existing_data:
        return jsonify({"message": "Estimativa não encontrada"}), 404

    db.delete(calc_uuid)
    return jsonify(existing_data), 200


@app.errorhandler(422)
def handle_validation_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return jsonify(error=messages), 422


if __name__ == '__main__':
    app_port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=app_port, debug=True)
