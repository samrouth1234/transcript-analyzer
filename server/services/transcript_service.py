from youtube_transcript_api import YouTubeTranscriptApi
from server.exceptions.api_exceptions import NotFoundException
from server.models.transcript_model import TranscriptModel
from server.utils.helpers import extract_video_id, format_transcript

import requests
import logging

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TranscriptService:

    @staticmethod
    def get_video_info(video_id: str) -> dict:
        try:
            # Add timeout for deployment environment
            response = requests.get(
                f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json",
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "title": data.get("title"),
                    "channel": data.get("author_name"),
                    "thumbnail": data.get("thumbnail_url")
                }
        except Exception as e:
            logger.warning(f"oEmbed failed for video {video_id}: {e}")

        return {
            "title": f"Video: {video_id}",
            "channel": "Unknown",
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        }

    @staticmethod
    def process_transcript(url: str) -> dict:
        try:
            video_id = extract_video_id(url)
            if not video_id:
                raise NotFoundException("Invalid YouTube URL")

            logger.info(f"Processing transcript for video: {video_id}")

            transcript_list = None
            for lang in ['en', 'en-US', 'en-GB', 'auto']:
                try:
                    transcript_list = (
                        YouTubeTranscriptApi.get_transcript(video_id)
                        if lang == 'auto' else
                        YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                    )
                    logger.info(f"Found transcript in language: {lang}")
                    break
                except Exception as lang_error:
                    logger.debug(f"Failed to get transcript in {lang}: {lang_error}")
                    continue

            if not transcript_list:
                raise NotFoundException("No transcript available for this video")

            formatted = format_transcript(transcript_list)
            info = TranscriptService.get_video_info(video_id)

            return TranscriptModel(
                video_id=video_id,
                title=info["title"],
                channel=info["channel"],
                thumbnail=info["thumbnail"],
                transcript=formatted,
                raw_transcript=transcript_list
            ).to_dict()
        
        except NotFoundException:
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing transcript: {e}")
            raise NotFoundException("Error processing transcript")
