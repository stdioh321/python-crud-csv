import csv
from datetime import datetime
from flask import request, jsonify
from flask import Blueprint

from src.service.collection import CollectionService
from src.controller.helper import Helper
from src.exceptions.custom_exception import CustomException

csv_bp = Blueprint('csv_bp', __name__)

ALLOWED_DELIMITERS = [",", ";"]


@csv_bp.route('/csv', methods=['POST'])
def post():
    """
    Creates a new MongoDB collection with a random UUID name from uploaded CSV file.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: The CSV file to upload.
    responses:
      201:
        description: Created new MongoDB collection with UUID name.
        schema:
          type: object
          properties:
            id:
              type: string
              description: The UUID name of the new MongoDB collection.
      400:
        description: Something is wrong with the uploaded CSV file.
      500:
        description: Something went wrong on the server side.
    """
    try:
        csv_file = request.files['file']
        data = csv_array_to_dict(csv_file)
        collection_name = CollectionService.create_collection(data)
        response = {'id': collection_name}
        return jsonify(response), 201, {'Content-Type': 'application/json'}
    except Exception as e:
        return Helper.exception_to_json_response(e)


@csv_bp.route('/csv/<collection_name>', methods=['PUT'])
def put(collection_name: str):
    """
    Uploads a CSV file, clears the specified collection, and inserts the data from the CSV.
    ---
    parameters:
      - name: collection_name
        in: path
        type: string
        required: true
        description: The name of the MongoDB collection to upload the CSV data to.
        default: 4aeb8f09-7786-4f16-9e62-3af8c7249130
      - name: file
        in: formData
        type: file
        required: true
        description: The CSV file to upload.
    responses:
      200:
        description: Success. Returns the UUID of the collection and the number of items inserted.
        schema:
          type: object
          properties:
            id:
              type: string
              description: The UUID of the MongoDB collection.
            count:
              type: integer
              description: The number of items inserted.
      400:
        description: Something is wrong with the uploaded CSV file.
      404:
        description: The specified MongoDB collection was not found.
      500:
        description: Something went wrong on the server side.
    """
    try:
        csv_file = request.files['file']
        data = csv_array_to_dict(csv_file)
        count = CollectionService.clear_and_insert_many(
            collection_name, data)
        response = {"id": collection_name, "count": count}
        return jsonify(response), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return Helper.exception_to_json_response(e)


def validate_csv_file(csv_file):
    if not csv_file:
        raise CustomException("No CSV file provided", status_code=400)

    if not csv_file.filename.endswith('.csv'):
        raise CustomException("File must be a CSV", status_code=400)

    try:
        csv_data = csv_file.read().decode('utf-8')
        csv_splited = csv_data.splitlines()
        dialect = csv.Sniffer().sniff(csv_splited[0], delimiters=ALLOWED_DELIMITERS)
        if dialect.delimiter not in ALLOWED_DELIMITERS:
            raise ValueError("Invalid delimiter")
        reader = csv.reader(csv_splited, delimiter=dialect.delimiter)
        headers = next(reader)
        if not headers:
            raise ValueError("CSV file must have headers")
    except (ValueError, csv.Error) as e:
        raise CustomException(status_code=400, message=str(
            e), display_message="File must be a valid CSV")

    return csv_data


def csv_array_to_dict(csv_file):
    contents = validate_csv_file(csv_file)
    delimiter = ',' if ',' in contents[:100] else ';'
    rows = csv.reader(contents.splitlines(), delimiter=delimiter)
    headers = next(rows)
    timestamp = datetime.utcnow()
    data = [dict(zip(headers, row), createdAt=timestamp,
                 updatedAt=timestamp) for row in rows]
    return data
