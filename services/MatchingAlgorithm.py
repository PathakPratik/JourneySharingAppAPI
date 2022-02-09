from constants import REDIS_JOURNEY_LIST
import time
import json

# Add new journey to the list with current timestamp as score
def createJourney(result, redisClient, score = time.time()):
    redisClient.zadd(REDIS_JOURNEY_LIST,{ json.dumps(result): score })