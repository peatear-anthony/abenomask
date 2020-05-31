from datetime import datetime
from flasksite import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)

    first_name = db.Column(db.String(50), unique=False, nullable=False)
    last_name = db.Column(db.String(50), unique=False, nullable=False)
    postal_code = db.Column(db.Integer, unique=False, nullable=False)
    prefecture = db.Column(db.String(120), unique=False, nullable=False, default='Tokyo')
    my_number = db.Column(db.Integer, unique=False, nullable=False)

    email = db.Column(db.String(120), unique=False, nullable=False)
    image_file = db.Column(db.String(20), unique=False, nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey('park.id'),unique=False, nullable=True, default=0)
    posts = db.relationship('Post', backref='author', lazy=True)
    reservations = db.relationship('Reservation', backref='author', lazy=True)

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
    prefecture = db.Column(db.String(100), nullable=False)
    area  = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=0)
    count = db.Column(db.Integer, nullable=False, default=0)
    people = db.relationship('User', backref='location', lazy=True)
    reservations = db.relationship('Reservation', backref='place', lazy=True)

    def __repr__(self):
        return f"Post('{self.name}', '{self.prefecture}', '{self.area}', {self.lat}', '{self.lon}', '{self.capacity}', '{self.present}')"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    park_id = db.Column(db.Integer, db.ForeignKey('park.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"Reservation('{self.date_created}', '{self.park_id}' ,'{self.user_id}')"
