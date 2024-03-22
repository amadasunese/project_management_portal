from flask import Flask
from models import db
from views import main
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.register_blueprint(main)
db.init_app(app)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = "secret_key"
db = SQLAlchemy(app)
migrate = Migrate(app, db)