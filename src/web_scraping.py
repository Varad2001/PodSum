"""
FOR FUTURE SCOPE : PODCASTS FROM LISTENNOTES CAN BE ADDED ALONG WITH YOUTUBE
"""


import os
import requests
from typing import Union, Optional, Tuple
from pathlib import Path
from bs4 import BeautifulSoup
from pytube import YouTube
from src.logger import logging
from src.config import env_var


def get_podcast_from_yt(url: str, save_file_dir: Union[str, Path]) -> Optional[str] :
    """
    Downloads the audio from a YouTube video and saves it as an MP3 file.

    Args:
        url (str): The URL of the YouTube video.
        save_file_dir (Union[str, Path]): The directory to save the downloaded audio file.

    Returns:
        Optional[str]: The file path of the downloaded audio file if successful, otherwise None.
    """
     
    logging.info(f"\nGetting podcast from Youtube : {url}")

    try :
        # Create a YouTube object
        yt = YouTube(url)

        # Get the audio stream
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Get the audio title
        audio_title = audio_stream.title

        file_path = os.path.join(save_file_dir, f"{audio_title}.mp3")

        # create directory if not exists
        os.makedirs(save_file_dir, exist_ok=True)

        # Download the audio
        audio_stream.download(filename=file_path)

        logging.info(f"\nAudio downloaded successfully!")

        return file_path
    except Exception as e:
        logging.exception(e)
        return None
    

def get_audio_url(url : str, headers=env_var.headers) -> Optional[Tuple[str, str]] :
    """
    Retrieves the audio URL and title from a webpage.

    Args:
        url (str): The URL of the webpage.
        headers (dict): Headers to be sent with the GET request (default: config.headers).

    Returns:
         A tuple containing the audio URL and title if found, otherwise None.
    """

    logging.info(f"\nGetting audio url...")

    try:
        # Send a GET request with headers to fetch the HTML content
        response = requests.get(url, headers=headers)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the <div> element with the specified ID
        div_element = soup.find("div", id="episode-play-button-toolbar")

        # Extract the value of the 'data-audio' attribute
        if div_element:
            data_audio = div_element.get("data-audio")
            data_title = div_element.get("data-title")

            logging.info(f"\nFound audio url.")
            
            return data_audio, data_title
        else :
            logging.info("\nAudio source not found.")
            return None
    except Exception as e:
        logging.exception(e)
        return None
    

def download_audio(url : str, save_file_dir : Union[str, Path], 
                   filename, headers=env_var.headers) -> Optional[str] :
    """
    Downloads an audio file from the specified URL and saves it to the given directory.

    Args:
        url (str): The URL of the audio file.
        save_file_dir (Union[str, Path]): The directory to save the downloaded audio file.
        filename (str): The desired filename for the downloaded audio file.
        headers (dict): Headers to be sent with the GET request (default: config.headers).

    Returns:
        Optional[str]: The file path of the downloaded audio file if successful, otherwise None.

    """

    logging.info(f"\nDownloading the audio file : {url}")

    try :
        response = requests.get(url, headers=headers)

        save_file_path = os.path.join(save_file_dir, filename)

        # create directory if not exists
        os.makedirs(save_file_dir, exist_ok=True)

        with open(save_file_path, 'wb') as f:
            f.write(response.content)

        logging.info(f"\nDownload successful. Saved to {save_file_path}")

        return save_file_path
    except Exception as e:
        logging.exception(f"\nDownload failed. {str(e)}")
        return None


def get_podcast_from_listennote(url: str, save_file_dir: Union[Path, str]) -> Optional[str]:
    """
    Retrieves a podcast from Listen Notes and saves the audio file.

    Args:
        url (str): The URL of the podcast on Listen Notes website.
        save_file_dir (Union[Path, str]): The directory to save the downloaded audio file.

    Returns:
        Optional[str]: The file path of the downloaded audio file if successful, otherwise None.

    """
    logging.info(f"\nGetting podcast from listen note : {url}")

    try :
        data_audio_info = get_audio_url(url)

        if not data_audio_info:
            logging.info("\nFailed to retrieve the podcast.")
            return None

        audio_url, audio_title = data_audio_info

        audio_path = download_audio(url=audio_url, save_file_dir=save_file_dir, filename=f"{audio_title}.mp3")

        return audio_path
    except Exception as e:
        logging.exception(e)
        return None




