from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from constants import REDIS_JOURNEY_LIST
from services.MatchingAlgorithm import createJourney, matchingAlgorithm
import json

app_match_users = Blueprint('app_match_users',__name__)

# Payload Schema for Schedule Journey API
class ScheduleJourneySchema(Schema):
    UserId = fields.Integer(required=True)
    TripStartLocation = fields.List(fields.String(), required=True)
    TripStopLocation = fields.List(fields.String(), required=True)
    ScheduleTime = fields.Float(required=True)
    GenderPrefrence = fields.String(required=False)
    RequiredRating = fields.String(required=False)
    ModeOfTransport = fields.String(required=False)

# Schedule Journey API
@app_match_users.route("/schedule-journey", methods=['POST'])
def ScheduleJourney():
    
    # Unmarshal Payload
    request_data = request.json
    schema = ScheduleJourneySchema()
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Add new journey to the list with current timestamp as score
    from app import redisClient
    try:
        createJourney(result, redisClient, result['UserId'])
    except redisClient.RedisError as err:
        return jsonify(err), 500

    # Return current journey list
    # curr_list = redisClient.zrange(REDIS_JOURNEY_LIST, 0, -1)
    # return ''.join(str(e) for e in curr_list), 200

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

# Payload Schema for Match Users API
class MatchUsersSchema(Schema):
    UserId = fields.Integer(required=True)
    TripStartLocation = fields.List(fields.String(), required=True)
    TripStopLocation = fields.List(fields.String(), required=True)

# Match Users API
@app_match_users.route("/match-users", methods=['POST'])
def MatchUsers():

    # Unmarshal Payload
    request_data = request.json
    schema = MatchUsersSchema()
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Get current journeys 
    from app import redisClient
    curr_list = redisClient.zrange(REDIS_JOURNEY_LIST, 0, -1)

    # Add new journey to the list
    try:
        createJourney(result, redisClient, result['UserId'])
    except redisClient.RedisError as err:
        return jsonify(err), 500

    # If not enough journeys created, return empty list
    if len(curr_list) == 0:
        return jsonify([]), 200

    # Get matches result
    res = matchingAlgorithm(curr_list, result)

    return jsonify(res), 200

    
# Payload Schema for Group Users API
class GroupUser(Schema):
    GroupId = fields.Integer(required=True)
    UserId = fields.Integer(required=True)
class GroupUsersSchema(Schema):
    GroupUser = fields.Nested(GroupUser)
    UserIds = fields.List(fields.Integer(required=True))

# Group Users API
@app_match_users.route("/group-users", methods=['POST'])
def GroupUsers():
    
    # Unmarshal Payload
    request_data = request.json
    schema = GroupUsersSchema()
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
                'Users': [User1, User2]
            }
            createJourney(Group, redisClient, Group['GroupId'])

            # Remove users added to group
            redisClient.zremrangebyscore(REDIS_JOURNEY_LIST, User1Score, User1Score)
            redisClient.zremrangebyscore(REDIS_JOURNEY_LIST, User2Score, User2Score)

            return jsonify({ "GroupId": abs(Group['GroupId']) }), 200
        except:
            return jsonify("Something went wrong!!"), 500
