# from flask import Flask
from datetime import datetime
# from jinja2 import Undefined
from views import main
from models import db, User
# from flask_sqlalchemy import SQLAlchemy
from config import app
from flask_login import LoginManager
from flask.cli import FlaskGroup
import getpass
import locale
from templates.reports import generate_report
from flask_migrate import Migrate
# from flask import Manager
# from flask_migrate import Migrate, MigrateCommand


def format_currency(value):
    if value is None or isinstance(value, str) and not value.isdigit():
        return 'N/A'
    try:
        return "${:,.2f}".format(float(value))
    except (ValueError, TypeError):
        return 'N/A'
    
app.jinja_env.filters['format_currency'] = format_currency

# Define a custom filter for date formatting
def date_format(value, format='%Y-%m-%d'):
    return value.strftime(format) if value else ''

app.jinja_env.filters['date_format'] = date_format


@app.template_filter('number_format')
def number_format(value, format_string=',.2f'):
    return format(value, format_string)

# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, '')

@app.template_filter('date_format')
def date_format(value, format='%Y-%m-%d'):
    """Format a datetime to a string."""
    if value is None:
        return ""
    return value.strftime(format)


# Import database models with app context
# with app.app_context():
#   from models import *

migrate = Migrate(app, db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.static_folder = 'static'


cli = FlaskGroup(app)


@cli.command("create_admin")
def create_admin():
    """Creates the admin user."""
    email = input("Enter email address: ")
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Enter password again: ")
    if password != confirm_password:
        print("Passwords don't match")
        return 1
    try:
        user = User(email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        print(f"Admin with email {email} created successfully!")
    except Exception:
        print("Couldn't create admin user.")



if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        from models import *

    app.run(debug=True)

