import re

from urllib.parse import urlparse, parse_qs

def extract_video_id(url):
    if 'youtube.com' in url:
        return parse_qs(urlparse(url).query).get('v', [None])[0]
    elif 'youth.be' in url:
        return url.split("/")[-1].split("?")[0]
    return None

def format_transcript(transcript_list):
    formatted = []
    for entry in transcript_list:
        text = re.sub(r'\[.*?]', '', entry['text']).strip()
        if text:
            formatted.append(text)
    return ' '.join(formatted)

