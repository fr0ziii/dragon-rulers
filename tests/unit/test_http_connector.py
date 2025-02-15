import unittest
import requests
from unittest.mock import patch
from src.connectors.http.http_connector import HttpConnector

class TestHttpConnector(unittest.TestCase):

    @patch('requests.get')
    def test_get_success(self, mock_get):
        # Configure the mock to return a successful response
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Success"

        connector = HttpConnector("https://example.com")
        response = connector.get("test")

        self.assertEqual(response, "Success")
        mock_get.assert_called_once_with("https://example.com/test", params=None)

    @patch('requests.get')
    def test_get_failure(self, mock_get):
        # Configure the mock to raise an exception
        mock_get.side_effect = requests.exceptions.RequestException("Error")

        connector = HttpConnector("https://example.com")
        response = connector.get("test")

        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()