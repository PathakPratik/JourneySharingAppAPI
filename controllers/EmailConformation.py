from setup import url_safe_timed_serializer
from flask import jsonify,Blueprint
from Models.Users import Users
from itsdangerous import SignatureExpired

app_confirm_email = Blueprint('confirm_email',__name__)

@app_confirm_email.route('/confirm_email/<token>')
def confirm_email(token):

    response = {}

    try:
        email = url_safe_timed_serializer.loads(token, salt='email-confirm', max_age=225)
        response['message'] = "The token is correct"
        response['status'] = 200
        return jsonify(response)

    except SignatureExpired:
        response['message'] = "The token is incorrect"
        response['status'] = 400
        return jsonify(response)
    