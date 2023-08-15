import os
from src.entity.episode import Episode
from src.entity.podcast import Podcast
from src.entity.PodcastDB import PodcastDB
from src.logger import logging
from src.config import env_var
import src.utils as utils



class PodcastDBManager:
    def __init__(self, db_path: str):
        self.db = PodcastDB(db_path)
        self.db.create_table()


    def add_new_podcast(self, podcast_url: str):
        """
        Add a new podcast to the database using the podcast URL.

        Parameters:
            podcast_url (str): The URL of the podcast to be added.

        Returns:
            None
        """
        logging.info(f"Adding a new podcast with URL: {podcast_url}")
        podcast = Podcast(podcast_url)

        # Store the podcast details along with the list of fresh episodes in the database
        self.db.add_podcast(podcast.url, podcast.name, [])
        logging.info("Podcast added successfully to the database.")


    def get_fresh_episodes(self, podcast: Podcast):
        """
        Check for fresh episodes for a single podcast and store them in a list.

        Parameters:
            podcast (Podcast): The Podcast object for which to check for fresh episodes.

        Returns:
            list: A list of Episode objects representing the fresh episodes.
        """
        
        logging.info(f"Checking for fresh episodes for podcast: {podcast.name}")

        podcast_details = self.db.get_podcast(podcast.url)
        current_episode_urls = podcast_details[2]   # this is a str
        current_episode_urls = [url for url in current_episode_urls.split(',')]
        updated_podcast = Podcast(podcast.url)

        limit = env_var.MAX_NEW_EPISODES

        new_episodes = updated_podcast.get_episodes_details(limit=limit)
        fresh_episodes = []

        for new_episode in  new_episodes:
            if not new_episode.episode_url in current_episode_urls:
                transcript = new_episode.get_transcript()
                if not transcript or transcript == "NA":
                    continue
                summary = new_episode.get_summary()
                fresh_episodes.append(new_episode)
                current_episode_urls.append(new_episode.episode_url)

        return fresh_episodes
  
