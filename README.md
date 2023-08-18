# Podcast Monitor Project

The Podcast Monitor project is a web application that allows users to monitor and keep track of their favorite podcasts. The application periodically checks for new episodes of podcasts and sends notifications to the user via email when new episodes are available. It also provides a user interface for adding new podcasts to monitor and viewing the available podcasts.

## How to Run the Project

To run the Podcast Monitor project, follow these steps:

## Installation

Make sure to install Anaconda and git first.

1. Create a new Conda environment:

```
conda create -n podcast-summarizer python=3.9
conda activate podcast-summarizer
conda install pip
```

2. Clone the repository:

```
git clone https://github.com/your-username/podcast-summarizer.git
cd podcast-summarizer
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

## Update the settings

1. Set up the necessary environment variables:
   - Create a `.env` file in the project root directory.
   - Add the following environment variables to the `.env` file:
     - `OPENAI_API_KEY` : Api key for openai api
     - `SENDER_PASSWORD`: The password for the email account from which notifications will be sent.

    -  Add the following environment variables to the `src/config.py` file:
     - `DB_NAME`: The name of the SQLite database file to be used for storing podcast information (e.g., `podcasts.db`).
     - `RECEIVER_EMAIL`: The email address where notifications will be sent.
     - `SENDER_EMAIL` : The email address which will be used to send the email.


2. Run the Flask application by executing `python app.py`.
2. The Flask application will start, and you can access it by visiting `http://127.0.0.1:5000/` in your web browser.

## Working of the Project

The Podcast Monitor project has the following main functionalities:

1. **Adding a New Podcast**: Users can add a new podcast to the monitoring list by entering the podcast URL and clicking the "Submit" button. The application will check if the podcast is already in the database and add it if it is not already present.

2. **Checking for Fresh Episodes**: The application periodically checks for fresh episodes of the podcasts in the database. It retrieves the latest episodes of each podcast using the YouTube API and stores them in the database. If any new episodes are found, the application sends an email notification to the user with details of the new episodes.

3. **Viewing Available Podcasts**: Users can view the list of available podcasts that are currently being monitored. The list displays the name of each podcast along with its URL.

## API Routes and Their Working

1. `/add_new_podcast` (POST):
   - This route is used to add a new podcast to the database.
   - Parameters:
     - `podcast_urls` (list): The list of URLs of the podcasts to be added.
   - Working:
     - The route receives the `podcast_urls` parameter from the client's request.
     - Then for each URL, :
     - It checks if the podcast is already in the database using the `PodcastDBManager` class.
     - If the podcast is not present, it adds the podcast to the database using the `add_new_podcast` method of the `PodcastDBManager` class.
     - The route returns a JSON response with a success message if the podcast is added successfully, or a message indicating that the podcast is already available.

2. `/get_available_podcasts` (GET):
   - This route is used to retrieve the list of available podcasts from the database.
   - Working:
     - Fetches the list of available podcasts from the database using the `PodcastDB` class.
     - It then extracts the podcast names from the database and returns those in json format.

3. `/see_podcasts` (GET):
   - This route is used to render the `see_podcasts.html` template and display the list of available podcasts to the user.
   - Working:
     - The route sends a GET request to the `/get_available_podcasts` route to fetch the list of available podcasts from the database.
     - It extracts the podcast names from the JSON response and passes them to the `see_podcasts.html` template for rendering.

4. `/check_fresh_episodes` (POST):
   - This route is responsible for checking for fresh episodes of the podcasts in the database and sending email notifications to the user if new episodes are found.
   - Working:
     - The route receives a POST request from the client.
     - It creates an instance of the `PodcastDBManager` class and retrieves all podcasts from the database using the `get_all_podcasts` method.
     - For each podcast, it retrieves the latest episodes using the `get_fresh_episodes` method and checks if any new episodes are available.
     - If new episodes are found, it sends an email notification to the user with details of the new episodes using the `send_email_to_user` function.
     - If the email is sent successfully, it updates the database with the latest episode URLs using the `update_podcast` method of the `PodcastDB` class.


