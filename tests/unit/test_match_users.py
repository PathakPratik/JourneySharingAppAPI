from app import app
import fakeredis
from mock import patch, create_autospec
from Models.Users import Users

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

    user_one = {
    "id":1,
    "email":"test1@gmail.com",
    "username":"test1",
    "gender":"Male"
    }

    journey_two = {
        "UserId":2,
        "TripStartLocation": ["53.345"," -6.2624"],
        "TripStopLocation": ["53.33263","-6.27554"]
    }

    user_two = {
    "id":2,
    "email":"test2@gmail.com",
    "username":"test2",
    "gender":"Male"
    }

    journey_three = {
        "UserId":3,
        "TripStartLocation": ["53.3433","-6.2612"],
        "TripStopLocation": ["53.33171","-6.27493"]
    }

    user_three = {
    "id":3,
    "email":"test3@gmail.com",
    "username":"test3",
    "gender":"Male"
    }

    journey_four = {
        "UserId":"4",
        "TripStartLocation": ["53.257","-6.126"],
        "TripStopLocation": ["53.2064","-6.1113"]
    }

    user_four = {
    "id":4,
    "email":"test4@gmail.com",
    "username":"test4",
    "gender":"Male"
    }

    users_map = {
        1:user_one,
        2:user_two,
        3:user_three,
        4:user_four
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
    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_single_match(self, mock_query):
        #Create the mock query for this instance
        tester = app.test_client(self)

        users_for_test = [self.user_one,self.user_two]
        mock_query\
            .return_value.filter_by\
            .return_value.first\
            .side_effect = users_for_test
        # First Journey
        tester.post('/match-users', json=self.journey_one)

        # Second Matching Journey
        response = tester.post('/match-users', json=self.journey_two)
        
        # Check for correct status code
        statuscode = response.status_code
        assert statuscode == 200

        # Check for correct response
        res_json = response.get_json()

        for maps in res_json:
            currUserID = maps["id"]
            for key, value in maps.items():
                assert maps[key] == self.users_map[currUserID][key]
    
    # Test for multiple matches case
    @patch("app.redisClient", fakeredis.FakeStrictRedis())
    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_multiple_match(self, mock_query):
        tester = app.test_client(self)

        users_for_test = [self.user_one,self.user_two,self.user_three]

        mock_query\
            .return_value.filter_by\
            .return_value.first\
            .side_effect = users_for_test
        
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
        
        for maps in res_json:
            currUserID = maps["id"]
            for key, value in maps.items():
                assert maps[key] == self.users_map[currUserID][key]
    
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