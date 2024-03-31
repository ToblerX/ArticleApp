from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'UAHSDIAHSIDHJASIDJ'  # Remember to change this to a secure random key in production

# Configuration for SQLAlchemy (replace 'postgresql://superuser:password@localhost/database' with your database URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://superuser:password@localhost/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Import routes after initializing the Flask app to avoid circular imports
from . import routes