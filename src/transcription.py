from APIs.yt_dlp_api import yt_dlpAPI
from APIs.whisper_api import whisperAPI

yt_dlp_api = yt_dlpAPI()
whisper_api = whisperAPI(model="turbo")

def save_transcription(transcription, video_id):
    try:
        file_name = f"transcription_{video_id}.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(transcription)
        print(f"Transcript saved in {file_name}")
    except Exception as e:
        print(f"Error saving transcript: {e}")

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=8pztmXSiHvw"

    print("Downloading audio from video...")
    audio_file = yt_dlp_api.download_audio(video_url)

    if audio_file:
        print(f"Audio downloaded successfully: {audio_file}")
        print("Transcribing the audio...")
        transcription = whisper_api.transcribe_audio(audio_file, language="pt")
        
        if transcription:
            print("Transcription completed.")
            video_id = video_url.split("v=")[-1]
            save_transcription(transcription, video_id)
        else:
            print("Error transcribing audio.")
    else:
        print("Error downloading audio.")
