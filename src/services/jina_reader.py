import sys
import requests

# Local imports
from src.logger import logging
from src.exception import CustomExceptionHandling


def fetch_data(url: str, token: str) -> str:
    """
    Fetch data from a given URL using Jina reader API.

    Args:
        - url (str): The URL to fetch data from.
        - token (str): The Bearer token for authorization.

    Returns:
        str: The response text from the URL if successful.
    """
    headers = {"Authorization": f"Bearer {token}"}

    try:
        logging.info(f"Fetching data from URL: {url}")

        # Send a GET request to the URL with the authorization header
        response = requests.get(f"https://r.jina.ai/{url}", headers=headers)

        # Check for non-successful status codes
        if response.status_code != 200:
            error_message = f"Failed to fetch data: Status {response.status_code} - {response.reason}"
            logging.error(error_message)
            raise CustomExceptionHandling(error_message, sys)

        logging.info(f"Received response with status code: {response.status_code}")

        # Return the response text if status is 200 OK
        return response.text

    # Handle exceptions that may occur during the request
    except Exception as e:
        # Custom exception handling
        raise CustomExceptionHandling(e, sys) from e
