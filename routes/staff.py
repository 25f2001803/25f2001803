from flask import Blueprint
from flask_login import login_required, current_user

staff = Blueprint("staff", __name__)


@staff.route("/staff")
@login_required
def staff_dashboard():
    return f"""
    <h1>Staff Dashboard</h1>
    <h3>Welcome {current_user.name}</h3>
    """