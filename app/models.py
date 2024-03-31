from . import db

class User(db.Model): # initializing class User inherited from db.Model class
    __tablename__ = 'users' # initializing table name
    id = db.Column(db.Integer, primary_key=True) # initializing 'id' as an instance of db.Column class
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('articles', lazy=True))