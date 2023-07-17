import os
import streamlit as st
from src.utils import extract_domain_name, is_valid_channel, is_podcast_url_valid
from src.entity.episode import YoutubeEpisode
from src.logger import logging
from src.components.podcast_ops import save_podcast_data

def text_extraction(url, mongodb_url, limit=None):
    url_valid, msg = is_podcast_url_valid(url)
    if not url_valid:
        return msg
    
    success = save_podcast_data(url=url, mongodb_url=mongodb_url,limit=limit)
    if success:
        return "Success. Details saved to database."
    else:
        return "Failed. Please check logs."


# Set up the Streamlit interface
st.title("Audio Text Extraction")

podcast_url = st.text_input("Enter the podcast URL:")
mongodb_url = st.text_input("Enter the Mongodb URL:", type='password')
limit = int(st.number_input("Enter the number of episodes to save:", min_value=1))
if st.button("Extract Text"):
    result = text_extraction(podcast_url, mongodb_url, limit)
    st.write(result)

