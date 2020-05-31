from models import db, Renter, Booking
from app import app
import datetime


db.drop_all()
db.create_all()


renter1 = Renter(
    id=100,
    username="SAM",
    email="sam@gmail.com",
    password="sampass",
    location="11379"
)


book1 = Booking(
    id=20,
    pet_id=48038022,
    renter_id=100,
    startTime=datetime.date.today(),
    endTime=datetime.date.today() + datetime.timedelta(days=1),
    rating=4
)

db.session.add_all([renter1, book1])
db.session.commit()
