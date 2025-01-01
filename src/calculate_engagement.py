import pandas as pd

input_csv = "data/videos.csv"
output_csv = "data/videos_br.csv"

def calculate_engagement(row, weight_of_likes, weight_of_comments):
    try:
        row["engagement"] = int(row["like_count"]) * weight_of_likes + int(row["comment_count"]) * weight_of_comments
    except Exception as e:
        print(f"Error processing video {row['video_id']}: {e}")
    return row

if __name__ == '__main__':
    df = pd.read_csv(input_csv)
    df = df[df["language"] == "pt"]

    df["like_count"] = pd.to_numeric(df["like_count"], errors="coerce").fillna(0).astype(int)
    df["comment_count"] = pd.to_numeric(df["comment_count"], errors="coerce").fillna(0).astype(int)

    total_likes = df["like_count"].astype(int).sum()
    total_comments = df["comment_count"].astype(int).sum()
    total_sample_engagement = total_likes + total_comments

    weight_of_likes = total_sample_engagement / (total_likes * 2)
    weight_of_comments = total_sample_engagement / (total_comments * 2)

    df = df.apply(calculate_engagement, axis=1, weight_of_likes=weight_of_likes, weight_of_comments=weight_of_comments)

    df.to_csv(output_csv, index=False)

    print(f"Processed data saved to {output_csv}")
