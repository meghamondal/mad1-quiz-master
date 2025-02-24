from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime

class Authentication(db.Model):
  __tablename__="auth"
  id=db.Column(db.Integer, primary_key=True)
  email=db.Column(db.String, unique=True, nullable=False)
  password=db.Column(db.String, nullable=False)
  role=db.Column(db.String, nullable=False)
  user_details=db.relationship("User", cascade="all,delete", backref="user", lazy=True)


class User(db.Model):
  __tablename__="user"
  user_id=db.Column(db.Integer, primary_key=True)
  email=db.Column(db.String, db.ForeignKey("auth.email"), unique=True, nullable=False)
  f_name=db.Column(db.String, nullable=False) # make 2 variables f_name
  l_name=db.Column(db.String, nullable=False) 
  qualification=db.Column(db.String)
  dob=db.Column(db.DateTime, nullable=False)
  scores=db.relationship("Scores", cascade="all,delete", backref="user", lazy=True)

class Subject(db.Model):
  __tablename__="subject"
  sub_id=db.Column(db.Integer, primary_key=True, nullable=False)
  name=db.Column(db.String, nullable=False)
  description=db.Column(db.String)
  chapters=db.relationship("Chapter", cascade="all,delete", backref="subject", lazy=True)

class Chapter(db.Model):
  __tablename__="chapter"
  ch_id=db.Column(db.Integer, primary_key=True, nullable=False)
  subject_id=db.Column(db.Integer, db.ForeignKey("subject.sub_id"), nullable=False)
  name=db.Column(db.String, nullable=False)
  description=db.Column(db.String)
  quizes=db.relationship("Quiz", cascade="all,delete", backref="chapter", lazy=True)

class Quiz(db.Model):
  __tablename__="quiz"
  q_id=db.Column(db.Integer, primary_key=True, nullable=False)
  chapter_id=db.Column(db.Integer, db.ForeignKey("chapter.ch_id"), nullable=False)
  date_of_quiz=db.Column(db.DateTime, nullable=False, default=datetime.now())
  time_duration=db.Column(db.Integer, nullable=True, default=60)
  remarks=db.Column(db.String)
  questions=db.relationship("Question", cascade="all,delete", backref="quiz", lazy=True)
  scores=db.relationship("Scores", cascade="all,delete", backref="quiz", lazy=True)

class Question(db.Model):
  __tablename__="question"
  ques_id=db.Column(db.Integer, primary_key=True, nullable=False)
  quiz_id=db.Column(db.Integer, db.ForeignKey("quiz.q_id"), nullable=False)
  question_statement=db.Column(db.String, nullable=False)
  option_1=db.Column(db.Integer, nullable=False)
  option_2=db.Column(db.Integer, nullable=False)
  option_3=db.Column(db.Integer, nullable=False)
  option_4=db.Column(db.Integer, nullable=False)
  correct_option=db.Column(db.Integer, nullable=False)

class Scores(db.Model):
  _tablename__="scores"
  score_id=db.Column(db.Integer, primary_key=True, nullable=False)
  quiz_id=db.Column(db.Integer, db.ForeignKey("quiz.q_id"), nullable=False)
  user_id=db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
  timestamp_of_attempt=db.Column(db.DateTime, nullable=False, default=datetime.now())
  total_scored=db.Column(db.Integer, nullable=False)






