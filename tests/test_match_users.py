from app import app
import fakeredis
from mock import patch

class TestMatchUsers:
    
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
        response = tester.post('/match-users', json={
            "UserId":"1",
            "TripStartLocation": "abc",
            "TripStopLocation": "bcd"
        })
        
        statuscode = response.status_code
        assert statuscode == 200
    