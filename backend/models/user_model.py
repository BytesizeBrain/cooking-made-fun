from app import db

class User(db.Model):
    # Define the User model
    # No init method as this is a SQLAlchemy model
    email = db.Column(db.String(128), primary_key=True, nullable=False)
    full_name = db.Column(db.String(128), nullable=False)

