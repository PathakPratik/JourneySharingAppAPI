from flask import jsonify,Blueprint
from flask import session
from Decorator import login_required

app_logout = Blueprint('app_logout',__name__)


@app_logout.route("/logout",methods=['GET'])
@login_required
def logout():
    response = {}
    response["message"] = 'User logged out successfully'
    response["status"] = 200
    print(session['id'])
    session.pop('id', None)
    return jsonify(response)