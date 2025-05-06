import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from googletrans import Translator
from moviepy.editor import VideoFileClip, AudioFileClip  # Fixed missing import
import whisper
from gtts import gTTS

# Load environment variables from .env file
load_dotenv()

# API credentials from Telegram BotFather
API_ID = os.getenv("API_ID")  # Make sure this matches the variable name in your environment
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Pyrogram client
app = Client("telugu_video_translator_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Initialize Whisper (for audio transcription)
whisper_model = whisper.load_model("base")  # You can choose other models like 'small', 'medium'

# Initialize Google Translator
translator = Translator()

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply("Hi! Send me a video, and I'll translate the audio to Telugu.")

@app.on_message(filters.video)
def handle_video(client, message: Message):
    video_file = message.video.file_id
    video_path = app.download_media(video_file)

    try:
        # Extract audio from video using moviepy
        video = VideoFileClip(video_path)
        audio_path = "audio.wav"
        video.audio.write_audiofile(audio_path)

        # Use Whisper to transcribe the audio
        result = whisper_model.transcribe(audio_path)
        original_text = result['text']
        logging.info(f"Original Audio Transcription: {original_text}")

        # Translate the transcription to Telugu
        translated_text = translator.translate(original_text, src='en', dest='te').text
        logging.info(f"Translated Text (Telugu): {translated_text}")

        # Convert translated text to speech using gTTS
        tts = gTTS(translated_text, lang='te')
        translated_audio_path = "translated_audio.mp3"
        tts.save(translated_audio_path)

        # Overlay translated audio onto the video (using moviepy)
        final_video_path = "final_video_with_audio.mp4"
        final_video = VideoFileClip(video_path)
        translated_audio = AudioFileClip(translated_audio_path)
        final_video = final_video.set_audio(translated_audio)

        # Save the final video with Telugu audio
        final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac")

        # Send the final translated video back to the user
        message.reply_video(final_video_path)

        # Clean up temporary files
        os.remove(video_path)
        os.remove(audio_path)
        os.remove(translated_audio_path)
        os.remove(final_video_path)

    except Exception as e:
        logging.error(f"Error processing video: {e}")
        message.reply("Sorry, I encountered an error while processing the video. Please try again.")

# Start the bot
app.run()
