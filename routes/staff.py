from flask import Blueprint, render_template , request , redirect , url_for , flash
from flask_login import login_required, current_user
from models.booking import Booking
from models.trek import Trek
from constants import ROLE_STAFF
from extensions import db
from constants import (
    TREK_OPEN,
    TREK_CLOSED,
    TREK_STARTED,
    TREK_ONGOING,
    TREK_COMPLETED,
    BOOKING_BOOKED,
    BOOKING_COMPLETED
)

staff = Blueprint("staff", __name__)

@staff.route("/staff")
@login_required
def staff_dashboard():

    if current_user.role != ROLE_STAFF:
        return "Unauthorized", 403

    treks = Trek.query.filter_by(staff_id=current_user.id).all()
    assigned_treks = len(treks)

    registered_trekkers = sum(
        len(trek.bookings)
        for trek in treks
    )
    
    open_treks = sum(
        1
        for trek in treks
        if trek.status == TREK_OPEN
    )
    
    completed_treks = sum(
        1
        for trek in treks
        if trek.status == TREK_COMPLETED
    )

    return render_template(
        "staff_dashboard.html",
        treks=treks,
        assigned_treks=assigned_treks,
        registered_trekkers=registered_trekkers,
        open_treks=open_treks,
        completed_treks=completed_treks
    )
@staff.route("/staff/trek/<int:trek_id>")
@login_required
def view_trekkers(trek_id):

    if current_user.role != ROLE_STAFF:
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:
        return "Unauthorized", 403

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "view_trekkers.html",
        trek=trek,
        bookings=bookings
    )

@staff.route("/staff/profile", methods=["GET", "POST"])
@login_required
def staff_profile():

    if current_user.role != ROLE_STAFF:
        return "Unauthorized", 403

    profile = current_user.staff_profile

    if request.method == "POST":

        profile.phone = request.form["phone"]
        profile.experience = int(request.form["experience"])
        profile.bio = request.form["bio"]

        db.session.commit()

        flash("Profile updated successfully!", "success")

        return redirect(url_for("staff.staff_profile"))

    return render_template(
        "staff_profile.html",
        profile=profile
    )
@staff.route("/staff/trek/<int:trek_id>/slots", methods=["POST"])
@login_required
def update_slots(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:
        return "Unauthorized", 403

    slots = int(request.form["available_slots"])

    if slots < 0:
        slots = 0

    if slots > trek.max_slots:
        slots = trek.max_slots

    trek.available_slots = slots

    db.session.commit()

    flash("Available slots updated successfully.", "success")

    return redirect(url_for("staff.staff_dashboard"))

@staff.route("/trek/<int:trek_id>/status", methods=["POST"])
@login_required
def update_status(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:
        return "Unauthorized", 403

    status = request.form["status"]

    allowed_status = [
        TREK_OPEN,
        TREK_CLOSED,
        TREK_STARTED,
        TREK_ONGOING,
        TREK_COMPLETED
    ]

    if status not in allowed_status:
        flash("Invalid status.", "danger")
        return redirect(url_for("staff.staff_dashboard"))

    trek.status = status

    if status == TREK_COMPLETED:
        for booking in trek.bookings:
            if booking.booking_status == BOOKING_BOOKED:
                booking.booking_status = BOOKING_COMPLETED

    db.session.commit()

    flash("Trek status updated.", "success")
    return redirect(url_for("staff.staff_dashboard"))