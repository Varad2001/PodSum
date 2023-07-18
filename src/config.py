import os
from dataclasses import dataclass
from dotenv import load_dotenv
import pymongo


class EnvironmentVariables:
    load_dotenv()

    # Define headers for sending requests to urls
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
        # Add more headers as needed
        }


    PODCAST_AUDIO_DIR = os.path.join(os.getcwd(), 'data', 'podcast_files')
    PODCAST_TRANSCRIPT_DIR = os.path.join(os.getcwd(), 'data', 'podcast_transcripts')

    MODELS_DIR = os.path.join(os.getcwd(), 'models')

    # mongodb database details
    DB_NAME = "PODSUM"
    POD_INFO_COLLECTION_NAME = "PODCAST_INFO"
    POD_EPISODES_COLLECTION_NAME = "PODCAST_EPISODES"

    MAX_NEW_EPISODES = 5

    AVAILABLE_PLATFORMS = ['youtube', 'listennotes']

    SPLIT_PART_DURATION = 70   # IN MINUTES

    LANGUAGES = ('en', 'en-US')

env_var = EnvironmentVariables()
mongo_client = pymongo.MongoClient(os.environ.get('MONGODB_URL'))

