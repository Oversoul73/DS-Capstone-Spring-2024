import torch
from transformers import BertForSequenceClassification, AutoTokenizer, Wav2Vec2ForCTC, Wav2Vec2Tokenizer
from transformers import Trainer, TrainingArguments
from sklearn.metrics import accuracy_score
import soundfile as sf
import logging
import librosa
import streamlit as st
from pydub import AudioSegment
import io
from io import BytesIO
import base64
from tempfile import NamedTemporaryFile
import tempfile
import os

# Dataset class for emotion classification
class EmotionDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Function to compute metrics for the model training
def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    acc = accuracy_score(labels, preds)
    return {'accuracy': acc}

# Function to predict emotion from text
def predict_emotion(text, model, tokenizer, device):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    predicted_label_index = logits.argmax(-1).item()
    label_map = {0: 'Sadness', 1: 'Joy', 2: 'Love', 3: 'Anger', 4: 'Fear', 5: 'Suprise'}
    predicted_label = label_map[predicted_label_index]

    return predicted_label

def speech_to_text(audio_path, recognizer, tokenizer):
    audio_input, sample_rate = librosa.load(audio_path, sr=16000)
    input_values = tokenizer(audio_input, return_tensors="pt", sampling_rate=sample_rate).input_values

    with torch.no_grad():
        logits = recognizer(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.decode(predicted_ids[0])
    return transcription

def load_models():
    # Load models and tokenizers
    speech_recognizer = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
    speech_tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")
    emotion_tokenizer = AutoTokenizer.from_pretrained('text_emotion_detection_model')
    emotion_model = BertForSequenceClassification.from_pretrained('text_emotion_detection_model', num_labels=6)

    # Move the emotion model to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    emotion_model = emotion_model.to(device)

    return speech_recognizer, speech_tokenizer, emotion_tokenizer, emotion_model, device

def save_temp_audio_file(data):
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio = AudioSegment.from_file(io.BytesIO(data), format="mp3")
        audio.export(temp_file.name, format="wav")
        temp_file_path = temp_file.name
        temp_file.close()  # Close the file handle but do not delete the file yet
        return temp_file_path
    except Exception as e:
        st.error(f"Failed to process audio file: {e}")
        return None

# def main():
#     # Load models and tokenizers
#     speech_recognizer = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")
#     speech_tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h")
#     emotion_tokenizer = AutoTokenizer.from_pretrained('text_emotion_detection_model')
#     emotion_model = BertForSequenceClassification.from_pretrained('text_emotion_detection_model', num_labels=6)

#     # Move the emotion model to GPU if available
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     emotion_model = emotion_model.to(device)

#     # Example for direct text input
#     text = "I am feeling very elated today!"
#     predicted_label = predict_emotion(text, emotion_model, emotion_tokenizer, device)
#     print(f"The predicted emotion from text is: {predicted_label}")

#     # Example for audio input
#     audio_path = '../database/Record.mp3'
#     recognized_text = speech_to_text(audio_path, speech_recognizer, speech_tokenizer)
#     print(f"Recognized text from audio: {recognized_text}")
#     predicted_label_from_audio = predict_emotion(recognized_text, emotion_model, emotion_tokenizer, device)
#     print(f"The predicted emotion from audio is: {predicted_label_from_audio}")

def app():
    st.title('EmotiSense')
    speech_recognizer, speech_tokenizer, emotion_tokenizer, emotion_model, device = load_models()

    input_type = st.radio("Select input type:", ("Text", "Audio File"))

    if input_type == "Text":
        text_input = st.text_area("Enter text here:")
        if st.button("Analyze Emotion"):
            if text_input:
                predicted_label = predict_emotion(text_input, emotion_model, emotion_tokenizer, device)
                st.write(f"The predicted emotion from text is: {predicted_label}")
            else:
                st.write("Please enter some text to analyze.")

    elif input_type == "Audio File":
        audio_files = os.listdir('../database/')
        audio_file = st.selectbox('Select an audio file:', audio_files)
        if audio_file:
            audio_path = os.path.join('../database/', audio_file)
            recognized_text = speech_to_text(audio_path, speech_recognizer, speech_tokenizer)
            st.write(f"Recognized text from audio: {recognized_text}")
            predicted_label_from_audio = predict_emotion(recognized_text, emotion_model, emotion_tokenizer, device)
            st.write(f"The predicted emotion from audio is: {predicted_label_from_audio}")

if __name__ == "__main__":
    app()
