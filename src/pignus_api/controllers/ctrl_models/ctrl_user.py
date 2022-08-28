"""Controller Model - User

"""

from flask import Blueprint, request, jsonify

from pignus_api.models.user import User
from pignus_api.utils import misc
from pignus_api.utils import log
from pignus_api.utils import auth


ctrl_user = Blueprint('user', __name__, url_prefix='/user')

@ctrl_user.route("/<user_id>")
@auth.auth_request
def get_model(user_id):
	data = {
		"status": "Success",
		"object_type": "user",
	}
	user = User()
	if not user.get_by_id(user_id):
		data["status"] = "Error"
		data["message"] = "Could not find User"
		return jsonify(data), 404
	data["object"] = user.json()
	return jsonify(data)

 
@ctrl_user.route("", methods=["POST"])
@ctrl_user.route("/<user_id>", methods=["POST"])
@auth.auth_request
def post_model(user_id: int=None):
	"""Create a new User."""
	resp_data = {
		"status": "Success"
	}
	request_data = request.get_json()


	if "user_id" not in request_data:
		user = User()
	else:
		user = User().get_by_id(user_id)
		if not user:
			resp_data["status"] = "Error"
			resp_data["message"] = "Could not find User ID: %s" % user_id
			return jsonify(resp_data), 404

	print(user)

	if "name" in request_data:
		user.name = request_data["name"]

	if "role_id" in request_data:
		user.role_id = request_data["role_id"]

	user.save()

	resp_data["object"] = user.json()
	return jsonify(resp_data), 201


@ctrl_user.route("/<user_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(user_id: int):
	"""Delete a User."""
	resp_data = {
		"status": "Success"
	}

	user = User()
	if not user.get_by_id(user_id):
		resp_data["status"] = "Error"
		resp_data["message"] = "User not found"
		return jsonify(resp_data), 404
	user.delete()
	resp_data["message"] = "User deleted successfully"
	resp_data["object"] = user.json()
	resp_data["object_type"] = "user"
	return jsonify(resp_data), 201

# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_user.py
