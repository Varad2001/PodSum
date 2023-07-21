import os
from flask import Flask, jsonify, request
import requests
from dotenv import load_dotenv
from src.components.podcast_ops import update_all_podcasts
from src.components.db_ops import connect_db
from src.logger import logging

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Hello</p>"


@app.route("/test", methods=['POST'])
def test():
    if request.method == 'POST':
        return jsonify({'status' : 200, 'msg' : 'success'})


def job():
    load_dotenv()
    mongo_url = os.environ.get("MONGODB_URL")
    if not mongo_url :
        logging.info(f"Mongodb url not found.")
        return

    client = connect_db(mongo_url)
    if not client:
        logging.info("Failed to connect to the database.")
        return

    status, msg = update_all_podcasts(client)
    logging.info(msg)

    logging.info("Database updated successfully.")


def schedule_job():
    import time
    time.sleep(5)
    print("Starting the schedule job....")
    import schedule

    schedule.every(60).seconds.do(job)

    i = 0
    while i < 50:
        print("Checking pending jobs...")
        i+=1
        schedule.run_pending()
        time.sleep(20)


if __name__ == '__main__':
    import threading
    
    t = threading.Thread(target=schedule_job)
    t.start()
    app.run()
