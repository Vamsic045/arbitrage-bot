from pyrogram import Client, filters
import whisper
from googletrans import Translator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip
import os

API_ID = 123456    # Your API ID
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

app = Client("telugu_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

model = whisper.load_model("base")
translator = Translator()

@app.on_message(filters.video)
def handle_video(client, message):
    # File names
    file_id = message.video.file_unique_id
    video_path = f"downloaded_videos/{file_id}.mp4"
    audio_path = f"translated_videos/audio_{file_id}.mp3"
    final_path = f"translated_videos/final_{file_id}.mp4"

    # Download video
    message.download(video_path)

    # Transcribe speech from video
    result = model.transcribe(video_path)
    text = result["text"]

    # Translate to Telugu
    translated_text = translator.translate(text, dest='te').text

    # Convert translated text to Telugu speech
    tts = gTTS(translated_text, lang='te')
    tts.save(audio_path)

    # Merge Telugu audio into original video
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final_video = video.set_audio(audio)
    final_video.write_videofile(final_path, codec='libx264', audio_codec='aac')

    # Send final video back to user
    message.reply_video(final_path)

app.run()
