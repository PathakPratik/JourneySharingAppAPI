from flask import Blueprint, request, jsonify, session
from marshmallow import Schema, fields, ValidationError, validate
from constants import REDIS_JOURNEY_LIST
from Models.ExtendedSchemas import MatchUsersSchema
from services.MatchingAlgorithm import createJourney, matchingAlgorithm, parseUser, parseGroup
from services.Decorator import login_required
from services.ScheduledJourneyModule import add_journey_to_db
from Models.ScheduledJourney import ScheduledJourney
from setup import db
import json

app_match_users = Blueprint('app_match_users', __name__)

# Payload Schema for Schedule Journey API
class ScheduleJourneySchema(Schema):
    TripStartLocation = fields.List(fields.String(), required=True)
    TripStopLocation = fields.List(fields.String(), required=True)
    ScheduleTime = fields.String(required=True)
    GenderPreference = fields.String(required=False)
    RequiredRating = fields.String(required=False)
    ModeOfTransport = fields.String(required=False)

# Schedule Journey API
@app_match_users.route("/schedule-journey", methods=['POST'])
@login_required
def ScheduleJourney():

    # Unmarshal Payload
    request_data = request.json
    schema = ScheduleJourneySchema()
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Add new journey to the list with schedule timestamp
    from app import redisClient
    try:
        userId = session.get('id')
        result["UserId"] = userId
        createJourney(result, redisClient, userId)
        scheduledJourney = ScheduledJourney(creatorId=str(userId), TripStartLocation=str(result['TripStartLocation']), TripStopLocation=str(result['TripStopLocation']),
                         ScheduleTime=str(result['ScheduleTime']), GenderPreference=str(result['GenderPreference']), RequiredRating=str(result['RequiredRating']),
                         ModeOfTransport=str(result['ModeOfTransport']))
        message, status = add_journey_to_db(scheduledJourney, db)

    except redisClient.RedisError as err:
        return jsonify(err), 500

    # Return Success
    return "Success", 200

# Empty current Journey List
@app_match_users.route("/delete-journeys", methods=['DELETE'])
def DeleteJourneys():

    try:
        from app import redisClient
        redisClient.delete(REDIS_JOURNEY_LIST)
    except redisClient.RedisError as err:
        return jsonify(err), 500

    return ("Success", 200)

@app_match_users.route("/match-users", methods=['POST'])
@login_required
def MatchUsers():

    # Unmarshal Payload
    request_data = request.json
    schema = MatchUsersSchema()
    
    if type(request_data) == str:
        request_data = json.loads(request_data)

    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Get current journeys
    from app import redisClient
    curr_list = redisClient.zrange(REDIS_JOURNEY_LIST, 0, -1)

    # Add new journey to the list
    try:
        userId = session.get('id')
        result["UserId"] = userId
        createJourney(result, redisClient, userId)
    except redisClient.RedisError as err:
        return jsonify(err), 500

    # If not enough journeys created, return empty list
    if len(curr_list) == 0:
        return jsonify([]), 200

    # Get matches result
    res = matchingAlgorithm(curr_list, result)

    trueRes = []
    for instance in res:
        #logic if given a user instead of a group
        if "GroupId" in instance:
            currGroup = instance
            parseGroup(trueRes, currGroup)
        else: 
            parseUser(trueRes, instance)

    return jsonify(trueRes), 200


@app_match_users.route("/create-n-matching-journeys", methods=['POST'])
def CreateNMatchingJourneys():
    """Creates N matching journeys, requires that the
        users ids are already created. 

    Args: 
        numjounreys, int: reads number of journeys to be created
            from request

    Returns:
        json: Returns a json stream of the created journeys
    """

    # Get number of matching journeys to make
    numJourneys = request.json['numjourneys']
    addedJourneys = []

    # Define mathcing journey conditions
    UserID = 1
    TripStartLocation = ["53.3451", "-6.2657"]
    TripStopLocation = ["53.3313", "-6.27875"]
    ScheduleTime = 43.54

    for i in range(numJourneys):
        # create the json for the journey
        currJson = {
            "UserId": UserID,
            "TripStartLocation": TripStartLocation,
            "TripStopLocation": TripStopLocation,
            "ScheduleTime": ScheduleTime
        }
        currSchema = ScheduleJourneySchema()
        try:
            result = currSchema.load(currJson)
            addedJourneys.append(result)
        except ValidationError as err:
            return jsonify(err.messages), 400

        # Add new journey to the list with current timestamp as score
        from app import redisClient
        try:
            score = result['ScheduleTime']
            del result['ScheduleTime']
            createJourney(result, redisClient, score)
        except redisClient.RedisError as err:
            return jsonify(err), 500

        UserID += 1

    final = ScheduleJourneySchema(many=True).dump(addedJourneys)
    return jsonify(final), 200

    
# Payload Schema for Group Users API
class GroupUser(Schema):
    GroupId = fields.Integer(required=True)
    UserId = fields.Integer(required=True)
class GroupUsersSchema(Schema):
    GroupUser = fields.Nested(GroupUser)
    UserIds = fields.List(fields.Integer(required=True))

# Group Users API
@app_match_users.route("/group-users", methods=['POST'])
@login_required
def GroupUsers():
    
    # Unmarshal Payload
    request_data = request.json
    schema = GroupUsersSchema()

    if type(request_data) == str:
        request_data = json.loads(request_data)

    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    from app import redisClient

    #If Group already exists, add users
    if 'GroupUser' in result:
        GroupId = result['GroupUser']['GroupId']
        UserId = result['GroupUser']['UserId']
        # Get the group and the user
        try:
            Group = redisClient.zrangebyscore(REDIS_JOURNEY_LIST, -GroupId, -GroupId)
            User = redisClient.zrangebyscore(REDIS_JOURNEY_LIST, UserId, UserId)

            if not Group or not User:
                return jsonify("Group or User does not exist!"), 400
            else:
                    Group = json.loads(Group[0])
                    User = json.loads(User[0])

            # Add user to group
            Group['Users'].append(User)

            # Update new group
            redisClient.zremrangebyscore(REDIS_JOURNEY_LIST, -GroupId, -GroupId)
            createJourney(Group, redisClient, -GroupId)
            redisClient.zremrangebyscore(REDIS_JOURNEY_LIST, UserId, UserId)

            return jsonify({ "GroupId": abs(GroupId) }), 200
        except:
            return jsonify("Something went wrong!!"), 500
    #Get Users to group journeys
    elif 'UserIds' in result:

        if len(result['UserIds']) != 2:
             return jsonify('Incorrect UserIds Argument'), 400
        
        try:
            User1Score = result['UserIds'][0]
            User2Score = result['UserIds'][1]
            
            User1 = redisClient.zrangebyscore(REDIS_JOURNEY_LIST, User1Score, User1Score)
            User2 = redisClient.zrangebyscore(REDIS_JOURNEY_LIST, User2Score, User2Score)
            
            if not User1 or not User2:
                return jsonify("No valid users!"), 400
            else:
                User1 = json.loads(User1[0])
                User2 = json.loads(User2[0])

            # Make a Group
            Group = {
                'GroupId': -User1['UserId'],
                'TripStartLocation': User1['TripStartLocation'],
                'TripStopLocation': User1['TripStopLocation'],
                'Users': [User1, User2],
                'JourneyStatus': 'Waiting'
            }
            createJourney(Group, redisClient, Group['GroupId'])

            # Remove users added to group
            redisClient.zremrangebyscore(REDIS_JOURNEY_LIST, User1Score, User1Score)
            redisClient.zremrangebyscore(REDIS_JOURNEY_LIST, User2Score, User2Score)

            return jsonify({ "GroupId": abs(Group['GroupId']) }), 200
        except:
            return jsonify("Something went wrong!!"), 500

# Payload Schema for Group Subcription API
class GroupSubscriptionSchema(Schema):
    GroupId = fields.Integer(required=True)

# Group Subscription API
@app_match_users.route("/group-subscription", methods=['POST'])
# @login_required
def GroupSubscription():
    # Unmarshal Payload
    request_data = request.json
    schema = GroupSubscriptionSchema()

    if type(request_data) == str:
        request_data = json.loads(request_data)

    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        from app import redisClient

        Group = redisClient.zrangebyscore(REDIS_JOURNEY_LIST, -result['GroupId'], -result['GroupId'])

        if not Group:
            return jsonify("Group does not exist!"), 400
        else:
            Group = json.loads(Group[0])
            Group['GroupId'] = abs(Group['GroupId'])
            TrueGroup = []
            parseGroup(TrueGroup, Group)
            return jsonify(TrueGroup[0]), 200
    except:
            return jsonify("Something went wrong!!"), 500

# Payload Schema for Group Subcription API
class StartJourneySchema(Schema):
    GroupId = fields.Integer(required=True)
    Action = fields.String(validate=validate.OneOf(['Start', 'End']), required=True)

# Start Journey API
@app_match_users.route("/journey-action", methods=['POST'])
# @login_required
def StartJourney():
    # Unmarshal Payload
    request_data = request.json
    schema = StartJourneySchema()

    if type(request_data) == str:
        request_data = json.loads(request_data)

    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    try:
        from app import redisClient

        GroupId = -result['GroupId']

        Group = redisClient.zrangebyscore(REDIS_JOURNEY_LIST, GroupId, GroupId)

        if not Group:
            return jsonify("Group does not exist!"), 400
        else:
            # Update Group Journey Status
            Group = json.loads(Group[0])
            Group['JourneyStatus'] = result['Action']
            redisClient.zremrangebyscore(REDIS_JOURNEY_LIST, GroupId, GroupId)
            createJourney(Group, redisClient, GroupId)
            return jsonify("Success!"), 200
    except:
        return jsonify("Something went wrong!!"), 500