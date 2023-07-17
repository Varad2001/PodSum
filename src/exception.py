

class InvalidChannelURL(Exception):
    """Exception raised for invalid YouTube channel URLs."""

    def __init__(self, channel_url):
        self.channel_url = channel_url
        super().__init__(f"Invalid channel URL: {channel_url}")