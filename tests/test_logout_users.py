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
    


    user_standard_register_logout = {
        'username' : 'test_user_logout',
        'password' : 'Secretpassword5',
        'confirmpassword' : 'Secretpassword5',
        'gender' : 'male',
        'email' : 'journeysharingappgroup_logout@gmail.com'
    }

    user_standard_login_logout = {
        'password' : 'Secretpassword5',
        'email' : 'journeysharingappgroup_logout@gmail.com'
    }


    def test_without_login(self):
        tester = app.test_client(self)
        response = tester.get('/logout')

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Session id not found', 'status': 400}
        assert res_json == expected_res
    

    def test_with_login_correct_user(self):
       
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_register_logout)
        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/login', content_type='multipart/form-data',data=self.user_standard_login_logout)
            res_json = response.get_json()
            expected_res = {'message': 'User logged in successfully', 'status': 200}
            if res_json == expected_res:
                response = tester.get('/logout')
                #Check for correct validation error
                res_json = response.get_json()
                expected_res = {'message': 'User logged out successfully', 'status': 200}
                assert res_json == expected_res
            else:
                assert res_json == expected_res
        else:
            assert res_json == expected_res
