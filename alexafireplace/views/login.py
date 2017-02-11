from flask import jsonify
from flask import make_response
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from alexafireplace.exceptions import BadRequest
from alexafireplace.server import app
import alexafireplace.models.user as user_model


@app.route('/', methods=['GET', 'POST'])
def login():
    """Logs the given user in."""
    if request.method == 'GET':
        return render_template('login.jinja')
    username = request.form.get('username')
    password = request.form.get('password')

    # Try form data first, if not present try JSON
    if username is None or password is None:
        payload = request.get_json()
        if payload is None:
            raise BadRequest('A Valid JSON or Form payload with `username` '
                             'and `password` is required')
        username = payload['username']
        password = payload['password']

    user = user_model.can_login(username, password)
    session['user'] = user.to_dict()
    import logging
    logging.warning('SESSION {}'.format(session))
    return redirect(request.args.get('next') or url_for('get_fireplace'))


@app.route('/logout', methods=['POST'])
def logout():
    """Logs the given user out"""
    session.pop('user', None)
    return make_response()
