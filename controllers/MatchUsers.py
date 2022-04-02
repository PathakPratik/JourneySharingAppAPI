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