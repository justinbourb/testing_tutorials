from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """
    400: The request could not be understood by the server due to malformed syntax.
    The client SHOULD NOT repeat the request without modifications.
    Reserve a 400 for when the request is missing required fields, an incorrect data type was provided, etc.
    """
    return error_response(400, message)
