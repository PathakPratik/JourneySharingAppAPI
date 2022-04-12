from sqlalchemy.exc import IntegrityError
from Models.ScheduledJourney import ScheduledJourney
from math import sin, cos, sqrt, atan2, radians



def add_journey_to_db(scheduled_journey, db):
    try:
        db.session.add(scheduled_journey)
        db.session.commit()
        return 'Journey added successfully', 200
    
    except IntegrityError:
        db.session.rollback()
        return 'Journey already exists', 400


def find_user_owned_journey(user_id):

    found_journies = ScheduledJourney.query.filter_by(creatorId=user_id).all()

    if found_journies == []:
        return 'Journey not found', None
    return 'Journey found', found_journies


def make_json_object(query_result):
    json_objects = {}
    for i in range(len(query_result)):
        json_object = {}
        json_object['creatorId'] = query_result[i].creatorId
        json_object['TripStartLocation'] = query_result[i].TripStartLocation
        json_object['TripStopLocation'] = query_result[i].TripStopLocation
        json_object['ScheduleTime'] = query_result[i].ScheduleTime
        json_object['GenderPreference'] = query_result[i].GenderPreference
        json_object['RequiredRating'] = query_result[i].RequiredRating
        json_object['ModeOfTransport'] = query_result[i].ModeOfTransport
        journey_index = 'journey' + str(i+1)
        json_objects[journey_index] = json_object

    return json_objects
