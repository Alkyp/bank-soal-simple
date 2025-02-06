from flask import make_response
import json


def success(values, message):
    res = {
        'data': values,
        'message': message
    }
    return make_response(json.dumps(res)), 200


def badRequest(values, message):
    res = {
        'data': values,
        'message': message
    }
    return make_response(json.dumps(res)), 400
