# Standard library imports
import unittest
from os import path, remove

# Third party imports
from flask import jsonify
from flask_testing import TestCase

# Local app imports
from partyparser import create_app
from partyparser.helpers import verified_file_type
from config import TestConfig


class HelperFunctionsTests(TestCase):
    """Test suite for helper functions"""

    def create_app(self):
        return create_app(TestConfig)

    # Setup before each test method
    def setUp(self):
        self.test_file = 'test_file.xml'

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


if __name__ == "__main__"
    unittest.main(verbosity=2)
