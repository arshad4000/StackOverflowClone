from flask import render_template,request,redirect,url_for,session
from sqlalchemy import and_
from wtforms import Form, StringField, TextAreaField, PasswordField
from app import app
from app import db
from app.models import Questions, Users, Answers, Upvotes, Downvotes, Tags, Comments

@app.route("/")
def index():
  return render_template('index.html', title="StackOverflowClone")


@app.route("/register", methods=['GET','POST'])
def register():
  form = RegisterForm(request.form)
  if(request.method=='POST' and form.validate()):
    name = form.name.data
    email = form.email.data
    username = form.username.data
    password = form.password.data
    if(name=="" or email=="" or username=="" or password==""):
      return render_template('register.html', requiredValuesMissing=True, form=form)

    user_email = Users.query.filter_by(email=email).first()
    user_username = Users.query.filter_by(username=username).first()
    if user_email or user_username:      
      return render_template('register.html', form=form, emailExists=user_email, usernameExists=user_username)
    else:
      #register the user
      new_row = Users(name, email, username, password)
      db.session.add(new_row)
      db.session.commit()
      session['registrationFlow']=True
      return render_template('login.html', registrationFlow=True)

  return render_template('register.html', form=form)

class RegisterForm(Form):
  name = StringField('Name')
  username = StringField('Username')
  email = StringField('Email')
  password = PasswordField('Password')
  confirmpass = PasswordField('Confirm Password')



@app.route("/login", methods=['GET','POST'])
def login():
  if(request.method == "POST"):
    email = request.form['email']
    password = request.form['password']
    user  = Users.query.filter(and_(Users.email == email, Users.password == password)).first()
    if user:
      session['username'] = user.username
      session['userid'] = user.user_id
      session['loggedin'] = True
      return render_template('index.html', session=session)
    else:
      return render_template('login.html', loginfailed=True)
  else:    
    if session.has_key('loggedin') and session['loggedin'] :      
      return render_template('index.html', session=session)
  
  return render_template('login.html')



@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for('index'))



@app.route("/ask", methods=['GET','POST'])
def ask():
  if(request.method=='POST' and request.form['question_keyword']):
    keyword = request.form['question_keyword']
    questions = Questions.query.all()
    titles={}
    links={}
    tags={}
    count=0
    flag=0
    for question in questions:
        if(question.title and keyword.lower() in question.title.lower()):
            flag=1            
            titles[question.question_id] = question.title
            links[question.question_id] = question.question_id
            tags[question.question_id] = Tags.query.filter_by(question_id=question.question_id).all()
    
    if(flag==0):    
      return render_template('results.html',nomatches=True)
    else:      
      return render_template('results.html',titles=titles, links=links,tags=tags)
  else:
    return redirect(url_for('index'))



#Util method
def getUsername(user_id):
  user = Users.query.filter_by(user_id=user_id).first()
  if user:
    return user.username

def getVotesAnswer(answer_id, type):
  if(type==1):
    upvotes= Upvotes.query.filter_by(answer_id=answer_id).all()
    return len(upvotes)
  else:
    downvotes = Downvotes.query.filter_by(answer_id=answer_id).all()
    return len(downvotes)


@app.route("/question/<id>")
def answers(id):
  commenters = {}
  upvotes={}
  downvotes={}
  tags=[]
  reputation={}
  question_comments=[]  
  answer_comments={}
  question_commenters={}
  answer_commenters={}
  if id :
    question = Questions.query.filter_by(question_id=id).first()  
    tags = Tags.query.filter_by(question_id=id).all()
    answers = Answers.query.filter_by(question_id=id).all()
    question_comments = Comments.query.filter_by(question_id=id).all()    
    for comment in question_comments:
      question_commenters[comment.user_id] = getUsername(comment.user_id)

    username = getUsername(question.user_id)
    for answer in answers:
      commenters[answer.answer_id] = getUsername(answer.user_id)
      upvotes[answer.answer_id] = getVotesAnswer(answer.answer_id,1)
      downvotes[answer.answer_id] = getVotesAnswer(answer.answer_id,-1)      
      reputation[answer.user_id] = getReputation(answer.user_id)
      answer_comments[answer.answer_id] = Comments.query.filter_by(answer_id=answer.answer_id).all()
      for comment in answer_comments[answer.answer_id]:
        answer_commenters[comment.comment_id] = getUsername(comment.user_id)
  return render_template('question.html',question=question, postedby=username, answers=answers,commenters=commenters, 
  upvotes=upvotes, downvotes=downvotes, tags=tags, reputation=reputation, question_comments=question_comments, 
  answer_comments=answer_comments, question_commenters=question_commenters, answer_commenters=answer_commenters)


@app.route("/question_post", methods=['GET','POST'])
def postQuestion():
  if(not session or not session['loggedin']):
    return redirect(url_for('index'))

  if(request and request.method=='POST'):
    title = request.form['title']
    body = request.form['content']
    code = request.form['code']
    tagstring = request.form['tags']
    tags = tagstring.split(';')
    
    new_row = Questions(title,body,code,session['userid'])
    question_id = new_row.question_id    
    db.session.add(new_row)

    for tag in tags:
      new_tag = Tags(tag,question_id)
      db.session.add(new_tag)

    db.session.commit()
    # return redirect(url_for("answers/"+str(2)))
    return answers(question_id)
  else:
    return render_template('question_post.html')


@app.route("/answer/<qid>", methods=['GET','POST'])
def answer(qid):
  if(request and request.method=='POST'):
    body = request.form['content']
    code = request.form['code']    
    new_row = Answers(qid,body,code,session['userid'])
    db.session.add(new_row)
    db.session.commit()
    return redirect(url_for('answers', id=qid))
  else:
    return render_template('answer.html')

def getReputation(user_id):
  upvotes_c = Upvotes.query.filter_by(user_id=user_id).all()
  downvotes_c = Downvotes.query.filter_by(user_id=user_id).all()
  reputation = len(upvotes_c)*10 - len(downvotes_c)*(5)
  return reputation

@app.route("/profile")
@app.route("/profile/<uid>")
def profile(uid=None):
  if session and session['userid']:
    if uid :
      user_id = uid
    else:
      user_id = session['userid']
    user = Users.query.filter_by(user_id=user_id).first()
    reputation = getReputation(user_id)
    return render_template('profile.html', user=user, reputation=reputation)
  else :
    return "you are not logged in.."



##VOTING SYSTEM
@app.route("/upvote/<answer_id>",methods=['GET','POST'])
def upvote(answer_id):
  if not session:
    return "unauthorized"  
  user_id=session['userid']   
  voted = Upvotes.query.filter(and_(Upvotes.user_id==user_id, Upvotes.answer_id==answer_id)).first()
  if voted is not None :
    return "false"
  else : 
    answer=Answers.query.filter_by(answer_id=answer_id).first()
    question_id = answer.question_id    
    new_vote = Upvotes(answer.user_id,question_id,answer_id)
    db.session.add(new_vote)
    db.session.commit()
    return str(getVotesAnswer(answer_id,1))


@app.route("/downvote/<answer_id>",methods=['GET','POST'])
def downvote(answer_id):
  if not session:
    return "unauthorized"

  user_id=session['userid']  
  voted = Downvotes.query.filter(and_(Downvotes.user_id==user_id, Downvotes.answer_id==answer_id)).first()
  if voted is not None :
    return "false"
  else : 
    answer=Answers.query.filter_by(answer_id=answer_id).first()
    question_id = answer.question_id
    new_vote = Downvotes(answer.user_id,question_id,answer_id)
    db.session.add(new_vote)
    db.session.commit()
    return str(getVotesAnswer(answer_id,-1))



@app.route("/comment_question/<question_id>",methods=['GET','POST'])
def comment_question(question_id):
  if not (session and session.has_key('userid')):
    return "unauthorized"
  else:
    comment_value = request.data
    comment_value = comment_value.split("=")[1]
    print(comment_value)
    new_comment = Comments(comment_value, session['userid'], question_id, None)
    db.session.add(new_comment)
    db.session.commit()
    return "true"

@app.route("/comment_answer/<answer_id>", methods=['GET','POST'])
def comment_answer(answer_id):
  if not (session and session.has_key('userid')):
    return "unauthorized"
  else:
    comment_value = request.data
    comment_value = comment_value.split("=")[1]
    new_comment = Comments(comment_value, session['userid'], None, answer_id)
    db.session.add(new_comment)
    db.session.commit()
    return "true"

@app.route("/search_by_tag/<tag>")
def searchByTag(tag):
  print(tag)
  tags = Tags.query.filter_by(body=tag).all()
  print(tags)
  questions=[]
  titles={}
  links={}
  tags_q={}
  for tag in tags:
    question_id = tag.question_id;
    print(question_id)
    if question_id:
      questions.append(Questions.query.filter_by(question_id=question_id).first())
      
  flag=0
  for question in questions:      
    flag=1            
    titles[question.question_id] = question.title
    links[question.question_id] = question.question_id
    tags_q[question.question_id] = Tags.query.filter_by(question_id=question.question_id).all()
  
  if(flag==0):    
    return render_template('search_by_tag.html',nomatches=True)
  else:      
    return render_template('search_by_tag.html',titles=titles, links=links,tags=tags_q)  


