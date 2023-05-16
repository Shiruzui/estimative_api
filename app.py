import os
from flask import Flask, jsonify
from webargs.flaskparser import use_args
import logging
from exceptions.color_value_error import ColorValueError
from exceptions.task_value_error import TaskValueError
from my_requests.post_request import process_post_request
from validations.post_request_validations import post_request_schema

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/estimative', methods=['POST'])
@use_args(post_request_schema, location="json")
def create_estimative(args):
    response_payload, error, status_code = process_post_request(args)
    if error:
        return jsonify(post_request_schema.error_messages), status_code
    return jsonify(response_payload), status_code


@app.errorhandler(422)
def handle_validation_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    return jsonify(error=messages), 422


@app.errorhandler(TaskValueError)
def handle_task_value_error(err):
    return jsonify(error=str(err.description)), err.code


@app.errorhandler(ColorValueError)
def handle_color_value_error(err):
    return jsonify(error=err.description), err.code


if __name__ == '__main__':
    app_port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=app_port, debug=True)
