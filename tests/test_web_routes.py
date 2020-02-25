# Standard library imports
import unittest
from os import path, remove
import time

# Third party imports
from flask_testing import TestCase
from xml.etree import ElementTree as ET

# Local app imports
from partyparser import create_app, db
from partyparser.models import CourtCase
from partyparser.helpers import verify_file_type
from config import TestConfig


class WebInterfaceRoutesTests(TestCase):
    """Test suite for web interface endpoints"""

    # Templates are tested via self.assert_template_used('template_name')
    render_templates = False

    def create_app(self):
        return create_app(TestConfig)

    # Setup before each test method
    def setUp(self):
        self.test_file = 'test_file.xml'
        self.uploads_dir = path.join(self.app.root_path, 'uploads')
        self.test_file_path = path.join(self.uploads_dir, self.test_file)
        db.create_all()
        self.seed_db()

    # Cleanup after each test method
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.remove_test_xml_file()

    # Helper methods
    def seed_db(self):
        # Seeds test db with two CourtCases
        mock_data = [
            CourtCase(plaintiff='John Doe', defendant='Jane Doe'),
            CourtCase(plaintiff='Frank Zappa', defendant='Eric Clapton')
        ]
        db.session.add_all(mock_data)
        db.session.commit()

    def create_test_xml_file(self):
        # Creates 'test_file.xml' in project root dir
        root = ET.Element('root')
        for x in range(3):
            child = ET.SubElement(root, 'child')
        ET.SubElement(child, 'grandchild').text = 'Some text!'
        tree = ET.ElementTree(root)
        with open(self.test_file, 'w'):
            tree.write(self.test_file)

    def remove_test_xml_file(self):
        # Deletes the file created by create_test_xml_file()
        if path.exists(self.test_file):
            remove(self.test_file)

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
        db_cases = CourtCase.query.all()
        res = self.client.get('/web/cases')
        self.assertEqual(res.status_code, 200,
                         'GET to /web/cases should return 200 status code')
        self.assert_template_used('index.html')
        self.assertEqual(self.get_context_variable('cases'), db_cases)

    def test_get_to_web_cases_id(self):
        """Test GET to /web/cases/<int:case_id> returns single case"""
        case_id = 2
        db_case = CourtCase.query.get(case_id)
        res = self.client.get('/web/cases/{}'.format(case_id))
        self.assertEqual(res.status_code, 200,
                         'GET to /web/cases/2 returns 200 status code')
        self.assert_template_used('index.html')
        self.assertEqual(self.get_context_variable('cases'), db_case)

    def test_post_to_web_cases_saves_file(self):
        """Test POST with xml payload to /web/cases saves xml file on server"""
        self.create_test_xml_file()
        data = {'name': 'Test'}
        with open(self.test_file, 'rb') as payload:
            data['file'] = (payload, self.test_file)
            res = self.client.post(
                '/web/cases', content_type='multipart/form-data', data=payload
            )
            self.assertEqual(res.status_code, 201,
                             'Should return 201 status code')
            self.assertTrue(path.isfile(self.test_file_path),
                            'Should save xml file to uploads dir')

    def test_verify_file_type_success(self):
        """Return True if filename has allowed extension"""
        result = verify_file_type(self.test_file)
        self.assertTrue(result)

    def test_verify_file_type_reject(self):
        """Return False if filename does not have allowed extension"""
        result = verify_file_type('some_random_file.jpeg')
        self.assertFalse(result)



if __name__ == '__main__':
    unittest.main(verbosity=2)
