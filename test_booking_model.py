"""booking model test."""
#    py -3 -m unittest test_booking_model.py
from app import app
import os
from unittest import TestCase
from sqlalchemy import exc
import datetime


from models import db, Renter, Booking
os.environ['DATABASE_URL'] = "postgresql:///fur_buddy-test"

db.create_all()


class BookingModelTestCase(TestCase):
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

    def test_booking_model(self):
        """Does basic model work?"""

        b = Booking(
            pet_id=48038022,
            renter_id=self.rid1,
            startTime=datetime.date.today(),
            endTime=datetime.date.today() + datetime.timedelta(days=1),
        )

        db.session.add(b)
        db.session.commit()
        self.assertEqual(len(self.r1.bookings), 1)
        self.assertEqual(self.r1.bookings[0].pet_id, 48038022)

    ####
    #
    # avg_rating Test
    #
    ####

    def test_avg_rating(self):

        b1 = Booking(
            pet_id=48038022,
            renter_id=self.rid1,
            startTime="2020-5-25",
            endTime="2020-5-26",
            rating=2
        )

        b2 = Booking(
            pet_id=48038022,
            renter_id=self.rid1,
            startTime="2020-6-25",
            endTime="2020-6-26",
            rating=4
        )

        db.session.add(b1)
        db.session.add(b2)
        db.session.commit()

        rating = Booking.avg_rating(id=48038022)
        self.assertEqual(rating, 3)
    ####
    #
    # is_avaliable Tests
    #
    # ####
    def test_is_avaliable(self):

        b1 = Booking(
            pet_id=48038022,
            renter_id=self.rid1,
            startTime=datetime.date(2020, 5, 3),
            endTime=datetime.date(2020, 6, 23),
            rating=2
        )

        db.session.add(b1)
        db.session.commit()

        isAvaliable = Booking.is_avaliable(
            id=48038022, start=datetime.date(2020, 6, 3), end=datetime.date(2020, 6, 5))
        self.assertFalse(isAvaliable)

     ####
    #
    #  booked_dates Tests
    #
    ####

    def test_booked_dates(self):

        b1 = Booking(
            pet_id=48038022,
            renter_id=self.rid1,
            startTime="2020-5-25",
            endTime="2020-5-28",
            rating=2
        )

        b2 = Booking(
            pet_id=48038022,
            renter_id=self.rid1,
            startTime="2020-6-5",
            endTime="2020-6-6",
            rating=4
        )

        db.session.add(b1)
        db.session.add(b2)
        db.session.commit()

        book_dates = Booking.booked_dates(id=48038022)
        self.assertEqual(len(book_dates), 6)
