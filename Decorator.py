from functools import wraps
from flask import jsonify
from flask import session

def login_required(f):
    @wraps(f)
    def decorated_function():
        response = {}
        if 'id' not in session:
            response["message"] = 'Session id not found'
            response["status"] = 400
            return jsonify(response)
        return f()
    return decorated_function