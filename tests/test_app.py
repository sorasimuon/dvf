import unittest
from src.app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app

    def test_home(self):
        """
        Check the text sends back Hello World
        """

        with self.app.test_client() as client:
            response = client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode('utf8'), "Hello World !!!")
