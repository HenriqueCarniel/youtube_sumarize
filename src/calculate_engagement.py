import pandas as pd
import math

input_csv = "data/videos.csv"
output_csv = "data/dataset.csv"

def calculate_engagement(row, weight_of_likes, weight_of_comments):
    try:
        channel_follower_count = row["channel_follower_count"]
        channel_follower_count = 1 if channel_follower_count == 0 else channel_follower_count

        engagement = row["like_count"] * weight_of_likes + row["comment_count"] * weight_of_comments
        row["engagement"] = engagement / math.log10(channel_follower_count + 1)
    except Exception as e:
        print(f"Error processing video {row['video_id']}: {e}")
    return row

def categorize_engagement(row, q1, q2, q3, upper_whisker):
    engagement = row["engagement"]
    if engagement <= q1:
        row["engagement_category"] = 1
    elif engagement <= q2:
        row["engagement_category"] = 2
    elif engagement <= q3:
        row["engagement_category"] = 3
    elif engagement <= upper_whisker:
        row["engagement_category"] = 4
    else:
        row["engagement_category"] = 5
    return row

if __name__ == '__main__':
    df = pd.read_csv(input_csv)
    df = df[df["language"] == "pt"]

    df["like_count"] = pd.to_numeric(df["like_count"], errors="coerce").fillna(0).astype(int)
    df["comment_count"] = pd.to_numeric(df["comment_count"], errors="coerce").fillna(0).astype(int)
    df["channel_follower_count"] = pd.to_numeric(df["channel_follower_count"], errors="coerce").fillna(0).astype(int)

    total_likes = df["like_count"].astype(int).sum()
    total_comments = df["comment_count"].astype(int).sum()
    total_sample_engagement = total_likes + total_comments

    weight_of_likes = total_sample_engagement / (total_likes * 2)
    weight_of_comments = total_sample_engagement / (total_comments * 2)

    df = df.apply(calculate_engagement, axis=1, weight_of_likes=weight_of_likes, weight_of_comments=weight_of_comments)

    q1 = df["engagement"].quantile(0.25)
    q2 = df["engagement"].quantile(0.50)
    q3 = df["engagement"].quantile(0.75)
    upper_whisker = df["engagement"].quantile(0.95)

    df = df.apply(categorize_engagement, axis=1, q1=q1, q2=q2, q3=q3, upper_whisker=upper_whisker)

    df.to_csv(output_csv, index=False)

    print(f"Processed data saved to {output_csv}")
