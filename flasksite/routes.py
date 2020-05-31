import os
import secrets
from datetime import datetime, date
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flasksite import app, db, bcrypt
from flasksite.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, MakeReservationForm
from flasksite.models import User, Post, Park, Reservation
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    # Get the page from the url
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=2, page=page)
    return render_template('home.html', posts=posts)

@app.route("/mainpage")
@login_required
def mainpage():
    # Get User and Park Info
    user = User.query.filter_by(username=current_user.username).first_or_404()
    parks = Park.query\
        .filter_by(prefecture=current_user.prefecture)\
        .order_by(Park.fake_distance).paginate(per_page=5)

    return render_template('mainpage.html', parks=parks, user=user)


@app.route("/my_reservations")
@login_required
def my_reservations():
    # Get User and Park Info
    reservations = db.session\
    .query(Reservation, Park)\
    .outerjoin(Park, Reservation.park_id == Park.id)\
    .filter(Reservation.user_id == current_user.id)\
    .order_by(Reservation.date.desc())

    return render_template('my_reservations.html', reservations=reservations)


@app.route("/make_reservation/<int:park_id>", methods=['GET', 'POST'])
@login_required
def make_reservation(park_id):
    form = MakeReservationForm()
    park =  Park.query.filter_by(id=park_id).first_or_404()

    if form.validate_on_submit():
        # create new reservation
        reservation = Reservation(
        date=form.date.data,
        start_time=form.start_time.data,
        end_time=form.start_time.data,
        creator=current_user,
        active=True,
        place=park)

        db.session.add(reservation)
        db.session.commit()
        flash('Your reservation has been made!', 'success')
        return redirect(url_for('mainpage'))
    elif request.method == 'GET':
        form.date.data = date.today()
        form.start_time.data = "1:00"
        form.end_time.data = "3:30"

    return render_template('make_reservation.html', 
        title='Reservation', form = form, park=park)

'''
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', 
        title='New Post', form = form, legend="New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    # get the id or give me a 404 if it doesn't exisit
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)
'''


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and (user.password == form.password.data):
            # Log-in the user
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            #flash('You have been logged in!', 'success')
            return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('mainpage'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    # Change uploaded picture to random name keep ext.
    # Also resizes the photo
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # Save the picture to path
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    
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


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', 
        title='New Post', form = form, legend="New Post")


@app.route("/post/<int:post_id>")
def post(post_id):
    # get the id or give me a 404 if it doesn't exisit
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    # Get the page from the url
    page = request.args.get('page', 1, type=int)
    # Get first user or retrun a 404 error if None
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=2, page=page)

    return render_template('user_post.html', posts=posts, user=user)