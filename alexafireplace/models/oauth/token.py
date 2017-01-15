from datetime import datetime
from datetime import timedelta

from alexafireplace import db
from alexafireplace import oauth


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token is not None:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token is not None:
        return Token.query.filter_by(refresh_token=refresh_token).first()
    return None


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    tokens = Token.query.filter_by(client_id=request.client.client_id,
                                   user_id=request.user.id)
    # Ensure that every user has only one valid token active
    _ = [db.session.delete(token) for token in tokens]

    expires_in = token.get('expires_in')
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    token = Token(access_token=token['access_token'],
                  refresh_token=token['refresh_token'],
                  token_type=token['token_type'],
                  _scopes=token['scope'], expires=expires,
                  client_id=request.client.client_id,
                  user_id=request.user.id)
    db.session.add(token)
    db.session.commit()
    return token


class Token(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'),
                          nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
