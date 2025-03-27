from flask_restful import Resource, Api
from flask import request, jsonify
from .models import *
from datetime import datetime
import json

api=Api()



class CommonApi(Resource):

#Creating data
  def post(self):
    name = request.json.get("email")
    print(name)
    password = request.json.get("password")
    print(password)
    try:
      authen=Authentication.query.filter_by(email=name, password=password).first()
      if authen and authen.role=="admin":
        return {"message" : "Admin logged in successfully..."}, 200
      elif authen and authen.role=="user":
        return {"message" : "User logged in successfully..."}, 200
      else:
        return {"error" : "Check your credentials..."}, 400
    except:
      return {"error":"Internal Server Error"}, 500

  def post(self):
    email = request.json.get("email")
    password = request.json.get("password")
    f_name = request.json.get("f_name")
    l_name = request.json.get("l_name")
    qualification = request.json.get("qualification")
    dob = request.json.get("dob")
    if(dob):
      dob=datetime.strptime(dob, '%Y-%m-%d')
    try:
      user=Authentication.query.filter_by(email=email).first()
      if user: 
        return {"message" : "Sorry, this email is already registered!"}, 400
      else:
        new_user_auth=Authentication(email=email, password=password, role='user')
        new_user=User(email=email,f_name=f_name, l_name=l_name, qualification=qualification, dob=dob)
        db.session.add(new_user_auth)
        db.session.add(new_user)
        db.session.commit()
        return {"message" : "Registration successfull, please proceed to login now!"}, 201
    except:
      return {"error":"Internal Server Error"}, 500

class SubjectApi(Resource):

  #Reading data
  def get(self):
    subjects = Subject.query.all()
    subjects_json = []
    for subject in subjects:
      subjects_json.append({"id" : subject.sub_id, "name" : subject.name, "description" : subject.description})
    return subjects_json

  #Creating data
  def post(self):
    sub_name = request.json.get("name")
    description = request.json.get("description")
    try:
      new_subject=Subject(name=sub_name, description=description)
      db.session.add(new_subject)
      db.session.commit()
      return {"message" : "New subject added!"}, 201
    except:
      return {"error":"Internal Server Error"}, 500

  #Updating data
  def put(self, subject_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      sub_name = request.json.get("name")
      description = request.json.get("description")
      subject.name=sub_name 
      subject.description=description
      db.session.commit()
      return {"message" : "Subject updated successfully..."}, 200
    except:
      return {"error":"Internal Server Error"}, 500

  #Deleting data
  def delete(self, subject_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      db.session.delete(subject)
      db.session.commit()
      return {"message" : "Subject deleted successfully..."}, 200
    except:
      return {"error" : "Internal Server Error"}, 500

class ChapterApi(Resource):
  #Reading data
  def get(self):
    chapters = Chapter.query.all()
    chapters_json = []
    for chapter in chapters:
      chapters_json.append({"id" : chapter.ch_id, "subject_id" : chapter.subject_id, "name" : chapter.name, "description" : chapter.description})
    return chapters_json

  #Creating data
  def post(self, subject_id):
    chap_name = request.json.get("name")
    description = request.json.get("description")
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      new_chapter=Chapter(subject_id=subject.sub_id, name=chap_name, description=description)
      db.session.add(new_chapter)
      db.session.commit()
      return {"message" : "New chapter added!"}, 201
    except:
      return {"error":"Internal Server Error"}, 500

  #Updating data
  def put(self, subject_id, chapter_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      ch_name = request.json.get("name")
      description = request.json.get("description")
      chapter.name=ch_name 
      chapter.description=description
      db.session.commit()
      return {"message" : "Chapter updated successfully..."}, 200
    except:
      return {"error":"Internal Server Error"}, 500

  def delete(self, subject_id, chapter_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      db.session.delete(chapter)
      db.session.commit()
      return {"message" : "Chapter deleted successfully..."}, 200
    except:
      return {"error" : "Internal Server Error"}, 500

class QuizApi(Resource):
  #Reading data
  def get(self):
    quizzes = Quiz.query.all()
    quizzes_json = []
    for quiz in quizzes:
      quizzes_json.append({"id" : quiz.q_id, "name" : quiz.name, "chapter_id" : quiz.chapter_id, "date_of_quiz" : str(quiz.date_of_quiz), "time_duration" : quiz.time_duration, "remarks" : quiz.remarks})
    return quizzes_json

  #Creating data
  def post(self, subject_id, chapter_id):
    q_name = request.json.get("name")
    date_of_quiz = request.json.get("date_of_quiz")
    if(date_of_quiz):
      date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d')
    time_duration = request.json.get("time_duration")
    remarks = request.json.get("remarks")
    try:
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      new_quiz=Quiz(date_of_quiz=date_of_quiz, time_duration=time_duration, remarks=remarks, name=q_name, chapter=chapter)
      db.session.add(new_quiz)
      db.session.commit()
      return {"message" : "New quiz added!"}, 201
    except:
      return {"error":"Internal Server Error"}, 500

  #Updating data
  def put(self, subject_id, chapter_id, quiz_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
      quiz_name=request.json.get("name")
      date_of_quiz=request.json.get("date_of_quiz")
      if(date_of_quiz):
        date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d')
      time_duration=request.json.get("time_duration")
      remarks=request.json.get("remarks")
      quiz.name=quiz_name 
      quiz.date_of_quiz=date_of_quiz
      quiz.time_duration=time_duration
      quiz.remarks=remarks
      db.session.commit()
      return {"message" : "Quiz updated successfully..."}, 200
    except:
      return {"error":"Internal Server Error"}, 500

  def delete(self, subject_id, chapter_id, quiz_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
      db.session.delete(quiz)
      db.session.commit()
      return {"message" : "Quiz deleted successfully..."}, 200
    except:
      return {"error" : "Internal Server Error"}, 500

class QuestionApi(Resource):

  #Reading data
  def get(self):
    questions = Question.query.all()
    questions_json = []
    for question in questions:
      questions_json.append({"id" : question.ques_id, "quiz_id" : question.quiz_id, "question_statement" : question.question_statement, "q_title" : question.q_title,
       "option_1" : question.option_1, "option_2" : question.option_2, "option_3" : question.option_3,  "option_4" : question.option_4, "correct_option" : question.correct_option})
    return questions_json

  #Creating data
  def post(self, subject_id, chapter_id, quiz_id):
    q_title = request.json.get("q_title")
    q_statement = request.json.get("q_statement")
    option_1 = request.json.get("option_1")
    option_2 = request.json.get("option_2")
    option_3 = request.json.get("option_3")
    option_4 = request.json.get("option_4")
    correct_option = request.json.get("correct_option")
    try:
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      new_question=Question(q_title=q_title, quiz_id=quiz_id, question_statement=q_statement, option_1=option_1, option_2=option_2, option_3=option_3, option_4=option_4, correct_option=correct_option)
      db.session.add(new_question)
      db.session.commit()
      return {"message" : "New question added!"}, 201
    except:
      return {"error":"Internal Server Error"}, 500

  #Updating data
  def put(self, subject_id, chapter_id, quiz_id, question_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
      question = db.session.query(Question).filter(Question.ques_id == question_id).first()
      q_title=request.json.get("q_title")
      question_statement=request.json.get("question_statement")
      option_1=request.json.get("option_1")
      option_2=request.json.get("option_2")
      option_3=request.json.get("option_3")
      option_4=request.json.get("option_4")
      correct_option=request.json.get("correct_option")
      question.q_title=q_title 
      question.question_statement=question_statement
      question.option_1=option_1
      question.option_2=option_2
      question.option_3=option_3
      question.option_4=option_4
      question.correct_option=correct_option
      db.session.commit()
      return {"message" : "Question updated successfully..."}, 200
    except:
      return {"error":"Internal Server Error"}, 500

  def delete(self, subject_id, chapter_id, quiz_id, question_id):
    try:
      subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
      chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
      quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
      question = db.session.query(Question).filter(Question.ques_id == question_id).first()
      db.session.delete(question)
      db.session.commit()
      return {"message" : "Question deleted successfully..."}, 200
    except:
      return {"error" : "Internal Server Error"}, 500

class ScoresApi(Resource):
  #Reading data
  def get(self):
    scores = Scores.query.all()
    scores_json = []
    for score in scores:
      scores_json.append({"id" : score.score_id, "quiz_id" : score.quiz_id, "user_id" : score.user_id, "timestamp_of_attempt" : str(score.timestamp_of_attempt), "total_scored" : score.total_scored})
    return scores_json

api.add_resource(CommonApi, "/api/login", "/api/register")
api.add_resource(SubjectApi,"/api/get_subjects", "/api/new_subject", "/api/edit_subject/<int:subject_id>", "/api/delete_subject/<int:subject_id>")
api.add_resource(ChapterApi,"/api/get_chapters", "/api/new_chapter/<int:subject_id>", "/api/edit_chapter/<int:subject_id>/<int:chapter_id>", "/api/delete_chapter/<int:subject_id>/<int:chapter_id>")
api.add_resource(QuizApi,"/api/get_quizzes", "/api/new_quiz/<int:subject_id>/<int:chapter_id>", "/api/edit_quiz/<int:subject_id>/<int:chapter_id>/<int:quiz_id>", "/api/delete_quiz/<int:subject_id>/<int:chapter_id>/<int:quiz_id>")
api.add_resource(QuestionApi,"/api/get_questions", "/api/new_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>", "/api/edit_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>", "/api/delete_question/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>")
api.add_resource(ScoresApi,"/api/get_scores")