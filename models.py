from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
# from app import db
from flask_migrate import Migrate

db = SQLAlchemy()
# db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    """
    User model for the database
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    donor = db.Column(db.String(100))
    thematic_area = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    project_amount = db.Column(db.Float)
    activities = db.relationship('Activity', backref='project', lazy=True)
    financial_reports = db.relationship('FinancialReport', backref='project', lazy=True)

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    name = db.Column(db.String(200))
    target_beneficiaries = db.Column(db.String(200))
    target_beneficiaries_male = db.Column(db.Integer)
    target_beneficiaries_female = db.Column(db.Integer)
    budget_amount = db.Column(db.Float)
    approved_budget_amount = db.Column(db.Float)
    reports = db.relationship('Report', backref='activity', lazy=True)

class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    report_title = db.Column(db.String(200))
    date_from = db.Column(db.DateTime)
    date_to = db.Column(db.DateTime)
    number_reached_male = db.Column(db.Integer)
    number_reached_female = db.Column(db.Integer)
    written_report = db.Column(db.String(200))
    photos = db.Column(db.String(200))

class FinancialReport(db.Model):
    __tablename__ = 'financialreport'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    budget = db.Column(db.Float)
    total_expenditure = db.Column(db.Float)
