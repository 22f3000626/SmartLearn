from flask import Flask, session, g
from dotenv import load_dotenv
import os

from extensions import db
from flask_migrate import Migrate
from models import User, Community, CommunityMembership, Post

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartlearn.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Register blueprints
from routes.mainroutes import main_routes
from routes.communityroutes import community_routes
app.register_blueprint(main_routes)
app.register_blueprint(community_routes)

# Auto-create all tables if they don't exist
with app.app_context():
    db.create_all()

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is not None:
        g.user = User.query.get(user_id)
    else:
        g.user = None

if __name__ == "__main__":
    app.run(debug=True)
