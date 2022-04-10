from encodings import utf_8
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
    
    user_without_email = {
        'password' : 'SecretPassword1',
        'email' : ''
    }

    user_without_password = {
        'password' : '',
        'email' : 'test_user@test.com'
    }

    user_standard = {
        'password' : 'Secretpassword1',
        'email' : 'test_user@test.com'
    }

    user_standard_wrong_email = {
        'password' : 'Secretpassword1',
        'email' : 'testtest.com'
    }

    user_standard_wrong_password = {
        'password' : 'Secretpassword1',
        'email' : 'test_user25@test.com'
    }

    user_standard_register = {
        'username' : 'test_user_',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup12@gmail.com'
    }

    user_2_standard_register = {
        'username' : 'test_user_new',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup998@gmail.com'
    }

    user_2_standard_login = {
        'password' : 'Secretpassword598',
        'email' : 'journeysharingappgroup998@gmail.com'
    }

    user_3_standard_register = {
        'username' : 'test_user_new_2',
        'password' : {'jslkdfjslk989O',True,'k;l'},
        'confirmpassword' : {'jslkdfjslk989O',True,'k;l'},
        'gender' : 'male',
        'email' : 'journeysharingappgroup9981@gmail.com'
    }

    user_3_standard_login = {
        'password' : {'jslkdfjslk989O',True,'k;l'},
        'email' : 'journeysharingappgroup9981@gmail.com'
    }

    user_standard_register_2 = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup12@gmail.com'
    }

    user_standard_register_ = {
         'email' : 'journeysharingappgroup1@gmail.com',
        'password' : 'Secretpassword67'
       
    }

    def test_missing_password(self):
        tester = app.test_client(self)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_without_password)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing password', 'status': 400}
        assert res_json == expected_res
    
    def test_missing_email(self):
        tester = app.test_client(self)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_without_email)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing email', 'status': 400}
        assert res_json == expected_res

    def test_registered_user_login(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_register)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User already exists', 'status': 400}
        assert res_json == expected_res
    
    def test_registered_user_login_2(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_register)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_register_2)
            res_json = response.get_json()
            expected_res = {'message': 'User logged in successfully', 'status': 200}
            assert res_json == expected_res
    
    def test_registered_user_login_wrong_password(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_2_standard_register)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/login', content_type='multipart/form-data',data=self.user_2_standard_login)
            res_json = response.get_json()
            expected_res = {'message': 'Wrong password', 'status': 400}
            assert res_json == expected_res
        else:
            assert res_json == expected_res
    
    def test_user_unsuccessful_login(self):
        tester = app.test_client(self)
        response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_register_)

        res_json = response.get_json()
        expected_res = {'message': 'User not found', 'status': 400}
        assert res_json == expected_res
    
   


   


        