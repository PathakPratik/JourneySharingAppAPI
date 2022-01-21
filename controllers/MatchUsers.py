from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from constants import REDIS_JOURNEY_LIST
import time
import json 

app_match_users = Blueprint('app_match_users',__name__)

# Payload Schema for MatchUsers API
class MatchUsersSchema(Schema):
    UserId = fields.Integer(required=True)
    TripStartLocation = fields.String(required=True)
    TripStopLocation = fields.String(required=True)

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