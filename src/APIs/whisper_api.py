import whisper
import torch

class whisperAPI:
    def __init__(self, model="turbo"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model, device=self.device)
        print(f"Model ({model}) loaded on {self.device}")

    def transcribe_audio(self, audio_file, language="pt"):
        try:
            result = self.model.transcribe(audio_file, language=language)
            return result['text']
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
