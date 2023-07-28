import os
from typing import List
from youtube_transcript_api import YouTubeTranscriptApi
import src.utils as utils
from src.logger import logging
from src.entity.episode import YoutubeEpisode
import scrapetube


YT_VIDEO_QUERY = "https://www.youtube.com/watch?v="


class Podcast:
    def __init__(self, url: str) -> None:
        """
        Initialize a Podcast object.

        Parameters:
            url (str): The URL of the podcast.

        Returns:
            None
        """
        self.url, self.name = utils.format_yt_podcast_url(url)


    def get_episodes_details(self, limit: int) -> List[YoutubeEpisode]:
        """
        Get details of episodes for the podcast.

        Parameters:
            limit (int): The maximum number of episodes to retrieve.

        Returns:
            List[YoutubeEpisode]: A list of YoutubeEpisode objects representing the episodes.
        """
        logging.debug(f"Getting {limit} episodes for : {self.url}")

        try:
            # Scrape videos from the channel URL
            videos = scrapetube.get_channel(channel_url=self.url, limit=limit, sort_by='newest', content_type='videos')

            episodes = []
            for video in videos:
                episode_title = video['title']['runs'][0]['text']
                episode_url = ''.join([YT_VIDEO_QUERY, video['videoId']])
                episode = YoutubeEpisode(url=episode_url, podcast_name=self.name, title=episode_title)

                episodes.append(episode)

            logging.debug(f"Extraction successful. ")
            return episodes
        except Exception as e:
            logging.exception(e)
            logging.info("Extraction failed. Please check logs.")
            return None
