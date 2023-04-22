from flask import jsonify
from src.exceptions.custom_exception import CustomException


class Helper:
    @staticmethod
    def exception_to_json_response(e: Exception):
        if isinstance(e, CustomException):
            return jsonify(e.to_dict()), e.status_code, {'Content-Type': 'application/json'}

        custom_ex = CustomException(message=str(
            e), display_message='Server Error', status_code=500)
        return jsonify(custom_ex.to_dict()), custom_ex.status_code, {'Content-Type': 'application/json'}

    @staticmethod
    def parse_query(query: dict):
        parsed_query = {}
        for key, value in query.items():
            if value.startswith(">="):
                parsed_query[key] = {"$gte": value[2:]}
            elif value.startswith(">"):
                parsed_query[key] = {"$gt": value[1:]}
            elif value.startswith("<="):
                parsed_query[key] = {"$lte": value[2:]}
            elif value.startswith("<"):
                parsed_query[key] = {"$lt": value[1:]}
            elif value.startswith("="):
                parsed_query[key] = value[1:]
            elif value.startswith("!"):
                parsed_query[key] = {"$ne": value[1:]}
            else:
                parsed_query[key] = value
        return parsed_query
