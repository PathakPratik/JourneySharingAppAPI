import re
import bcrypt
from db import db
from flask import Flask,request,jsonify,Blueprint
from flask_sqlalchemy import SQLAlchemy
from Models.Users import Users
import re
from sqlalchemy.exc import IntegrityError

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 chracters"
    elif re.search('[0-9]',password) is None:
        return "Password must contain at least one digit"
    elif re.search('[A-Z]',password) is None: 
        return "Password must contain at least one capital letter"
    else:
        return ""

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

        #username_ = request.json.get('username', None)
        #password_ = request.json.get('password', None)
        #email_ = request.json.get('email', None)

        if not username_:
            response['message'] = 'Missing username'
            response['status'] = 400
            return jsonify(response)

        if not password_:
            response['message'] = 'Missing password'
            response['status'] = 400
            return jsonify(response)

        elif validate_password(password_) != "":
            response['message'] = validate_password(password_)
            response['status'] = 400
            return jsonify(response)

        elif password_ != confirmpassword_:
            response['message'] = 'Password confirmation incorrect'
            response['status'] = 400
            return jsonify(response)
        
        if not email_:
            response['message'] = 'Missing email'
            response['status'] = 400
            return jsonify(response)
    
        hashed_password = bcrypt.hashpw(password_.encode('utf-8'), bcrypt.gensalt())

        registered_user = Users(username_, email_, gender_, hashed_password)
        db.session.add(registered_user)
        db.session.commit()
        response["message"] = 'User registered successfully'
        response["status"] = 200
        return jsonify(response)
        
    except IntegrityError:
        #the rollback func reverts the changes made to the db ( so if an error happens after we commited changes they will be reverted )
        db.session.rollback()
        response["message"] = 'User already exists'
        response["status"] = 409
        return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - Provide an username and Password in JSON format in the request body'
        response["status"] = 400
        return jsonify(response)