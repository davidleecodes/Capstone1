"""renter model test."""
#    py -3 -m unittest test_renter_views.py
from app import app, CURR_RENTER_KEY
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, Renter, Booking
os.environ['DATABASE_URL'] = "postgresql:///fur_buddy-test"

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testRenter = Renter.signup(username="testuser",
                                        email="test@test.com",
                                        password="testuser",
                                        location=11373)
        self.testRenter_id = 8989
        self.testRenter.id = self.testRenter_id
        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_user_show(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_RENTER_KEY] = self.testRenter_id
            resp = c.get(f"/renter")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("testuser", str(resp.data))

    def test_unauthorized_user_show(self):
        with self.client as c:
            resp = c.get(f"/renter", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            self.assertIn("Access unauthorized", str(resp.data))
