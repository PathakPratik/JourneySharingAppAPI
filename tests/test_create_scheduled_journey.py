from app import app
from setup import db

app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

class TestUserLogin:
    
    standard_journey = {
        'source_longitude': "53.3498",
        'source_latitude' : "6.2603",
        'destination_longitude':"35.6892",
        'destination_latitude' : '51.3890',
        'weekday':"Wed",
        'hour':"13",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':'Hamed56p'
    }

    standard_journey_1 = {
        'source_longitude': "",
        'source_latitude' : "6.2603",
        'destination_longitude':"35.6892",
        'destination_latitude' : '51.3890',
        'weekday':"Wed",
        'hour':"13",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':'Hamed56p'
    }

    standard_journey_2 = {
        'source_longitude': "53.3498",
        'source_latitude' : "",
        'destination_longitude':"35.6892",
        'destination_latitude' : '51.3890',
        'weekday':"Wed",
        'hour':"13",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':'Hamed56p'
    }

    standard_journey_3 = {
        'source_longitude': "53.3498",
        'source_latitude' : "6.2603",
        'destination_longitude':"",
        'destination_latitude' : '51.3890',
        'weekday':"Wed",
        'hour':"13",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':'Hamed56p'
    }

    standard_journey_4 = {
        'source_longitude': "53.3498",
        'source_latitude' : "6.2603",
        'destination_longitude':"35.6892",
        'destination_latitude' : '',
        'weekday':"Wed",
        'hour':"13",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':'Hamed56p'
    }

    standard_journey_5 = {
        'source_longitude': "53.3498",
        'source_latitude' : "6.2603",
        'destination_longitude':"35.6892",
        'destination_latitude' : '51.3890',
        'weekday':"",
        'hour':"13",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':'Hamed56p'
    }

    standard_journey_6 = {
        'source_longitude': "53.3498",
        'source_latitude' : "6.2603",
        'destination_longitude':"35.6892",
        'destination_latitude' : '51.3890',
        'weekday':"Wed",
        'hour':"",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':'Hamed56p'
    }

    standard_journey_8 = {
        'source_longitude': "53.3498",
        'source_latitude' : "6.2603",
        'destination_longitude':"35.6892",
        'destination_latitude' : '51.3890',
        'weekday':"Wed",
        'hour':"13",
        'gender_preference':'*',
        'required_rating':'',
        'quota':'',
        'journey_name':''
    }

    user_standard_2 = {
        'username' : 'test_user_5',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword1',
        'gender' : 'male',
        'email' : 'meslami22@tcd.ie'
    }

    user_standard = {
        'password' : 'Secretpassword1',
        'email' : 'meslami22@tcd.ie'
    }


    def test_without_login(self):
        tester = app.test_client(self)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Session id not found', 'status': 400}
        assert res_json == expected_res

    def test_with_login(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Journey added successfully', 'status': 200}
        assert res_json == expected_res
    
    def test_duplicate_journies(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Journey already exists', 'status': 400}
        assert res_json == expected_res
    
    def test_without_src_long(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey_1)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing source longitude', 'status': 400}
        assert res_json == expected_res
    
    def test_without_src_lat(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey_2)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing source latitude', 'status': 400}
        assert res_json == expected_res

    def test_without_dst_long(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey_3)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing destination longitude', 'status': 400}
        assert res_json == expected_res

    def test_without_dst_lat(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey_4)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing destination latitude', 'status': 400}
        assert res_json == expected_res
    
    def test_without_weekday(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey_5)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing weekday', 'status': 400}
        assert res_json == expected_res
    
    def test_without_hour(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard)
        response = tester.post('/create_journey', content_type='multipart/form-data',data=self.standard_journey_6)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing hour', 'status': 400}
        assert res_json == expected_res
    

    
