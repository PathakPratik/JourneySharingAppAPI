from setup import db
from flask import jsonify, Blueprint, session
from services.UserModule import find_user_by_id
from services.Decorator import login_required

user_info = Blueprint('app_ratings',__name__)
ratings_Currently=0

@user_info.route("/user-info",methods=["GET"])
@login_required
def userInfo():

    response = {}
    message, user = find_user_by_id(session.get('id'))

    if user is None:
        response['message']=message
        response['status']=400
        return jsonify(response)

    response['username'] = user.username
    response['rating'] = user.current_rating
  
    return jsonify(response)


