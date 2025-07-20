from flask import request, Blueprint, jsonify

from server.exceptions.api_exceptions import NotFoundException
from  server.services.transcript_service import TranscriptService

transcript_bp = Blueprint("api", __name__, url_prefix="/api/v1")

transcript_service = TranscriptService()

@transcript_bp.route("/transcript", methods=["POST"])
def transcript_api():
    data = request.get_json()
    url = data.get("url")

    if not url:
        raise NotFoundException("No URL provided")

    return jsonify({"success": True, **transcript_service.process_transcript(url)})