"""Ctrl Collects - Options

"""

from flask import Blueprint, jsonify

from pignus_api.collects.options import Options


ctrl_options = Blueprint('options', __name__, url_prefix='/options')

@ctrl_options.route('')
def index():
	options = Options().get_all_keyed()

	print(options)

	data = {
		# "objects": ret_images,
		"object_type": "options"
	}
	return jsonify(data)

# End File: pignus/src/pignus_api/controllers/ctrl_collectioms/ctrl_options.py
