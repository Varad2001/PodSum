import os
from dataclasses import dataclass
from dotenv import load_dotenv
import pymongo



def get_settings_from_mongodb(mongodb_url):
    client = pymongo.MongoClient(mongodb_url)
    db = client['PODSUM']
    config_collection = db['CONFIG']

    try:
        # Retrieve all documents from the 'config' collection
        config_documents = config_collection.find()

        # Update env_var with the settings from the retrieved documents
        for document in config_documents:
            for setting_name, setting_value in document.items():
                #setting_name = document['setting_name']
                #setting_value = document['setting_value']
                
                # Update env_var with the retrieved setting value
                setattr(env_var, setting_name, setting_value)

    except Exception as e:
        # If there's an error while fetching settings from the database,
        # use the locally defined settings instead
        print(f"Error fetching settings from MongoDB: {e}")

    finally:
        client.close()


class EnvironmentVariables:
    load_dotenv()


    def get_config_from_db(self,url):
        get_settings_from_mongodb(url)

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
    DB_NAME = "podcasts.db"

    MAX_NEW_EPISODES = 5

    AVAILABLE_PLATFORMS = ['youtube', 'listennotes']

    SPLIT_PART_DURATION = 70   # IN MINUTES

    LANGUAGES = ('en', 'en-US')

    SENDER_EMAIL = "testingrecast@gmail.com"

    SENDER_PASSWORD = "gxmjtehhqhdncolz"

    RECEIVER_EMAIL = "vktesting4@gmail.com"


env_var = EnvironmentVariables()
env_var.get_config_from_db(os.environ.get('MONGODB_URL'))
print(f"Config updated from database. Limit : {env_var.MAX_NEW_EPISODES}")
#get_settings_from_mongodb(os.environ.get("MONGODB_URL"))
#mongo_client = pymongo.MongoClient(os.environ.get('MONGODB_URL'))

