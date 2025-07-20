class TranscriptModel:
    def __init__(self, video_id, title, channel, thumbnail, transcript, raw_transcript):
        self.video_id = video_id
        self.title = title
        self.channel = channel
        self.thumbnail = thumbnail
        self.transcript = transcript
        self.word_count = len(transcript.split())
        self.estimated_duration = f"{len(raw_transcript) * 3 // 60}:{len(raw_transcript) * 3 % 60:02d}"
        self.raw_transcript = raw_transcript

    def to_dict(self):
        return {
            "video_id": self.video_id,
            "title": self.title,
            "channel": self.channel,
            "thumbnail": self.thumbnail,
            "transcript": self.transcript,
            "word_count": self.word_count,
            "estimated_duration": self.estimated_duration,
            "raw_transcript": self.raw_transcript,
        }