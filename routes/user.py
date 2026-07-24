from flask import Blueprint,request, render_template,flash,redirect,url_for
from flask_login import login_required, current_user
from models.trek import Trek
from constants import TREK_OPEN
from models.booking import Booking
from sqlalchemy import or_
from extensions import db
from constants import (
    BOOKING_BOOKED,
    PAYMENT_PENDING,
)
from constants import (
    TREK_OPEN,
    BOOKING_BOOKED,
    BOOKING_CANCELLED,
    PAYMENT_PENDING,
)

user = Blueprint("user", __name__)

@user.route("/user")
@login_required
def user_dashboard():

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")

    query = Trek.query.filter_by(status=TREK_OPEN)

    if search:
        query = query.filter(
            or_(
                Trek.name.ilike(f"%{search}%"),
                Trek.location.ilike(f"%{search}%")
            )
        )

    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)

    treks = query.all()

    return render_template(
        "user_dashboard.html",
        treks=treks,
        search=search,
        difficulty=difficulty
    )

@user.route("/book/<int:trek_id>")
@login_required
def book_trek(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    # Check if seats are available
    if trek.available_slots <= 0:
        flash("No slots available for this trek.", "danger")
        return redirect(url_for("user.user_dashboard"))

    # Check if the user has already booked this trek
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek.id,
        booking_status=BOOKING_BOOKED
    ).first()

    if existing_booking:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for("user.user_dashboard"))

    booking = Booking(
        user_id=current_user.id,
        trek_id=trek.id,
        booking_status=BOOKING_BOOKED,
        payment_status=PAYMENT_PENDING
    )

    db.session.add(booking)

    # Reduce available slots
    trek.available_slots -= 1

    db.session.commit()

    flash("Trek booked successfully!", "success")

    return redirect(url_for("user.user_dashboard"))

@user.route("/my-bookings")
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=current_user.id
    ).order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )

@user.route("/cancel-booking/<int:booking_id>")
@login_required
def cancel_booking(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    # Make sure the booking belongs to the logged-in user
    if booking.user_id != current_user.id:
        return "Unauthorized", 403

    # Only cancel active bookings
    if booking.booking_status == BOOKING_BOOKED:

        booking.booking_status = BOOKING_CANCELLED

        # Return the slot to the trek
        booking.trek.available_slots += 1

        db.session.commit()

        flash("Booking cancelled successfully.", "success")

    return redirect(url_for("user.my_bookings"))