import csv
from tqdm import tqdm
from APIs.yt_dlp_api import yt_dlpAPI
from multiprocessing import Pool

yt_dlp_api = yt_dlpAPI()
input_csv = "data/videos.csv"
output_csv = "data/videos_updated.csv"

def process_video_row(row):
    if len(row["timestamp_metadata"]) == 0:
        video_id = row["video_id"]
        metadata = yt_dlp_api.get_video_metadata(video_id)
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
