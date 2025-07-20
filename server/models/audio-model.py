class AudioModel:
    def __init__(self, video_id, title, channel, thumbnail, transcript, raw_transcript):
        self.video_id = video_id
        self.title = title
        self.channel = channel
        self.thumbnail = thumbnail
        self.transcript = transcript
        self.raw_transcript = raw_transcript