from flask import request, Blueprint, jsonify
import logging

from server.exceptions.api_exceptions import NotFoundException, BadRequestException
from server.services.transcript_service import TranscriptService

transcript_bp = Blueprint("api", __name__, url_prefix="/api/v1")

transcript_service = TranscriptService()
logger = logging.getLogger(__name__)

@transcript_bp.route("/transcript", methods=["POST"])
def transcript_api():
    try:
        data = request.get_json()
        if not data:
            raise BadRequestException("No JSON data provided")
        
        url = data.get("url")
        if not url:
            raise BadRequestException("No URL provided")

        logger.info(f"Processing transcript request for URL: {url}")
        result = transcript_service.process_transcript(url)
        
        return jsonify({"success": True, **result})
    
    except (NotFoundException, BadRequestException):
        raise
    except Exception as e:
        logger.error(f"Unexpected error in transcript API: {e}")
        raise NotFoundException("Error processing request")

@transcript_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "Transcript API is running"})