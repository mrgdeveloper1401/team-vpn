from rest_framework.exceptions import APIException


class ResponseError(APIException):
    status_code = 400

    def __init__(self, status_code=None, *args, **kwargs):
        if status_code:
            self.status_code = status_code
        super().__init__(status_code, *args, **kwargs)
