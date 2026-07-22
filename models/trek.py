from extensions import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(30), nullable=False)

    duration = db.Column(db.Integer, nullable=False)

    max_slots = db.Column(db.Integer, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)

    price = db.Column(db.Float, nullable=False)

    status = db.Column(db.String(30), nullable=False)

    description = db.Column(db.Text)

# create relationship between User to many Treks
    staff_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True
    )

    bookings = db.relationship(
        "Booking",
        #backref = it automatically creates the reverse relationship
        backref="trek",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Trek {self.name}>"