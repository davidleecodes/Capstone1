import requests
import datetime
import decimal
import os
from flask import Flask, redirect, render_template, request, session, g, jsonify, url_for, flash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Renter, Booking
from forms import PetForm, RenterForm, LoginForm, BookRatingForm
try:
    API_SECRET_KEY = os.environ['API_SECRET_KEY']
    API_ID = os.environ['API_ID']
except KeyError:
    print("error")
    from secrets import API_SECRET_KEY, API_ID

app = Flask(__name__)
# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///fur_buddy'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "ssh")
toolbar = DebugToolbarExtension(app)

connect_db(app)

API_TOKEN = "api_token"
CURR_RENTER_KEY = "curr_renter"


##############################################################################
# User signup/login/logout
##############################################################################


@app.before_request
def add_renter_to_g():
    """If we're logged in, add curr renter to Flask global."""

    if CURR_RENTER_KEY in session:
        g.renter = Renter.query.get(session[CURR_RENTER_KEY])

    else:
        g.renter = None


def do_login(renter):
    """Log in renter."""
    # print(renter)
    session[CURR_RENTER_KEY] = renter.id


def do_logout():
    """Logout renter."""

    if CURR_RENTER_KEY in session:
        del session[CURR_RENTER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle renter signup.

    Create new renter and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a renter with that username: flash message
    and re-present form.
    """
    if CURR_RENTER_KEY in session:
        del session[CURR_RENTER_KEY]
    form = RenterForm()

    if form.validate_on_submit():
        try:
            renter = Renter.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                location=form.location.data
            )
            # print("commit", renter)
            db.session.commit()

        except IntegrityError as e:
            # print("error", e)
            flash("Username already taken", 'danger')
            return render_template('renter/signup.html', form=form)
        # print("hit")
        do_login(renter)

        return redirect("/")

    else:
        return render_template('renter/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        renter = Renter.authenticate(form.username.data,
                                     form.password.data)

        if renter:
            do_login(renter)
            flash(f"Hello, {renter.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('renter/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")

##############################################################################
# api
##############################################################################


@app.route("/api/get-token", methods=["GET"])
def get_new_token():
    """returns new token "expires_in": 3600"""
    token_request = requests.post("https://api.petfinder.com/v2/oauth2/token", json={
        "grant_type": "client_credentials",
        "client_id": API_ID,
        "client_secret": API_SECRET_KEY
    })
    access_token = {"token": token_request.json().get("access_token")}
    # print(access_token)
    # session[API_TOKEN] = access_token
    return jsonify(access_token)


@app.route("/api/get-pets", methods=["POST"])
def get_pets():
    """return pets"""
    token = request.json.get("token")
    type = request.json.get("type")
    location = request.json.get("location")
    params = {}
    if type != "None":
        params["type"] = type
    if location != "None" and location != "":
        params["location"] = location
        params["sort"] = "distance"
    # print(type, location, params)
    resp = requests.get(f" https://api.petfinder.com/v2/animals", params=params, headers={
        "Authorization": f"Bearer {token}"})
    # print(resp.json())
    return jsonify(resp.json())


@app.route("/api/get-pet", methods=["POST"])
def get_pet():
    """return pet with id"""
    token = request.json.get("token")
    id = request.json.get("id")
    # print(id)
    resp = requests.get(f" https://api.petfinder.com/v2/animals/{id}", headers={
        "Authorization": f"Bearer {token}"})
    rating = Booking.avg_rating(id=id)
    resp_json = resp.json()
    resp_json["rating"] = rating

    # print(resp_json)
    return jsonify(resp_json)


##############################################################################
# Booking
##############################################################################

@app.route("/pet/<int:pet_id>", methods=["GET", "POST"])
def pet(pet_id):
    "return pet page"
    form = PetForm()
    rating = Booking.avg_rating(id=pet_id)
    if not g.renter:
        flash("Sign in", "danger")
        return render_template("pet.html", id=pet_id)
    booked_dates = Booking.booked_dates(id=pet_id)
    print("_____BOOKED", booked_dates)

    if form.validate_on_submit():
        isAvaliable = Booking.is_avaliable(
            id=pet_id, start=form.start_date.data, end=form.end_date.data)
        print("ISAVALIABLE", isAvaliable)
        if isAvaliable:
            booking = Booking(
                pet_id=pet_id,
                renter_id=g.renter.id,
                startTime=form.start_date.data,
                endTime=form.end_date.data
            )
            db.session.add(booking)
            db.session.commit()
            print("____red")
            return redirect(f"/renter")
        else:
            flash("already booked pick another date", "danger")
            return render_template("pet.html", id=pet_id, form=form, rating=rating, booked=booked_dates)
    else:
        return render_template("pet.html", id=pet_id, form=form, rating=rating, booked=booked_dates)


@app.route("/pet/<int:pet_id>/booking/<int:book_id>/cancel", methods=["GET", "POST"])
def booking_cancel(pet_id, book_id):
    "delete booking"
    if not g.renter:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    book = Booking.query.get_or_404(book_id)
    if book.renter_id != g.renter.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    db.session.delete(book)
    db.session.commit()

    return redirect(f"/renter")


@app.route("/pet/<int:pet_id>/booking/<int:book_id>/edit", methods=["GET", "POST"])
def booking_edit(pet_id, book_id):
    "return edit booking page"

    if not g.renter:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    book = Booking.query.get_or_404(book_id)
    if book.renter_id != g.renter.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = PetForm(obj=book)
    if form.validate_on_submit():
        book.startTime = form.start_date.data,
        book.endTime = form.end_date.data
        db.session.commit()
        return redirect(f"/renter")
    else:
        return render_template("booking_edit.html", id=pet_id, form=form, editing=True)


@app.route("/booking/<int:book_id>/rating", methods=["POST"])
def booking_rating(book_id):
    "rate booking "

    if not g.renter:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    book = Booking.query.get_or_404(book_id)
    if book.renter_id != g.renter.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = BookRatingForm(obj=request.json, meta={'csrf': False})
    if form.validate():
        book.rating = request.json.get('rating')
        db.session.commit()
        return ({"rating": book.rating}, 201)
    else:
        return ({"error": "submission failed"}, 201)


@app.route("/pets", methods=["GET"])
def pets():
    "return pet page"
    location = request.args.get("location")
    if location == None and g.renter:
        location = g.renter.location

    # print(location)
    type = request.args.get("type")

    return render_template('petList.html',  location=location, type=type)


@app.route("/")
def homepage():

    return redirect(url_for('pets'))
##############################################################################
# Renter
##############################################################################


@app.route("/renter")
def renter_show():
    """show renter profile"""
    print("____g", g.renter)
    if not g.renter:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    pastBookings = Booking.query.filter(Booking.renter_id == g.renter.id).filter(
        Booking.endTime < datetime.date.today()
    ).all()

    currBookings = Booking.query.filter(Booking.renter_id == g.renter.id).filter(
        Booking.endTime >= datetime.date.today()
    ).all()
    # print("past", pastBookings)
    # print("curr", currBookings)

    return render_template('renter/show.html', renter=g.renter, pastBookings=pastBookings, currBookings=currBookings)


@app.route("/renter/edit", methods=['GET', 'POST'])
def renter_edit():
    """update renter profile"""
    if not g.renter:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    renter = g.renter
    form = RenterForm(obj=renter)

    if form.validate_on_submit():
        if Renter.authenticate(renter.username, form.password.data):
            renter.username = form.username.data
            renter.email = form.email.data
            renter.location = form.location.data

            db.session.commit()
            return redirect('/renter')

        flash("Wrong password, please try again.", 'danger')

    return render_template('renter/edit.html', form=form, renter_id=renter.id)
