from flask import jsonify,Blueprint
from flask import session

app_logout = Blueprint('app_logout',__name__)

@app_logout.before_request
def session_check():
    if 'id' not in session:
        response = {}
        response["message"] = 'Session id not found'
        response["status"] = 400
        return jsonify(response)

@app_logout.route("/logout",methods=['GET'])
def logout():
    response = {}
    response["message"] = 'User logged out successfully'
    response["status"] = 200
    session.pop('id', None)
    return jsonify(response)