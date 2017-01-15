from alexafireplace.server import db
from alexafireplace.server import oauth
from flask_bcrypt import check_password_hash


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    user = User.query.filter_by(username=username).first()
    if check_password_hash(user.password_hash, password) is True:
        return user
    return None


class User(db.Model):
    """Defines a Fireplace User"""
    pk = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)
