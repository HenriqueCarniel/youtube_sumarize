from dotenv import load_dotenv
from datetime import datetime, timedelta
from APIs.youtube_api import YoutubeAPI
import json
import os
import csv

def load_categories(categories_file):
    with open(categories_file, "r", encoding="utf-8") as f:
        categories_data = json.load(f)
    categories = [
        {"id": category["id"], "name": category["snippet"]["title_translated"]}
        for category in categories_data["items"]
    ]
    return categories

def save_progress(tracking_file, current_week_start):
    with open(tracking_file, "w", encoding="utf-8") as f:
        json.dump({"current_week_start": current_week_start.isoformat()}, f, indent=4)

def load_progress(tracking_file, default_start_date):
    if os.path.exists(tracking_file):
        with open(tracking_file, "r", encoding="utf-8") as f:
            return datetime.fromisoformat(json.load(f)["current_week_start"])
    return default_start_date

def get_week_range(start_date):
    end_date = start_date + timedelta(days=6)
    return start_date.isoformat() + "Z", end_date.isoformat() + "Z"

def write_videos_csv(output_csv, videos_list):
    fieldnames = [
        "video_id", "video_title", "video_description", "published_at", 
        "category_id", "channel_id", "channel_title", "timestamp_metadata", 
        "duration", "view_count", "comment_count", "like_count", 
        "channel_follower_count", "language"
    ]
    file_exists = os.path.isfile(output_csv)

    with open(output_csv, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        
        for video in videos_list:
            writer.writerow({
                "video_id": video["id"]["videoId"],
                "video_title": video["snippet"]["title"],
                "video_description": video["snippet"]["description"],
                "published_at": video["snippet"]["publishedAt"],
                "category_id": video["categoryId"],
                "channel_id": video["snippet"]["channelId"],
                "channel_title": video["snippet"]["channelTitle"],
                "timestamp_metadata": None,
                "duration": None,
                "view_count": None,
                "comment_count": None,
                "like_count": None,
                "channel_follower_count": None,
                "language": None
            })

if __name__ == '__main__':
    load_dotenv()
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    youtube_api = YoutubeAPI(api_key=youtube_api_key)

    max_videos_per_week = 100
    start_week_date = datetime(2024, 12, 15)
    tracking_file = "src/tracking.json"
    categories_file = "src/filtered_categories.json"
    output_csv = "data/videos.csv"

    categories = load_categories(categories_file=categories_file)
    current_week_start = load_progress(tracking_file, start_week_date)
    is_running = True

    while (is_running):
        print(f"Processing week starting: {current_week_start.date()}")
        week_start, week_end = get_week_range(current_week_start)
        videos_list = []

        for category in categories:
            category_id = category["id"]
            category_name = category["name"]

            videos = youtube_api.search_videos_with_pagination(
                video_category_id=category_id,
                start_date=week_start,
                end_date=week_end,
                query=category_name,
                total_results=max_videos_per_week
            )

            if (videos == "ERROR"):
                is_running = False
                break
            
            for video in videos:
                video["categoryId"] = category_id
            videos_list.extend(videos)

        write_videos_csv(output_csv, videos_list)
        current_week_start -= timedelta(days=7)
        save_progress(tracking_file, current_week_start)
