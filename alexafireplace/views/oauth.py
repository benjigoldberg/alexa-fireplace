from alexafireplace.server import app
from alexafireplace.server import oauth


@app.route('/oauth/authorize', methods=['GET', 'POST'])
#@require_login
@oauth.authorize_handler
def authorize(*args, **kwargs):
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        return render_template('oauthorize.html', **kwargs)

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
