import sys
import os
import streamlit as st

current_dir = os.path.dirname(__file__)
backend_dir = os.path.abspath(os.path.join(current_dir, '..', 'back_end'))

sys.path.append(backend_dir)
print(sys.path)

import AudioTranscriber

# Streamlit UI
st.title("Audio to Text with Wav2Vec")

tokenizer, model = AudioTranscriber.load_model()

audio_file = st.file_uploader("Upload your audio file", type=['wav', 'mp3'])

if audio_file is not None:
    transcription = AudioTranscriber.transcribe_audio(audio_file, tokenizer, model)
    st.write("Transcription:", transcription)