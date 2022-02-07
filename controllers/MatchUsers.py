from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from constants import REDIS_JOURNEY_LIST
import time
import json
import numpy as np 

from scipy.spatial import cKDTree
from scipy import inf

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
        score = result['ScheduleTime']
        del result['ScheduleTime']
        createJourney(result, redisClient, score)
    except redisClient.RedisError as err:
        return jsonify(err), 500

    # Return current journey list
    # curr_list = redisClient.zrange(REDIS_JOURNEY_LIST, 0, -1)
    # return ''.join(str(e) for e in curr_list), 200

    # Return Success
    return "Success", 200

# Add new journey to the list with current timestamp as score
def createJourney(result, redisClient, score = time.time()):
    redisClient.zadd(REDIS_JOURNEY_LIST,{ json.dumps(result): score })

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
        createJourney(result, redisClient)
    except redisClient.RedisError as err:
        return jsonify(err), 500

    # If not enough journeys created, return empty list
    if len(curr_list) == 0:
        return jsonify([]), 200

    start_arr, dest_arr = [], []
    
    for each in curr_list:
        journey = json.loads(each)
        start_arr.append(journey.get("TripStartLocation"))
        dest_arr.append(journey.get("TripStopLocation"))
    
    # Get neighbour points
    neighbors = findNeighbours(start_arr, dest_arr, result)

    # Save result
    res = []
    for i in neighbors:
        res.append(json.loads(curr_list[i]))

    return jsonify(res), 200

def findNeighbours(start_arr, dest_arr, point):

    # Create KD tree for start & destination points
    start_tree, dest_tree = cKDTree(start_arr), cKDTree(dest_arr)

    # Max distance = 500 meters
    max_distance = 0.01
    
    # Find nearest points
    start_distances, start_indices = (start_tree.query(point.get("TripStartLocation"), len(start_arr), p=1, distance_upper_bound=max_distance))
    dest_distances, dest_indices = (dest_tree.query(point.get("TripStopLocation"), len(dest_arr), p=1, distance_upper_bound=max_distance))
    
    start_distances, start_indices = handleSingleNeighbour(start_distances, start_indices)
    dest_distances, dest_indices = handleSingleNeighbour(dest_distances, dest_indices)

    start_points, dest_points = handleMultipleNeighbours(start_indices, start_distances), handleMultipleNeighbours(dest_indices, dest_distances)

    # Matching journeys
    return start_points & dest_points

def handleSingleNeighbour(d, i):
    return  np.array([d]) if type(d) is float else d, np.array([i]) if type(i) is int else i

def handleMultipleNeighbours(indexes, distances):
    points = set()
    for i, dist in zip(indexes, distances):
        if dist == inf:
            break
        points.add(i)
    return points