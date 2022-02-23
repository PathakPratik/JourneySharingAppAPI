import bcrypt
from flask import request, jsonify, Blueprint, session
from services.UserModule import valiadte_login_form, check_password, find_user_by_email
from Decorator import login_required
import uuid

app_login = Blueprint('app_login',__name__)

@app_login.route("/login",methods=["POST"])
def login():

    response = {}

    try:
        email_ = request.form['email']
        password_ = request.form['password']

        message, form_is_correct = valiadte_login_form(password_, email_)
        if not form_is_correct:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
        
        message, user = find_user_by_email(email_)
        if(user == None):
            response["message"] = 'User not found'
            response["status"] = 400
            return jsonify(response)
        
        message, password_is_correct = check_password(user, password_)
        if not password_is_correct:
            response["message"] = 'Wrong password'
            response["status"] = 400
            return jsonify(response)
        
        session['id'] = uuid.uuid4()

        response["message"] = 'User logged in successfully'
        response["status"] = 200
        response['session'] = session
        return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - Provide an username and Password in JSON format in the request body'
        response["status"] = 400
        return jsonify(response)

@app_login.route("/logout")
@login_required
def logout():
    response = {}
    response["message"] = 'User logged out successfully'
    response["status"] = 200
    print(session['id'])
    session.pop('id', None)
    return jsonify(response)

@app_login.route("/get/")
def show_session():
     return str(session.get('id', 'not set'))