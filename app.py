import os
import time
import requests
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from src.entity.PodcastDBManager import PodcastDBManager
from src.entity.PodcastDB import PodcastDB
from src.entity.podcast import Podcast
from src.entity.episode import YoutubeEpisode
from src.components.email_ops import send_email_with_json_attachment
from src.logger import logging
from src.config import env_var


app = Flask(__name__)
PORT = 10000


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check_fresh_episodes", methods=["POST"])
def check_fresh_episodes():
    if request.method == 'POST' :
        try:
            podcast_manager = PodcastDBManager(db_path=env_var.DB_PATH)

            fresh_episodes = []
            updated_podcasts = []
            # get all the podcasts in the database
            all_podcasts = podcast_manager.db.get_all_podcasts()
            for podcast_details in all_podcasts:
                podcast = Podcast(podcast_details[0])
                fresh_episodes += podcast_manager.get_fresh_episodes(podcast=podcast)
                # add details of the podcast to update in the  database
                updated_podcasts.append({
                    'podcast' : podcast,
                    'episodes' : [epi.episode_url for epi in fresh_episodes]
                    })

            # send the data to email
            if len(fresh_episodes) > 0 :
                data = [episode.to_dict() for episode in fresh_episodes]
                for episode in data:
                    del episode['transcript']

                new_episodes = {'new_episodes' : data}

                # if data is sent successfully, update the database
                if send_email_to_user(user_email=env_var.RECEIVER_EMAIL, json_data=new_episodes) :
                    for updated_podcast in updated_podcasts:
                        
                        podcast_to_be_updated = updated_podcast['podcast']
                        episode_urls_to_be_updated = updated_podcast['episodes']
                        podcast_manager.db.update_podcast(
                            podcast_to_be_updated.url, 
                            podcast_to_be_updated.name, 
                            episode_urls_to_be_updated)
                    
            else:
                new_episodes = {'new_episodes' : None}
                send_email_to_user(user_email=env_var.RECEIVER_EMAIL, json_data=new_episodes)
            
            return jsonify({'message': 'Successful.'}), 200
        except Exception as e:
            logging.info(f"Error : {e}")
            return jsonify({'message': f'Error. {str(e)}'}), 500
        


@app.route('/add_new_podcast', methods=['POST'])
def add_new_podcast():
    try:
        db_manager = PodcastDBManager(env_var.DB_PATH)
        data = request.json
        podcast_urls = data.get('podcast_urls')

        logging.info(f"Received urls : {podcast_urls}")

        for podcast_url in podcast_urls:
            logging.info(f"Processing url : {podcast_url}")

            # add the podcast if not already present
            if not db_manager.db.get_podcast(podcast_url):
                logging.info(f"Podcast not in the database. Adding ...")
                db_manager.add_new_podcast(podcast_url)

                #return jsonify({'message': 'Podcast added successfully.'}), 200
            else:
                logging.info("Podcast already available.")
                #return jsonify({'message': 'Podcast already available.'}), 200
        return jsonify({'message': 'Podcast added successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Error occurred. Please check the logs for details.'}), 500


@app.route('/get_available_podcasts', methods=['GET'])
def get_available_podcasts():
    try:
        db : PodcastDB = PodcastDB(env_var.DB_PATH)
        # Get the list of available podcasts from the database
        available_podcasts = db.get_all_podcasts()

        if not available_podcasts:
            return jsonify({'message': 'No podcasts found in the database.'}), 404

        # Format the response as a JSON object
        response = {'podcasts': available_podcasts}
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'message': 'Error occurred. Please check the logs for details.'}), 500



# following route has been added for html pages


@app.route('/see_podcasts', methods=['GET'])
def see_podcasts():
    # Send a GET request to the '/get_available_podcasts' route on the same machine
    response = requests.get(f'http://127.0.0.1:{PORT}/get_available_podcasts')

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the JSON data from the response
        response_data = response.json()

        # Process the JSON response to extract only the podcast names
        podcast_names = [podcast[1] for podcast in response_data["podcasts"]]

        # Render the "podcasts.html" template and pass the podcast_names to it
        return render_template("see_podcasts.html", podcast_names=podcast_names)
    elif response.status_code == 404:
        return "No podcasts found in the database."
    else:
        # If the request failed, return an error message
        return "Error: Failed to retrieve available podcasts"


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

    app.run(port=PORT, debug=True)
