from extensions import db


class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        #one staff member = 1 staff profile
        unique=True
    )

    phone = db.Column(db.String(15), nullable=False)

    experience = db.Column(db.Integer, default=0)

    bio = db.Column(db.Text)

    def __repr__(self):
        return f"<StaffProfile User ID: {self.user_id}>"