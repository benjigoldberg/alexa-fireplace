from alexafireplace.exceptions import PermissionDenied
from alexafireplace.exceptions import UserNotFound
from alexafireplace.server import db
from alexafireplace.server import oauth
from flask_bcrypt import check_password_hash


def can_login(username, password):
    """The user can login if the User is valid and the password works."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise UserNotFound
    if check_password_hash(user.password_hash, password) is False:
        raise PermissionDenied
    return user


@oauth.usergetter
def get_user(username, password, *args, **kwargs):
    return can_login(username, password)


class User(db.Model):
    """Defines a Fireplace User"""
    pk = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(80))
    email = db.Column(db.String(80), unique=True)

    def to_dict(self):
        """Returns the user as a ``dict``"""
        return {
            'id': self.pk,
            'username': self.username,
            'email': self.email
        }
