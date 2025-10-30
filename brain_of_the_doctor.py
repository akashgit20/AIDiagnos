# 1. Setup GROQ API Key
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
#print("GROQ API Key:", GROQ_API_KEY)

# 2. Convert image to required format
import base64

image_path="acne.jpg"
image_file=open(image_path, "rb")
encoded_image=base64.b64encode(image_file.read()).decode('utf-8')


# 3. Setup Multimodal LLM
from groq import Groq

client=Groq()
query="Is there something wrong with my face?"
model="llama-3.2-90b-vision-preview"
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

print(chat_completion.choices[0].message.content)