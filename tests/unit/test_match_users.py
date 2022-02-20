from app import app
import fakeredis
from mock import patch

class TestMatchUsers:
    
    journey_wrong_type = {
        "UserId":1,
        "TripStartLocation": "abc",
        "TripStopLocation": "bcd"
    }

    journey_one = {
        "UserId":1,
        "TripStartLocation": ["53.3451","-6.2657"],
        "TripStopLocation": ["53.3313","-6.27875"]
    }

    journey_two = {
        "UserId":2,
        "TripStartLocation": ["53.345"," -6.2624"],
        "TripStopLocation": ["53.33263","-6.27554"]
    }

    journey_three = {
        "UserId":3,
        "TripStartLocation": ["53.3433","-6.2612"],
        "TripStopLocation": ["53.33171","-6.27493"]
    }

    journey_four = {
        "UserId":"4",
        "TripStartLocation": ["53.257","-6.126"],
        "TripStopLocation": ["53.2064","-6.1113"]
    }

    # Test for mandatory fields in payload
    def test_fields(self):
        tester = app.test_client(self)
        response = tester.post('/match-users', json={
            "UserId":"1",
        })

        # Check for correct error code
        statuscode = response.status_code
        assert statuscode == 400
        
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'TripStartLocation': ['Missing data for required field.'], 'TripStopLocation': ['Missing data for required field.']}
        assert res_json == expected_res
    
    # Test for correct field types in payload
    def test_field_types(self):
        tester = app.test_client(self)
        response = tester.post('/match-users', json=self.journey_wrong_type)

        # Check for correct error code
        statuscode = response.status_code
        assert statuscode == 400
        
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {"TripStartLocation":["Not a valid list."],"TripStopLocation":["Not a valid list."]}
        assert res_json == expected_res

    # Test correct content type
    def test_content_type(self):
        tester = app.test_client(self)
        response = tester.post('/match-users', json={
            "UserId":"1",
        })
        
        assert response.content_type == "application/json"

    # Test for Success Case
    @patch("app.redisClient", fakeredis.FakeStrictRedis())
    def test_success(self):
        tester = app.test_client(self)
        response = tester.post('/match-users', json=self.journey_one)
        
        # Check for correct status code
        statuscode = response.status_code
        assert statuscode == 200

        # Check for correct response
        res_json = response.get_json()
        expected_res = []
        assert res_json == expected_res
    
    # Test for single match case
    @patch("app.redisClient", fakeredis.FakeStrictRedis())
    def test_single_match(self):
        tester = app.test_client(self)
        
        # First Journey
        tester.post('/match-users', json=self.journey_one)

        # Second Matching Journey
        response = tester.post('/match-users', json=self.journey_two)
        
        # Check for correct status code
        statuscode = response.status_code
        assert statuscode == 200

        # Check for correct response
        res_json = response.get_json()
        assert sorted(res_json[0].items()) == sorted(self.journey_one.items())
    
    # Test for multiple matches case
    @patch("app.redisClient", fakeredis.FakeStrictRedis())
    def test_multiple_match(self):
        tester = app.test_client(self)
        
        # First Journey
        tester.post('/match-users', json=self.journey_one)

        # Second Matching Journey
        tester.post('/match-users', json=self.journey_two)

        # Third Matching Journey
        response = tester.post('/match-users', json=self.journey_three)
        
        # Check for correct status code
        statuscode = response.status_code
        assert statuscode == 200

        # Check for correct response
        res_json = response.get_json()
        expected_res = [self.journey_one, self.journey_two]
        res_json = sorted(res_json, key=lambda d: d['UserId'])

        for i in range(len(res_json)):
            assert sorted(res_json[i].items()) == sorted(expected_res[i].items())
    
    # Test for non-matching journey case
    @patch("app.redisClient", fakeredis.FakeStrictRedis())
    def test_non_match(self):
        tester = app.test_client(self)
        
        # First Journey
        tester.post('/match-users', json=self.journey_one)

        # Second Non-matching Journey
        response = tester.post('/match-users', json=self.journey_four)
        
        # Check for correct status code
        statuscode = response.status_code
        assert statuscode == 200

        # Check for correct response
        res_json = response.get_json()
        assert res_json == []