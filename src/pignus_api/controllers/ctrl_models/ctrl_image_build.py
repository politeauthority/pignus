"""Controller Model - Image Build

"""

from flask import Blueprint, request, jsonify, Response

from pignus_api.controllers.ctrl_models import ctrl_base
from pignus_api.models.image import Image
from pignus_api.utils import auth
from pignus_api.utils import misc

ctrl_image_build = Blueprint('image_build', __name__, url_prefix='/image-build')


@ctrl_image_build.route("")
@ctrl_image_build.route("/<image_build_id>")
@auth.auth_request
def get_model(image_build_id: int=None) -> Response:
	"""GET opperation for an ImageBuild
	"""
	data = ctrl_base.get_model(ImageBuild, image_build_id)
	if not isinstance(data, dict):
		return data

	return jsonify(data)


@ctrl_image_build.route("/<image_build_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_build_id: int=None) -> Response:
	"""DELETE opperation for ImageBuild.
	"""
	data = ctrl_base.delete_model(ImageBuild, image_build_id)
	if not isinstance(data, dict):
		return data


	return jsonify(data), 201


# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_image.py
