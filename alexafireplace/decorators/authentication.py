from functools import wraps
from flask import redirect
from flask import request
from flask import session
from flask import url_for


def login_required(func):
    """User must be logged in to invoke all decorated functions."""
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_func
