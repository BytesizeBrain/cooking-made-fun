from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes.users import users_bp
from .models import db

app = Flask(__name__)
# Replace with your actual Supabase connection string
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:[YOUR-PASSWORD]@db.snkxtjwgcpbtztvxbdrg.supabase.co:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(users_bp)