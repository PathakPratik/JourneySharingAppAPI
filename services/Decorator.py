from functools import wraps
from flask import jsonify
from flask import session
from setup import test_mode

def login_required(f):
    @wraps(f)
    def decorated_function():
        response = {}
        #if 'id' not in session:
        if not session.get('id'):
            response["message"] = 'Session id not found'
            response["status"] = 400
            return jsonify(response)
        return f()
    return decorated_function

def test_mode_login_required(f):
    @wraps(f)
    def decorated_function():
        response = {}
        if not test_mode:
            #if 'id' not in session:
            if not session.get('id'):
                response["message"] = 'Session id not found'
                response["status"] = 400
                return jsonify(response)
        return f()
    return decorated_function