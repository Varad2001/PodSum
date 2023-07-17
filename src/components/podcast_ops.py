from src.entity.podcast import Podcast
from src.entity.episode import YoutubeEpisode
import src.utils as utils
from src.config import env_var, mongo_client
from src.components import db_ops
from src.logger import logging


def save_podcast_data(client, url,  limit=env_var.MAX_NEW_EPISODES):
    
    url , _ = utils.format_yt_podcast_url(url)

    try :
        pod = db_ops.search_podcast_in_db(client,url)
    except Exception as e:
        logging.exception(e)
        return 0, f"Error searching podcast in database."


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
            msg = f"Podcast {podcast.name} and {limit} episodes saved to database."
            logging.info(msg)
            return 1, msg
        else:
            logging.info("Failed.")
            return 0, f"Failure performing database operations."
        
    else :

        logging.info(f"Podcast already in the database. Searching for new episodes...")

        podcast = Podcast(pod['podcast_url'])
        episode_urls = pod['episode_urls']

        episodes = podcast.get_episodes_details(limit=limit)
        
        new_videos_found = False
        results = []

        for episode in episodes:
            if not episode.episode_url in episode_urls :
                _ = episode.get_transcript()
                results.append(episode.to_dict())
                episode_urls.append(episode.episode_url)

                new_videos_found = True

        if not new_videos_found:
            msg = f'No new episodes found for podcast.'
            logging.info(msg)
            return 1, msg

        if db_ops.insert_episodes_to_db(client, results) and db_ops.update_podcast_info(client,podcast.url, episode_urls) :
            logging.info("New episodes saved successfully.")
            return 1, "New episodes saved successfully."
        else :
            logging.info('Failure')
            return 0, "Failure performing database operations."

    