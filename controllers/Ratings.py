from setup import db
from flask import request, jsonify, Blueprint
from services.UserModule import update_user_in_db, find_user_by_email

app_ratings = Blueprint('app_ratings',__name__)

@app_ratings.route("/update_rating",methods=["POST"])
def update_rating():

    response = {}

    email_ = request.form['email']
    new_ratings = request.form['rating']
    message, user = find_user_by_email(email_)

    user.travel_count += 1 
    user.current_rating = (user.current_rating + int(new_ratings)) / user.travel_count

    message, status = update_user_in_db(user, db)

    response['status'] = status
    response['message']= message

    return jsonify(response)
        


