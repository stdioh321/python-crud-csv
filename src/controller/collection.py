from flask import request, jsonify, make_response
from src.service.collection import CollectionService
from flask import Blueprint
from src.controller.helper import Helper
from src.exceptions.custom_exception import CustomException

collection_bp = Blueprint('collection_bp', __name__)
header_json = {'Content-Type': 'application/json'}


@collection_bp.route('/collection', methods=['GET'])
def get_collection_names():
    """
    Returns JSON data from the specified collection filtered by the query parameters.
    ---
    responses:
      200:
        description: Success. Returns JSON data with the collection names
        schema:
          type: array
          items:
            type: string
      500:
        description: Something went wrong on the server side.
    """
    try:
        response = CollectionService.list_collections()

        return jsonify(response), 200, header_json
    except Exception as e:
        return Helper.exception_to_json_response(e)


@collection_bp.route('/collection/<string:collection_name>', methods=['GET'])
def get_by_collection(collection_name):
    """
    Returns JSON data from the specified collection filtered by the query parameters.
    ---
    parameters:
      - name: collection_name
        in: path
        type: string
        required: true
        description: The name of the MongoDB collection to retrieve data from.
      - in: query
        name: field01
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
      - in: query
        name: field02
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
      - in: query
        name: field03
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
      - in: query
        name: field04
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
      # Add more fields and values as needed
    responses:
      200:
        description: Success. Returns JSON data from the specified collection filtered by the query parameters.
        schema:
          type: array
          items:
            type: object
            properties:
              _id:
                type: string
                description: The unique identifier of the document in the collection.
              # Add more fields and their types as needed
              field01:
                type: string
                description: Field 01
              field02:
                type: string
                description: Field 02
              field03:
                type: string
                description: Field 03
      404:
        description: The specified MongoDB collection was not found.
      500:
        description: Something went wrong on the server side.
    """
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
    """
    Insert new document on the specific colllection
    Returns the inserted document
    ---
    parameters:
      - name: collection_name
        in: path
        type: string
        required: true
        description: The name of the MongoDB collection to retrieve data from.
      - in: body
        name: document
        required: true
        schema:
          type: object
          properties:
            field1:
              type: string
            field2:
              type: string
    responses:
      200:
        description: Success. Returns JSON with the inserted document
        schema:
          type: object
          properties:
            _id:
              type: string
              description: The unique identifier of the document in the collection.
            # Add more fields and their types as needed
            field01:
              type: string
              description: Field 01
            field02:
              type: string
              description: Field 02
            field03:
              type: string
              description: Field 03
      404:
        description: The specified MongoDB collection was not found.
      500:
        description: Something went wrong on the server side.
    """
    try:
        data = {key: str(value) for key, value in request.json.items()}

        result = CollectionService.insert(collection_name, data)
        return jsonify(result), 201, header_json
    except Exception as e:
        return Helper.exception_to_json_response(e)


@collection_bp.route('/collection/<string:collection_name>', methods=['PATCH', 'PUT'])
def patch_put(collection_name):
    """
    Update document(s) on the specific colllection
    Returns total of itens updated
    ---
    parameters:
      - name: collection_name
        in: path
        type: string
        required: true
        description: The name of the MongoDB collection to retrieve data from.
      - in: query
        name: field01
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
      - in: query
        name: field02
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
      - in: body
        name: document
        required: true
        schema:
          type: object
          properties:
            field1:
              type: string
            field2:
              type: string
    responses:
      200:
        description: Success. Returns JSON with the inserted document
        schema:
          type: object
          properties:
            _id:
              type: string
              description: The unique identifier of the document in the collection.
            # Add more fields and their types as needed
            count:
              type: integer
              description: Total of items updated
      400:
        description: Data provided is invalid
      404:
        description: The specified MongoDB collection was not found or no item updated.
      500:
        description: Something went wrong on the server side.
    """
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
    """
    Delete document(s) on the specific colllection
    Returns total of itens deleted
    ---
    parameters:
      - name: collection_name
        in: path
        type: string
        required: true
        description: The name of the MongoDB collection to retrieve data from.
      - in: query
        name: field01
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
      - in: query
        name: field02
        description: Dynamic query parameters
        required: false
        explode: true
        schema:
          type: object
          additionalProperties:
            type: string
    responses:
      200:
        description: Success. Returns JSON with the deleted document
        schema:
          type: object
          properties:
            _id:
              type: string
              description: The unique identifier of the document in the collection.
            # Add more fields and their types as needed
            count:
              type: integer
              description: Total of items deleted
      404:
        description: The specified MongoDB collection was not found or no item deleted.
      500:
        description: Something went wrong on the server side.
    """
    try:
        query = Helper.parse_query(dict(request.args))

        result = CollectionService.delete(collection_name, query)
        if result < 1:
            raise CustomException('No items deleted', status_code=404)
        return jsonify({"count": result}), 200, header_json
    except Exception as e:
        return Helper.exception_to_json_response(e)
