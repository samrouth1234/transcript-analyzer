import re
from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    if 'youtube.com' in url:
        return parse_qs(urlparse(url).query).get('v', [None])[0]
    elif 'youtu.be' in url:  # Fixed typo: 'youth.be' -> 'youtu.be'
        return url.split("/")[-1].split("?")[0]
    return None

def format_transcript(transcript_list):
    """Format transcript list into readable text"""
    formatted = []
    for entry in transcript_list:
        text = re.sub(r'\[.*?]', '', entry['text']).strip()
        if text:
            formatted.append(text)
    return ' '.join(formatted)