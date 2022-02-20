import bcrypt
from setup import db
from flask import request,jsonify,Blueprint
from Models.Users import Users
from marshmallow import Schema
from random import randint
from services.UserModule import valiadte_register_form, validate_email, validate_password , password_match_confrimation, add_user_to_db, send_confirmation_account_email

#Create User Schema
class UserSchema(Schema):
    class Meta:
        fields = ("id","username","email","gender")
        # exclude = ("password")

#Init User Schemas
user_schema = UserSchema() #return 1 user
users_schema = UserSchema(many=True) #return many users

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

        message, form_is_correct = valiadte_register_form(username_, password_, gender_, email_, confirmpassword_)
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
        registered_user = Users(username_, email_, gender_, hashed_password, admin=False, confirmed=False, confirmed_on=None)

        message, status = add_user_to_db(registered_user, db)
        response['message'] = message
        response['status'] = status

        send_confirmation_account_email(email_)

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
    results =db.Model.dump(all_users)
    return jsonify(all_users), 200


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
    """Dev method to generate a number of random users

    Args: 
        numusers: Reads the number of users to be generated
         from request.form[]
    Returns:
        json: Return a json stream of the random users generated
    """
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



