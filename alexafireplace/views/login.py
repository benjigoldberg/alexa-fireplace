from flask import jsonify
from flask import make_response
from flask import request
from flask import session

from alexafireplace.exceptions import BadRequest
from alexafireplace.server import app
import alexafireplace.models.user as user_model


@app.route('/login', methods=['POST'])
def login():
    """Logs the given user in."""
    payload = request.get_json()
    if payload is None:
        raise BadRequest('A Valid JSON payload with `username` '
                         'and `password` is required')
    user = user_model.can_login(payload['username'], payload['password'])
    session['user'] = user.to_dict()
    return make_response()


@app.route('/logout', methods=['POST'])
def logout():
    """Logs the given user out"""
    session.pop('user', None)
    return make_response()
