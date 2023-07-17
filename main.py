import os
from src.web_scraping import get_podcast_from_listennote, get_podcast_from_yt
from src.audio_conversion import get_text_from_audio
from src.logger import logging
from src.entity.episode import YoutubeEpisode
from src import config
from src.utils import extract_domain_name

if __name__ == '__main__':
    url = input("Enter url :")

    domain = extract_domain_name(url)

    if 'youtube' in domain:
        episode = YoutubeEpisode(url)
        print(episode.get_transcript())
        exit()
    else :
        print("\nPlease enter urls from Youtube  only.")
        exit()

    


