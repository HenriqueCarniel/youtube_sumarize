import whisper

class whisperAPI:
    def __init__(self, model="turbo"):
        self.model = whisper.load_model(model)

    def transcribe_audio(self, audio_file, language="pt"):
        try:
            result = self.model.transcribe(audio_file, language=language)
            return result['text']
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None