import csv
from datetime import datetime
from flask import request, jsonify
from flask import Blueprint

from src.service.collection import CollectionService
from src.controller.helper import Helper
from src.exceptions.custom_exception import CustomException

csv_bp = Blueprint('csv_bp', __name__)


@csv_bp.route('/csv', methods=['POST'])
def post():
    try:
        csv_file = request.files['file']
        csv_data = validate_csv_file(csv_file)
        data = csv_array_to_dict(csv_data)
        collection_name = CollectionService.create_collection(data)
        response = {'id': collection_name}
        return jsonify(response), 201, {'Content-Type': 'application/json'}
    except Exception as e:
        return Helper.exception_to_json_response(e)


@csv_bp.route('/csv/<collection_name>', methods=['PUT'])
def put(collection_name: str):
    try:
        csv_file = request.files['file']
        csv_data = validate_csv_file(csv_file)
        data = csv_array_to_dict(csv_data)
        count = CollectionService.clear_and_insert_many(
            collection_name, data)
        response = {"id": collection_name, "count": count}
        return jsonify(response), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return Helper.exception_to_json_response(e)


def csv_array_to_dict(csv_data):
    headers = csv_data[0].split(',')
    timestamp = datetime.utcnow()
    data = [dict(zip(headers, row.split(',')), createdAt=timestamp,
                 updatedAt=timestamp) for row in csv_data[1:]]
    return data


def validate_csv_file(csv_file):
    if not csv_file:
        raise CustomException("No CSV file provided", status_code=400)

    if not csv_file.filename.endswith('.csv'):
        raise CustomException("File must be a CSV", status_code=400)

    csv_data = csv_file.read().decode('utf-8').splitlines()
    try:
        allowed_delimiters = [",", ";"]
        dialect = csv.Sniffer().sniff(csv_data[0], delimiters=allowed_delimiters)
        if dialect.delimiter not in allowed_delimiters:
            raise Exception("Invalid delimiter")
        reader = csv.reader(csv_data, delimiter=dialect.delimiter)
        for row in reader:
            pass
    except Exception as e:
        raise CustomException(status_code=400, message=str(
            e), display_message="File must be a valid CSV")
    csv_reader = csv.reader(csv_data)
    headers = next(csv_reader, None)
    if not headers:
        raise CustomException("CSV file must have headers", status_code=400)

    return csv_data
