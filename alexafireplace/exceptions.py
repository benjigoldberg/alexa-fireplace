

class HttpException(Exception):
    """Defines common error handling for the application."""

    def __init__(self, message):
        """Initializes the HTTP exception."""
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code or 500

    def to_dict(self):
        """Returns the HTTP Exception formatted as a dictionary."""
        return {'message': message}


class BadRequest(Exception):
    """Malformed or missing data received from the client."""
    status_code = 400


class PermissionDenied(HttpException):
    """Requesting object has incorrect permissions for this resource."""
    status_code = 403


class UserNotFound(HttpException):
    """Requested user does not exist or could not be found."""
    status_code = 404
