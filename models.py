from extensions import db
from datetime import datetime
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True, default=None) 
    bio = db.Column(db.Text, nullable=True, default="") 
    college_name = db.Column(db.String(120), nullable=True)
    qualification = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    communities = db.relationship('CommunityMembership', back_populates='user', cascade="all, delete")
    posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f'<User {self.username}>'
class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.relationship('User', backref='created_communities', foreign_keys=[created_by])
    members = db.relationship('CommunityMembership', back_populates='community', cascade="all, delete")
    posts = db.relationship('Post', backref='community', lazy=True)

    def __repr__(self):
        return f'<Community {self.name}>'
class CommunityMembership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='communities')
    community = db.relationship('Community', back_populates='members')
    def __repr__(self):
        return f'<Membership User:{self.user_id} -> Community:{self.community_id}>'
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    likes = db.relationship('PostLike', backref='post', lazy='dynamic', cascade="all, delete-orphan")
    @property
    def like_count(self):
        return self.likes.filter_by(is_like=True).count()
    @property
    def dislike_count(self):
        return self.likes.filter_by(is_like=False).count()
    def __repr__(self):
        return f'<Post {self.id} by User:{self.user_id} in Community:{self.community_id}>'
class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    is_like = db.Column(db.Boolean, nullable=False)
    user = db.relationship('User', backref='post_likes')
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.relationship('User', backref='comments')
    post = db.relationship('Post', backref='comments')
    def __repr__(self):
        return f'<Comment {self.id} by User:{self.user_id}>'
