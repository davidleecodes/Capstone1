"""renter model test."""
#    py -3 -m unittest test_booking_views.py
from app import app, CURR_RENTER_KEY
import os
from unittest import TestCase
from sqlalchemy import exc
import datetime


from models import db, Renter, Booking
os.environ['DATABASE_URL'] = "postgresql:///fur_buddy-test"

db.create_all()
app.config['WTF_CSRF_ENABLED'] = False


class BookingViewTestCase(TestCase):
    """Test views for Bookings."""

    def setUp(self):
        """Create test Renter, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testrenter = Renter.signup(username="testuser",
                                        email="test@test.com",
                                        password="testuser",
                                        location=11373)
        self.testrenter_id = 8989
        self.testrenter.id = self.testrenter_id

        db.session.commit()

    def test_add_booking(self):
        """Can use add a booking?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_RENTER_KEY] = self.testrenter.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/pet/48038022", data={
                # "pet_id"=48038022,
                "renter_id": self.testrenter.id,
                "start_date": datetime.date.today() + datetime.timedelta(days=1),
                "end_date": datetime.date.today() + datetime.timedelta(days=2)
            })

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            booking = Booking.query.one()
            self.assertEqual(booking.pet_id, 48038022)

    def test_add_no_session(self):
        with self.client as c:
            resp = c.post("/pet/48038022", data={
                # pet_id=48038022,
                "renter_id": self.testrenter.id,
                "start_date": datetime.date.today() + datetime.timedelta(days=1),
                "end_date": datetime.date.today() + datetime.timedelta(days=2)
            })
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Sign in", str(resp.data))

    def test_booking_show(self):

        b = Booking(
            id=1234,
            pet_id=48038022,
            renter_id=self.testrenter.id,
            startTime=datetime.date.today() + datetime.timedelta(days=1),
            endTime=datetime.date.today() + datetime.timedelta(days=2)
        )

        db.session.add(b)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_RENTER_KEY] = self.testrenter.id

            b = Booking.query.get(1234)

            resp = c.get(f'/pet/{b.pet_id}/booking/{b.id}/edit')

            self.assertEqual(resp.status_code, 200)
            self.assertIn(str(b.startTime), str(resp.data))

    def test_booking_delete(self):

        b = Booking(
            id=1234,
            pet_id=48038022,
            renter_id=self.testrenter.id,
            startTime=datetime.date.today() + datetime.timedelta(days=1),
            endTime=datetime.date.today() + datetime.timedelta(days=2)
        )

        db.session.add(b)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_RENTER_KEY] = self.testrenter.id

            resp = c.post(
                f'/pet/{b.pet_id}/booking/{b.id}/cancel', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)

            b = Booking.query.get(1234)
            self.assertIsNone(b)
