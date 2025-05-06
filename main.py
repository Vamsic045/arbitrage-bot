import os
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from googletrans import Translator
from moviepy.editor import VideoFileClip, AudioFileClip
import whisper
from gtts import gTTS
import subprocess

# Load environment variables
load_dotenv()

# Configuration
API_ID = int(os.getenv("API_ID", 21232960))  # Fallback values for Render
API_HASH = os.getenv("API_HASH", "3b2158246c886c3ddc15f6c6b5912166")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7802388978:AAGs1K461PsA6CgzqXaucWj5HkpCZJfApyI")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize clients
app = Client(
    "translator_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Load models once at startup
whisper_model = whisper.load_model("base")
translator = Translator()

@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply("👋 Send me a video and I'll translate it to Telugu audio!")

@app.on_message(filters.video)
async def handle_video(client: Client, message: Message):
    try:
        # Download video
        video_path = await app.download_media(message.video.file_id)
        logger.info(f"Downloaded video to {video_path}")

        # Process video
        output_path = await process_video(video_path)
        
        # Send result
        await message.reply_video(
            output_path,
            caption="Here's your video with Telugu audio!"
        )
        logger.info("Sent processed video")

    except Exception as e:
        logger.error(f"Error processing video: {e}")
        await message.reply("❌ Error processing video. Please try again.")

async def process_video(video_path: str) -> str:
    """Process video and return output path"""
    # Extract audio
    audio_path = "audio.wav"
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

    # Transcribe
    result = whisper_model.transcribe(audio_path)
    original_text = result['text']
    logger.info(f"Original text: {original_text}")

    # Translate
    telugu_text = translator.translate(original_text, src='en', dest='te').text
    logger.info(f"Translated text: {telugu_text}")

    # Generate Telugu audio
    tts_path = "telugu_audio.mp3"
    tts = gTTS(telugu_text, lang='te')
    tts.save(tts_path)

    # Merge audio with video
    output_path = "output.mp4"
    telugu_audio = AudioFileClip(tts_path)
    final_video = video.set_audio(telugu_audio)
    final_video.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=4,  # Better for Render's environment
        preset='ultrafast'  # Faster processing
    )

    # Cleanup
    for file in [video_path, audio_path, tts_path]:
        if os.path.exists(file):
            os.remove(file)

    return output_path

if __name__ == "__main__":
    logger.info("Starting bot...")
    app.run()

