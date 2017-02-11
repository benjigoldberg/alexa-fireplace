from flask import render_template
from flask import request

from alexafireplace.decorators import login_required
from alexafireplace.models import Client
from alexafireplace.server import app
from alexafireplace.server import oauth


@app.route('/oauth/settings', methods=['GET'])
@login_required
def oauth_settings():
    return render_template('oauth_settings.jinja')


@app.route('/oauth/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['redirect_uri'] = kwargs.get('redirect_uri', 
                                            client.default_redirect_uri)
        kwargs['scope'] = kwargs.get('scope', 'all')
        kwargs['response_type'] = kwargs.get('response_type', 'code')
        kwargs['state'] = kwargs.get('state')
        return render_template('oauth_confirm.jinja', **kwargs)
    confirm = request.form.get('confirm', 'no') 
    return confirm == 'yes'


@app.route('/oauth/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return None


@app.route('/oauth/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token():
    return None
