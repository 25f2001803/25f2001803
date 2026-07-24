from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user import User
from constants import ROLE_ADMIN, ROLE_STAFF
from extensions import db

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

    return render_template(
        "admin_dashboard.html",
        pending_staff=pending_staff
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