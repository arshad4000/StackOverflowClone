from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

#connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/jarvis/MyGitRepositories/MyStackOverflow/app/app.db'
db = SQLAlchemy(app)
app.secret_key='MYSECRETKEY'

#tables -- in models.py

#app module
from app import views