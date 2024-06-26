from flask import flash
from app import app
from models import User, db
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt


def add_admin(email, password):
    with app.app_context():
        if isinstance(password, bytes):
            password = password.decode('utf-8')

        hashed_password = generate_password_hash(password) # .decode('utf-8')

        admin_user = User(name=name, phone_number=phone_number, email=email, password=hashed_password, is_admin=True)
        db.session.add(admin_user)
        db.session.commit()


if __name__ == "__main__":
    name = input("Enter admin name")
    phone_number = input("Enter admin phone number")
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    add_admin(email, password)
