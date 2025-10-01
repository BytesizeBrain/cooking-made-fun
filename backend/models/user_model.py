from extensions import db

class User(db.Model):
    # Define the User model
    # No init method as this is a SQLAlchemy model
    id = db.Column(db.String(36), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    profile_pic = db.Column(db.String(256), nullable=False, default="https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg")
    # TODO: fields for friends count, recipes count, profile pic URL, etc.

