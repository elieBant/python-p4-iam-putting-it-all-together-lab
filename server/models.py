from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=True)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = relationship('Recipe', back_populates='user')

    def __init__(self, username, password=None, image_url=None, bio=None):
        if not username:
            raise ValueError("Username is required")
        self.username = username
        if password:
            self.password = password
        else:
            self._password_hash = None
        self.image_url = image_url
        self.bio = bio

    def authenticate(self, password):
        if self._password_hash is None:
            return False
        return self.check_password(password)

    @hybrid_property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        if password:
            self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        else:
            self._password_hash = None

    def check_password(self, password):
        if self._password_hash is None:
            return False
        return bcrypt.check_password_hash(self._password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not username or username.strip() == '':
            raise ValueError('Username must be present.')
        return username

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='recipes')

    @validates('title')
    def validate_title(self, key, title):
        if not title or title.strip() == '':
            raise ValueError('Title must be present.')
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions or len(instructions) < 50:
            raise ValueError('Instructions must be at least 50 characters long.')
        return instructions
