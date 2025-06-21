from flask import Flask
from routes.mainroutes import main_routes
from dotenv import load_dotenv
import os
from extensions import db
from models import User

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Use secret key from environment or fallback
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartlearn.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Remove permanent session logic so sessions expire on browser close
# (Do not set app.permanent_session_lifetime or session.permanent)

# Initialize extensions

db.init_app(app)

# Create tables if they don't exist
def create_tables():
    with app.app_context():
        db.create_all()

create_tables()

# Register blueprint
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True)
