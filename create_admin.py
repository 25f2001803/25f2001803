from create_app import create_app
from extensions import db
from models.user import User
from constants import ROLE_ADMIN

app = create_app()


def create_admin():
    with app.app_context():
        admin = User.query.filter_by(email="admin@trek.com").first()

        if admin:
            print("✅ Admin already exists.")
            return

        admin = User(
            name="Administrator",
            email="admin@trek.com",
            role=ROLE_ADMIN,
            approved=True,
            blacklisted=False,
            password_hash="admin123",
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Default admin created successfully.")


if __name__ == "__main__":
    create_admin()