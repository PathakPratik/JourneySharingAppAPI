from sqlalchemy.exc import IntegrityError
from Models.ScheduledJourney import ScheduledJourney
from math import sin, cos, sqrt, atan2, radians

def validate_create_jorney_form(
                                journey_name,
                                source_longitude,
                                source_latitude, 
                                destination_longitude,
                                destination_latitude, 
                                weekday,
                                hour
                                ):

    if not journey_name:
        return 'Missing journey name', False

    if not source_longitude:
        return 'Missing source longitude', False

    elif not source_latitude:
        return 'Missing source latitude', False
    
    elif not destination_longitude:
        return 'Missing destination longitude', False

    elif not destination_latitude:
        return 'Missing destination latitude', False
    
    elif not weekday:
        return 'Missing weekday', False
    
    elif not hour:
        return 'Missing hour', False

    return 'Form is correct', True

def validate_search_jorney_form(
                                journey_name,
                                source_longitude,
                                source_latitude, 
                                destination_longitude,
                                destination_latitude, 
                                weekday,
                                hour,
                                gender_preference,
                                required_rating
                                ):

    if not journey_name:
        return 'Missing journey name', False

    if not source_longitude:
        return 'Missing source longitude', False

    elif not source_latitude:
        return 'Missing source latitude', False
    
    elif not destination_longitude:
        return 'Missing destination longitude', False

    elif not destination_latitude:
        return 'Missing destination latitude', False
    
    elif not weekday:
        return 'Missing weekday', False
    
    elif not hour:
        return 'Missing hour', False
    
    elif not gender_preference:
        return 'Missing gender preference', False
    
    elif not required_rating:
        return 'Missing required rating', False

    return 'Form is correct', True


def validate_search_jorney_form(
                                source_longitude,
                                source_latitude, 
                                destination_longitude,
                                destination_latitude, 
                                weekday,
                                hour
                                ):


    if not source_longitude:
        return 'Missing source longitude', False

    elif not source_latitude:
        return 'Missing source latitude', False
    
    elif not destination_longitude:
        return 'Missing destination longitude', False

    elif not destination_latitude:
        return 'Missing destination latitude', False
    
    elif not weekday:
        return 'Missing weekday', False
    
    elif not hour:
        return 'Missing hour', False

    return 'Form is correct', True

def check_optional_fields(gender_preference, required_rating, quota):

    if not gender_preference:
        gender_preference = '*'

    if not required_rating:
        required_rating = '0'
    
    if not quota:
        quota = '5'
    
    return gender_preference , required_rating, quota

def add_journey_to_db(scheduled_journey, db):
    try:
        db.session.add(scheduled_journey)
        db.session.commit()
        return 'Journey added successfully', True
    
    except IntegrityError:
        db.session.rollback()
        return 'Journey already exists', False

def user_exist_in_journey(journey, user_id):
    if journey.members.find(str(user_id)) != -1:
        return 'User already in journey members', True
    return 'User can join the journey', False

def journey_has_quota(journey):
    print("journey.members.count('/')")
    if journey.members.count('/') < int(journey.quota):
        return 'User can join the journey', True
    return 'Journey has reached full quota', False

def update_journey_in_db(scheduled_journey, db):

    db.session.add(scheduled_journey)
    db.session.commit()
    return 'Journey info updated successfully', 200


def distance(lat1, long1, lat2, long2):

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(lat1))
    long1 = radians(float(long1))
    lat2 = radians(float(lat2))
    long2 = radians(float(long2))

    dlong = long2 - long1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return  distance

def check_src_distance_constraint(lat1, long1, lat2, long2):
    if distance(lat1, long1, lat2, long2) < 1:
        return True
    return False

def check_dst_distance_constraint(lat1, long1, lat2, long2):
    if distance(lat1, long1, lat2, long2) < 1:
        return True
    return False

def check_required_rating_constraint(required_rating, current_rating):
    if required_rating <= current_rating:
        return True
    return False

def check_constraints(src_lat1, src_long1, src_lat2, src_long2, dst_lat1, dst_long1, dst_lat2, dst_long2,required_rating, current_rating):
    if(check_src_distance_constraint(src_lat1, src_long1, src_lat2, src_long2) and \
        check_dst_distance_constraint(dst_lat1, dst_long1, dst_lat2, dst_long2) and \
        check_required_rating_constraint(required_rating, current_rating)):
        return True
    return False

def find_journey_by_id(journey_id):
    found_journey = ScheduledJourney.query.filter_by(id=journey_id).first()
    if found_journey is None:
        return 'Journey Not Found', None
    return 'Journey found', found_journey
    

def find_matching_journey(source_longitude,
                 source_latitude, 
                 destination_longitude,
                 destination_latitude, 
                 weekday,
                 hour,
                 gender_preference,
                 required_rating):

    found_journies = ScheduledJourney.query.filter_by(  weekday=weekday,
                                                        hour=hour,
                                                        gender_preference=gender_preference
                                                        ).all()
    if not found_journies:
        return 'Journey not found', None

    matching_journies = []
    for journey in found_journies:
        if check_constraints(journey.source_latitude,journey.source_longitude, source_latitude, source_longitude, \
                             journey.destination_latitude,journey.destination_longitude, destination_latitude, destination_longitude, \
                             journey.required_rating, required_rating):
            matching_journies.append(journey)
    
    return 'Journey found', matching_journies

def find_user_owned_journey(user_id):

    found_journies = ScheduledJourney.query.all()
    user_owned_journies = []
    for journey in found_journies:
        if journey.creator_id == str(user_id):
            user_owned_journies.append(journey)

    if user_owned_journies == []:
        return 'Journey not found', None
    return 'Journey found', user_owned_journies


def find_user_joined_journey(user_id):

    found_journies = ScheduledJourney.query.all()

    user_joined_journies = []
    for journey in found_journies:
        if journey.creator_id != str(user_id) and user_exist_in_journey(journey, user_id):
            user_joined_journies.append(journey)

    if user_joined_journies == []:
        return 'Journey not found', None
    return 'Journey found', user_joined_journies

def make_json_object(query_result):
    json_objects = {}
    for i in range(len(query_result)):
        json_object = {}
        json_object['journey_id'] = query_result[i].id
        json_object['creator_id'] = query_result[i].creator_id
        json_object['journey_name'] = query_result[i].journey_name
        json_object['source_longitude'] = query_result[i].source_longitude
        json_object['source_latitude'] = query_result[i].source_latitude
        json_object['destination_longitude'] = query_result[i].destination_longitude
        json_object['destination_latitude'] = query_result[i].destination_latitude
        json_object['weekday'] = query_result[i].weekday
        json_object['hour'] = query_result[i].hour 
        json_object['gender_preference'] = query_result[i].gender_preference
        json_object['required_rating'] = query_result[i].required_rating
        json_object['quota']= query_result[i].quota
        journey_index = 'journey' + str(i+1)
        json_objects[journey_index] = json_object

    return json_objects

