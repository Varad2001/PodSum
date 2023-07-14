import os

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