from flask import request,jsonify,Blueprint, session
from Models.ScheduledJourney import ScheduledJourney
from services.JourenyUtility import validate_create_jorney_form, add_journey_to_db, check_optional_fields
from setup import db
from services.Decorator import login_required


app_create_scheduled_journey = Blueprint('app_create_scheduled_journey',__name__)

@app_create_scheduled_journey.route("/create_journey", methods=["POST"])
@login_required
def create_journey():

    response = {}

    try:
        journey_name = request.form['journey_name']
        source_longitude = request.form['source_longitude']
        source_latitude = request.form['source_latitude']
        destination_longitude = request.form['destination_longitude']
        destination_latitude = request.form['destination_latitude']
        weekday = request.form['weekday']
        hour = request.form['hour']
        gender_preference =  request.form['gender_preference']
        required_rating = request.form['required_rating']
        quota = request.form['quota']

        message, form_is_correct = validate_create_jorney_form(
                                                                journey_name,
                                                                source_longitude,
                                                                source_latitude, 
                                                                destination_longitude,
                                                                destination_latitude, 
                                                                weekday,
                                                                hour,
                                                                )
                                                                
        gender_preference , required_rating, quota = check_optional_fields(
                                                                            gender_preference,
                                                                            required_rating,
                                                                            quota)
        if not form_is_correct:
            response['message'] = message
            response['status'] = 400
            return jsonify(response)
        
        scheduled_journey = ScheduledJourney(
                                            creator_id=session.get('id'),
                                            journey_name=journey_name,
                                             source_longitude=source_longitude,
                                             source_latitude=source_latitude,
                                             destination_longitude=destination_longitude,
                                             destination_latitude=destination_latitude,
                                             weekday=weekday,
                                             hour=hour,
                                             gender_preference=gender_preference,
                                             required_rating=required_rating,
                                             quota=quota
                                             )

        message, status = add_journey_to_db(scheduled_journey, db)
        response['message'] = message
        response['status'] = status
        return jsonify(response)

    except AttributeError:
        response["message"] = 'Bad request - Could not add a new journey'
        response["status"] = 400
        return jsonify(response)




