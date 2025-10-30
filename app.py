from groq import Groq
from dotenv import load_dotenv
import os
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import ffmpeg  
import base64
import subprocess
import platform
from gtts import gTTS
from pydub import AudioSegment
import gradio as gr


load_dotenv()  # Load .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def encode_image(image_path):
    image_file=open(image_path, "rb")
    return base64.b64encode(image_file.read()).decode('utf-8')


query="Is there something wrong with my face?"
model="llama-3.2-90b-vision-preview"
def analyze_image_with_query(query, model, encoded_image):
    client=Groq()
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        },
    ]

    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )
    return chat_completion.choices[0].message.content


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


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
sst_model="whisper-large-v3"
def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    
    client=Groq(api_key=GROQ_API_KEY)

    audio_file=open(audio_filepath, "rb")
    transcription=client.audio.transcriptions.create(
        model=sst_model,
        file=audio_file,
        language="en"
    )

    return transcription.text


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


system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath_mp3="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor

# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)