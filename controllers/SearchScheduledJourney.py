from flask import request,jsonify,Blueprint
from services.JourenyUtility import validate_search_jorney_form, find_matching_journey, make_json_object
from json import dumps
from Decorator import login_required



app_search_scheduled_journey = Blueprint('app_search_scheduled_journey',__name__)

@app_search_scheduled_journey.route("/search_journey", methods=["POST"])
@login_required
def search_journey():

    response = {}

    try:
        source_longitude = request.form['source_longitude']
        source_latitude = request.form['source_latitude']
        destination_longitude = request.form['destination_longitude']
        destination_latitude = request.form['destination_latitude']
        weekday = request.form['weekday']
        hour = request.form['hour']
        gender_preference =  request.form['gender_preference']
        required_rating = request.form['required_rating']


        message, form_is_correct = validate_search_jorney_form(
                                                                source_longitude,
                                                                source_latitude, 
                                                                destination_longitude,
                                                                destination_latitude, 
                                                                weekday,
                                                                hour,
                                                                )
                                                                
        if not form_is_correct:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
        
        message, scheduled_journey = find_matching_journey(  source_longitude,
                                                    source_latitude, 
                                                    destination_longitude,
                                                    destination_latitude, 
                                                    weekday,
                                                    hour,
                                                    gender_preference,
                                                    required_rating)

        response['message'] = message
        response['journeys'] = make_json_object(scheduled_journey)
        return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - Provide the journey information in a correct format'
        response["status"] = 400
        return jsonify(response)




