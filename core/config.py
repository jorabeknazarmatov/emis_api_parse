import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

LOGIN = os.getenv("ONEID_LOGIN")
PASSWORD = os.getenv("ONEID_PASSWORD")

STATE_PATH = Path("oneid_state.json")  # сюда сохраняем cookies+storage
ONE_ID_URL = "https://id.egov.uz/uz"
TARGET_URL = "https://prof-emis.edu.uz/api/v2/auth/one-id/redirect/"
BASE_URL = "https://prof-emis.edu.uz/longs/groups"