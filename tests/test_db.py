# Standard library imports
import unittest

# Third party imports
from sqlalchemy import exc

# Local app imports
from partyparser import create_app, db
from partyparser.models import CourtCase
from config import TestConfig


class CourtCaseModelTests(unittest.TestCase):
    """Test suite for CourtCase model db operations"""

    # Before each test method
    def setUp(self):
        self.p1 = 'John Doe'
        self.d1 = 'Jane Doe'
        self.p2 = 'Neil Young'
        self.d2 = 'Mark Knopfler'
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    # After each test method
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_courtcase(self):
        """Test creating new courtcase is successful"""
        case1 = CourtCase(plaintiff=self.p1, defendant=self.d1)
        db.session.add(case1)
        db.session.commit()
        result = CourtCase.query.get(1)
        self.assertIsNotNone(result.id, 'Should have an id')
        self.assertEqual(result.plaintiff, case1.plaintiff)
        self.assertEqual(result.defendant, case1.defendant)

    def test_add_multiple_courtcases(self):
        """Test creating multiple courtcases is successful"""
        case1 = CourtCase(plaintiff=self.p1, defendant=self.d1)
        case2 = CourtCase(plaintiff=self.p2, defendant=self.d2)
        cases = [case1, case2]
        db.session.add_all(cases)
        db.session.commit()
        result = CourtCase.query.all()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].plaintiff, case1.plaintiff)
        self.assertEqual(result[1].plaintiff, case2.plaintiff)
        self.assertIsNotNone(result[0].id, 'Should have an id')
        self.assertIsNotNone(result[1].id, 'Should have an id')

    def test_add_incomplete_courtcase(self):
        """Test creating courtcase with missing party raises error"""
        case = CourtCase(plaintiff=self.p1, defendant=None)
        # defendant is non-nullable field, an IntegrityError should be raised
        with self.assertRaises(exc.IntegrityError):
            db.session.add(case)
            db.session.commit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
