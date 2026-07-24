from models.staff_profile import StaffProfile
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)
from models.user import User
from extensions import db
from constants import ROLE_USER,ROLE_STAFF
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        print(request.method)
        print(request.form)

        email = request.form.get("email")
        password = request.form.get("password")

        print(email)
        print(password)

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))
        

        if not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return redirect(url_for("auth.login"))
        
        if user.role == ROLE_STAFF and not user.approved:
            flash(
                "Your account is waiting for Admin approval."
                "warning"
            )
            return redirect(url_for("auth.login"))

        login_user(user)

        flash(f"Welcome {user.name}!", "success")

        if user.role == "admin":
            return redirect(url_for("admin.admin_dashboard"))

        elif user.role == "staff":
            return redirect(url_for("staff.staff_dashboard"))

        else:
            return redirect(url_for("user.user_dashboard"))

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        role = request.form["role"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("auth.register"))
        
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for("auth.register"))
        
        new_user = User(
            name = name,
            email = email,
            role = role,
            approved = (role == ROLE_USER),
            blacklisted = False
        )

        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        if role == ROLE_STAFF:
            staff_profile = StaffProfile(
                user_id=new_user.id,
                phone="",
                experience=0,
                bio=""
            )
            db.session.add(staff_profile)
            db.session.commit()

            flash(
                "Staff registration successful ! Please wait for Admin approval before logging in."
                "warning"
            )
        else:
            flash(
                "Registration successful ! Please login.",
                "success"
            )
        return redirect(url_for("auth.login"))

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully.", "success")

    return redirect(url_for("auth.login"))