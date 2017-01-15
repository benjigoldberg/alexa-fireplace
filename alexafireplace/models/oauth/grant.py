from datetime import datetime
from datetime import timedelta

from alexafireplace.server import db
from alexafireplace.server import oauth

@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    expires = datetime.utcnow() + timedelta(seconds=60)
    grant = Grant(client_id=client_id, code=code['code'], 
                  redirect_uri=request.redirect_uri,
                  _scopes=' '.join(request.scopes),
                  user=get_current_user(),
                  expires=expires)
    db.session.add(grant)
    db.session.commit()
    return grant


class Grant(db.Model):
    """Defines a Grant to be exchanged with the client during Authorization"""
    pk = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')
    client_id = db.Column(db.String(40), db.ForeignKey('client.client_id'),
                          nullable=False)
    client = db.relationship('Client')
    code = db.Column(db.String(255), index=True, nullable=False)
    redirect_uri = db.Column(db.String(255))
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
