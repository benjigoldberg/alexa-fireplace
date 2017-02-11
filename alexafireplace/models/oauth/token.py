from datetime import datetime
from datetime import timedelta
from flask import session

from alexafireplace.server import db
from alexafireplace.server import oauth


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token is not None:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token is not None:
        return Token.query.filter_by(refresh_token=refresh_token).first()
    return None


@oauth.tokensetter
def save_token(new_token, request, *args, **kwargs):
    tokens = Token.query.filter_by(client_id=request.client.client_id,
                                   user_id=request.user.pk)
    # Ensure that every user has only one valid token active
    _ = [db.session.delete(token) for token in tokens]

    expires_in = new_token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    new_token_inst = Token(access_token=new_token['access_token'],
                           refresh_token=new_token['refresh_token'],
                           token_type=new_token['token_type'],
                           _scopes=new_token['scope'], expires=expires,
                           client_id=request.client.client_id,
                           user_id=request.user.pk)
    db.session.add(new_token_inst)
    db.session.commit()
    return new_token_inst


class Token(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'),
                          nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.pk'))
    user = db.relationship('User')

    token_type = db.Column(db.String(40))
    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes is not None:
            return self._scopes.split()
        return []
