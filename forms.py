from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, TextAreaField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Email, Optional
from wtforms import FloatField, IntegerField,  SelectField, DateField, DecimalField
from wtforms_sqlalchemy.fields import QuerySelectField
from models import Project, Activity



class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])




# Assuming you have a function to get all projects for the QuerySelectField
def project_choices():
    return Project.query.all()

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    donor = StringField('Donor', validators=[DataRequired(), Length(max=100)])
    thematic_area = StringField('Thematic Area', validators=[DataRequired(), Length(max=100)])
    start_date = DateField('Start Date', validators=[DataRequired()], format='%Y-%m-%d')
    end_date = DateField('End Date', validators=[Optional()], format='%Y-%m-%d')  # Optional if the project can be ongoing
    project_amount = FloatField('Project Amount', validators=[DataRequired()])

# class ActivityForm(FlaskForm):
#     project_id = QuerySelectField('Project', query_factory=project_choices, allow_blank=False, get_label='name', validators=[DataRequired()])
#     name = StringField('Activity Name', validators=[DataRequired(), Length(max=200)])
#     target_beneficiaries = StringField('Target Beneficiaries', validators=[DataRequired(), Length(max=200)])
#     target_beneficiaries_male = IntegerField('Target Male Beneficiaries', validators=[DataRequired()])
#     target_beneficiaries_female = IntegerField('Target Female Beneficiaries', validators=[DataRequired()])
#     budget_amount = FloatField('Budget Amount', validators=[DataRequired()])
#     approved_budget_amount = FloatField('Approved Budget Amount', validators=[DataRequired()])

class ActivityForm(FlaskForm):
    project_id = SelectField('Project ID', coerce=int, validators=[DataRequired()])
    # The project name is auto-filled and not a direct form submission, so it's handled client-side
    name = StringField('Name of Activity', validators=[DataRequired()])
    budget_amount = DecimalField('Activity Budget', places=2, validators=[DataRequired()])
    approved_budget_amount = DecimalField('Approved Budget Amount', places=2, validators=[DataRequired()])
    target_beneficiaries = StringField('Target Beneficiaries', validators=[DataRequired()])
    target_beneficiaries_male = IntegerField('Target Beneficiaries Male', validators=[DataRequired()])
    target_beneficiaries_female = IntegerField('Target Beneficiaries Female', validators=[DataRequired()])
    # category = SelectField('Category', coerce=int)
    submit = SubmitField('Add Activity')
    

class ReportForm(FlaskForm):
    activity_id = QuerySelectField('Activity', query_factory=lambda: Activity.query.all(), allow_blank=False, get_label='name', validators=[DataRequired()])
    report_title = StringField('Title of Report', validators=[DataRequired()])
    date_from = DateField('Date From', validators=[DataRequired()], format='%Y-%m-%d')
    date_to = DateField('Date To', validators=[DataRequired()], format='%Y-%m-%d')
    number_reached_male = IntegerField('Number Reached Male', validators=[DataRequired()])
    number_reached_female = IntegerField('Number Reached Female', validators=[DataRequired()])
    written_report = TextAreaField('Written Report', validators=[DataRequired(), Length(max=200)])
    photos = TextAreaField('Photos', validators=[Optional(), Length(max=200)])  # Assuming this might be a URL or path


class FinancialReportForm(FlaskForm):
    project_id = QuerySelectField('Project', query_factory=project_choices, allow_blank=False, get_label='name', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    total_expenditure = FloatField('Total Expenditure', validators=[DataRequired()])
    submit = SubmitField('Add Financial Report')
