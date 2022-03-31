from app import app
from setup import db
from controllers.Ratings import *
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()


class TestUsersRatings:
    user_without_email = {
        'rating' : 'Ratings1'
        'email' : ''
    }
    
    user_standard_register_ = {
         'email' : 'journeysharingappgroup1@gmail.com',
        'password' : 'Secretpassword67'
       
    }

    def test_user_not_found(self):
        tester = app.test_client(self)
        response = tester.post('/update_rating', content_type='multipart/form-data',data=self.user_standard_register_)

        # Check for correct validation error
        res_json = response.get_json()
        
        expected_res = {'message': 'User not Found', 'status': 400}
        assert res_json == expected_res
    
    def test_missing_email(self):
        tester = app.test_client(self)
        response = tester.post('/update_rating', content_type='multipart/form-data',data=self.user_without_email)

        # Check for correct validation error
        res_json = response.get_json()
        expected_res = {'message': 'Missing email', 'status': 400}
        assert res_json == expected_res
    
    def test_range_of_ratings(self):
        if (Ratings.ratings_Currentlyt > 5):
            response = tester.post('/update_rating', content_type='multipart/form-data')
                    # Check for correct validation error
            res_json = response.get_json()
            expected_res = {'message': 'Ratings cannot be more than 5', 'status': 400}
            assert res_json == expected_res

        if(Ratings.ratings_Currently < 0):
            response = tester.post('/update_rating', content_type='multipart/form-data')
                    # Check for correct validation error
            res_json = response.get_json()
            expected_res = {'message':'Ratings cannot be negative' ratings_range_error, 'status': 400}
            assert res_json == expected_res
