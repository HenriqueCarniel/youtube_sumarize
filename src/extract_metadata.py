import csv
from yt_dlp import YoutubeDL
from datetime import datetime
from tqdm import tqdm
from multiprocessing import Pool

input_csv = "data/videos.csv"
output_csv = "data/videos_updated.csv"

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'extract_flat': True,
    'no_warnings': True
}

def get_video_metadata(video_id):
    with YoutubeDL(ydl_opts) as ydl:
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

def process_video_row(row):
    if len(row["timestamp_metadata"]) == 0:
        video_id = row["video_id"]
        metadata = get_video_metadata(video_id)
        row.update(metadata)
    return row

def update_csv_with_metadata(input_csv, output_csv):
    with open(input_csv, mode="r", encoding="utf-8") as infile, \
         open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        rows = list(reader)
        with Pool() as pool:
            updated_rows = list(tqdm(pool.imap(process_video_row, rows), total=len(rows), desc="Processing Videos"))
        writer.writerows(updated_rows)

if __name__ == "__main__":
    update_csv_with_metadata(input_csv, output_csv)
    print(f"Updated metadata in: {output_csv}")
