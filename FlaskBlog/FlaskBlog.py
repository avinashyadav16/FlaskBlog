from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# Importing forms
from forms import RegistrationForm, LoginForm

# Flask object
app = Flask(__name__)

# This will protect againgst modifing cookies, cross-site requests and forgery attack etc.
app.config['SECRET_KEY'] = '66cf0b437764821383b62fd5da549db4'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# Creating a class for the database table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # This is a relationship
    posts = db.relationship('Post', backref='author',
                            lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        # Redirect to home page
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


# localhost:5000/login
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'avinashurmilayadav@gmail.com' and form.password.data == '123':
            flash('Congrats! You have been logged in!', 'success')
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
