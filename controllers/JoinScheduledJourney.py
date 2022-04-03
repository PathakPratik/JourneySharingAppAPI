from flask import request,jsonify,Blueprint, session
from services.JourenyUtility import find_journey_by_id, update_journey_in_db, user_exist_in_journey, journey_has_quota
from json import dumps
from Decorator import login_required
from setup import db

app_join_scheduled_journey = Blueprint('app_join_scheduled_journey',__name__)

@app_join_scheduled_journey.route("/join_journey", methods=["POST"])
@login_required
def join_journey():

    response = {}

    try:
        user_id = session.get('id')
        journey_id = request.form['journey_id']
        
        message, scheduled_journey = find_journey_by_id(journey_id=journey_id)

        if scheduled_journey == None:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)

        message, user_exist = user_exist_in_journey(scheduled_journey, user_id)
        if user_exist == True:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
        
        message, can_join = journey_has_quota(scheduled_journey)
        if can_join == False:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)

        scheduled_journey.members = scheduled_journey.members + str(user_id) + '/'
        message, status = update_journey_in_db(scheduled_journey, db)
        response['message'] = message
        response['status'] = status
        return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - Provide the journey information in a correct format'
        response["status"] = 400
        return jsonify(response)




