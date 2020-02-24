# Standard library imports
import unittest

# Third party imports
from sqlalchemy import exc

# Local app imports
from partyparser import create_app, db
from partyparser.models import CourtCase
from config import TestConfig


class WebInterfaceRoutesTests(unittest.TestCase):
    """Test suite for web interface endpoints"""

    # Before each test method
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    # After each test method
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_request_to_base_url(self):
        """Test sending GET request to base url returns 200 status code"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200, 'GET to / should return 200 status code')

    def test_get_to_index_url(self):
        """Test sending GET request to /index returns 200 status code"""
        res = self.client.get('/index')
        self.assertEqual(res.status_code, 200, 'GET to /index should return 200 status code')

if __name__ == '__main__':
    unittest.main(verbosity=2)
