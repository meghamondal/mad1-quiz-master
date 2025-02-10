from flask import current_app as app
from backend.models import Authentication, db

with app.app_context():
  db.create_all()

  if not Authentication.query.filter_by(role='admin').first():
    admin = Authentication(email = 'admin@quizmaster.com', password = 'test', role = 'admin')
    db.session.add(admin)
    db.session.commit()
    
  

  