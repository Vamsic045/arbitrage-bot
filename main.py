import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from googletrans import Translator
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper
from gtts import gTTS

# Load .env variables
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

# Start bot
app = Client("translator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Load models
whisper_model = whisper.load_model("base")
translator = Translator()

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply("👋 Send me a video and I will send it back with Telugu audio!")

@app.on_message(filters.video)
def handle_video(client, message: Message):
    video_file = message.video.file_id
    video_path = app.download_media(video_file)

    try:
        # Extract audio
        video = VideoFileClip(video_path)
        audio_path = "audio.wav"
        video.audio.write_audiofile(audio_path)

        # Transcribe
        result = whisper_model.transcribe(audio_path)
        original_text = result['text']
        logging.info(f"Transcribed: {original_text}")

        # Translate
        telugu_text = translator.translate(original_text, src='en', dest='te').text
        logging.info(f"Translated: {telugu_text}")

        # Convert to speech
        tts = gTTS(telugu_text, lang='te')
        tts_path = "telugu_audio.mp3"
        tts.save(tts_path)

        # Merge new audio
        telugu_audio = AudioFileClip(tts_path)
        final_video = video.set_audio(telugu_audio)
        output_path = "output.mp4"
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Send back
        message.reply_video(output_path)

        # Clean up
        os.remove(video_path)
        os.remove(audio_path)
        os.remove(tts_path)
        os.remove(output_path)

    except Exception as e:
        logging.error(f"Error: {e}")
        message.reply("❌ Error occurred while processing the video.")

# Run bot
app.run()

