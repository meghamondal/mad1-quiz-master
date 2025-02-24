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
    
@app.route('/admin_dashboard', methods=["GET","POST"])
def admin_dashboard():
  if request.method=="GET":
    return render_template("admin_dashboard.html")
  
  @app.route("/register",method=['GET','POST'])
  def register():
    if request.method=='GET':
      return render_template('register.html')
    

    