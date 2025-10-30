# AIDiagnos
An intelligent multimodal AI assistant that listens to your voice, analyzes your uploaded image (such as a face or skin condition), and responds like a professional doctor — complete with text and spoken feedback.

This system combines speech recognition, image analysis, and text-to-speech synthesis using Groq’s Whisper and LLaMA Vision models, creating a seamless voice–vision–text interaction.

🚀 Features

🎙️ Speech-to-Text: Converts spoken input into text using Groq’s Whisper Large V3 model.

🩻 Image Understanding: Analyzes medical-related images using LLaMA 3.2 Vision via Groq API.

🧠 Doctor Simulation: Generates natural, human-like responses mimicking a doctor’s advice.

🔊 Voice Response: Converts AI’s medical feedback to speech using gTTS (Google Text-to-Speech).

🖼️ Interactive Gradio UI: Record voice, upload an image, and get spoken medical feedback—all in one app.

🧩 Tech Stack

Groq API – For LLaMA Vision and Whisper transcription.

Gradio – For the user-friendly web interface.

SpeechRecognition – For live voice capture.

pydub & gTTS – For text-to-speech audio generation.

dotenv – For secure environment variable management.

FFmpeg – For audio conversion.

📂 Project Structure
├── app.py                     # Main Gradio app script
├── .env                        # Stores your Groq API key
├── requirements.txt            # Python dependencies
├── final.mp3                   # Generated doctor voice output (runtime)
└── README.md                   # Documentation

⚙️ Setup Instructions
1. Clone the repository
git clone https://github.com/<your-username>/ai-doctor-vision-voice.git
cd ai-doctor-vision-voice

2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate       # For Linux/Mac
venv\Scripts\activate          # For Windows

3. Install dependencies
pip install -r requirements.txt

4. Create a .env file

Create a .env file in the root directory and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here


You can get your key from https://console.groq.com/keys

🧠 How It Works

🎤 Voice Input:
The user records a voice query (e.g., “I have a rash on my cheek, what could it be?”).

🔊 Speech Recognition (Groq Whisper):
The app converts your voice to text using the Whisper Large V3 model.

🖼️ Image Analysis (LLaMA Vision):
The uploaded image (like a selfie or skin photo) is analyzed by LLaMA 3.2 Vision for possible medical insights.

🩺 AI Doctor Reasoning:
The system combines the text + image context, prompting the model to respond as a concise, empathetic doctor.

🔈 Text-to-Speech:
The AI’s answer is synthesized into speech using gTTS, and played automatically.

🧩 Example Usage

Launch the app:

python app.py


In the Gradio interface:

Record your voice input (e.g., “I have red spots on my face, what could it be?”)

Upload a clear face image.

Click Submit.

The app will display:

Speech-to-Text output

Doctor’s textual response

Spoken voice reply

📦 Example requirements.txt
groq
gradio
gtts
pydub
SpeechRecognition
python-dotenv
ffmpeg-python

🧑‍⚕️ System Prompt Logic

The AI is instructed to behave like a professional doctor (for learning and simulation only, not real medical use).
It responds in two short sentences, no markdown or list format, and no disclaimers like “As an AI...”.

system_prompt = """
You have to act as a professional doctor, i know you are not but this is for learning purpose.
What's in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them. Don’t use numbers or bullet points.
Your answer should be concise (max 2 sentences) and human-like.
"""
