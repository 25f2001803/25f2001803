from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import or_

from extensions import db
from models.user import User
from models.trek import Trek
from models.booking import Booking

from constants import ROLE_ADMIN, ROLE_USER, ROLE_STAFF,TREK_COMPLETED

admin = Blueprint("admin", __name__)

@admin.route("/admin/users")
@login_required
def manage_users():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    search = request.args.get("search", "")

    users = User.query.filter(User.role == ROLE_USER)

    if search:

        users = users.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.id.cast(db.String).ilike(f"%{search}%")
            )
        )

    users = users.all()

    return render_template(
        "manage_users.html",
        users=users,
        search=search
    )

admin = Blueprint("admin", __name__)

@admin.route("/admin")
@login_required
def admin_dashboard():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    pending_staff = User.query.filter_by(
        role=ROLE_STAFF,
        approved=False
    ).all()

    total_treks = Trek.query.count()

    total_users = User.query.filter_by(role=ROLE_USER).count()

    total_staff = User.query.filter_by(role=ROLE_STAFF).count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin_dashboard.html",
        pending_staff=pending_staff,
        total_treks=total_treks,
        total_users=total_users,
        total_staff=total_staff,
        total_bookings=total_bookings
    )
    
@admin.route("/approve/<int:user_id>")
@login_required
def approve_staff(user_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    staff = User.query.get_or_404(user_id)

    staff.approved = True

    db.session.commit()

    flash(f"{staff.name} has been approved.", "success")

    return redirect(url_for("admin.admin_dashboard"))

@admin.route("/admin/treks")
@login_required
def manage_treks():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    treks = Trek.query.all()

    return render_template(
        "manage_treks.html",
        treks=treks
    )

@admin.route("/admin/treks/create", methods=["GET", "POST"])
@login_required
def create_trek():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    if request.method == "POST":

        trek = Trek(
            name=request.form["name"],
            location=request.form["location"],
            difficulty=request.form["difficulty"],
            duration=int(request.form["duration"]),
            max_slots=int(request.form["max_slots"]),
            available_slots=int(request.form["max_slots"]),
            price=float(request.form["price"]),
            status=request.form["status"],
            description=request.form["description"]
        )

        db.session.add(trek)
        db.session.commit()

        flash("Trek created successfully!", "success")

        return redirect(url_for("admin.manage_treks"))

    return render_template("create_trek.html")

@admin.route("/admin/treks/edit/<int:trek_id>", methods=["GET", "POST"])
@login_required
def edit_trek(trek_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    if request.method == "POST":

        trek.name = request.form["name"]
        trek.location = request.form["location"]
        trek.difficulty = request.form["difficulty"]
        trek.duration = int(request.form["duration"])
        trek.max_slots = int(request.form["max_slots"])
        trek.available_slots = int(request.form["available_slots"])
        trek.price = float(request.form["price"])
        trek.status = request.form["status"]
        trek.description = request.form["description"]

        db.session.commit()

        flash("Trek updated successfully!", "success")

        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "edit_trek.html",
        trek=trek
    )

@admin.route("/admin/treks/delete/<int:trek_id>")
@login_required
def delete_trek(trek_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully!", "success")

    return redirect(url_for("admin.manage_treks"))

@admin.route("/admin/treks/<int:trek_id>/assign", methods=["GET", "POST"])
@login_required
def assign_staff(trek_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    staff_members = User.query.filter_by(
        role=ROLE_STAFF,
        approved=True
    ).all()

    if request.method == "POST":

        trek.staff_id = request.form["staff_id"]

        db.session.commit()

        flash("Staff assigned successfully!", "success")

        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "assign_staff.html",
        trek=trek,
        staff_members=staff_members
    )

@admin.route("/admin/users")
@login_required
def manage_users():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    search = request.args.get("search", "")

    users = User.query.filter(User.role == ROLE_USER)

    if search:

        users = users.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.id.cast(db.String).ilike(f"%{search}%")
            )
        )

    users = users.all()

    return render_template(
        "manage_users.html",
        users=users,
        search=search
    )

@admin.route("/admin/users/blacklist/<int:user_id>")
@login_required
def blacklist_user(user_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    user = User.query.get_or_404(user_id)

    user.blacklisted = True

    db.session.commit()

    flash(f"{user.name} has been blacklisted.", "success")

    return redirect(url_for("admin.manage_users"))


@admin.route("/admin/users/activate/<int:user_id>")
@login_required
def activate_user(user_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    user = User.query.get_or_404(user_id)

    user.blacklisted = False

    db.session.commit()

    flash(f"{user.name} has been activated.", "success")

    return redirect(url_for("admin.manage_users"))

@admin.route("/admin/staff")
@login_required
def manage_staff():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    search = request.args.get("search", "")

    staff_members = User.query.filter(
        User.role == ROLE_STAFF
    )

    if search:

        staff_members = staff_members.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.id.cast(db.String).ilike(f"%{search}%")
            )
        )

    staff_members = staff_members.all()

    return render_template(
        "manage_staff.html",
        staff_members=staff_members,
        search=search
    )

@admin.route("/admin/staff/blacklist/<int:user_id>")
@login_required
def blacklist_staff(user_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    staff = User.query.get_or_404(user_id)

    staff.blacklisted = True

    db.session.commit()

    flash(f"{staff.name} has been blacklisted.", "success")

    return redirect(url_for("admin.manage_staff"))

@admin.route("/admin/staff/activate/<int:user_id>")
@login_required
def activate_staff(user_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    staff = User.query.get_or_404(user_id)

    staff.blacklisted = False

    db.session.commit()

    flash(f"{staff.name} has been activated.", "success")

    return redirect(url_for("admin.manage_staff"))

@admin.route("/admin/bookings")
@login_required
def view_bookings():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    bookings = Booking.query.order_by(
        Booking.booking_date.desc()
    ).all()

    return render_template(
        "view_bookings.html",
        bookings=bookings
    )

@admin.route("/admin/treks/<int:trek_id>/trekkers")
@login_required
def view_trekkers_admin(trek_id):

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    trek = Trek.query.get_or_404(trek_id)

    bookings = Booking.query.filter_by(
        trek_id=trek.id
    ).all()

    return render_template(
        "admin_view_trekkers.html",
        trek=trek,
        bookings=bookings
    )

@admin.route("/admin/history")
@login_required
def trek_history():

    if current_user.role != ROLE_ADMIN:
        return "Unauthorized", 403

    completed_treks = Trek.query.filter_by(
        status=TREK_COMPLETED
    ).all()

    return render_template(
        "trek_history.html",
        treks=completed_treks
    )