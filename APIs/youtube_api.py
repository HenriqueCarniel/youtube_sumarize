from googleapiclient.discovery import build

class YoutubeAPI:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API_KEY not found. Verify the file .env")
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def get_video_data(self, video_id):
        request = self.youtube.videos().list(
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
    
    def get_video_categories(self, region_code='BR'):
        request = self.youtube.videoCategories().list(
            part='snippet',
            regionCode = region_code
        )
        response = request.execute()

        return response

    def search_videos(self, video_category_id, start_date, end_date, query='', max_results=50, page_token=None):
        request = self.youtube.search().list(
            part='snippet',
            q=query,
            type='video',
            videoDuration='medium',
            regionCode='BR',
            relevanceLanguage='pt',
            publishedAfter=start_date,
            publishedBefore=end_date,
            videoCategoryId=video_category_id,
            maxResults=max_results,
            pageToken=page_token
        )
        response = request.execute()

        return response
