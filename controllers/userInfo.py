from flask import jsonify, Blueprint, session
from services.UserModule import find_user_by_id
from services.Decorator import login_required

app_user_info = Blueprint('app_user_info',__name__)


@app_user_info.route("/user-info",methods=["GET"])
@login_required
def userInfo():

    response = {}
    message, user = find_user_by_id(session.get('id'))

    response['userid'] = user.id
    response['username'] = user.username
    response['rating'] = user.current_rating
  
    return jsonify(response)


