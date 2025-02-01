class CustomException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        response = dict(self.payload or {})
        response['error'] = self.message
        response['status_code'] = self.status_code
        return response


class NotFoundException(CustomException):
    def __init__(self, message="Not Found"):
        super().__init__(message, status_code=404)


class BadRequestException(CustomException):
    def __init__(self, message="Bad Request"):
        super().__init__(message, status_code=400)


class InternalServerErrorException(CustomException):
    def __init__(self, message="Internal Server Error"):
        super().__init__(message, status_code=500)
