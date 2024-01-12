from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String,nullable = False)
    description = db.Column(db.String,nullable=False)
    completed = db.Column(db.Boolean,nullable=False,default=False)
    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    due_date = db.Column(db.DateTime)