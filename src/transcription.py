import csv
import os
from tqdm import tqdm
from APIs.yt_dlp_api import yt_dlpAPI
from APIs.whisper_api import whisperAPI

yt_dlp_api = yt_dlpAPI()
whisper_api = whisperAPI(model="turbo")

input_csv = "data/videos.csv"
output_csv = "data/videos_with_transcriptions.csv"

def process_video_row(row):
    try:
        if row["language"] == "pt" and not row["transcription"]:
            video_id = row["video_id"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            audio_file = yt_dlp_api.download_audio(video_url)
            transcription = whisper_api.transcribe_audio(audio_file, language="pt")
            row["transcription"] = transcription
            os.remove(audio_file)
    except Exception as e:
        print(f"Error processing video {row['video_id']}: {e}")
    return row

def update_csv_with_transcriptions(input_csv, output_csv):
    with open(input_csv, mode="r", encoding="utf-8") as infile, \
         open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        rows = list(reader)
        for row in tqdm(rows, total=len(rows), desc="Processing Videos"):
            updated_row = process_video_row(row)
            writer.writerow(updated_row)

if __name__ == "__main__":
    update_csv_with_transcriptions(input_csv, output_csv)
    print(f"Updated CSV with transcriptions: {output_csv}")
