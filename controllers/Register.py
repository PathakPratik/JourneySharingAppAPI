import re
import bcrypt
from db import db
from flask import Flask,request,jsonify,Blueprint
from flask_sqlalchemy import SQLAlchemy
from Models.Users import Users
import re
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema
from random import randint

#Create User Schema
class UserSchema(Schema):
    class Meta:
        fields = ("id","username","email","gender")
        # exclude = ("password")

#Init User Schemas
user_schema = UserSchema() #return 1 user
users_schema = UserSchema(many=True) #return many users

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 chracters"
    elif re.search('[0-9]',password) is None:
        return "Password must contain at least one digit"
    elif re.search('[A-Z]',password) is None: 
        return "Password must contain at least one capital letter"
    else:
        return ""

def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 
    if re.search(regex,email) is None:   
        return "Invalid email address"
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

        elif validate_email(email_) != "":
            response['message'] = validate_email(email_)
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

#testing use case to get all users in database
@app_register.route("/show-all", methods=["GET"])
def get_all_users():
    """Dev method to return all users currently int the db

    Returns:
        json: Returns a json stream containing all the current users
    """
    all_users = Users.query.all()
    results =users_schema.dump(all_users)
    return jsonify(results), 200


@app_register.route("/generate-random-user", methods=["POST"])
def generate_random_user():
    """Dev method to generate a single random user

    Returns:
        json: Details of the random user generated in json format.
    """
    # create random int
    random_int = randint(1,9000000000)

    #use random int to generate random fields for the user
    username = "RandomUser" + str(random_int)
    email =  "RandomUser"+str(random_int) + "@gmail.com"
    password = "RandomPassword"+str(random_int)
    gender = "Male" if random_int%2==0 else "Female"

    #create random user and commit to db
    new_user = Users(username,email,gender,password)
    db.session.add(new_user)
    db.session.commit()

    #return the added user 
    randUser = user_schema.dump(new_user)
    return jsonify(randUser), 200

@app_register.route("/generate-n-random-users", methods=["POST"])
def generate_n_random_users():
    numusers_ = int(request.form['numusers'])
    generated_users = []
    for i in range(numusers_):
        # create random int
        random_int = randint(1,9000000000)

        #use random int to generate random fields for the user
        username = "RandomUser" + str(random_int)
        email =  "RandomUser"+str(random_int) + "@gmail.com"
        password = "RandomPassword"+str(random_int)
        gender = "Male" if random_int%2==0 else "Female"

        #create random user and commit to db
        new_user = Users(username,email,gender,password)
        db.session.add(new_user)
        db.session.commit()

        #append to generated users
        generated_users.append(new_user)
    
    newusers = users_schema.dump(generated_users)
    return jsonify(newusers), 200



