import bcrypt
from flask import Flask,request,jsonify,Blueprint
from Models.Users import Users


app_login = Blueprint('app_login',__name__)

@app_login.route("/login",methods=["POST"])
def login():

    response = {}

    try:
        email_ = request.form['email']
        password_ = request.form['password']

        #email_ = request.json.get('email', None)

        if not email_:
            response["message"] = 'Missing username'
            response["status"] = 400
            return jsonify(response)

        if not password_:
            response["message"] = 'Missing password'
            response["status"] = 400
            return jsonify(response)

        user = Users.query.filter_by(email=email_).first()

        if not user:
            response["message"] = 'Username not found'
            response["status"] = 401
            return jsonify(response)

        if bcrypt.checkpw(password_.encode('utf-8'), user.password.encode('utf-8')):
            response["message"] = 'User logged in successfully'
            response["status"] = 200
            return jsonify(response)
        else:
            response["message"] = 'Wrong password'
            response["status"] = 401
            return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - Provide an username and Password in JSON format in the request body'
        response["status"] = 400
        return jsonify(response)