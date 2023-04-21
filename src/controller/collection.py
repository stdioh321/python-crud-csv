from flask import request, jsonify, make_response
from src.service.collection import collection_service
from flask import Blueprint

collection_bp = Blueprint('collection_bp', __name__)

header_json = {'Content-Type': 'application/json'}


@collection_bp.route('/collection/<string:collection_name>', methods=['GET'])
def get(collection_name):
    query = dict(request.args)

    response = collection_service.find(collection_name, query)
    if len(response) < 1:
        return make_response(jsonify(''), 404)

    return jsonify(response), 200, header_json


@collection_bp.route('/collection/<string:collection_name>', methods=['POST'])
def post(collection_name):
    data = {key: str(value) for key, value in request.json.items()}

    result = collection_service.insert(collection_name, data)
    return jsonify(result), 201, header_json


@collection_bp.route('/collection/<string:collection_name>', methods=['PATCH', 'PUT'])
def patch_put(collection_name):
    data = {key: str(value) for key, value in request.json.items()}
    query = dict(request.args)

    result = collection_service.update_patch(collection_name, query, data)
    return jsonify({"count": result}), 200, header_json


@collection_bp.route('/collection/<string:collection_name>', methods=['DELETE'])
def delete(collection_name):
    query = dict(request.args)

    result = collection_service.delete(collection_name, query)
    return jsonify({"count": result}), 200, header_json
