import yt_dlp
import json

def fetch_video_metadata(video_urls):
    metadata_list = []
    ydl_opts = {
        'quiet': True,
        'sjip_download': True,
        'extract_flat': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in video_urls:
            try:
                info = ydl.extract_info(url, download=False)
                metadata_list.append(info)
            except Exception as e:
                print(f"Error extracting metadata for {url}: {e}")

    return metadata_list

if __name__ == '__main__':
    video_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ]

    metadata = fetch_video_metadata(video_urls)
    output_file = "videos_metadata.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
