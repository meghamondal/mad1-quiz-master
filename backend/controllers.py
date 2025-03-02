from flask import Flask, render_template, request
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
      return render_template("admin_dashboard.html")
    elif authen and authen.role=="user":
      return render_template("user_dashboard.html")
    else:
      return render_template("login.html", msg="Invalid credentials...")
    
'''@app.route('/admin_dashboard', methods=["GET","POST"])
def admin_dashboard():
  if request.method=="GET":
    return render_template("admin_dashboard.html")'''
  
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

'''@app.route("/admin_dashboard", methods=['GET','POST'])  
def admin_dashboard():'''
