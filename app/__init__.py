from flask import Flask
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager
from app.admin_page import IndexView

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)
admin = Admin(app, name='Админка', template_mode='bootstrap3', index_view=IndexView())
babel = Babel(app)

from app import  route, admin, bot