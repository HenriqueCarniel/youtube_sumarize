from yt_dlp import YoutubeDL
from datetime import datetime

class yt_dlpAPI:
    def __init__(self):
        self.ydl_opts_metadata = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': True,
            'no_warnings': True
        }
        self.ydl_opts_audio = {
            'quiet': True,
            'format': 'bestaudio/best',
            'extract_audio': True,
            'audio_format': 'mp3',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
        }

    def get_video_metadata(self, video_id):
        with YoutubeDL(self.ydl_opts_metadata) as ydl:
            try:
                url = f"https://www.youtube.com/watch?v={video_id}"
                info = ydl.extract_info(url, download=False)
                return {
                    "timestamp_metadata": datetime.now().isoformat(),
                    "duration": info.get("duration", 0),
                    "view_count": info.get("view_count", 0),
                    "comment_count": info.get("comment_count", 0),
                    "like_count": info.get("like_count", 0),
                    "channel_follower_count": info.get("channel_follower_count", 0),
                    "language": info.get("language", "unknown"),
                }
            except Exception as e:
                print(f"Error processing video {video_id}: {e}")
                return {
                    "timestamp_metadata": None,
                    "duration": None,
                    "view_count": None,
                    "comment_count": None,
                    "like_count": None,
                    "channel_follower_count": None,
                    "language": None,
                }

    def download_audio(self, video_url):
        with YoutubeDL(self.ydl_opts_audio) as ydl:
            try:
                info = ydl.extract_info(video_url, download=True)
                audio_file = ydl.prepare_filename(info)
                return audio_file
            except Exception as e:
                print(f"Error downloading audio: {e}")
                return None
