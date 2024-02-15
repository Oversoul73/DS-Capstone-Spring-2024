import sys
import os
import streamlit as st
from pymongo import MongoClient
import gridfs
import soundfile as sf
import io

# current_dir = os.path.dirname(__file__)
# backend_dir = os.path.abspath(os.path.join(current_dir, '..', 'back_end'))

# sys.path.append(backend_dir)
# print(sys.path)

# import AudioTranscriber

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
        

# Streamlit UI
st.title("Audio to Text with Wav2Vec")

tokenizer, model = AudioTranscriber.load_model()

audio_file = st.file_uploader("Upload your audio file", type=['wav', 'mp3'])

if audio_file is not None:
    transcription = AudioTranscriber.transcribe_audio(audio_file, tokenizer, model)
    st.write("Transcription:", transcription)

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['database_name']  # Adjust as per MongoDB setup
fs = gridfs.GridFS(db)

# Streamlit UI
st.title("Audio to Text with Wav2Vec")

# Load model
tokenizer, model = AudioTranscriber.load_model()

# Option to select an audio file from MongoDB
file_id = st.text_input("Enter MongoDB File ID for Transcription")

if file_id:
    audio_file = fs.find_one({'_id': file_id})
    if audio_file:
        audio_data = audio_file.read()
        transcription = AudioTranscriber.transcribe_audio(audio_data, tokenizer, model)
        st.write("Transcription:", transcription)
    else:
        st.write("File not found. Please check the File ID.")