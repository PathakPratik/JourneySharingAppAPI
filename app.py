import os
from time import sleep
from flask import Flask,request,jsonify
from constants import FLASK_HOSTNAME, FLASK_PORT, REDIS_HOST, REDIS_PORT
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import redis
from models import User2
from db import db
import bcrypt


app = Flask(__name__)
sleep(30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', 'Yahya1377!'),
    os.getenv('DB_HOST', 'db:3306'),
    os.getenv('DB_NAME', 'flask')
) #'mysql+pymysql://root:Yahya1377!@db:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

redisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

@app.route("/login",methods=["POST"])
def login():

    response = {}

    try:
        #username_ = request.form['username']
        #password_ = request.form['password']

        username_ = request.json.get('username', None)
        password_ = request.json.get('password', None)

        if not username_:
            response["message"] = 'Missing username'
            response["status"] = 400
            return jsonify(response)

        if not password_:
            response["message"] = 'Missing password'
            response["status"] = 400
            return jsonify(response)

        user = User2.query.filter_by(username=username_).first()

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
            

@app.route("/register", methods=["POST"])
def register():

    response = {}

    try:
        print("A")
        #username_ = request.form['username']
        #password_ = request.form['password']
        #password_ = request.form['email']

        username_ = request.json.get('username', None)
        password_ = request.json.get('password', None)
        email_ = request.json.get('email', None)

        if not username_:
            response['message'] = 'Missing username'
            response['status'] = 400
            return jsonify(response)

        if not password_:
            response['message'] = 'Missing password'
            response['status'] = 400
            return jsonify(response)

        if not email_:
            response['message'] = 'Missing email_'
            response['status'] = 400
            return jsonify(response)
    
        hashed_password = bcrypt.hashpw(password_.encode('utf-8'), bcrypt.gensalt())

        users = User2.query.all()
        for user in users:
            print(user.username)

        registered_user = User2(username_, email_, hashed_password)
        db.session.add(registered_user)
        db.session.commit()
        response["message"] = 'User registered successfully'
        response["status"] = 200
        db.session.flush()
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

# Add MatchUsers Controller
from controllers.MatchUsers import app_match_users
app.register_blueprint(app_match_users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)