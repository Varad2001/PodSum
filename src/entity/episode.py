import os
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import src.utils as utils
from src.logger import logging
from src.config import env_var


class Episode:
    def __init__(self, url: str, podcast_name: str, title: str) -> None:
        """
        Initialize an Episode object.

        Parameters:
            url (str): The URL of the episode.
            podcast_name (str): The name of the podcast to which the episode belongs.
            title (str): The title of the episode.

        Returns:
            None
        """
        self.episode_url = url
        self.episode_title = title
        self.podcast_name = podcast_name
        self.transcript = None

    def to_dict(self):
        """
        Convert the Episode object to a dictionary.

        Parameters:
            None

        Returns:
            dict: A dictionary representation of the Episode object.
        """
        return self.__dict__


class YoutubeEpisode(Episode):
    def __init__(self, url: str, podcast_name: str, title: Optional[str] = None):
        """
        Initialize a YoutubeEpisode object.

        Parameters:
            url (str): The URL of the episode.
            podcast_name (str): The name of the podcast to which the episode belongs.
            title (Optional[str]): The title of the episode.

        Returns:
            None
        """
        super().__init__(url=url, podcast_name=podcast_name, title=title)

    def get_transcript(self):
        """
        Get the transcript of the Youtube episode.

        Parameters:
            None

        Returns:
            Union[str, None]: The transcript of the episode if available, or "NA" if not found or disabled.
        """
        logging.debug(f"Getting transcripts for episode : {self.episode_url}")

        try:
            video_id = utils.extract_yt_video_id(self.episode_url)

            if not video_id:
                return None

            try:
                transcripts = YouTubeTranscriptApi.get_transcript(video_id, env_var.LANGUAGES)
            except NoTranscriptFound as e:
                return "NA"
            except TranscriptsDisabled as e:
                return "NA"

            result = utils.split_transcripts(transcripts, env_var.SPLIT_PART_DURATION * 60)

            logging.debug("Getting transcripts Successful.")

            self.transcript = result
            return result
        except Exception as e:
            logging.exception(e)
            logging.info("Failed to retrieve transcripts.")
            return None
