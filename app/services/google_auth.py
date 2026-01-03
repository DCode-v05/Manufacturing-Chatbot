from google.oauth2 import service_account
import google.generativeai as genai

SERVICE_ACCOUNT_FILE = "service_account.json"

def init_gemini():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/generative-language"]
    )
    genai.configure(credentials=creds)
