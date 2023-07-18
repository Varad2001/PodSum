import os
import requests
from src.logger import logging
from src.exception import InvalidChannelURL
from urllib.parse import urlparse, parse_qs

def extract_domain_name(url: str) -> str:
    """
    Extracts the domain name from a given URL.

    Args:
        url (str): The URL to extract the domain name from.

    Returns:
        str: The domain name extracted from the URL.

    """

    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc

    if domain_name.startswith("www."):
        domain_name = domain_name[4:]

    return domain_name


def extract_yt_video_id(url):
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    try :
        video = query["v"][0]
        return video
    except KeyError as e:
        logging.info(f"Id not found. Invalid url : {url}")
        return None
    except Exception as e:
        logging.exception(e)
        return None
    

def format_yt_podcast_url(url : str):
    if 'featured' in url :
        url =  url.replace('/featured', '')
    elif 'videos' in url:
        url = url.replace('/videos', '')
    else :
        pass
    name = url.split('.com')[1]
    if '/c/' in name:
        name = name.replace('/c/' , '')
    elif '/@' in name:
        name = name.replace('/@', '')
    else :
        pass
    
    if name[-1] == '/':
        name = name[:-1]
    return url, name


def is_valid_channel(channel_url):
    try:
        response = requests.get(channel_url)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            # Handle other status codes if needed
            return False
    except requests.exceptions.RequestException:
        return False


def is_podcast_url_valid(url):
    domain = extract_domain_name(url)
    if not domain:
        return False, "Invalid domain name."

    if not 'youtube.com' in domain:
        return False, "Please enter URLs from Youtube only."

    url_path = urlparse(url).path
    if not ('/c/' in url_path or '/@' in url_path):
        return False, f"Invalid Youtube podcast name."
    
    if not is_valid_channel(url):
        return False, "Youtube podcast not found."

    return True, "success"
        

def split_transcripts(transcripts, duration_limit_in_sec):

    transcript_parts = []
    current_part = 1
    current_transcript = ''

    for transcript in transcripts:
        text = transcript['text'].replace('\n', ' ')

        if (transcript['start'] + transcript['duration']) > current_part * duration_limit_in_sec:
            print(f"Getting part number  : {current_part} ")
            transcript_parts.append(current_transcript)
            current_transcript = text
            current_part += 1

        else:
            current_transcript = ' '.join([current_transcript, text])

    print(f"Getting part number  : {current_part} ")
    transcript_parts.append(current_transcript)   

    return transcript_parts
