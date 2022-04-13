from flask import request, jsonify, Blueprint, session
from services.UserModule import validate_login_form, check_password, find_user_by_email, check_email_confirmation
from services.Decorator import email_confirmed
import uuid

app_login = Blueprint('app_login',__name__)

@app_login.route("/login",methods=["POST"])
#@email_confirmed
def login():

    response = {}

    try:
        email_ = request.form['email']
        password_ = request.form['password']

        message, form_is_correct = validate_login_form(password_, email_)
        if not form_is_correct:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
        
        message, email_confirmed = check_email_confirmation(email=email_)
        if not email_confirmed:
            response["message"] = message
            response["status"] = 400
            return jsonify(response)
        
        message, user = find_user_by_email(email_)
        if(user == None):
            response["message"] = message
            response["status"] = 400
            return jsonify(response)
        
        message, password_is_correct = check_password(user, password_)
        if not password_is_correct:
            response["message"] = message
            response["status"] = 400
            return jsonify(response)
        
        session['id'] = user.id
        session.modified = True

        response["message"] = 'User logged in successfully'
        response["status"] = 200
        return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - User could not log in'
        response["status"] = 400
        return jsonify(response)

