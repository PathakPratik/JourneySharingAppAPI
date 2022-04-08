import bcrypt
from flask import request,jsonify,Blueprint
from Models.Users import Users
from services.UserModule import validate_register_form, validate_email, validate_password, \
                                password_match_confrimation, add_user_to_db, send_confirmation_account_email
from setup import db

app_register = Blueprint('app_register',__name__)

@app_register.route("/register", methods=["POST"])
def register():

    response = {}

    try:

        username_ = request.form['username']
        password_ = request.form['password']
        gender_ = request.form['gender']
        email_ = request.form['email']
        confirmpassword_ = request.form['confirmpassword']

        message, form_is_correct = validate_register_form(username_, password_, gender_, email_, confirmpassword_)
        if not form_is_correct:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
        
        message, password_is_correct = validate_password(password_)
        if not password_is_correct:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)

        message, email_is_correct = validate_email(email_)
        if not email_is_correct:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
        
        message, password_confirm_matches = password_match_confrimation(password_, confirmpassword_)
        if not password_confirm_matches:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
    
        hashed_password = bcrypt.hashpw(password_.encode('utf-8'), bcrypt.gensalt())
        registered_user = Users(username_, email_, gender_, hashed_password, \
                                admin=False, confirmed=False, confirmed_on=None,\
                                current_rating=0, rating_count=0)

        message, status = add_user_to_db(registered_user, db)
        response['message'] = message
        response['status'] = status
        if status == 400:
            return jsonify(response)

        message, status = send_confirmation_account_email(email_)

        return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - Provide an username and Password in JSON format in the request body'
        response["status"] = 400
        return jsonify(response)