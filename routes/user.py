from flask import Blueprint,request, render_template,flash,redirect,url_for
from flask_login import login_required, current_user
from models.trek import Trek
from constants import TREK_OPEN
from models.booking import Booking
from sqlalchemy import or_
from extensions import db
from models.user import User
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
from constants import ROLE_USER,TREK_OPEN

user = Blueprint("user", __name__)

@user.route("/user")
@login_required
def user_dashboard():
    search = request.args.get("search", "").strip()
    difficulty = request.args.get("difficulty", "").strip()
    location = request.args.get("location", "").strip()

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

    if location:
        query = query.filter(Trek.location.ilike(f"%{location}%"))

    treks = query.all()

    return render_template(
        "user_dashboard.html",
        treks=treks,
        search=search,
        difficulty=difficulty,
        location=location
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

@user.route("/user/profile", methods=["GET", "POST"])
@login_required
def user_profile():

    if current_user.role != ROLE_USER:
        return "Unauthorized", 403

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        existing_user = User.query.filter(
            User.email == email,
            User.id != current_user.id
        ).first()

        if existing_user:
            flash("Email already exists.", "danger")
            return redirect(url_for("user.user_profile"))

        current_user.name = name
        current_user.email = email

        if password:
            if password != confirm_password:
                flash("Passwords do not match.", "danger")
                return redirect(url_for("user.user_profile"))
            current_user.set_password(password)

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("user.user_profile"))

    return render_template("user_profile.html")
