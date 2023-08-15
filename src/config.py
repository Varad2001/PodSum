import os
from dataclasses import dataclass
from dotenv import load_dotenv


class EnvironmentVariables:
    load_dotenv()

    PODCAST_TRANSCRIPT_DIR = os.path.join(os.getcwd(), 'data', 'podcast_transcripts')

    DATABASE_DIR = os.path.join(os.getcwd(), 'database')
    os.makedirs(DATABASE_DIR, exist_ok=True)

    DB_NAME = "podcasts.db"

    DB_PATH = os.path.join(DATABASE_DIR, DB_NAME)

    MAX_NEW_EPISODES = 1

    AVAILABLE_PLATFORMS = ['youtube']

    SPLIT_PART_DURATION = 70   # IN MINUTES

    LANGUAGES = ('en', 'en-US')

    RECEIVER_EMAIL = "mike@mihfinancial.ca"

    SENDER_EMAIL = "testingrecast@gmail.com"

    SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")


env_var = EnvironmentVariables()

