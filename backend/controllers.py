from flask import Flask, render_template, request, redirect, url_for
from .models import *
from flask import current_app as app
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



@app.route("/")
def home():
  return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method=="GET":
    return render_template("login.html", msg="")
  if request.method=="POST":
    name=request.form.get("username")
    password=request.form.get("password")
    authen=Authentication.query.filter_by(email=name, password=password).first()
    if authen and authen.role=="admin":
      return redirect("/admin_dashboard/"+name)
    elif authen and authen.role=="user":
      return redirect("/user_dashboard/"+name)
    else:
      return render_template("login.html", msg="Invalid credentials...")
    
@app.route('/admin_dashboard/<name>', methods=["GET","POST"])
def admin_dashboard(name):
  if request.method=="GET":
    subjects = db.session.query(Subject).all()
    return render_template("admin_dashboard.html", name=name, subjects=subjects)


## for quizzes in a chapter
@app.route('/admin_dashboard/<int:subject_id>/<int:chapter_id>/<string:name>')
def quizzes_in_chapters(subject_id, chapter_id, name):
  quizzes_in_chapters = db.session.query(Chapter).filter((Chapter.subject_id == subject_id) & (Chapter.ch_id == chapter_id)).first().quizes
  chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
  subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
  for quiz in quizzes_in_chapters:
    quiz.date_of_quiz_str = datetime.date(quiz.date_of_quiz)
  return render_template('quizzes_page.html', quizzes = quizzes_in_chapters, chapter=chapter, subject=subject, name=name)

#for questions in quiz
@app.route('/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<string:name>')
def questions_in_quizzes(subject_id, chapter_id, quiz_id, name):
  quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
  questions_in_quizzes=quiz.questions
  chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
  subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
  return render_template('questions_page.html', quiz=quiz, questions = questions_in_quizzes, chapter=chapter, subject=subject, name=name)

#for question details
@app.route('/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>/<string:name>')
def question_details(subject_id, chapter_id, quiz_id, question_id, name):
  if request.method == 'GET':
    question = db.session.query(Question).filter(Question.ques_id == question_id).first()
    return render_template('admin_quiz.html', question=question, name=name)




  
  
@app.route("/register", methods=['GET','POST'])
def register():
  if request.method=='POST':
    email=request.form.get("email")
    password=request.form.get("password")
    f_name=request.form.get("f_name")
    l_name=request.form.get("l_name")
    qualification=request.form.get("qualification")
    dob=request.form.get("dob")
    if(dob):
      dob=datetime.strptime(dob, '%Y-%m-%d')
    user=Authentication.query.filter_by(email=email).first()
    if user: 
      return render_template("register.html", msg="Sorry, this email is already registered!")
    new_user_auth=Authentication(email=email, password=password, role='user')
    new_user=User(email=email,f_name=f_name, l_name=l_name, qualification=qualification, dob=dob)

    db.session.add(new_user_auth)
    db.session.add(new_user)
    db.session.commit()
    return render_template("login.html", msg="Registration successfull, please proceed to login now!")
  return render_template('register.html', msg="")

#for new quiz
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/new_quiz/<string:name>", methods=['GET','POST'])
def new_quiz(subject_id, chapter_id, name):
  if request.method=='POST':
    q_name=request.form.get("name")
    date_of_quiz=request.form.get("date_of_quiz")
    if(date_of_quiz):
      date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d')
    time_duration=request.form.get("time_duration")
    remarks=request.form.get("remarks")
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    new_quiz=Quiz(date_of_quiz=date_of_quiz, time_duration=time_duration, remarks=remarks, name=q_name, chapter=chapter)
    db.session.add(new_quiz)
    db.session.commit()
    return redirect('/admin_dashboard/'+str(subject_id)+"/"+str(chapter_id)+"/"+str(name))
  
  elif(request.method=='GET'):
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    return render_template('new_quiz.html', chapter=chapter, name=name)
  
#for new question
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/new_question/<string:name>", methods=['GET','POST'])
def new_question(subject_id, chapter_id, quiz_id, name):
  if request.method=='POST':
    q_title=request.form.get("q_title")
    q_statement=request.form.get("q_statement")
    option_1=request.form.get("option_1")
    option_2=request.form.get("option_2")
    option_3=request.form.get("option_3")
    option_4=request.form.get("option_4")
    correct_option=request.form.get("correct_option")
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    new_question=Question(q_title=q_title, quiz_id=quiz_id, question_statement=q_statement, option_1=option_1, option_2=option_2, option_3=option_3, option_4=option_4, correct_option=correct_option)
    db.session.add(new_question)
    db.session.commit()
    return redirect('/admin_dashboard/'+str(subject_id)+"/"+str(chapter_id)+"/"+str(quiz_id)+"/"+str(name))
  
  elif(request.method=='GET'):
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    return render_template('new_question.html', chapter=chapter, quiz=quiz, name=name)
    


#foe new subject
@app.route("/admin_dashboard/new_subject/<string:name>", methods=['GET','POST'])
def new_subject(name):
  if request.method=='POST':
    sub_name=request.form.get("name")
    description=request.form.get("description")
    new_subject=Subject(name=sub_name, description=description)
    db.session.add(new_subject)
    db.session.commit()
    return redirect('/admin_dashboard/'+"/"+str(name))
  
  elif(request.method=='GET'):
    return render_template('new_subject.html', name=name)
    

#for new chapter
@app.route("/admin_dashboard/<int:subject_id>/new_chapter/<string:name>", methods=['GET','POST'])
def new_chapter(subject_id, name):
  if request.method=='POST':
    chap_name=request.form.get("name")
    description=request.form.get("description")
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    new_chapter=Chapter(subject_id=subject.sub_id, name=chap_name, description=description)
    db.session.add(new_chapter)
    db.session.commit()
    return redirect('/admin_dashboard/'+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    return render_template('new_chapter.html',subject=subject, name=name)

#for edit subject 
@app.route("/admin_dashboard/<int:subject_id>/edit_subject/<string:name>", methods=['GET','POST'])
def edit_subject(subject_id,name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    sub_name=request.form.get("name")
    description=request.form.get("description")
    subject.name=sub_name 
    subject.description=description
    db.session.commit()
    return redirect('/admin_dashboard/'+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    return render_template('edit_subject.html',subject=subject, name=name)
  
#for delete subject
@app.route("/admin_dashboard/<int:subject_id>/delete_subject/<string:name>", methods=['GET','POST'])
def delete_subject(subject_id,name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    db.session.delete(subject)
    db.session.commit()
    return redirect('/admin_dashboard/'+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    return render_template('delete_subject.html',subject=subject, name=name)
  

#for edit chapter
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/edit_chapter/<string:name>", methods=['GET','POST'])
def edit_chapter(subject_id, chapter_id, name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    ch_name=request.form.get("name")
    description=request.form.get("description")
    chapter.name=ch_name 
    chapter.description=description
    db.session.commit()
    return redirect('/admin_dashboard/'+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    return render_template('edit_chapter.html',subject=subject, chapter=chapter, name=name)
  
#for delete chapter
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/delete_chapter/<string:name>", methods=['GET','POST'])
def delete_chapter(subject_id, chapter_id, name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    db.session.delete(chapter)
    db.session.commit()
    return redirect('/admin_dashboard/'+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    return render_template('delete_chapter.html',subject=subject, chapter=chapter, name=name)
  
#for edit chapter
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/edit_quiz/<string:name>", methods=['GET','POST'])
def edit_quiz(subject_id, chapter_id, quiz_id, name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    quiz_name=request.form.get("name")
    date_of_quiz=request.form.get("date_of_quiz")
    if(date_of_quiz):
      date_of_quiz=datetime.strptime(date_of_quiz, '%Y-%m-%d')
    time_duration=request.form.get("time_duration")
    remarks=request.form.get("remarks")
    quiz.name=quiz_name 
    quiz.date_of_quiz=date_of_quiz
    quiz.time_duration=time_duration
    quiz.remarks=remarks
    db.session.commit()
    return redirect('/admin_dashboard/'+str(subject_id)+"/"+str(chapter_id)+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    quiz.date_of_quiz_str = datetime.date(quiz.date_of_quiz)
    return render_template('edit_quiz.html',subject=subject, chapter=chapter, quiz=quiz, name=name)
  

#for delete quiz  
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/delete_quiz/<string:name>", methods=['GET','POST'])
def delete_quiz(subject_id, chapter_id, quiz_id, name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    db.session.delete(quiz)
    db.session.commit()
    return redirect('/admin_dashboard/'+str(subject_id)+"/"+str(chapter_id)+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    quiz.date_of_quiz_str = datetime.date(quiz.date_of_quiz)
    return render_template('delete_quiz.html',subject=subject, chapter=chapter, quiz=quiz, name=name)
  
#for edit question
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>/edit_question/<string:name>", methods=['GET','POST'])
def edit_question(subject_id, chapter_id, quiz_id, question_id, name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    question = db.session.query(Question).filter(Question.ques_id == question_id).first()
    q_title=request.form.get("q_title")
    question_statement=request.form.get("question_statement")
    option_1=request.form.get("option_1")
    option_2=request.form.get("option_2")
    option_3=request.form.get("option_3")
    option_4=request.form.get("option_4")
    correct_option=request.form.get("correct_option")
    question.q_title=q_title 
    question.question_statement=question_statement
    question.option_1=option_1
    question.option_2=option_2
    question.option_3=option_3
    question.option_4=option_4
    question.correct_option=correct_option
    db.session.commit()
    return redirect('/admin_dashboard/'+str(subject_id)+"/"+str(chapter_id)+"/"+str(quiz_id)+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    question = db.session.query(Question).filter(Question.ques_id == question_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    return render_template('edit_question.html',subject=subject, chapter=chapter,question=question, quiz=quiz, name=name)
  
#for delete question
@app.route("/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<int:question_id>/delete_question/<string:name>", methods=['GET','POST'])
def delete_question(subject_id, chapter_id, quiz_id, question_id, name):
  if request.method=='POST':
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    question = db.session.query(Question).filter(Question.ques_id == question_id).first()
    db.session.delete(question)
    db.session.commit()
    return redirect('/admin_dashboard/'+str(subject_id)+"/"+str(chapter_id)+"/"+str(quiz_id)+"/"+str(name))
  
  elif(request.method=='GET'):
    subject = db.session.query(Subject).filter(Subject.sub_id == subject_id).first()
    chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
    question = db.session.query(Question).filter(Question.ques_id == question_id).first()
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    return render_template('delete_question.html',subject=subject, chapter=chapter,question=question, quiz=quiz, name=name)
  

#admin_summary
@app.route("/admin_summary/<string:name>")
def admin_summary(name):

  plot = subjectwise_top_score()
  plot.savefig("./static/style/images/subjectwise_top_score.jpeg", dpi=300, bbox_inches='tight')
  plot.clf()

  pie_plot = subjectwise_user_attempts()
  pie_plot.savefig("./static/style/images/subjectwise_user_attempts.jpeg", dpi=300, bbox_inches='tight')
  pie_plot.clf()

  return render_template("admin_summary.html", name=name)
#bar chart
def subjectwise_top_score():
  scores = db.session.query(Scores).all()
  print(scores)
  top_scores_dict = {}
  for score in scores:
    score.subject = score.quiz.chapter.subject
    if score.subject.name in top_scores_dict.keys():
      if top_scores_dict[score.subject.name] < score.total_scored:
        top_scores_dict[score.subject.name] = score.total_scored
    else:
      top_scores_dict[score.subject.name] = score.total_scored

  x_names=list(top_scores_dict.keys())
  y_top_scores=list(top_scores_dict.values())
  plt.figure(figsize=(20, 10))
  plt.bar(x_names,y_top_scores,color="blue", width=0.4)
  plt.title("Subjects/Top Scores", fontsize=40)
  plt.xlabel("Subjects", fontsize=35)
  plt.ylabel("Top Scores", fontsize=35)
  plt.xticks(fontsize=35, rotation=10)
  plt.yticks(fontsize=35)
  return plt

#pie chart  
def subjectwise_user_attempts():
  scores = db.session.query(Scores).all()
  user_attemps_dict = {}
  for score in scores:
    score.subject = score.quiz.chapter.subject
    if score.subject.name in user_attemps_dict.keys():
      user_attemps_dict[score.subject.name] += 1
    else:
      user_attemps_dict[score.subject.name] = 1

  labels = list(user_attemps_dict.keys())
  sizes = list(user_attemps_dict.values())

  plt.figure(figsize=(8,8))
  plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['red', 'green', 'blue', 'orange', 'yellow'])
  plt.title('Subjectwise user attempts', fontsize=16)
  return plt

  

    






######################################## User Controllers ##################################################################


@app.route('/user_dashboard/<name>', methods=["GET","POST"])
def user_dashboard(name):
  if request.method=="GET":
    quizzes = db.session.query(Quiz).order_by((Quiz.date_of_quiz)).all()
    for quiz in  quizzes:
      questions = db.session.query(Question).filter(Question.quiz_id == quiz.q_id).all()
      quiz.questions = questions
    return render_template("user_dashboard.html", name=name, quizzes=quizzes)
  
@app.route('/explore_subject/<string:name>')
def subject_for_quizzes(name):
  subjects= db.session.query(Subject).all()
  return render_template('subjectwise_quizzes.html', subjects=subjects, name=name)

@app.route('/explore_subject/<int:subject_id>/<string:name>')
def chapter_for_quizzes(subject_id, name):
  
  chapters= db.session.query(Chapter).filter(Chapter.subject_id == subject_id).all()
  return render_template('chapter_quizzes.html', chapters=chapters, name=name)

@app.route('/explore_subject/<int:subject_id>/<int:chapter_id>/<string:name>')
def quiz_for_quizzes( subject_id, chapter_id, name):
  quizzes= db.session.query(Quiz).filter(Quiz.chapter_id == chapter_id).all()
  chapter = db.session.query(Chapter).filter(Chapter.ch_id == chapter_id).first()
  return render_template('user_quizzes.html', chapter=chapter, quizzes=quizzes, name=name)

@app.route('/attempt_quiz/<int:quiz_id>/<string:name>', methods=['GET','POST'])
def mainquiz(quiz_id, name):
  if request.method == 'GET':
    quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
    questions = db.session.query(Question).filter(Question.quiz_id == quiz_id).all()
    return render_template('user_mainquiz.html', quiz=quiz, questions=questions, name=name)
  elif request.method == 'POST':
    questions = db.session.query(Question).filter(Question.quiz_id == quiz_id).all()
    score=0
    for question in questions:
      selected_option = request.form.get(f"{question.ques_id}")
      print(selected_option)
      correct_option = question.correct_option
      if(int(selected_option)==correct_option):
        score += 1
    print(f'score: {score}') #to be removed
    user = db.session.query(User).filter(User.email == name).first()
    new_score = Scores(quiz_id=int(quiz_id), user_id=user.user_id, timestamp_of_attempt=datetime.now(), total_scored=score)
    db.session.add(new_score)
    db.session.commit()
    return redirect('/score/' + name)
  
@app.route('/score/<string:name>', methods=['GET','POST']) 
def quiz_score(name):
  if request.method=="GET":
    user = db.session.query(User).filter(User.email == name).first()
    scores = db.session.query(Scores).filter(Scores.user_id == user.user_id).order_by(Scores.timestamp_of_attempt).all()
    return render_template("quiz_score.html", scores=scores, name=name)

#customer details 
@app.route('/admin_user/<string:name>', methods=['GET', 'POST'])
def admin_user(name):
  if request.method=="GET":
     users=db.session.query(User).all()
     return render_template("admin_user.html", users=users, name=name)
  

#user_summary
@app.route("/user_summary/<string:name>")
def user_summary(name):

  plot = subjectwise_quiz_attempts(name)
  plot.savefig("./static/style/images/subjectwise_quiz_attempts.jpeg", dpi=300, bbox_inches='tight')
  plot.clf()

  pie_plot = subjectwise_average(name)
  pie_plot.savefig("./static/style/images/subjectwise_average.jpeg", dpi=300, bbox_inches='tight')
  pie_plot.clf()




  return render_template("user_summary.html", name=name)

#bar chart
def subjectwise_quiz_attempts(name):
  user = User.query.filter_by(email=name).first()
  if not user :
    return plt
  attempts = db.session.query(Scores).filter(Scores.user_id == user.user_id).all()
  sub_attempts = {}
  for attempt in attempts:
    subject = attempt.quiz.chapter.subject
    if subject.name in sub_attempts.keys():
      sub_attempts[subject.name] += 1
    else:
      sub_attempts[subject.name] = 1

  x_names = list(sub_attempts.keys())
  y_counts = list(sub_attempts.values())

  plt.figure(figsize=(20, 10))
  plt.bar(x_names, y_counts, color='blue', width=0.4)
  plt.title("Subjectwise number of quizzes attempts", fontsize=40)
  plt.xlabel("Subjects", fontsize=35)
  plt.ylabel("No. of Quizzes Attempted", fontsize=35)
  plt.xticks(fontsize=35, rotation=10)
  plt.yticks(fontsize=35)
  return plt

#pie chart
def subjectwise_average(name):
  user = User.query.filter_by(email=name).first()
  if not user :
    return plt
  attempts = db.session.query(Scores).filter(Scores.user_id == user.user_id).all()
  sub_scores = {}
  sub_attempts = {}

  for attempt in attempts:
    subject = attempt.quiz.chapter.subject.name
    if subject not in sub_scores:
      sub_scores[subject] = 0
      sub_attempts[subject] = 0
    sub_scores[subject] += attempt.total_scored
    sub_attempts[subject] +=1
  average_scores = {}
  for sub in sub_scores:
    average_scores[sub] = sub_scores[subject]/sub_attempts[sub]

  labels = list(average_scores.keys())
  sizes = list(average_scores.values())

  plt.figure(figsize=(8,8))
  plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['red', 'green', 'yellow', 'orange', 'violet'])
  plt.title('Subjectwise Average Scores', fontsize=16)
  return plt

    


  
################################################ Search ###############################################################################

#admin_search
@app.route("/search/<name>", methods=['GET','POST'])
def admin_search(name):
  if request.method=="POST":
    search = request.form.get("search")
    by_subject = search_by_subject(search)
    by_name = search_by_name(search)
    by_quiz = search_by_quiz(search)
    if by_subject:
      return render_template("admin_dashboard.html", name=name, subjects=by_subject)
    elif by_name:
      return render_template("admin_user.html", name=name, users=by_name)
    elif by_quiz:
      return render_template("quiz_search.html", name=name, quizzes=by_quiz)
  return redirect('/admin_dashboard/'+"/"+str(name))

#supported functions
def search_by_subject(search):
  subjects = Subject.query.filter(Subject.name.ilike(f"%{search}%")).all()
  return subjects

def search_by_name(search):
  users = User.query.filter(User.email.ilike(f"%{search}%")).all()
  return users


def search_by_quiz(search):
  quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{search}%")).all()
  return quizzes

#user_search
@app.route("/user_search/<name>", methods=['GET','POST'])
def user_search(name):
  if request.method=="POST":
    search = request.form.get("search")
    by_subject = user_search_by_subject(search)
    by_chapter = user_search_by_chapter(search)
    by_quiz = user_search_by_quiz(search)
    if by_subject:
      return render_template("user_dashboard.html", name=name, quizzes=by_subject)
    elif by_chapter:
      return render_template("user_dashboard.html", name=name, quizzes=by_chapter)
    elif by_quiz:
      return render_template("user_dashboard.html", name=name, quizzes=by_quiz)
  return redirect('/user_dashboard/'+"/"+str(name))

##Supporting function for user dashboard
def user_search_by_subject(search):
  subjects = db.session.query(Subject.sub_id).filter(Subject.name.ilike(f"%{search}%"))
  chapters = db.session.query(Chapter.ch_id).filter(Chapter.subject_id.in_(subjects))
  quizzes = Quiz.query.filter(Quiz.chapter_id.in_(chapters)).all()
  return quizzes

def user_search_by_chapter(search):
  chapters = db.session.query(Chapter.ch_id).filter(Chapter.name.ilike(f"%{search}%"))
  quizzes = Quiz.query.filter(Quiz.chapter_id.in_(chapters)).all()
  return quizzes

def user_search_by_quiz(search):
  quizzes = Quiz.query.filter(Quiz.name.ilike(f"%{search}%")).all()
  return quizzes