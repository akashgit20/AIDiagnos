# 1a. Setup Text to Speech-TTS-model with gTTS-->google text to speech
import os
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj=gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

#input_text="hii how are you!"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing.mp3")




# # 1b. Setup Text to Speech-TTS-model with ElevenLabs--free trial --
# import elevenlabs
# from elevenlabs.client import ElevenLabs
# from dotenv import load_dotenv
# import os
# from groq import Groq

# load_dotenv()  # Load .env file

# ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# #print("ELEVENLABS API Key:", ELEVENLABS_API_KEY)

# def text_to_speech_with_elevenlabs(input_text, output_filepath):
#     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
#     audio=client.generate(
#         text=input_text,
#         voice="Aria",
#         output_format="mp3_22050_32",
#         model="eleven_turbo_v2"
#     )
#     elevenlabs.save(audio, output_filepath)

# input_text="hii how are you!"
# text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing.mp3")




# 2. Use Model for Text output to voice
import subprocess
import platform
import os
from gtts import gTTS
from pydub import AudioSegment

def text_to_speech_with_gtts(input_text, output_filepath_mp3):
    language = "en"

    # Generate speech
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath_mp3)

    # Convert MP3 to WAV (Windows requires WAV for SoundPlayer)
    output_filepath_wav = output_filepath_mp3.replace(".mp3", ".wav")
    audio = AudioSegment.from_mp3(output_filepath_mp3)
    audio.export(output_filepath_wav, format="wav")

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath_wav])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath_wav}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath_wav])  # Alternative: 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

input_text = "Hi, how are you? I am fine, thank you."
text_to_speech_with_gtts(input_text, output_filepath_mp3="gtts_testing_autoplay.mp3")
