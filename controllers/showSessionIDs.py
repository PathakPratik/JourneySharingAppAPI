from flask import jsonify, Blueprint, session


app_session_ids = Blueprint('app_session_ids',__name__)

@app_session_ids.route("/show-session-ids")
def show_session():

    response = {}
    return jsonify(session.get('id'))
    
        

