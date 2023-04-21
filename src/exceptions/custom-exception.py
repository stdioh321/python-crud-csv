import traceback


class CustomException(Exception):
    def __init__(self, message, display_message=None, status_code=500, errors=None):
        self.message = message
        self.display_message = display_message or message
        self.status_code = status_code
        self.errors = errors or []
        self.trace_string = ''.join(traceback.format_stack())

    def to_dict(self):
        return {
            'message': self.message,
            'display_message': self.display_message,
            'status_code': self.status_code,
            'errors': self.errors,
            'trace_string': self.trace_string
        }
