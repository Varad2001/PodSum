from src.entity.podcast import Podcast
from src.entity.episode import YoutubeEpisode
import src.utils as utils
from src.config import env_var, mongo_client
from src.components import db_ops
from src.logger import logging


def save_podcast_data(url, mongodb_url, limit=env_var.MAX_NEW_EPISODES):

    client = db_ops.connect_db(mongodb_url=mongodb_url)
    if not client:
        return 0

    try :
        pod = db_ops.search_podcast_in_db(client,url)
    except Exception as e:
        logging.exception(e)
        return 0


    # if the podcast is not present in the database
    if not pod: 

        logging.info(f"No podcast exists. Creating new entry and saving {limit} number of episodes...")

        podcast = Podcast(url)
        episodes = podcast.get_episodes_details(limit=limit)
        for episode in episodes :
            _ = episode.get_transcript()

        episodes_data = [epi.to_dict() for epi in episodes]
        episode_urls = [epi.episode_url for epi in episodes]

        if db_ops.insert_episodes_to_db(client, episodes_data) and db_ops.insert_podcast_info_to_db(client,
            {
                'podcast_url' : podcast.url,
                'episode_urls' : episode_urls,
                'name' : podcast.name
            }
            ):
            logging.info("Operation successful. ")
        else:
            logging.info("Failed.")
            return 0
        
    else :

        logging.info(f"Updating the database....")

        podcast = Podcast(pod['podcast_url'])
        episode_urls = pod['episode_urls']

        episodes = podcast.get_episodes_details(limit=limit)
        results = []
        for episode in episodes:
            if not episode.episode_url in episode_urls :
                _ = episode.get_transcript()
                results.append(episode.to_dict())
                episode_urls.append(episode.episode_url)

        if db_ops.insert_episodes_to_db(results) and db_ops.update_podcast_info(podcast.url, episode_urls) :
            logging.info("Operation successful.")
        else :
            logging.info('Failure')
            return 0

    return 1