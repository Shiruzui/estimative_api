from werkzeug.exceptions import HTTPException


class TaskValueError(HTTPException):
    code = 400

    def __init__(self, description=None, response=None, code=None):
        if code is not None:
            self.code = code
        super(TaskValueError, self).__init__(description, response)
        self.description