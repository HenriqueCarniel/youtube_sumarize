from googleapiclient.discovery import build
from dotenv import load_dotenv
import json
import os

load_dotenv()

api_key = os.getenv('API_KEY')
if not api_key:
    raise ValueError("API_KEY not found. Verify the file .env")

youtube = build('youtube', 'v3', developerKey=api_key)

def get_video_data(video_id):
    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=video_id
    )
    response = request.execute()

    video = response['items'][0]
    snippet = video['snippet']
    statistics = video['statistics']
    content_details = video['contentDetails']

    return {
        'title': snippet['title'],
        'description': snippet['description'],
        'views': int(statistics.get('viewCount', 0)),
        'likes': int(statistics.get('likeCount', 0)),
        'comments': int(statistics.get('commentCount', 0)),
        'duration': content_details['duration'],
        'published_at': snippet['publishedAt']
    }

def get_video_categories():
    request = youtube.videoCategories().list(
        part='snippet',
        regionCode = 'BR'
    )
    response = request.execute()

    with open("categories.json", 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)

    return response

if __name__ == "__main__":
    video_id = 'dQw4w9WgXcQ'

    # =================== Video data ===================
    '''
    video_data = get_video_data(video_id)

    with open("rick_astley.json", 'w', encoding='utf-8') as f:
        json.dump(video_data, f, ensure_ascii=False, indent=4)

    print(json.dumps(video_data, indent=4, ensure_ascii=False))
    '''

    # =================== Categories ===================
    video_categories = get_video_categories()
    print(json.dumps(video_categories, indent=4, ensure_ascii=False))