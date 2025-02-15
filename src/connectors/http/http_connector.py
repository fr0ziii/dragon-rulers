import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class HttpConnector:
    """
    A basic HTTP connector for fetching data.
    """

    def __init__(self, base_url: str):
        """
        Initializes the connector with a base URL.
        """
        self.base_url = base_url
        logging.info("HttpConnector initialized with base URL: {}".format(self.base_url))

    def get(self, endpoint: str, params: dict = None):
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): Query parameters. Defaults to None.

        Returns:
            The response text if the request was successful, otherwise None.
        """
        try:
            url = f"{self.base_url}/{endpoint}"
            logging.info("Sending GET request to: {} with params: {}".format(url, params))
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            logging.info("Request to {} successful".format(url))
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during request: {e}")
            return None

    def post(self, endpoint: str, data: dict, params: dict = None):
        """Sends a POST request."""
        return self._request('post', endpoint, params, data)

    def put(self, endpoint: str, data: dict, params: dict = None):
        """Sends a PUT request."""
        return self._request('put', endpoint, params, data)

    def delete(self, endpoint: str, params: dict = None):
        """Sends a DELETE request."""
        return self._request('delete', endpoint, params)

    def _request(self, method: str, endpoint: str, params: dict = None, data: dict = None):
        """Helper function to handle requests."""
        try:
            url = f"{self.base_url}/{endpoint}"
            logging.info(f"Sending {method.upper()} request to: {url} with params: {params}, data: {data}")
            response = requests.request(method, url, params=params, json=data)
            response.raise_for_status()
            logging.info(f"Request to {url} successful")
            return response.text
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error during request to {url}: {e}")
            return None
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error during request to {url}: {e}")
            return None
        except requests.exceptions.Timeout as e:
            logging.error(f"Timeout error during request to {url}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during request to {url}: {e}")
            return None