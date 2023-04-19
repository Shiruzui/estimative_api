from flask import Flask, make_response, request, jsonify
from database import Database
from utils import process_request
from webargs.flaskparser import use_args, parser
from validations import request_schema

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
@use_args(request_schema, location="json")
def create_estimative(args):
    response_payload, error, status_code = process_request(args)
    if error:
        return jsonify(request_schema.error_messages), status_code
    return jsonify(response_payload), status_code


@app.route('/estimative/<calc_uuid>', methods=['PUT'])
@use_args(request_schema, location="json")
def update_estimative(args, calc_uuid):
    response_payload, error, status_code = process_request(
        args, calc_uuid=calc_uuid, is_update=True)
    if error:
        return jsonify(error), status_code
    return jsonify(response_payload), status_code


@app.errorhandler(422)
def handle_validation_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return jsonify(error=messages), 422


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
