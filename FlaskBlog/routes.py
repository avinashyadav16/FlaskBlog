from flask import render_template, url_for, flash, redirect, request
from FlaskBlog.forms import RegistrationForm, LoginForm
from FlaskBlog.models import User, Post
from FlaskBlog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

POSTS = [
    {
        'author': 'Avinash Yadav',
        'title': 'All About GEN-AI',
        'content': 'GEN-AI stands for General Artificial Intelligence, an advanced form of artificial intelligence that is capable of performing any intellectual task that a human being can. In this post, we explore the potential, challenges, and future prospects of GEN-AI.',
        'date_posted': 'April 14, 2024'
    },
    {
        'author': 'New User',
        'title': 'Plateau Of Latent Potential',
        'content': 'The Plateau of Latent Potential refers to a phase in machine learning and artificial intelligence where advancements appear to stagnate. However, beneath the surface, significant progress is being made in refining algorithms, improving data processing capabilities, and pushing the boundaries of what AI can achieve.',
        'date_posted': 'March 29, 2024'
    }
]


# Decorator
# localhost:5000/
@app.route("/")
def home():
    return render_template('home.html', posts=POSTS)


# localhost:5000/about
@app.route("/about")
def about():
    return render_template('about.html', title='About')


# localhost:5000/register
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        with app.app_context():
            user = User(username=form.username.data,
                        email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()

        flash(f'Account has been created for {form.username.data}!', 'success')
        # Redirect to home page

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# localhost:5000/login
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        with app.app_context():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('Congrats! You have been logged in!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully!',
          'alert alert-primary d-flex align-items-center')
    return redirect(url_for('home'))
