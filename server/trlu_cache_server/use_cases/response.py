

class Response:
    SUCCESS = 'Success'
    FAIL = 'Fail'

    def __init__(self, type_response, value):
        self.type_response = type_response
        self.value = value