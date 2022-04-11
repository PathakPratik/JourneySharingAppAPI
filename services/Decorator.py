from functools import wraps
from flask import jsonify
from flask import session
from services.UserModule import find_user_by_email

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


def email_confirmed(f):
    @wraps(f)
    def decorated_function():
        response = {}
        message, user = find_user_by_email(session.get('email'))
        if user.confirmed == False:
            response["message"] = 'User email has not been confirmed'
            response["status"] = 400
            return jsonify(response)
        return f()
    return decorated_function