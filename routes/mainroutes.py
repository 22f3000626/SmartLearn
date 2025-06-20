from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from services.booksearch import search_books
from services.youtubescrapper import search_youtube
from services.roadmap import generate_roadmap
from services.bookspdf import search_pdfs  # ✅ New import
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

main_routes = Blueprint('main_routes', __name__)

@main_routes.route("/welcome")
def welcome():
    registered_success = session.pop("registered_success", None)
    logout_success = session.pop("logout_success", None)
    return render_template("landing.html", registered_success=registered_success, logout_success=logout_success)

@main_routes.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("main_routes.welcome"))
    results = {"videos": [], "books": [], "pdfs": []}
    logged_in = True
    username = session["user"]
    login_success = session.pop("login_success", None)
    if request.method == "POST":
        topic = request.form["topic"]
        results["videos"] = search_youtube(topic)
        results["books"] = search_books(topic)
        results["pdfs"] = search_pdfs(topic)
    return render_template("home.html", results=results, logged_in=logged_in, username=username, login_success=login_success)

@main_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            return render_template("login.html", error="User does not exist.")
        if not check_password_hash(user.password, password):
            return render_template("login.html", error="Incorrect password.")
        session["user"] = user.username  # Store the actual username
        session["user_id"] = user.id     # Store the user id for community features
        session["login_success"] = True
        return redirect(url_for("main_routes.home"))
    return render_template("login.html")

@main_routes.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if not fullname or not email or not password or not confirm_password:
            return render_template("signup.html", error="All fields are required.")

        if password != confirm_password:
            return render_template("signup.html", error="Passwords do not match.")

        if User.query.filter((User.username == fullname) | (User.email == email)).first():
            return render_template("signup.html", error="User with this name or email already exists.")

        hashed_password = generate_password_hash(password)
        user = User(username=fullname, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        session["registered_success"] = True
        return redirect(url_for("main_routes.welcome"))
    return render_template("signup.html")

@main_routes.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("user_id", None)
    session["logout_success"] = True
    return redirect(url_for("main_routes.welcome"))

@main_routes.route("/learn", methods=["GET", "POST"])
def learn():
    results = {"videos": [], "books": [], "roadmap": "", "pdfs": []}
    if request.method == "POST":
        topic = request.form["topic"]
        level = request.form["level"]

        results["roadmap"] = generate_roadmap(topic, level)
        results["books"] = search_books(topic)
        results["pdfs"] = search_pdfs(topic)
        results["videos"] = search_youtube(topic)

        # Store in session to reuse during /search_videos
        session["current_topic"] = topic
        session["current_books"] = results["books"]
        session["current_pdfs"] = results["pdfs"]
        session["current_roadmap"] = results["roadmap"]

    return render_template("learn.html", results=results)

@main_routes.route("/search_videos", methods=["POST"])
def search_videos():
    query = request.form["video_query"]

    results = {
        "roadmap": session.get("current_roadmap", ""),
        "books": session.get("current_books", []),
        "pdfs": session.get("current_pdfs", []),
        "videos": search_youtube(query)
    }

    return render_template("learn.html", results=results)
@main_routes.route("/ai-videos", methods=["GET", "POST"])
def ai_video_search():
    videos = []
    searched = None
    if request.method == "POST":
        topic = request.form.get("topic")
        searched = topic
        if topic:
            videos = search_youtube(topic)  # This should return a list of {title, url, thumbnail}
    return render_template("aivideosearch.html", videos=videos, searched=searched)


# Create a new user
@main_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    if not username or not email:
        return jsonify({'error': 'Username and email are required'}), 400
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'User with this username or email already exists'}), 409
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201

# Get all users
@main_routes.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email}
        for u in users
    ])

# Get a user by ID
@main_routes.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

# Update a user by ID
@main_routes.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    if username:
        user.username = username
    if email:
        user.email = email
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

# Delete a user by ID
@main_routes.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@main_routes.route('/debug/users', methods=['GET'])
def debug_users():
    users = User.query.all()
    return jsonify([
        {'id': u.id, 'username': u.username, 'email': u.email}
        for u in users
    ])
