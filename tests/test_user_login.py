from app import app
from unittest.mock import MagicMock, patch

class TestUserRegistration:
    
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
    


   


        