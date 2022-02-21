from app import app
from unittest.mock import MagicMock, patch

class TestUserRegistration:
    
    user_without_username = {
        'username' : '',
        'password' : 'SecretPassword1',
        'confirmpassword' : 'SecretPassword1',
        'gender' : 'male',
        'email' : 'test_user_@test.com'
    }

    user_without_password = {
        'username' : 'test_user_',
        'password' : '',
        'confirmpassword' : 'SecretPassword1',
        'gender' : 'male',
        'email' : 'test_user_@test.com'
    }

    user_without_password_confirmation = {
        'username' : 'test_user_',
        'password' : 'SecretPassword1',
        'confirmpassword' : '',
        'gender' : 'male',
        'email' : 'test_user_@test.com'
    }

    user_without_email = {
        'username' : 'test_user_',
        'password' : 'SecretPassword1',
        'confirmpassword' : 'SecretPassword1',
        'gender' : 'male',
        'email' : ''
    }

    user_without_gender = {
        'username' : 'test_user_',
        'password' : 'SecretPassword1',
        'confirmpassword' : 'SecretPassword1',
        'gender' : '',
        'email' : 'test_user@test.com'
    }

    user_wrong_password_format_1 = {
        'username' : 'test_user',
        'password' : 'secretpassword1',
        'confirmpassword' : 'secretpassword1',
        'gender' : 'male',
        'email' : 'test_user@test.com'
    }

    user_wrong_password_format_2 = {
        'username' : 'test_user',
        'password' : 'Secretpassword',
        'confirmpassword' : 'Secretpassword',
        'gender' : 'male',
        'email' : 'test_user@test.com'
    }

    user_wrong_password_format_3 = {
        'username' : 'test_user',
        'password' : 'secret',
        'confirmpassword' : 'secret',
        'gender' : 'male',
        'email' : 'test_user@test.com'
    }

    user_wrong_email_format_1 = {
        'username' : 'test_user',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword1',
        'gender' : 'male',
        'email' : 'testtest.com'
    }

    user_wrong_email_format_2 = {
        'username' : 'test_user',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword1',
        'gender' : 'male',
        'email' : 'test_user@testcom'
    }

    user_wrong_password_confirm_mismatch = {
        'username' : 'test_user',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword2',
        'gender' : 'male',
        'email' : 'test_user@test.com'
    }

    user_standard = {
        'username' : 'test_user',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword1',
        'gender' : 'male',
        'email' : 'test_user@test.com'
    }

    user_standard_2 = {
        'username' : 'test_user_25',
        'password' : 'Secretpassword1',
        'confirmpassword' : 'Secretpassword1',
        'gender' : 'male',
        'email' : 'test_user25@test.com'
    }

    def test_missing_username(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_without_username)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing username', 'status': 400}
        assert res_json == expected_res
    
    def test_missing_password(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_without_password)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing password', 'status': 400}
        assert res_json == expected_res

    def test_missing_password_confirmation(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_without_password_confirmation)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing password confirmation', 'status': 400}
        assert res_json == expected_res
    
    def test_missing_email(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_without_email)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing email', 'status': 400}
        assert res_json == expected_res
    
    def test_missing_gender(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_without_gender)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing gender', 'status': 400}
        assert res_json == expected_res

    def test_wrong_password_1(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_wrong_password_format_1)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Password must contain at least one capital letter', 'status': 400}
        assert res_json == expected_res
    
    def test_wrong_password_2(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_wrong_password_format_2)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Password must contain at least one digit', 'status': 400}
        assert res_json == expected_res

    def test_wrong_password_3(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_wrong_password_format_3)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Password must be at least 8 chracters', 'status': 400}
        assert res_json == expected_res

    def test_wrong_email_1(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_wrong_email_format_1)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Invalid email address', 'status': 400}
        assert res_json == expected_res

    def test_wrong_email_2(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_wrong_email_format_2)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Invalid email address', 'status': 400}
        assert res_json == expected_res

    def test_password_confirm_mismatch(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_wrong_password_confirm_mismatch)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Password confirmation incorrect', 'status': 400}
        assert res_json == expected_res

    def test_user_registration(self):
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard_2)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        assert res_json == expected_res
           
    def test_similar_credentials(self):
        session = MagicMock()
        tester = app.test_client(self)
        response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'User registered successfully', 'status': 200}
        if res_json == expected_res:
            response = tester.post('/register', content_type='multipart/form-data',data=self.user_standard)
            res_json = response.get_json()
            expected_res = {'message': 'User already exists', 'status': 409}
            assert res_json == expected_res
        assert res_json == expected_res



        