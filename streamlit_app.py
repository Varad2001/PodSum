import os
import streamlit as st
from src.utils import extract_domain_name, is_valid_channel, is_podcast_url_valid
from src.entity.episode import YoutubeEpisode
from src.logger import logging
from src.components.podcast_ops import save_podcast_data
from src.components.db_ops import connect_db
from dotenv import load_dotenv

load_dotenv()

def text_extraction(urls, mongodb_url, limit=None):
    logging.info(f"\n{len(urls)} podcast urls received...\n")

    result = ''

    client = connect_db(mongodb_url=mongodb_url)
    if not client:
        return "FAILURE"
    
    
    for i, url in enumerate(urls):
        logging.info(f"\n>>>>>Processing url : {url}...")

        url_valid, msg = is_podcast_url_valid(url)
        if not url_valid:
            result = '\n'.join([result, f"{url} : ", msg])
            continue
        
        success, msg = save_podcast_data(client=client, url=url, limit=limit)
        if success:
            result = '\n'.join([result, f"{url} : ", msg])
        else:
            result = '\n'.join([result, f"{url} : ", msg])

    return result


# Set up the Streamlit interface
st.title("Audio Text Extraction")

# Input channel URLs
channel_urls = st.text_area("Enter Youtube Channel URLs (one per line)", "", height=200)

# Convert the input into a list of URLs
channel_url_list = channel_urls.split("\n")

mongodb_url = st.text_input("Enter the Mongodb URL:", type='password', value=os.environ.get("MONGODB_URL"))

limit = int(st.number_input("Enter the number of episodes to save:", min_value=1))

if st.button("Extract Text"):
    result = text_extraction(channel_url_list, mongodb_url, limit)
    st.write(result)

