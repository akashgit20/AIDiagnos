import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import ffmpeg  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")

            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            # Convert to WAV with better compatibility
            wav_data = audio_data.get_wav_data(convert_rate=16000, convert_width=2)
            
            # Convert WAV data to an AudioSegment
            audio_segment = AudioSegment.from_raw(BytesIO(wav_data), sample_width=2, frame_rate=16000, channels=1)
            
            # Export as MP3
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to {file_path}")

    except sr.WaitTimeoutError:
        logging.error("Listening timed out while waiting for phrase to start.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Run the function
audio_file_path="patient_voice_test.mp3"
record_audio(file_path=audio_file_path)



# 2. Setup Speech to text-STT-model for transcription
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()  # Load .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#print("GROQ API Key:", GROQ_API_KEY)

sst_model="whisper-large-v3"
client=Groq(api_key=GROQ_API_KEY)

audio_file=open(audio_file_path, "rb")
transcription=client.audio.transcriptions.create(
    model=sst_model,
    file=audio_file,
    language="en"
)

print(transcription.text)