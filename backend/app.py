from extensions import app, db

# Import blueprints after app and db are initialized
from routes.main_routes import main_bp
from routes.user_routes import users_bp

# Registering Blueprints (Routes)
app.register_blueprint(users_bp)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    # Create a db and tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)