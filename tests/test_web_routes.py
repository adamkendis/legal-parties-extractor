# Standard library imports
import unittest

# Third party imports
from flask_testing import TestCase
from sqlalchemy import exc

# Local app imports
from partyparser import create_app, db
from partyparser.models import CourtCase
from config import TestConfig


class WebInterfaceRoutesTests(TestCase):
    """Test suite for web interface endpoints"""

    render_templates = False

    def create_app(self):
        return create_app(TestConfig)

    # Before each test method
    def setUp(self):
        self.mock_data = [
            {'id': 1, 'plaintiff': 'John Doe', 'defendant': 'Jane Doe'},
            {'id': 2, 'plaintiff': 'Frank Zappa', 'defendant': 'Eric Clapton'}
        ]
        db.create_all()

    # After each test method
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_request_to_base_url(self):
        """Test sending GET request to base url returns 200 status code"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200, 'GET to / should return 200 status code')

    def test_get_request_to_index(self):
        """Test sending GET request to index returns 200 status code"""
        res = self.client.get('/index')
        self.assertEqual(res.status_code, 200, 'GET to / should return 200 status code')

    def test_post_request_to_index(self):
        """Test sending POST request to index returns 405 status code"""
        res = self.client.post('/index', data={})
        self.assertEqual(res.status_code, 405)

    def test_get_to_web_cases(self):
        """Test sending GET request to /web/cases returns all courtcases stored in db"""
        res = self.client.get('/web/cases')
        self.assertEqual(res.status_code, 200, 'GET to /web/cases should return 200 status code')
        self.assert_template_used('index.html')
        self.assertTrue('John Doe' and 'Jane Doe' in res.body)
        self.assertTrue('Frank Zappa' and 'Eric Clapton' in res.body)


if __name__ == '__main__':
    unittest.main(verbosity=2)
