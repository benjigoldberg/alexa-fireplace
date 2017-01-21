from flask import jsonify
from flask import render_template
from flask import request

from alexafireplace.controls import fireplace
from alexafireplace.decorators import login_required
from alexafireplace.server import app


@app.route('/fireplace', methods=['POST', 'GET'])
@login_required
def get_set_fireplace():
    """Gets or modifies the state of the fireplace system"""
    if request.method == 'POST':
        json_data = request.get_json()
        if json_data is None:
            raise BadRequest('This endpoint only supports JSON data.')
        print(json_data)
        print(json_data['blower_fan'])
        if 'flame' in json_data:
            fireplace.set_flame(json_data['flame'] is True)
        if 'blower_fan' in json_data:
            fireplace.set_blower_fan(json_data['blower_fan'] is True)

    fireplace_state = {
        'flame': fireplace.get_flame_state(),
        'blower_fan': fireplace.get_blower_fan_state()
    }
    if request.method == 'POST':
        return jsonify(fireplace_state)
    return render_template('fireplace.jinja', fireplace_state=fireplace_state)
