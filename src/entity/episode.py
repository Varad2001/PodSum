import os
import requests
from typing import Union, Optional, Tuple
from pathlib import Path
from bs4 import BeautifulSoup
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from src.web_scraping import get_podcast_from_listennote
from src.audio_conversion import get_text_from_audio
import src.utils as utils
from src.logger import logging
from src.config import env_var


class Episode:
    def __init__(self, url : str, podcast_name:str,title:str) -> None:
        self.episode_url = url
        self.episode_title = title
        self.podcast_name = podcast_name
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

            try :
                transcripts = YouTubeTranscriptApi.get_transcript(id, env_var.LANGUAGES)
            except NoTranscriptFound as e:
                logging.exception(e)
                return "NA"
            result = utils.split_transcripts(transcripts, env_var.SPLIT_PART_DURATION * 60)
            
            logging.info("Getting transcripts Successful.")
            
            self.transcript = result
            return result
        except Exception as e:
            logging.exception(e)
            logging.info("Failed to retrieve transcripts.")
            return None


class ListenNoteEpisode(Episode):
    def __init__(self, url, podcast_name,title:str = None):
        super().__init__(url=url, podcast_name=podcast_name,title=title)
        
        self.podcast_dir = os.path.join(env_var.PODCAST_AUDIO_DIR, self.podcast_name)
        self.audio_file_path = None


    def get_transcript(self):
        
        try:
            audio_path = get_podcast_from_listennote(self.episode_url, self.podcast_dir)
            
            if not audio_path:
                return None
            
            self.audio_file_path = audio_path
            tr = get_text_from_audio(self.audio_file_path)

            if not tr:
                return None
            
            self.transcript = tr

            logging.info("Getting transcripts Successful.")

            return self.transcript
        except Exception as e:
            logging.exception(e)
            logging.info("Failed to retrieve transcripts.")
            return None



if __name__ == '__main__':
    ep = Episode('sfsf')
    print(ep.__dict__)

