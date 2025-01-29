import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CLOUD_BUCKET = os.getenv("CLOUD_BUCKET")
STAGE = os.getenv("STAGE")
XAI_API_KEY = os.getenv("XAI_API_KEY")
GITHUB_PAT = os.getenv("GITHUB_PAT")
