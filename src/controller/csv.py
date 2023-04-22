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
    try:
        csv_file = request.files['file']
        data = csv_array_to_dict(csv_file)
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

    try:
        csv_data = csv_file.read().decode('utf-8')
        dialect = csv.Sniffer().sniff(
            csv_data[:1024], delimiters=ALLOWED_DELIMITERS)
        if dialect.delimiter not in ALLOWED_DELIMITERS:
            raise ValueError("Invalid delimiter")
        reader = csv.reader(csv_data.splitlines(), delimiter=dialect.delimiter)
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
    data = [dict(zip(headers, row)) for row in rows]
    return data
