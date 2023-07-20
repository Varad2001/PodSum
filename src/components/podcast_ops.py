from src.entity.podcast import Podcast
from src.entity.episode import YoutubeEpisode
import src.utils as utils
from src.config import env_var, mongo_client
from src.components import db_ops
from src.logger import logging


def update_one_podcast(client, old_podcast, limit=env_var.MAX_NEW_EPISODES):
    logging.info(f"Searching for new episodes for :{old_podcast['name']}")

    updated_podcast = Podcast(old_podcast['podcast_url'])
    current_episode_urls = old_podcast['episode_urls']

    new_episodes = updated_podcast.get_episodes_details(limit=limit)
    
    new_videos_found = False
    results = []

    for episode in new_episodes:
        if not episode.episode_url in current_episode_urls :
            
            tr = episode.get_transcript()

            if not tr:
                msg = f"Encounted problem with {episode.episode_url}"
                continue
            if tr == 'NA':
                msg = f"No transcripts were found for any of the requested language codes: {env_var.LANGUAGES}"
                continue

            results.append(episode.to_dict())
            current_episode_urls.append(episode.episode_url)

            new_videos_found = True

    if not new_videos_found:
        msg = f"{updated_podcast.name} : No new episodes found for podcast."
        logging.info(msg)
        return 1, msg

    if db_ops.insert_episodes_to_db(client, results) and db_ops.update_podcast_info(client,updated_podcast.url, current_episode_urls) :
        msg = f"{updated_podcast.name} : New episodes saved successfully."
        logging.info(msg)
        return 1, msg
    else :
        msg = f"{updated_podcast.name} :Failure"
        logging.info(msg)
        return 0, msg
    

def update_all_podcasts(client):
    
    logging.info(f"Updating all the available podcasts in the database....")
    try:
        podcasts = db_ops.get_all_podcasts(client=client)
        if len(podcasts) == 0:
            return 1, [f"No podcasts found in the database."]
    except Exception as e:
        logging.exception(e)
        return 0, [f"Could not retrieve the podcasts details."]
    
    msg_logs = []

    for podcast in podcasts:
        try:
            status, msg = update_one_podcast(client=client, old_podcast=podcast)
        except Exception as e:
            logging.exception(e)
            msg = f"Could not update the podcast : {podcast['name']}"

        msg_logs.append(msg)
    
    return 1, msg_logs


def add_podcast_to_db(client, url, limit=env_var.MAX_NEW_EPISODES):

    url , _ = utils.format_yt_podcast_url(url)

    try :
        pod = db_ops.search_podcast_in_db(client, url)
    except Exception as e:
        logging.exception(e)
        return 0, f"Error searching podcast in database."
    
    if pod:
        return 1, f"Podcast already in the database. ({url})"
    

    logging.info(f"No podcast exists. Creating new entry and saving {limit} number of episodes...")

    podcast = Podcast(url)
    episodes = podcast.get_episodes_details(limit=limit)

    msg = ''

    for episode in episodes :
        tr = episode.get_transcript()

        # if getting transcript fails, skip this episode
        if not tr:
            msg = f"Encounted problem with {episode.episode_url}"
            episodes.remove(episode)


    episodes_data = [epi.to_dict() for epi in episodes]
    episode_urls = [epi.episode_url for epi in episodes]

    if db_ops.insert_episodes_to_db(client, episodes_data) and db_ops.insert_podcast_info_to_db(client,
        {
            'podcast_url' : podcast.url,
            'episode_urls' : episode_urls,
            'name' : podcast.name
        }
        ):
        msg += f"{podcast.name} : Added to the database. Last {len(episode_urls)} episodes saved to database."
        logging.info(msg)
        return 1, msg
    else:
        logging.info("Failed.")
        return 0, f"Failure performing database operations."