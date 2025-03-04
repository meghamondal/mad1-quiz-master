from flask import Flask, render_template, request, redirect, url_for
from .models import *
from flask import current_app as app



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
  return render_template('quizzes_page.html', quizzes = quizzes_in_chapters, chapter=chapter, name=name)

@app.route('/admin_dashboard/<int:subject_id>/<int:chapter_id>/<int:quiz_id>/<string:name>')
def questions_in_quizzes(subject_id, chapter_id, quiz_id, name):
  quiz = db.session.query(Quiz).filter(Quiz.q_id == quiz_id).first()
  questions_in_quizzes=quiz.questions
  return render_template('questions_page.html', quiz=quiz, questions = questions_in_quizzes, name=name)



@app.route('/user_dashboard/<name>', methods=["GET","POST"])
def user_dashboard(name):
  if request.method=="GET":
    return render_template("user_dashboard.html", name=name)
  
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
    


