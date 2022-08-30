"""Controller Model - Image

"""

from flask import Blueprint, request, jsonify, Response

from pignus_api.controllers.ctrl_models import ctrl_base
from pignus_api.models.image import Image
from pignus_api.models.image_build import ImageBuild
from pignus_api.utils import auth
from pignus_shared.utils import misc

ctrl_image = Blueprint('image', __name__, url_prefix='/image')


@ctrl_image.route("")
@ctrl_image.route("/<image_id>")
@auth.auth_request
def get_model(image_id: int=None) -> Response:
    """
    """
    data = ctrl_base.get_model(Image, image_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data)


@ctrl_image.route("", methods=["POST"])
@ctrl_image.route("/<image_id>", methods=["POST"])
@auth.auth_request
def post_model(image_id: int=None):
    """Create a new Image or modify an existing one.
    """
    resp_data = {
        "status": "Success",
        "object": {},
        "object_type": "image",
    }

    request_data = request.get_json()
    if "name" not in request_data:
        resp_data["status"] = "Error"
        return jsonify(resp_data)

    image_parsed = misc.parse_image_url(request_data["name"])

    image = Image().check_image_exists(image_parsed)

    if not image:
        image = Image()

    image.name = image_parsed["name"]
    image.maintained = True
    image.repositories = [image_parsed["repository"]]
    image.save()

    print("\n\n")
    print(image)

    print(image_parsed)
    print("\n\n"
        )
    resp_data["ext"] = image_parsed
    resp_data["object"] = image.json()
    return jsonify(resp_data)


@ctrl_image.route("/<image_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_id: int=None) -> Response:
    """DELETE opperation for Image.
    """
    data = ctrl_base.delete_model(Image, image_id)
    if not isinstance(data, dict):
        return data


    return jsonify(data), 201



@ctrl_image.route("/add", methods=["POST"])
@auth.auth_request
def add() -> Response:
    """Route for adding an Image and ImageBuild in a single request.
    POST /image/add

    """
    entity = Image()
    data = {
        "status": "Error",
        "message": "",
        "object": {},
        "object_type": entity.model_name
    }

    return jsonify(data), 201


# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_image.py
