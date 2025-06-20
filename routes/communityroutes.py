from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Community, CommunityMembership, Post, User
from datetime import datetime
from werkzeug.utils import secure_filename
import os

community_routes = Blueprint('community_routes', __name__)

# Route: Show all communities
@community_routes.route("/communities")
def list_communities():
    query = request.args.get("q")
    if query:
        communities = Community.query.filter(Community.name.ilike(f"%{query}%")).all()
    else:
        communities = Community.query.all()
    community_created_success = session.pop("community_created_success", None)
    return render_template("community/list.html", communities=communities, query=query, community_created_success=community_created_success)

# Route: Create a community
@community_routes.route("/communities/create", methods=["GET", "POST"])
def create_community():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]
        user_id = session.get("user_id")

        if not user_id:
            return redirect("/login")

        new_comm = Community(name=name, description=description, created_by=user_id)
        db.session.add(new_comm)
        db.session.commit()

        # Auto-join the creator
        membership = CommunityMembership(user_id=user_id, community_id=new_comm.id)
        db.session.add(membership)
        db.session.commit()

        session["community_created_success"] = True
        return redirect(url_for("community_routes.list_communities"))

    return render_template("community/create.html")

# Route: Join a community
@community_routes.route("/communities/<int:community_id>/join")
def join_community(community_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    already_member = CommunityMembership.query.filter_by(user_id=user_id, community_id=community_id).first()
    if not already_member:
        db.session.add(CommunityMembership(user_id=user_id, community_id=community_id))
        db.session.commit()

    return redirect(url_for("community_routes.view_community", community_id=community_id))

# Route: Leave a community
@community_routes.route("/communities/<int:community_id>/leave")
def leave_community(community_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    membership = CommunityMembership.query.filter_by(user_id=user_id, community_id=community_id).first()
    if membership:
        db.session.delete(membership)
        db.session.commit()

    return redirect(url_for("community_routes.list_communities"))

# Route: View a specific community and its posts
@community_routes.route("/communities/<int:community_id>")
def view_community(community_id):
    community = Community.query.get_or_404(community_id)
    posts = Post.query.filter_by(community_id=community.id).order_by(Post.timestamp.desc()).all()

    user_id = session.get("user_id")
    is_member = False
    if user_id:
        is_member = CommunityMembership.query.filter_by(user_id=user_id, community_id=community.id).first() is not None

    return render_template("community/view.html", community=community, posts=posts, is_member=is_member)

# Route: Add a post to a community
@community_routes.route("/communities/<int:community_id>/post", methods=["POST"])
def post_to_community(community_id):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    # Check if user is a member
    is_member = CommunityMembership.query.filter_by(user_id=user_id, community_id=community_id).first()
    if not is_member:
        return "You must join the community to post.", 403

    content = request.form["content"]
    image = request.files.get("image")

    image_path = None
    if image and image.filename:
        filename = secure_filename(image.filename)
        upload_folder = "static/uploads"
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        image.save(image_path)

    post = Post(
        content=content,
        image_path=image_path,
        user_id=user_id,
        community_id=community_id,
        timestamp=datetime.utcnow()
    )
    db.session.add(post)
    db.session.commit()

    return redirect(url_for("community_routes.view_community", community_id=community_id))

@community_routes.route("/my-communities")
def my_communities():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    memberships = CommunityMembership.query.filter_by(user_id=user_id).all()
    community_ids = [m.community_id for m in memberships]
    communities = Community.query.filter(Community.id.in_(community_ids)).all()

    return render_template("community/my_communities.html", communities=communities)

@community_routes.route("/user/<int:user_id>", methods=["GET", "POST"])
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        bio = request.form.get("bio")
        file = request.files.get("profile_pic")
        if bio is not None:
            user.bio = bio
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = "static/profile_pics"
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            user.profile_pic = f"profile_pics/{filename}"
        db.session.commit()
        return redirect(url_for("community_routes.user_profile", user_id=user.id))
    return render_template("community/user_profile.html", user=user)
