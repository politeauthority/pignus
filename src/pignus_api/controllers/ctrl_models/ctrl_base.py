"""Controller Model - Base

"""

from flask import Blueprint, make_response, request, jsonify

from pignus_api.utils import misc
from pignus_api.utils import log



def get_model(model, entity_id: int=None) -> dict:
    """Base GET operation for a model.
    :unit-test: TestCtrlModelsBase::test__get_model
    """
    data = {
        "status": "Error"
    }
    if not entity_id:
        data["message"] = "Missing entity ID"
        return make_response(jsonify(data), 401)
    entity = model()

    data["status"] ="Success"
    data["object_type"] = entity.entity_name

    if not entity.get_by_id(entity_id):
        data["message"] = "Could not find Entity"
        return make_response(jsonify(data), 404)
    
    data["object"] = entity.json()
    return data


def post_model(model, entity_id: int=None):
    """Base POST operation for a model. Create or modify a entity."""
    data = {
        "status": "Error"
    }
    request_data = request.get_json()

    print("\n\n")
    print(request_data)
    print("\n\n")

    entity = model()

    # Search for the entity by it's ID.
    entity_id_field = "%s_id" % entity.model_name
    if entity_id or entity_id_field in request_data:
        search_id = None
        if entity_id:
            search_id = entity_id
        elif entity_id_field in request_data:
            search_id = request_data[entity_id_field]

        if not entity.get_by_id(search_id):
            resp_data["status"] = "Error"
            resp_data["message"] = "Could not find User ID: %s" % user_id
            return jsonify(resp_data), 404

    data["object"] = entity.json()
    data["object_type"] = entity.model_name

    # if "name" in request_data:
    #     user.name = request_data["name"]

    # if "role_id" in request_data:
    #     user.role_id = request_data["role_id"]

    # user.save()
    # resp_data["object"] = user.json()
    return data




# End File: pignus/src/pignus_api/controllers/ctrl_modles/ctrl_base.py
