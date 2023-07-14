import os
import streamlit as st
from src.utils import extract_domain_name
from src.web_scraping import get_podcast_from_yt, get_podcast_from_listennote
from src.audio_conversion import get_text_from_audio
import src.config as config
from src.logger import logging


def text_extraction(url):
    domain = extract_domain_name(url)

    if 'youtube' in domain:
        podcast_path = get_podcast_from_yt(url, config.PODCAST_AUDIO_DIR)
    elif 'listennotes' in domain:
        podcast_path = get_podcast_from_listennote(url, config.PODCAST_AUDIO_DIR)
    else:
        msg = "Please enter URLs from YouTube or Listen Notes only."
        logging.info(f"\n{msg}")
        return msg

    if not podcast_path:
        msg = "No podcasts found."
        logging.info(f"\n{msg}")
        return msg

    text = get_text_from_audio(podcast_path)

    if text:
        return text


# Set up the Streamlit interface
st.title("Audio Text Extraction")

url_input = st.text_input("Enter the podcast URL:")
if st.button("Extract Text"):
    result = text_extraction(url_input)
    st.write(result)

