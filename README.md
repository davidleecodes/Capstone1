# Fur Buddy

https://fur-buddy.herokuapp.com/pets

Rent a pet from an adoption center. Unsure or not ready for full time commitment, rent a pet, and help keep your local adoption centers open.

Search by location and by type of pet. Sign in to rent a pet. Create bookings. View current and past booking. Edit or cancel current bookings and leave ratings for past bookings
When booking dates that are already booked, dates are disabled in the start and end date picker

Having dates disable when the user is choosing dates, felt more user friendly rather than just having server side verification
Updating ratings take place in the background rather refresh the page, so the page does not have to reload

api : https://www.petfinder.com/developers/v2/docs/

database: psql

serverside: python, flask, jinja, wtforms, flask-sqlalchemy

clientside: jquery, bootstrap, jquery-ui
