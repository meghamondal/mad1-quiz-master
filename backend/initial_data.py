from flask import current_app as app
from backend.models import Authentication, User, Subject, Chapter, Quiz, Question, Scores, db
from datetime import datetime

with app.app_context():
  db.create_all()

  if not Authentication.query.filter_by(role='admin').first():
    admin = Authentication(email = 'admin@quizmaster.com', password = 'test', role = 'admin')
    db.session.add(admin)
    db.session.commit()

  if not Authentication.query.filter_by(role='user').first():
    user_auth = Authentication(email = 'rahul@quizmaster.com', password = 'rahul12', role = 'user')
    user_dob = datetime(day=17, month=6, year=2001)
    user_data=User(email= 'rahul@quizmaster.com', f_name = 'Rahul', l_name = 'Kumar', qualification = '12th Standard', dob = user_dob)
    db.session.add(user_auth)
    db.session.add(user_data)
    db.session.commit()

sub=db.session.query(Subject).filter_by(name='Physics').first()
if (not sub):
  sub=Subject(name='Physics', description='Challenge your understanding of the physics subject with our engaging and educational physics quiz!')
  db.session.add(sub)
  db.session.commit()

chap=db.session.query(Chapter).filter_by(name='Electrostatics').first()
if(not chap):
  sub=db.session.query(Subject).filter_by(name='Physics').first()
  chap=Chapter(name='Electrostatics', description='Test your knowledge on electric fields, charges, and forces.', subject_id=sub.sub_id)
  db.session.add(chap)
  db.session.commit()

chap=db.session.query(Chapter).filter_by(name='Electrostatics').first()
test_quiz=db.session.query(Quiz).filter_by(chapter_id=chap.ch_id).first()
if(not test_quiz):
  current_date=datetime.now()
  test_quiz=Quiz(name='Quiz 1', chapter_id=chap.ch_id, date_of_quiz=current_date, time_duration=60, remarks='Quiz.')
  db.session.add(test_quiz)
  db.session.commit()

test_quiz=db.session.query(Quiz).filter_by(chapter_id=chap.ch_id).first()
ques=db.session.query(Question).filter_by(quiz_id=test_quiz.q_id).first()
if(not ques):
  ques=Question(q_title='Q1',quiz_id=test_quiz.q_id, question_statement='What is the work done in moving a charge of Q through a potential difference of V ?',
                option_1='Q + V', option_2='Q - V', option_3='Q / V', option_4='Q x V', correct_option='Q x V'  )
  db.session.add(ques)
  db.session.commit()

  

  