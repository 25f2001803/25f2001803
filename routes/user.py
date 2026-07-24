from flask import Blueprint
from flask_login import login_required, current_user

user = Blueprint("user", __name__)


@user.route("/user")
@login_required
def user_dashboard():
    return f"""
    <h1>User Dashboard</h1>
    <h3>Welcome {current_user.name}</h3>
    """