from flask import jsonify
from flask import Response
from flask import render_template
from flask import request

from alexafireplace.controls import fireplace
from alexafireplace.decorators import login_required
from alexafireplace.server import app
from alexafireplace.server import oauth


@app.route('/fireplace', methods=['POST'])
@oauth.require_oauth('all')
def set_fireplace():
    """Gets the state of the fireplace system"""
    json_data = request.get_json()
    if json_data is None:
        raise BadRequest('This endpoint only supports JSON data.')
    if 'flame' in json_data:
        fireplace.set_flame(json_data['flame'] is True)
    if 'blower_fan' in json_data:
        fireplace.set_blower_fan(json_data['blower_fan'] is True)

    fireplace_state = {
        'flame': fireplace.get_flame_state(),
        'blower_fan': fireplace.get_blower_fan_state()
    }
    return jsonify(fireplace_state)

@app.route('/fireplace', methods=['GET'])
@login_required
def get_fireplace():
    """Gets fireplace state"""
    fireplace_state = {
        'flame': fireplace.get_flame_state(),
        'blower_fan': fireplace.get_blower_fan_state()
    }
    return render_template('fireplace.jinja', fireplace_state=fireplace_state)


@app.route('/fireplace/record.csv', methods=['GET'])
@login_required
def record_remote():
    """Records remote data and then returns the recorded data"""
    times, signals = fireplace.record_remote_code()
    def generate():
        for row in zip(times, signals):
            yield '{},{}\n'.format(str(row[0]), str(row[1]))
    return Response(generate(), mimetype='text/csv')
