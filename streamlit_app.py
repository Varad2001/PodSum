import os
import streamlit as st
import pymongo
from src.utils import is_podcast_url_valid
from src.entity.episode import YoutubeEpisode
from src.logger import logging
from src.components import podcast_ops
from src.components.db_ops import connect_db, get_all_podcasts
from src.config import env_var
from dotenv import load_dotenv

load_dotenv()


# Function to get or set MongoDB URL using SessionState
def get_or_set_mongodb_url():
    st.session_state.mongodb_url = st.text_input("Enter MongoDB URL:")
    return st.session_state.mongodb_url


# Function to reset session state and clear outputs
def clear_screen():
    st.experimental_rerun()


def get_tr_for_one(podcast_name, selected_episode, client):
    db = client[env_var.DB_NAME]
    episodes_collection = db[env_var.POD_EPISODES_COLLECTION_NAME]
    print(f"{podcast_name} : {selected_episode}")

    # Show button to view transcripts for the selected episode
    transcript_expander = st.expander(f"Transcripts for {selected_episode}")
    with transcript_expander:
        episode = episodes_collection.find_one({"podcast_name": podcast_name, "episode_title": selected_episode})
        transcripts = ''
        for t in episode['transcript']:
            transcripts = transcripts + ' ' + t

        if episode:
            st.write("Transcripts:")
            st.write(transcripts)
        else:
            st.warning("Episode not found in the database.")


# Function to get transcripts for episodes of a given podcast
def get_transcripts(client, podcast_name):
    db = client[env_var.DB_NAME]
    episodes_collection = db[env_var.POD_EPISODES_COLLECTION_NAME]

    # Query the episodes for the given podcast URL from the PODCAST_EPISODES collection
    episodes = episodes_collection.find({"podcast_name": podcast_name})
    
    # Display the podcast name and list of episodes
    st.write("")
    st.write(f"**Podcast Name: {podcast_name}**")
    
    episode_list = [episode["episode_title"] for episode in episodes]
    selected_episode = st.selectbox("Select an episode", episode_list)
    
    #if st.button("Get transcript"):

    # Show button to view transcripts for the selected episode
    transcript_expander = st.expander(f"Transcripts for : **{selected_episode}**")
    with transcript_expander:
        episode = episodes_collection.find_one({"podcast_name": podcast_name, "episode_title": selected_episode})
        transcripts = ''
        for t in episode['transcript']:
            transcripts = transcripts + ' ' + t

        if episode:
            st.write("Transcripts:")
            st.write(transcripts)
        else:
            st.warning("Episode not found in the database.")


# Function to see the list of podcasts available in the database
def see_podcasts(client):
    podcasts = get_all_podcasts(client)
    if len(podcasts) == 0:
        st.write("No podcasts found in the database.")
        return

    podcast_list = [podcast["name"] for podcast in podcasts]
    selected_podcast = st.selectbox("Select a podcast", podcast_list)


    #st.button("Set podcast", on_click=set_podcast, args=[selected_podcast])

    #if st.button("Get Episodes"):
    get_transcripts(client, selected_podcast)
        
# Streamlit app
def main():
    
    client = st.session_state.client

    st.title("Podcast Transcript Saver")
    option = st.selectbox("Select an option", ["Check Fresh Episodes", "Add Channel Name", "See Podcasts"])

    if option == "Check Fresh Episodes":
        if st.button("Check"):
            logs = podcast_ops.update_all_podcasts(client)[1]
            for log in logs:
                st.write(log)
    
    elif option == "Add Channel Name":
        channel_urls = st.text_area("Enter Channel URL", height=200)
        if st.button("Add Channel Name"):
            channel_urls = [url.strip() for url in channel_urls.splitlines()]
            for channel_url in channel_urls:
                logs = podcast_ops.add_podcast_to_db(client=client,
                                                    url=channel_url)
                st.write("Channel name added successfully!")
                st.write(logs[1])

    elif option == "See Podcasts":
        see_podcasts(client)

    else:
        pass


if __name__ == "__main__":


    if 'client' not in st.session_state:
        st.session_state.client = None
    if not st.session_state.client:
        st.title("MongoDB Connection Test")
        
        # Ask user to enter MongoDB URL
        mongodb_url = st.text_input("Enter MongoDB URL:", type='password')
        
        if st.button("Submit"):
            # Attempt to initialize MongoDB connection
            try:
                client = connect_db(mongodb_url)
                st.session_state.client = client
            except Exception as e:
                client = None

            if client is not None:
                # Connection successful, display the rest of the code
                st.success("Connected to the MongoDB database!")
                # Your further code here...
                main()
            else:
                # Connection failed, show error message
                st.error("Error: Failed to connect to the MongoDB database. Please enter a valid URL.")
    else :
        main()
    

