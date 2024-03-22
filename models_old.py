from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Project Table
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    donor = db.Column(db.String(100))
    thematic_area = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    project_amount = db.Column(db.Float)

    # Relationship with Activities
    activities = db.relationship('Activity', backref='project', lazy=True)

# Activities Table
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    target_beneficiaries = db.Column(db.String(200))
    target_beneficiaries_male = db.Column(db.Integer)
    target_beneficiaries_female = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    budget_amount = db.Column(db.Float)
    approved_budget_amount = db.Column(db.Float)

    # Relationship with Reports
    reports = db.relationship('Report', backref='activity', lazy=True)

# Report Table
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    donor = db.Column(db.String(100))
    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)
    number_reached_male = db.Column(db.Integer)
    number_reached_female = db.Column(db.Integer)
    written_report = db.Column(db.String(200))  # Path to the file
    photos = db.Column(db.String(200))  # Path to the file

# Financial Report Table
class FinancialReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    budget = db.Column(db.Float)
    expenditure = db.Column(db.Float)