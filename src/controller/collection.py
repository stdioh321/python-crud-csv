from flask import request, jsonify, make_response
from src.service.collection import CollectionService
from flask import Blueprint
from src.controller.helper import Helper
from src.exceptions.custom_exception import CustomException

collection_bp = Blueprint('collection_bp', __name__)

header_json = {'Content-Type': 'application/json'}


@collection_bp.route('/collection/<string:collection_name>', methods=['GET'])
def get(collection_name):
    try:
        query = Helper.parse_query(dict(request.args))
        response = CollectionService.find(collection_name, query)
        if len(response) < 1:
            raise CustomException('No items found', status_code=404)

        return jsonify(response), 200, header_json
    except Exception as e:
        return Helper.exception_to_json_response(e)


@collection_bp.route('/collection/<string:collection_name>', methods=['POST'])
def post(collection_name):
    try:
        data = {key: str(value) for key, value in request.json.items()}

        result = CollectionService.insert(collection_name, data)
        return jsonify(result), 201, header_json
    except Exception as e:
        return Helper.exception_to_json_response(e)


@collection_bp.route('/collection/<string:collection_name>', methods=['PATCH', 'PUT'])
def patch_put(collection_name):
    try:
        data = {key: str(value) for key, value in request.json.items()}
        query = Helper.parse_query(dict(request.args))

        result = CollectionService.update_patch(collection_name, query, data)
        if result < 1:
            raise CustomException('No items updated', status_code=404)

        return jsonify({"count": result}), 200, header_json
    except Exception as e:
        return Helper.exception_to_json_response(e)


@collection_bp.route('/collection/<string:collection_name>', methods=['DELETE'])
def delete(collection_name):
    try:
        query = Helper.parse_query(dict(request.args))

        result = CollectionService.delete(collection_name, query)
        if result < 1:
            raise CustomException('No items deleted', status_code=404)
        return jsonify({"count": result}), 200, header_json
    except Exception as e:
        return Helper.exception_to_json_response(e)
