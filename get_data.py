from dotenv import load_dotenv
from datetime import datetime
from APIs.youtube_api import YoutubeAPI
import json
import os

if __name__ == '__main__':
    load_dotenv()
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    youtube_api = YoutubeAPI(api_key=youtube_api_key)

    # =================== Search videos ===================
    start_date = datetime(2024, 12, 1).isoformat() + "Z"
    end_date = datetime(2024, 12, 7).isoformat() + "Z"

    videos = youtube_api.search_videos(
        query='Jogos',
        video_category_id='20',
        start_date=start_date,
        end_date=end_date
    )

    with open("videos.json", 'w', encoding='utf-8') as f:
        json.dump(videos, f, ensure_ascii=False, indent=4)
