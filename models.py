import datetime
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def connect_db(app):
    """connect to database."""
    db.app = app
    db.init_app(app)


class Renter(db.Model):
    """renter"""
    __tablename__ = 'renters'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    location = db.Column(db.Text, nullable=False)
    # pets = db.relationship('Pet', secondary='bookings', backref='renters')
    bookings = db.relationship('Booking', backref="renters")

    def __repr__(self):
        return f"<Renter #{self.id}: {self.username}, {self.email}, {self.location}>"

    @classmethod
    def signup(cls, username, email, password, location):
        """Sign up user.

        Hashes password and adds user to system.
        """
        # hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        renter = Renter(
            username=username,
            email=email,
            password=password,
            location=location,
        )

        db.session.add(renter)
        return renter

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        renter = cls.query.filter_by(username=username).first()

        if renter:
            if renter.password == password:
                return renter
            # is_auth = bcrypt.check_password_hash(renter.password, password)
            # if is_auth:
            #     return renter

        return False


class Booking(db.Model):
    """booking"""
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, nullable=False)
    renter_id = db.Column(db.Integer, db.ForeignKey(
        'renters.id'), nullable=False)
    startTime = db.Column(db.Date, nullable=False)
    endTime = db.Column(db.Date, nullable=False)
    rating = db.Column(db.Integer, default=0)

    @classmethod
    def avg_rating(cls, id):
        """returns avg rating for pet_id"""

        pet = cls.query.filter_by(pet_id=id).first()
        if pet:
            ratingAvg = db.session.query(
                func.avg(Booking.rating).label("avg")).filter(Booking.pet_id == id).first()
            # print("AVG", ratingAvg)
            rating = round((ratingAvg._asdict().get('avg')), 1)
            if rating == 0:
                return "not yet rated"
            else:
                return float(rating)
        else:
            return "not yet rated"

    @classmethod
    def is_avaliable(cls, id, start, end):
        """returns true/ false for given pet and dates"""
        pet = cls.query.filter(cls.pet_id == id)
        if pet.first():
            print("_____pet al", pet)
            in_progress = pet.filter(
                cls.endTime > datetime.date.today()).all()
            for b in in_progress:
                print("_____pet", b.startTime, start, b.endTime, b.startTime <= start <=
                      b.endTime)
                if(b.startTime <= start <= b.endTime or b.startTime <= end <= b.endTime):
                    return False
                else:
                    return True
        else:
            return True

    @classmethod
    def booked_dates(cls, id):
        """returns booked future dates"""
        pet = cls.query.filter(cls.pet_id == id)
        # print("____________PET", pet)
        if pet:
            in_progress = pet.filter(
                cls.endTime > datetime.date.today()).all()
            # print("____________InProgress", in_progress)

            dates = []
            for b in in_progress:
                i = b.startTime
                while i <= b.endTime:
                    dates.append(i.__str__())
                    i = i + datetime.timedelta(days=1)
            return dates
        else:
            []
