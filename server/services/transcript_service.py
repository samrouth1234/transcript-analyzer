from youtube_transcript_api import YouTubeTranscriptApi
from server.exceptions.api_exceptions import NotFoundException
from server.models.transcript_model import TranscriptModel
from server.utils.helpers import extract_video_id, format_transcript

import requests


class TranscriptService:

    @staticmethod
    def get_video_info(video_id: str) -> dict:
        try:
            response = requests.get(
                f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "title": data.get("title"),
                    "channel": data.get("author_name"),
                    "thumbnail": data.get("thumbnail_url")
                }
        except Exception as e:
            print("oEmbed failed:", e)

        return {
            "title": f"Video: {video_id}",
            "channel": "Unknown",
            "thumbnail": f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        }

    @staticmethod
    def process_transcript(url: str) -> dict:
        video_id = extract_video_id(url)
        if not video_id:
            raise NotFoundException("Invalid YouTube URL")

        transcript_list = None
        for lang in ['en', 'en-US', 'en-GB', 'auto']:
            try:
                transcript_list = (
                    YouTubeTranscriptApi.get_transcript(video_id)
                    if lang == 'auto' else
                    YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                )
                break
            except Exception:
                continue

        if not transcript_list:
            raise NotFoundException("No transcript available")

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
