from gtts import gTTS

def speak_text(text):
    tts = gTTS(text=text)
    tts.save("static/response.mp3")
