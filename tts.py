from gtts import gTTS
import os

def speak(text):
    if not text or text.strip() == "":
        return

    tts = gTTS(text=text, lang="en")
    audio_file = "speech.mp3"
    tts.save(audio_file)

    # plays sound
    os.system(f'start {audio_file}')  # Windows only