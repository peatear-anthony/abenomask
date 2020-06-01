# main/routes.py
from flask import render_template, request, Blueprint
from flasksite.models import Post, Park, User
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route("/home")
def home():
    # Get the page from the url
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=2, page=page)
    return render_template('home.html', posts=posts)

@main.route("/")
@main.route("/mainpage")
@login_required
def mainpage():
    # Get User and Park Info
    user = User.query.filter_by(username=current_user.username).first_or_404()
    parks = Park.query\
        .filter_by(prefecture=current_user.prefecture)\
        .order_by(Park.fake_distance).paginate(per_page=5)
    return render_template('mainpage.html', parks=parks, user=user)

@main.route("/about")
def about():
    return render_template('about.html', title='About')