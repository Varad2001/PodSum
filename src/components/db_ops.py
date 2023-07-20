import os
import pymongo
from src.config import env_var
from src.logger import logging


def connect_db(mongodb_url):
    logging.info(f"Connecting to the database...")
    try :
        client = pymongo.MongoClient(host=mongodb_url, serverSelectionTimeoutMS=2000)
        client.server_info()
        logging.info(f"Connected successfully.")
        return client
    except pymongo.errors.ServerSelectionTimeoutError as e:
        #logging.exception(e)
        logging.info(f"Failed to connect : {str(e)}")
        return None


def search_podcast_in_db(mongo_client, podcast_url):

    logging.info(f"Searching for podcast url : {podcast_url}")
    
    db = mongo_client[env_var.DB_NAME]
    coll = db[env_var.POD_INFO_COLLECTION_NAME]

    pod = coll.find_one({'podcast_url' : podcast_url})
    
    return pod


def get_all_podcasts(client):
    db = client[env_var.DB_NAME]
    coll = db[env_var.POD_INFO_COLLECTION_NAME]

    pods = list(coll.find())

    return pods


def insert_episodes_to_db(mongo_client, episodes:list):

    logging.info(f"Inserting episodes to database....")

    try :
        db = mongo_client[env_var.DB_NAME]
        coll = db[env_var.POD_EPISODES_COLLECTION_NAME]

        coll.insert_many(episodes)

        logging.info(f"{len(episodes)} number of episodes inserted successfully.")
        return True
    except Exception as e:
        logging.exception(e)
        return False


def insert_podcast_info_to_db(mongo_client, podcast):

    logging.info(f"Inserting the podcast to database : {podcast['podcast_url']}")
    
    try :
        db = mongo_client[env_var.DB_NAME]
        coll = db[env_var.POD_INFO_COLLECTION_NAME]

        coll.insert_one(podcast)

        logging.info(f"Successful.")
        return True
    except Exception as e:
        logging.exception(e)
        return False


def update_podcast_info(mongo_client, pod_url, data):

    logging.info(f"Updating podcast info for : {pod_url}")

    try:
        db = mongo_client[env_var.DB_NAME]
        coll = db[env_var.POD_INFO_COLLECTION_NAME]

        coll.update_one(
            { 'podcast_url' : pod_url},
            {'$set' : {'episode_urls' : data}}
        )

        logging.info("Success.")
        return True
    except Exception as e:
        logging.exception(e)
        return False


