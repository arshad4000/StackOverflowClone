from views import db
from flask import session
import datetime
import uuid
from sqlalchemy import func

def getNextUniqueId(classn):
    max=0
    if classn=="Questions" :
        max = db.session.query(func.max(Questions.question_id)).scalar()
    elif classn=="Tags":
        max = db.session.query(func.max(Tags.tag_id)).scalar()
    elif classn=="Users":
        max = db.session.query(func.max(Users.user_id)).scalar()
    elif classn=="Answers":
        max = db.session.query(func.max(Answers.answer_id)).scalar()
    elif classn=="Upvotes":
        max = db.session.query(func.max(Upvotes.vote_id)).scalar()
    elif classn=="Downvotes":
        max = db.session.query(func.max(Downvotes.vote_id)).scalar()    
    elif classn=="Comments":
        max = db.session.query(func.max(Comments.comment_id)).scalar()    
    return max+1
    
class Questions(db.Model):
    __tablename__='questions'
    question_id = db.Column('question_id',db.Integer, primary_key=True)
    title = db.Column('title', db.Unicode)
    body = db.Column('body',db.String)
    code = db.Column('code', db.String)
    user_id = db.Column('user_id',db.Integer)
    answered = db.Column('answered', db.Integer)
    timestamp = db.Column('timestamp', db.DateTime)

    def __repr__(self):
        return "Questions('{self.question_id}')"
    def __init__(self, title, body, code, user_id):                
        self.question_id = getNextUniqueId("Questions")        
        self.title = title
        self.body = body
        self.code = code
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()

class Tags(db.Model):
    __tablename__="tags"
    tag_id = db.Column('tag_id', db.Integer, primary_key=True)
    body = db.Column('body', db.Unicode)
    question_id = db.Column('question_id', db.Integer)
    def __repr__(self):
        return "Tags('{self.tag_id}')"
    def __init__(self, body,question_id):
        self.tag_id = getNextUniqueId("Tags")
        self.body = body
        self.question_id = question_id


class Users(db.Model):
    __tablename__="users"
    username = db.Column('username', db.Unicode)
    password = db.Column('password_hash', db.Unicode)
    email = db.Column('email', db.Unicode)
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    reputation = db.Column('reputation', db.Integer)
    def __repr__(self):
        return "User('{self.username}')"
    def __init__(self, name, email, username, password):
        self.user_id = getNextUniqueId("Users")
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.reputation = 0

class Answers(db.Model):
    __tablename__="answers"
    answer_id = db.Column('answer_id', db.Integer, primary_key=True)
    title = db.Column('title', db.Unicode)
    body = db.Column('body', db.Text)
    code = db.Column('code', db.Text)
    user_id = db.Column('user_id', db.Integer)
    timestamp = db.Column('timestamp', db.DateTime)
    question_id = db.Column('question_id', db.Integer)
    def __repr__(self):
        return "Answer('{self.title}')"
    def __init__(self, question_id, body, code, user_id):                
        self.answer_id = getNextUniqueId("Answers")
        self.question_id = question_id
        self.body = body
        self.code = code
        self.user_id = user_id
        self.timestamp = datetime.datetime.now()

class Upvotes(db.Model):
    __tablename__="upvotes"
    vote_id = db.Column('vote_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    question_id = db.Column('question_id', db.Integer)
    answer_id = db.Column('answer_id', db.Integer)
    def __repr__(self):
        return "Upvotes('{self.vote_id}')"
    def __init__(self, user_id, question_id, answer_id):
        self.vote_id = getNextUniqueId("Upvotes")
        self.user_id = user_id
        self.question_id = question_id
        self.answer_id = answer_id


class Downvotes(db.Model):
    __tablename__="downvotes"
    vote_id = db.Column('vote_id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    question_id = db.Column('question_id', db.Integer)
    answer_id = db.Column('answer_id', db.Integer)
    def __repr__(self):
        return "Downvotes('{self.vote_id}')"
    def __init__(self, user_id, question_id, answer_id):
        self.vote_id = getNextUniqueId("Downvotes")
        self.user_id = user_id
        self.question_id = question_id
        self.answer_id = answer_id
        

class Comments(db.Model):
    __tablename__="comments"
    comment_id = db.Column('comment_id', db.Integer, primary_key=True)
    body = db.Column('body', db.Text)
    user_id = db.Column('user_id', db.Integer)
    question_id = db.Column('question_id', db.Integer)
    answer_id = db.Column('answer_id', db.Integer)
    def __repr__(self):
        return "Comments('{self.comment_id}')"
    def __init__(self, body, user_id, question_id, answer_id):
        self.comment_id = getNextUniqueId("Comments")
        self.body = body
        self.user_id = user_id
        self.question_id = question_id
        self.answer_id = answer_id