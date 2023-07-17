import os
import requests
from typing import Union, Optional, Tuple
from pathlib import Path
from bs4 import BeautifulSoup
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import src.utils as utils
from src.logger import logging
import src.config as config
from src.entity.episode import YoutubeEpisode
import scrapetube


YT_VIDEO_QUERY = "https://www.youtube.com/watch?v="

class Podcast:
    def __init__(self, url) -> None:
        self.url, self.name = utils.format_yt_podcast_url(url)


    def get_episodes_details(self, limit):

        logging.info(f"Getting {limit} episodes for : {self.url}")

        try :
            videos = scrapetube.get_channel(channel_url=self.url, limit=limit, 
                                            sort_by='newest', content_type='videos')
            
            episodes = []
            for video in videos:
                episode_title = video['title']['runs'][0]['text']
                episode_url = ''.join([YT_VIDEO_QUERY, video['videoId']])
                episode = YoutubeEpisode(url=episode_url, podcast_name=self.name,title=episode_title)

                episodes.append(episode)

            logging.info(f"Extraction successful. ")
            return episodes
        except Exception as e:
            logging.exception(e)
            logging.info("Extraction failed. Please check logs.")
            return None

    
