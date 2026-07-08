from google.genai import Client
from decouple import config

def get_gemini_model():
    try:
        client = Client(api_key=config("GEMINI_KEY"))
    except Exception as e:
        raise e
    return client

