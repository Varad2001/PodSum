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
            result =  result + '\n' + f"{url} : {msg}" 
            continue
        
        success, msg = save_podcast_data(client=client, url=url, limit=limit)
        if success:
            result =  result + '\n' + f"{url} : {msg}" 
        else:
            result =  result + '\n' + f"{url} : {msg}" 

    return result


# Set up the Streamlit interface
st.title("Audio Text Extraction")

# Input channel URLs

# Youtube
yt_channel_urls = st.text_area("Enter Youtube Channel URLs (one per line)", "", height=200)

# Listennotes
#ln_channel_urls = st.text_area("Enter Listennotes Channel URLs (one per line)", "", height=200)

# Convert the input into a list of URLs
yt_channel_url_list = yt_channel_urls.split("\n")
#ln_channel_url_list = ln_channel_urls.split("\n")

#channel_urls = {
#    'Youtube' : yt_channel_url_list,
#    'Listennotes' : ln_channel_url_list
#}

mongodb_url = st.text_input("Enter the Mongodb URL:", type='password')

limit = int(st.number_input("Enter the number of episodes to save:", min_value=1))

if st.button("Extract Text"):
        
    result = text_extraction(yt_channel_url_list, mongodb_url, limit)
    st.write(result)

