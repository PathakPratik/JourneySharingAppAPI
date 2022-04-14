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
    
    user_standard = {
        'username' : 'test_user_journey_info',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword1',
        'gender' : 'male',
        'email' : 'testuserjourneyinfo@gmail.com'
    }

    user_standard_login = {
        'password' : 'Secretpassword1',
        'email' : 'testuserjourneyinfo@gmail.com'
    }

    user_standard_2 = {
        'username' : 'test_user_journey_info_2',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword1',
        'gender' : 'male',
        'email' : 'testuserjourneyinfo2@gmail.com'
    }

    user_standard_2_login = {
        'password' : 'Secretpassword1',
        'email' : 'testuserjourneyinfo2@gmail.com'
    }


    def test_user_registration_user_info(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        assert res_json == expected_res
    
    def test_user_info(self):
       
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        print(res_json == expected_res)
        if res_json == expected_res:
            response = tester.get('/get-journey')
            res_json = response.get_json()
            expected_res = {'message': 'Session id not found','status': 400}
            assert res_json == expected_res
        else:
            assert res_json == expected_res

    def test_with_login_missing_rating(self):
       
        tester = app.test_client(self)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_2_login)
        res_json = response.get_json()
        expected_res = {'message': 'User logged in successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.get('/get-journey')
            res_json = response.get_json()
            expected_res = {'message': 'Journey not found', 'status': 400}
            assert expected_res == res_json
        else:
            assert res_json == expected_res
