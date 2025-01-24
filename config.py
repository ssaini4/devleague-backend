import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
CLOUD_BUCKET = os.getenv("CLOUD_BUCKET")
STAGE = os.getenv("STAGE")
XAI_API_KEY = os.getenv("XAI_API_KEY")
GITHUB_PAT = os.getenv("GITHUB_PAT")
