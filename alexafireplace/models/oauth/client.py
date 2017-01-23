import binascii
import os

from alexafireplace.server import db
from alexafireplace.server import oauth


@oauth.clientgetter
def load_client(client_id):
    return Client.query.filter_by(client_id=client_id).first()


class Client(db.Model):
    """Defines an OAuth2 Client"""
    name = db.Column(db.String(40))
    user_id = db.Column(db.ForeignKey('user.pk'))
    user = db.relationship('User')
    client_id = db.Column(db.String(40), primary_key=True, 
                          default=str(binascii.hexlify(os.urandom(12))))
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False,
                              default=str(binascii.hexlify(os.urandom(36))))
    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def redirect_uris(self):
        """Returns the supported Redirect URIs for this client"""
        if self._redirect_uris is not None:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        """Returns the default Redirect URI for this client"""
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        """Returns default scopes for the client."""
        if self._default_scopes:
            return self._default_scopes.split()
        return []
