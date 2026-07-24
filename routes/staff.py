from flask import Blueprint, render_template , request , redirect , url_for , flash
from flask_login import login_required, current_user
from models.booking import Booking
from models.trek import Trek
from constants import ROLE_STAFF
from extensions import db
from constants import (
    TREK_OPEN,
    TREK_CLOSED,
    TREK_COMPLETED
)

staff = Blueprint("staff", __name__)


@staff.route("/staff")
@login_required
def staff_dashboard():

    if current_user.role != ROLE_STAFF:
        return "Unauthorized", 403

    treks = Trek.query.filter_by(staff_id=current_user.id).all()

    return render_template(
        "staff_dashboard.html",
        treks=treks
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
@staff.route("/trek/<int:trek_id>/status", methods=["POST"])
@login_required
def update_status(trek_id):

    trek = Trek.query.get_or_404(trek_id)

    if trek.staff_id != current_user.id:
        return "Unauthorized", 403

    trek.status = request.form["status"]

    db.session.commit()

    flash("Trek status updated.", "success")

    return redirect(url_for("staff.staff_dashboard"))