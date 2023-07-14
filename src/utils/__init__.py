import os


from urllib.parse import urlparse

def extract_domain_name(url: str) -> str:
    """
    Extracts the domain name from a given URL.

    Args:
        url (str): The URL to extract the domain name from.

    Returns:
        str: The domain name extracted from the URL.

    """

    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc

    if domain_name.startswith("www."):
        domain_name = domain_name[4:]

    return domain_name
