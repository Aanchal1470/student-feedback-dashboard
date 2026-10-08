import unittest
from app import app


class FeedbackAppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        response = self.app.get("/dashboard")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_data(self):
        response = self.app.get("/dashboard-data")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()