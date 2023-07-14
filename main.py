import os
from src.web_scraping import get_podcast_from_listennote, get_podcast_from_yt
from src.audio_conversion import get_text_from_audio
from src.logger import logging
from src import config
from src.utils import extract_domain_name

if __name__ == '__main__':
    url = input("Enter url :")

    domain = extract_domain_name(url)

    if 'youtube' in domain:
        podcast_path = get_podcast_from_yt(url, config.PODCAST_AUDIO_DIR)
    elif 'listennotes' in domain:
        podcast_path = get_podcast_from_listennote(url, config.PODCAST_AUDIO_DIR)
    else :
        print("\nPlease enter urls from Youtube or Listennotes only.")
        exit()

    if not podcast_path:
        print(f"NO podcasts found.")
        exit()
    
    text = get_text_from_audio(podcast_path)

    if text:
        print("Transcript:")
        print(text)



