import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from googletrans import Translator
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper
from gtts import gTTS

# Load environment variables from .env file
load_dotenv()

# Load API credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Pyrogram client
app = Client("telugu_video_translator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize Whisper model
whisper_model = whisper.load_model("base")

# Initialize Google Translator
translator = Translator()

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply("👋 Hi! Send me a video, and I’ll translate its audio to Telugu for you.")

@app.on_message(filters.video)
def handle_video(client, message: Message):
    video_file = message.video.file_id
    video_path = app.download_media(video_file)
    logging.info(f"Downloaded video to: {video_path}")

    try:
        # Extract audio from video
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path)

        # Transcribe audio with Whisper
        result = whisper_model.transcribe(audio_path)
        original_text = result['text']
        logging.info(f"Original Transcription: {original_text}")

        # Translate to Telugu
        translated_text = translator.translate(original_text, src='en', dest='te').text
        logging.info(f"Translated Text (Telugu): {translated_text}")

        # Text-to-speech in Telugu
        tts = gTTS(translated_text, lang='te')
        translated_audio_path = "translated_audio.mp3"
        tts.save(translated_audio_path)

        # Overlay translated audio onto the video
        final_video_path = "final_output.mp4"
        translated_audio = AudioFileClip(translated_audio_path)
        final_video = video.set_audio(translated_audio)
        final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac")

        # Send translated video back to user
        message.reply_video(final_video_path, caption="✅ Here's your translated video in Telugu!")

    except Exception as e:
        logging.error(f"Error: {e}")
        message.reply("⚠️ Sorry, something went wrong while processing your video.")
    finally:
        # Clean up
        for f in [video_path, audio_path, translated_audio_path, final_video_path]:
            if os.path.exists(f):
                os.remove(f)

# Run the bot
app.run()
