from flask import Flask, session, g
from dotenv import load_dotenv
import os
import logging

from extensions import db
from flask_migrate import Migrate
from models import User, Community, CommunityMembership, Post
from config import Config

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

# Apply configuration
app.config.from_object(Config)

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
