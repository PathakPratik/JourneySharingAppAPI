from setup import db
from flask import request, jsonify, Blueprint
from services.UserUtility import validate_rating_form, update_user_in_db, find_user_by_id
from services.Decorator import login_required

app_ratings = Blueprint('app_ratings',__name__)
ratings_Currently=0

@app_ratings.route("/update_rating",methods=["POST"])
@login_required
def update_rating():

    response = {}

    user_id = request.form['id']
    new_ratings = request.form['rating']

    message, form_is_ok = validate_rating_form(new_ratings, user_id)
    if form_is_ok == False:
        response['message']=message
        response['status']= 400
        return jsonify(response)

    message, user = find_user_by_id(user_id)

    if user is None:
        response['message']=message
        response['status']=400
        return jsonify(response)

    user.rating_count += 1 
    user.current_rating = (user.current_rating + int(new_ratings)) / (user.rating_count)
    

    message, status = update_user_in_db(user, db)

    response['status'] = status
    response['message']= message
  
    return jsonify(response)
        


