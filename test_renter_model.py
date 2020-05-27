"""renter model test."""
#    python -m unittest test_renter_model.py
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Renter, Booking
os.environ['DATABASE_URL'] = "postgresql:///fur_buddy-test"

db.create_all()


class RenterModelTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        r1 = Renter.signup("test1", "email1@email.com", "password", 11373)
        rid1 = 1111
        r1.id = rid1

        db.session.commit()

        r1 = Renter.query.get(rid1)

        self.r1 = r1
        self.rid1 = rid1
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_renter_model(self):
        """Does basic model work?"""

        r = Renter(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            location="11373"
        )

        db.session.add(r)
        db.session.commit()
        self.assertEqual(len(r.bookings), 0)

    ####
    #
    # Signup Tests
    #
    ####
    def test_valid_signup(self):
        r_test = Renter.signup(
            "testName", "test@email.com", "testPassword", "11373")
        rid = 99999
        r_test.id = rid
        db.session.commit()

        r_test = Renter.query.get(rid)
        self.assertIsNotNone(r_test)
        self.assertEqual(r_test.username, "testName")
        self.assertEqual(r_test.email, "test@email.com")
        self.assertEqual(r_test.password, "testPassword")
        self.assertEqual(r_test.location, "11373")
        # self.assertNotEqual(r_test.password, "testPassword")
        # Bcrypt strings should start with $2b$
        # self.assertTrue(r_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = Renter.signup(None, "test@email.com",
                                "testPassword", "11373")
        rid = 123456789
        invalid.id = rid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = Renter.signup("testName", None,
                                "testPassword", "11373")
        rid = 123789
        invalid.id = rid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        # with self.assertRaises(ValueError) as context:
        #     Renter.signup("testName", "test@email.com", "", None)

        with self.assertRaises(ValueError) as context:
            Renter.signup("testName", "test@email.com", None, None)

    ####
    #
    # Authentication Tests
    #
    ####
    def test_valid_authentication(self):
        r = Renter.authenticate(self.r1.username, "password")
        self.assertIsNotNone(r)
        self.assertEqual(r.id, self.rid1)

    def test_invalid_username(self):
        self.assertFalse(Renter.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(Renter.authenticate(self.r1.username, "badpassword"))
