from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from typing import Optional
from FlaskBlog import db, login_manager, app
from datetime import datetime, timezone
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Creating a class for the database table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # This is a relationship
    posts = db.relationship('Post', backref='author',
                            lazy=True)

    def get_reset_token(self, expires_sec=1200):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    # def verify_reset_token(token):
    def verify_reset_token(token: str) -> Optional['User']:
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data_tuple = s.loads(token)

            # Extract the data from the tuple
            data: dict = data_tuple[0]

            # user_id can be None
            user_id: Optional[int] = data.get('user_id')
            if user_id is None:
                return None
            # user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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
