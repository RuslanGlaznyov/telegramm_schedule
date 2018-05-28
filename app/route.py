from app import app, admin, db, babel
from app.models import Group, Faculty, Specialty, Course, User
from flask_admin.contrib.sqla import ModelView
from app.admin_page import GroupView, FacultyView,SpecialtyView,CourseView, UserView

from flask import request
import telebot
from telebot import types
import time


from app.const import WEBHOOK_PATH, TOKEN 

bot = telebot.TeleBot(TOKEN, threaded=False)

@app.route('/{}'.format(TOKEN), methods=["POST"])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@app.route('/')
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_PATH)
    return "CONNECTED", 200


#admin view
admin.add_view(FacultyView(Faculty, db.session, 'Факультет'))
admin.add_view(SpecialtyView(Specialty, db.session, 'Специальность'))
admin.add_view(CourseView(Course, db.session, 'Курс'))
admin.add_view(GroupView(Group, db.session,'Группа'))
admin.add_view(UserView(User, db.session, 'Пользоватили'))

@babel.localeselector
def get_locale():
        # Put your logic here. Application can store locale in
        # user profile, cookie, session, etc.
        return 'ru'