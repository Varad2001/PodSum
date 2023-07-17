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


class Episode:
    def __init__(self, url : str, podcast_name:str,title:str) -> None:
        self.episode_url = url
        self.episode_title = title
        self.podcast = podcast_name
        self.transcript = None


    def to_dict(self):
        return self.__dict__
    

class YoutubeEpisode(Episode):
    def __init__(self, url, podcast_name,title:str = None):
        super().__init__(url=url, podcast_name=podcast_name,title=title)

    
    def get_transcript(self):

        logging.info(f"Getting transcripts for episode : {self.episode_url}")

        try :
            id = utils.extract_yt_video_id(self.episode_url)

            if not id:
                return None

            transcripts = YouTubeTranscriptApi.get_transcript(id)
            result = ''
            for transcript in transcripts:
                result = ' '.join([result, transcript['text']])

            logging.info("Getting transcripts Successful.")
            
            self.transcript = result
            return result
        except Exception as e:
            logging.exception(e)
            logging.info("Failed to retrieve transcripts.")
            return None



if __name__ == '__main__':
    ep = Episode('sfsf')
    print(ep.__dict__)

