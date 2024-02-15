from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer
import soundfile as sf
import torch

class AudioTranscriber:
    @staticmethod
    def load_model():
        tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")
        model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
        return tokenizer, model

    @staticmethod
    def transcribe_audio(audio_file: str, tokenizer: Wav2Vec2Tokenizer, model: Wav2Vec2ForCTC) -> str:
        try:
            # Load the audio file
            audio_input, _ = sf.read(audio_file)
            # Process for model input
            input_values = tokenizer(audio_input, return_tensors="pt").input_values
            # Perform inference
            logits = model(input_values).logits
            # Decode the predicted ids
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = tokenizer.decode(predicted_ids[0], skip_special_tokens=True)
            return transcription
        except Exception as e:
            print(f"An error occurred: {e}")
            return ""


