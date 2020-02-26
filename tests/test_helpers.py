# Standard library imports
import unittest

# Third party imports
from flask_testing import TestCase

# Local app imports
from partyparser import create_app
from partyparser.helpers import verified_file_type, format_case
from config import TestConfig


class HelperFunctionsTests(TestCase):
    """Test suite for helper functions"""

    def create_app(self):
        return create_app(TestConfig)

    # Setup before each test method
    def setUp(self):
        self.test_file = 'test_file.xml'
        # Test case as it will be returned from the db
        self.test_case = {
            'id': 1,
            'plaintiff': 'John Doe',
            'defendant': 'Jane Doe'
        }
        # Test case formatted for JSON response
        self.formatted_test_case = {
            'type': 'courtcase',
            'id': 1,
            'attributes': {
                'plaintiff': 'John Doe',
                'defendant': 'Jane Doe'
            }
        }

    # Cleanup after each test method
    def tearDown(self):
        pass

    def test_verified_file_type_success(self):
        """Return True if filename has allowed extension"""
        result = verified_file_type(self.test_file)
        self.assertTrue(result)

    def test_verified_file_type_reject(self):
        """Return False if filename does not have allowed extension"""
        result = verified_file_type('some_random_file.jpeg')
        self.assertFalse(result)

    def test_format_case_success(self):
        """
        Return formatted case object.
        Input: { id: <int>, plaintiff: <str>, defendant: <str> }
        Output: {
            type: 'courtcase',
            id: <int>
            attributes: {
                plaintiff: <str>,
                defendant: <str>
            }
        }
        """
        result = format_case(self.test_case)
        self.assertEqual(result, self.formatted_test_case)


if __name__ == "__main__":
    unittest.main(verbosity=2)
