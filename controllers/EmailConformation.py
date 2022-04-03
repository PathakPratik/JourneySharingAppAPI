from setup import url_safe_timed_serializer
from setup import db
from flask import jsonify,Blueprint
from Models.Users import Users
from itsdangerous import SignatureExpired
from services.UserUtility import find_user_by_email, update_user_in_db
import datetime

app_confirm_email = Blueprint('confirm_email',__name__)

@app_confirm_email.route('/confirm_email/<token>')
def confirm_email(token):

    response = {}

    try:
        email = url_safe_timed_serializer.loads(token, salt='email-confirm', max_age=225)

        message, user = find_user_by_email(email)
        
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()

        update_user_in_db(user,db)

        response['message'] = "User email is confirmed"
        response['status'] = 200
        return jsonify(response)

    except SignatureExpired:
        response['message'] = "User email could not be confirmed"
        response['status'] = 400
        return jsonify(response)
    