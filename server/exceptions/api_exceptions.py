from flask import jsonify

class APIException(Exception):
    status_code = 500
    message = "Internal server error"

    def to_response(self):
        return jsonify({"error": self.message}), self.status_code

class BadRequestException(APIException):
    status_code = 400
    message = "Bad request"

class NotFoundException(APIException):
    status_code = 404
    message = "Resource not found"

def register_error_handlers(app):
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        return error.to_response()

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({"error": "Internal Server Error"}), 500
