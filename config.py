from dotenv import load_dotenv
import os

load_dotenv()


SQLITE_BASE_URL = os.getenv("SQLITE_BASE_URL")
APP_NAME = os.getenv("APP_NAME")
APP_VERSION = os.getenv("APP_VERSION")