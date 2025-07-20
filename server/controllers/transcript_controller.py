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

# @transcript_bp.route("/transcribe", methods=["POST"])
# def transcribe_audio():
#     if "file" not in request.files:
#         return jsonify({"error": "No file part"}), 400
#
#     file = request.files["file"]
#     method = request.form.get("method", "openai")
#     language = request.form.get("language", "en")
#
#     if file.filename == "":
#         return jsonify({"error": "No selected file"}), 400
#
#     try:
#         result = transcript_service.transcribe_audio(file, method, language)
#         return jsonify({"transcript": result}), 200
#     except ValueError as ve:
#         return jsonify({"error": str(ve)}), 400
#     except Exception as e:
#         return jsonify({"error": "Transcription failed", "details": str(e)}), 500