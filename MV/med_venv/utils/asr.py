import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid

def transcribe_audio(audio_file):
    # Convert uploaded audio to WAV format using pydub
    temp_filename = f"temp_{uuid.uuid4().hex}.wav"
    audio = AudioSegment.from_file(audio_file)
    audio.export(temp_filename, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_filename) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)

    os.remove(temp_filename)  # Clean up temp file
    return text
