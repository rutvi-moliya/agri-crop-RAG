import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  # loads .env into environment variables

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Check your .env file.")

genai.configure(api_key=GOOGLE_API_KEY)

print("Listing models available to your API key...\n")

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)
