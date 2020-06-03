from flask import Blueprint
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flasksite import db
from flasksite.models import Park, User, Reservation
from flasksite.reservations.forms import MakeReservationForm
import datetime

reservations = Blueprint('reservations', __name__)

@reservations.route("/my_reservations")
@login_required
def my_reservations():
    # Get User and Park Info
    reservations = db.session\
    .query(Reservation, Park)\
    .outerjoin(Park, Reservation.park_id == Park.id)\
    .filter(Reservation.user_id == current_user.id)\
    .order_by(Reservation.date.desc())

    return render_template('my_reservations.html', reservations=reservations)


@reservations.route("/make_reservation/<int:park_id>", methods=['GET', 'POST'])
@login_required
def make_reservation(park_id):
    form = MakeReservationForm()
    park =  Park.query.filter_by(id=park_id).first_or_404()

    if form.validate_on_submit():
        # create new reservation
        reservation = Reservation(
        date=form.date.data,
        start_time=form.start_time.data,
        end_time=form.end_time.data,
        creator=current_user,
        active=True,
        place=park)
        db.session.add(reservation)
        db.session.commit()
        flash('Your reservation has been made!', 'success')
        return redirect(url_for('main.mainpage'))
    elif request.method == 'GET':
        form.date.data = datetime.date.today()
        form.start_time.data = "1:00"
        form.end_time.data = "3:30"

    return render_template('make_reservation.html', 
        title='Reservation', form = form, park=park)


@reservations.route("/reservation/<int:reservation_id>/delete", methods=['POST'])
@login_required
def delete_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    db.session.delete(reservation)
    db.session.commit()
    flash('Your reservation has been cancelled!', 'success')
    return redirect(url_for('reservations.my_reservations'))
