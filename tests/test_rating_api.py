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
    

    user_standard_register = {
        'username' : 'test_user_3',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup13@gmail.com'
    }

    user_standard_login = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup13@gmail.com'
    }

    user_standard_register_2 = {
        'username' : 'test_user_5',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup15@gmail.com'
    }

    user_standard_login_2 = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup15@gmail.com'
    }

    user_standard_register_3 = {
        'username' : 'test_user_5',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup23@gmail.com'
    }

    user_standard_login_3 = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup23@gmail.com'
    }

    user_standard_register_4 = {
        'username' : 'test_user_5',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup34@gmail.com'
    }

    user_standard_login_4 = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup34@gmail.com'
    }

    user_standard_register_5 = {
        'username' : 'test_user_8',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup35@gmail.com'
    }

    user_standard_login_5 = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup35@gmail.com'
    }

    user_standard_register_6 = {
        'username' : 'test_user_6',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup26@gmail.com'
    }

    user_standard_login_6 = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup26@gmail.com'
    }

    rating_request_user_not_found = {
        'id' : '20',
        'rating': '12'
    }

    rating_request_user_found = {
        'id' : '3',
        'rating': '15'
    }

    rating_missing_user_id = {
        'id' : '',
        'rating': '15'
    }

    rating_missing_rating = {
        'id' : '1',
        'rating': ''
    }

    rating_request_user_found = {
        'id' : '1',
        'rating': '15'
    }

    def test_without_login(self):
        tester = app.test_client(self)
        response = tester.post('/update_rating', content_type='multipart/form-data',data=self.rating_request_user_found)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Session id not found', 'status': 400}
        assert res_json == expected_res
    

    def test_with_login_correct_user(self):
       
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_register)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_login)
            res_json = response.get_json()
            expected_res = {'message': 'User logged in successfully', 'status': 200}
            if res_json == expected_res:
                response = tester.post('/update_rating', content_type='multipart/form-data',data=self.rating_request_user_found)
                #Check for correct validation error
                res_json = response.get_json()
                expected_res = {'message': 'User info updated successfully', 'status': 200}
                assert res_json == expected_res
            else:
                assert res_json == expected_res
        else:
            assert res_json == expected_res

    def test_with_login_wrong_user(self):
       
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_register_3)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_login_3)
            res_json = response.get_json()
            expected_res = {'message': 'User logged in successfully', 'status': 200}
            if res_json == expected_res:
                response = tester.post('/update_rating', content_type='multipart/form-data',data=self.rating_request_user_not_found)
                #Check for correct validation error
                res_json = response.get_json()
                expected_res = {'message': 'User not found', 'status': 400}
                assert res_json == expected_res
            else:
                assert res_json == expected_res
        else:
            assert res_json == expected_res 

    def test_with_login_missing_rating(self):
       
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_register_5)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_register_5)
            res_json = response.get_json()
            expected_res = {'message': 'User logged in successfully', 'status': 200}
            if res_json == expected_res:
                response = tester.post('/update_rating', content_type='multipart/form-data',data=self.rating_missing_rating)
                #Check for correct validation error
                res_json = response.get_json()
                expected_res = {'message': 'Missing user id', 'status': 400}
                assert res_json == expected_res
            else:
                assert res_json == expected_res
        else:
            assert res_json == expected_res   

    def test_with_login_missing_user_id(self):
       
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_register_6)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_register_6)
            res_json = response.get_json()
            expected_res = {'message': 'User logged in successfully', 'status': 200}
            if res_json == expected_res:
                response = tester.post('/update_rating', content_type='multipart/form-data',data=self.rating_missing_user_id)
                #Check for correct validation error
                res_json = response.get_json()
                expected_res = {'message': 'Missing rating', 'status': 400}
                assert res_json == expected_res
            else:
                assert res_json == expected_res
        else:
            assert res_json == expected_res
    
   


   


        