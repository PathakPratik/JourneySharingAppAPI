from flask import request,jsonify,Blueprint, session
from services.JourenyUtility import find_user_owned_journey, find_user_joined_journey, make_json_object
from json import dumps
from services.Decorator import login_required
from setup import db

app_get_scheduled_journey = Blueprint('app_get_scheduled_journey',__name__)

@app_get_scheduled_journey.route("/get_journey", methods=["GET"])
@login_required
def join_journey():

    response = {}

    try:
        user_id = session.get('id')
       
        message, owned_journey = find_user_owned_journey(user_id)
        message, joined_journey = find_user_joined_journey(user_id)

        if joined_journey == None and owned_journey == None:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)

        elif joined_journey == None:
            response['creator'] = make_json_object(owned_journey)
            response['status'] = 200
            return jsonify(response)
        
        elif owned_journey == None:
            response['member'] = make_json_object(joined_journey)
            response['status'] = 200
            return jsonify(response)
        
        response['member'] = make_json_object(joined_journey)
        response['creator'] = make_json_object(owned_journey)
        response['status'] = 200
        return jsonify(response)


    except AttributeError:
        response["message"] = 'Bad request - Provide the journey information in a correct format'
        response["status"] = 400
        return jsonify(response)




