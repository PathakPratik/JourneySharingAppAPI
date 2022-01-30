from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from constants import REDIS_JOURNEY_LIST
import time
import json 

from scipy.spatial import cKDTree
from scipy import inf

app_match_users = Blueprint('app_match_users',__name__)

# Payload Schema for MatchUsers API
class MatchUsersSchema(Schema):
    UserId = fields.Integer(required=True)
    TripStartLocation = fields.List(fields.String(), required=True)
    TripStopLocation = fields.List(fields.String(), required=True)

# MatchUsers API
@app_match_users.route("/match-users", methods=['POST'])
def matchUsers():
    
    # Unmarshal Payload
    request_data = request.json
    schema = MatchUsersSchema()
    try:
        result = schema.load(request_data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Add new journey to the list with current timestamp as score
    from app import redisClient
    redisClient.zadd(REDIS_JOURNEY_LIST,{ json.dumps(result): time.time() })

    # Return Current Journey List
    curr_list = redisClient.zrange(REDIS_JOURNEY_LIST, 0, -1)
    curr_list_str = ''.join(map(str, curr_list))
    return (curr_list_str,200)

# Empty current Journey List
@app_match_users.route("/delete-journeys", methods=['DELETE'])
def deleteJourneys():

    from app import redisClient
    redisClient.delete(REDIS_JOURNEY_LIST)

    curr_list = redisClient.zrange(REDIS_JOURNEY_LIST, 0, -1)
    curr_list_str = ''.join(map(str, curr_list))
    return (curr_list_str, 200)

# Run Algorithm
@app_match_users.route("/run-match-algo", methods=['GET'])
def RunAlgo():

    from app import redisClient
    curr_list = redisClient.zrange(REDIS_JOURNEY_LIST, 0, -1)
    
    start_arr = []
    dest_arr = []
    
    for each in curr_list:
        journey = json.loads(each)
        start_arr.append(journey.get("TripStartLocation"))
        dest_arr.append(journey.get("TripStopLocation"))
    
    from_point = 0 if not request.args.get('from') else int(request.args.get('from'))
    neighbors = findNeighbours(start_arr, dest_arr, from_point)

    res = []
    for i in neighbors:
        res.append(curr_list[i])

    res_str = ''.join(map(str, res))
    return (res_str, 200)

def findNeighbours(start_arr, dest_arr, point = 0):

    # Create KD tree for start & destination points
    start_tree = cKDTree(start_arr)
    dest_tree = cKDTree(dest_arr)

    # Max distance = 500 meters
    max_distance = 0.01
    
    # Find nearest points
    start_distances, start_indices = start_tree.query(start_arr[point], len(start_arr), p=1, distance_upper_bound=max_distance)
    dest_distances, dest_indices = dest_tree.query(dest_arr[point], len(dest_arr), p=1, distance_upper_bound=max_distance)
    
    start_points = set()
    for i, dist in zip(start_indices, start_distances):
        if dist == inf:
            break
        start_points.add(i)

    dest_points = set()
    for i, dist in zip(dest_indices, dest_distances):
        if dist == inf:
            break
        dest_points.add(i)

    # Matching journeys
    return start_points & dest_points