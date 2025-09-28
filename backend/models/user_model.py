from extensions import db

class User(db.Model):
    # Define the User model
    # No init method as this is a SQLAlchemy model
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    display_name = db.Column(db.String(128), nullable=False)
    # TODO: fields for friends count, recipes count, profile pic URL, etc.

