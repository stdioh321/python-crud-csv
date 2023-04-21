import os
from datetime import datetime
from flask import request, jsonify
from src.service.collection import collection_service
from flask import Blueprint

csv_bp = Blueprint('csv_bp', __name__)


@csv_bp.route('/csv', methods=['POST'])
def upload():
    csv_file = request.files['file']
    csv_data = csv_file.read().decode('utf-8').splitlines()
    data = csv_array_to_dict(csv_data)
    collection_name = collection_service.create_collection(data)
    response = {"id": collection_name}
    return jsonify(response), 200, {'Content-Type': 'application/json'}


def csv_array_to_dict(csv_data):
    headers = csv_data[0].split(',')
    timestamp = datetime.utcnow()
    data = [dict(zip(headers, row.split(',')), createdAt=timestamp,
                 updatedAt=timestamp) for row in csv_data[1:]]
    return data
