
import unittest
import json
from unittest.mock import patch
from app import app

class FeedbackAppTest(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 200)

    @patch("app.sqlite3.connect")
    def test_dashboard_data(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value

        mock_cursor.fetchone.return_value = (0,)
        mock_cursor.fetchall.return_value = []

        response = self.client.get("/dashboard-data")

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total"], 0)
        self.assertIn("ratings", data)

if __name__ == "__main__":
    unittest.main()
