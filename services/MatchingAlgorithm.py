from datetime import datetime, timedelta
from constants import REDIS_JOURNEY_LIST
import time
import json
from dateutil import parser

import numpy as np
from scipy.spatial import cKDTree
from scipy import inf

# Add new journey to the list with current timestamp as score
def createJourney(result, redisClient, score):

    #Check if already exists
    entry = redisClient.zrangebyscore(REDIS_JOURNEY_LIST, score, score)
    
    if len(entry) != 0:
        is_stale = filterFutureJourney(entry)

        if not is_stale:
            return
    
    result["time"] = result['ScheduleTime'] if 'ScheduleTime' in result else time.time()
    redisClient.zadd(REDIS_JOURNEY_LIST,{ json.dumps(result): score })

# Matching Algorithm
def matchingAlgorithm(curr_list, point):
    start_arr, dest_arr = [], []
    
    for each in curr_list:
        journey = json.loads(each)
        
        if filterFutureJourney(journey):
            continue

        start_arr.append(journey.get("TripStartLocation"))
        dest_arr.append(journey.get("TripStopLocation"))
    
    # If no journeys pass filters return empty result
    if not start_arr or not dest_arr:
        return []

    # Get neighbour points
    neighbors = findNeighbours(start_arr, dest_arr, point)
    
    # Save result
    res = []
    for i in neighbors:
        each = json.loads(curr_list[i])
        if 'GroupId' in each:
            each['GroupId'] = abs(each['GroupId'])
            res.append(each)
        elif 'UserId' in each and each['UserId'] != point['UserId']:
            res.append(each)
    
    return res

# Remove journeys scheduled for future
def filterFutureJourney(journey):
    if type(journey['time']) == str:
        diff = parser.parse(journey['time']) - datetime.today()
        if diff > timedelta(minutes=3):
            return True
        if diff < timedelta(0):
            return True
    else:
        diff = journey['time'] - time.time()

        if diff < -180:
            return True

# Find neighbouring points from start and destinations
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