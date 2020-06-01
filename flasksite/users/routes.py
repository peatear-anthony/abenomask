from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flasksite import db, bcrypt
from flasksite.models import User, Post, Park, Reservation
from flasksite.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flasksite.users.utils import save_picture


users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # If they create an account hash the password and add to the DB
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create a new user
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            postal_code=form.postal_code.data,
            prefecture=form.prefecture.data,
            my_number=form.my_number.data,
            password=form.password.data,
            email=form.email.data)
        # Add to DB
        #user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        # Flash message to User
        flash('Your account has been created, You are now able to log in!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (user.password == form.password.data):
            # Log-in the user
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #flash('You have been logged in!', 'success')
            return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('main.mainpage'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form  = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file =  picture_file
        current_user.username = form.username.data
        current_user.prefecture = form.prefecture.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.my_number.data = current_user.my_number
        form.postal_code.data = current_user.postal_code
        form.prefecture.data = current_user.prefecture
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
        image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    # Get the page from the url
    page = request.args.get('page', 1, type=int)
    # Get first user or retrun a 404 error if None
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=2, page=page)

    return render_template('user_post.html', posts=posts, user=user)