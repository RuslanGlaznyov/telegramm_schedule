from flask import Flask
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_babelex import Babel

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)
admin = Admin(app, name='admin', template_mode='bootstrap3')
babel = Babel(app)


from app import  route, admin, bot