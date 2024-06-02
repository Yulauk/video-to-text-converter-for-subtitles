from moviepy.editor import VideoFileClip
import speech_recognition as sr
from pydub import AudioSegment
import os
from googletrans import Translator


def video_to_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)


def recognize_speech_from_audio(audio_path, chunk_length=5):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    duration = len(audio) // 1000  # convert to seconds
    timestamps = []

    for i in range(0, duration, chunk_length):
        start = i * 1000
        end = start + (chunk_length * 1000)
        chunk = audio[start:end]
        chunk.export("template.wav", format="wav")

        with sr.AudioFile('template.wav') as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language='ru-RU')
                timestamps.append((i, text))
            except sr.UnknownValueError:
                timestamps.append((i, "[Unrecognized]"))
            except sr.RequestError as e:
                timestamps.append((i, f"[Error: {e}]"))

        os.remove("template.wav")

    return timestamps


def translate_text(text, dest_language='en'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_language)
    return translation.text


video_path = "/Users/macbook/PycharmProjects/audio_to_text/second_grilhouse.mp4"  # path to your video file
audio_path = "extracted_audio.wav"

# Extract audio from video
video_to_audio(video_path, audio_path)

# Recognize speech from audio with timestamps
timestamps = recognize_speech_from_audio(audio_path)

# Translate and print results
for timestamp in timestamps:
    original_text = timestamp[1]
    translated_text = translate_text(original_text)
    print(f"{timestamp[0]}s: {original_text} / {translated_text}")
