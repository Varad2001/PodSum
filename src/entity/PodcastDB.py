import sqlite3

class PodcastDB:
    def __init__(self, db_path: str):
        """
        Initialize the Podcast class with the path to the SQLite database.

        Parameters:
            db_path (str): The path to the SQLite database.

        Returns:
            None
        """
        self.db_path = db_path

    def create_table(self):
        """
        Create the 'podcasts' table in the database if it doesn't exist.

        Parameters:
            None

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS podcasts (
                    url TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    episode_urls TEXT NOT NULL
                )
            ''')

    def add_podcast(self, url: str, name: str, episode_urls: list):
        """
        Add a new podcast to the 'podcasts' table if not already .

        Parameters:
            url (str): The URL of the podcast (unique identifier).
            name (str): The name of the podcast.
            episode_urls (list): A list of episode URLs for the podcast.

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO podcasts (url, name, episode_urls) VALUES (?, ?, ?)', (url, name, ','.join(episode_urls)))

    def get_podcast(self, url: str) -> tuple:
        """
        Get the details of a specific podcast by its URL.

        Parameters:
            url (str): The URL of the podcast.

        Returns:
            tuple: A tuple containing the podcast details (url, name, episode_urls).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM podcasts WHERE url = ?', (url,))
            return cursor.fetchone()

    def get_all_podcasts(self) -> list:
        """
        Get the details of all podcasts in the 'podcasts' table.

        Parameters:
            None

        Returns:
            list: A list of tuples, each containing the podcast details (url, name, episode_urls).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM podcasts')
            return cursor.fetchall()

    def update_podcast(self, url: str, name: str, episode_urls: list):
        """
        Update the details of a specific podcast by its URL.

        Parameters:
            url (str): The URL of the podcast to be updated (unique identifier).
            name (str): The updated name of the podcast.
            episode_urls (list): A list of updated episode URLs for the podcast.

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE podcasts SET name = ?, episode_urls = ? WHERE url = ?', (name, ','.join(episode_urls), url))

    def delete_podcast(self, url: str):
        """
        Delete a specific podcast by its URL from the 'podcasts' table.

        Parameters:
            url (str): The URL of the podcast to be deleted (unique identifier).

        Returns:
            None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM podcasts WHERE url = ?', (url,))


if __name__ == "__main__":
    # Example usage:
    db_path = 'podcasts.db'
    podcast_manager = PodcastDB(db_path)
    podcast_manager.create_table()

    # Add a new podcast
    podcast_manager.add_podcast('Podcast Name', 'https://example.com/podcast', ['https://example.com/episode1', 'https://example.com/episode2'])

    # Get a specific podcast
    podcast = podcast_manager.get_podcast(1)
    print(podcast)

    # Get all podcasts
    all_podcasts = podcast_manager.get_all_podcasts()
    print(all_podcasts)

    # Update a podcast
    podcast_manager.update_podcast(1, 'Updated Podcast Name', 'https://example.com/updated-podcast', ['https://example.com/episode1', 'https://example.com/episode2', 'https://example.com/episode3'])

    # Delete a podcast
    podcast_manager.delete_podcast(1)
