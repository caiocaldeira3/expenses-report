import os
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent
ROOT_PATH = BASE_PATH
EXPENSES_PATH = ROOT_PATH / "expenses"
PDFS_PATH = ROOT_PATH / "pdf-expenses"
PROFILE_PATH = ROOT_PATH / "profile"

import dotenv

dotenv.load_dotenv(BASE_PATH / "service.env", override=False)


PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["LOCATION"]
PROCESSOR_ID = os.environ["PROCESSOR_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
PDF_MIME_TYPE = "application/pdf"
DOAI_KEY_PATH = ROOT_PATH / "google-secrets/doai-key.json"
SHEETS_API_KEY_PATH = ROOT_PATH / "google-secrets/sheet-api-key.json"
