import os
import time
import requests
import threading
import schedule
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from src.entity.PodcastDBManager import PodcastDBManager
from src.entity.podcast import Podcast
from src.entity.episode import YoutubeEpisode
from src.components.email_ops import send_email_with_json_attachment
from src.logger import logging
from src.config import env_var

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Hello</p>"

# route to keep server alive by sending requests every 10 mins
@app.route("/test", methods=['POST'])
def test():
    if request.method == 'POST':
        return jsonify({'status' : 200, 'msg' : 'success'})


@app.route("/check_fresh_episodes", methods=["POST"])
def check_fresh_episodes():
    if request.method == 'POST' :
        try:
            podcast_manager = PodcastDBManager(db_path=env_var.DB_NAME)

            fresh_episodes = []
            updated_podcasts = []
            # get all the podcasts in the database
            all_podcasts = podcast_manager.db.get_all_podcasts()
            for podcast_details in all_podcasts:
                podcast = Podcast(podcast_details[0])
                fresh_episodes += podcast_manager.get_fresh_episodes(podcast=podcast)
                # add details of the podcast to update in the  database
                updated_podcasts.append(zip(podcast, [epi.episode_url for epi in fresh_episodes]))

            # send the data to email
            if len(fresh_episodes) > 0 :
                data = [episode.to_dict() for episode in fresh_episodes]
                new_episodes = {'new_episodes' : data}
                # if data is sent successfully, update the database
                if send_email_to_user(user_email=env_var.RECEIVER_EMAIL, json_data=new_episodes):
                    for podcast, updated_urls in updated_podcasts:
                        podcast_manager.db.update_podcast(podcast.url, podcast.name, updated_urls)
                
            else:
                new_episodes = {'new_episodes' : None}
                send_email_to_user(user_email=env_var.RECEIVER_EMAIL, json_data=new_episodes)
            
        except Exception as e:
            logging.info(f"Error : {e}")
        


def send_email_to_user(user_email, json_data):
    try :
        sender_email = env_var.SENDER_EMAIL
        sender_pass = env_var.SENDER_PASSWORD
        send_email_with_json_attachment(
            sender_email=sender_email,
            sender_password=sender_pass,
            receiver_email=user_email,
            json_data=json_data
        )

        logging.info(f"Email sent successfully to : {user_email}")
        return True
    except Exception as e:
        logging.info(f"Error occurred : {e}")
        return False
    

if __name__ == '__main__':
    
    
    #t = threading.Thread(target=schedule_job)
    #t.start()
    app.run()
