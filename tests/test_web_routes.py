# Standard library imports
import unittest

# Third party imports
from flask_testing import TestCase

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
        db.create_all()

    # After each test method
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Helper method
    def seed_db(self):
        mock_data = [
            CourtCase(plaintiff='John Doe', defendant='Jane Doe'),
            CourtCase(plaintiff='Frank Zappa', defendant='Eric Clapton')
        ]
        db.session.add_all(mock_data)
        db.session.commit()

    def test_get_request_to_base_url(self):
        """Test GET request to base url returns 200 status code"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200,
                         'GET to / should return 200 status code')

    def test_get_request_to_index(self):
        """Test GET request to index returns 200 status code"""
        res = self.client.get('/index')
        self.assertEqual(res.status_code, 200,
                         'GET to / should return 200 status code')

    def test_post_request_to_index(self):
        """Test POST request to index returns 405 status code"""
        res = self.client.post('/index', data={})
        self.assertEqual(res.status_code, 405)

    def test_get_to_web_cases(self):
        """Test GET to /web/cases returns all courtcases in context variable"""
        self.seed_db()
        db_cases = CourtCase.query.all()
        res = self.client.get('/web/cases')
        self.assertEqual(res.status_code, 200,
                         'GET to /web/cases should return 200 status code')
        self.assert_template_used('index.html')
        self.assertEqual(self.get_context_variable('cases'), db_cases)

    def test_get_to_web_cases_id(self):
        """Test GET to /web/cases/<int:case_id> returns single case"""
        self.seed_db()
        case_id = 2
        db_case = CourtCase.query.get(case_id)
        print(db_case)
        res = self.client.get('/web/cases/{}'.format(case_id))
        self.assertEqual(res.status_code, 200,
                         'GET to /web/cases/2 returns 200 status code')
        self.assert_template_used('index.html')
        self.assertEqual(self.get_context_variable('cases'), db_case)


if __name__ == '__main__':
    unittest.main(verbosity=2)
