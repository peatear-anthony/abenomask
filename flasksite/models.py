from datetime import datetime
from flasksite import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    postal_code = db.Column(db.Integer, unique=True, nullable=False)
    my_number = db.Column(db.Integer, unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey('park.id'),unique=False, nullable=True, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Park(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    prefecture = db.Column(db.String(100), unique=True, nullable=False)
    Area  = db.Column(db.Float, nullable=False)
    Lat = db.Column(db.Float, nullable=False)
    Long = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    present = db.Column(db.Integer, nullable=False, default=0)
    people = db.relationship('User', backref='people', lazy=True)

    def __repr__(self):
        return f"Post('{self.name}', '{self.prefecture}', '{self.area}', {self.lat}', '{self.long}', '{self.capacity}', '{self.present}')"
