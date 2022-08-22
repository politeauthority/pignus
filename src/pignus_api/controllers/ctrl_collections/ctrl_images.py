"""Collecton - Images

"""

from flask import Blueprint, jsonify

from pignus_api.collections.images import Images


ctrl_images = Blueprint('images', __name__, url_prefix='/images')

@ctrl_images.route('')
def index():
	images = Images().get_all()

	ret_images = []
	for image in images:
		ret_images.append(image.json())

	data = {
		"objects": ret_images,
		"object_type": "images"
	}
	return jsonify(data)

# End File: pignus/src/pignus_api/controllers/ctrl_collectioms/ctrl_images.py
