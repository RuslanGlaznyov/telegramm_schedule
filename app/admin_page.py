from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView, AdminIndexView
from flask_login import  current_user
from flask import redirect, url_for,request



class IndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin.html')

class FacultyView(ModelView):
    column_labels = dict(name='Название факультета', spec='Специальность')    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class SpecialtyView(ModelView):
    column_labels = dict(name='Название спецальности', course='курс', faculty="Факультет")    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class CourseView(ModelView):
    column_labels = dict(number_of_course='Номер курса', group='группа', spec="Спицальность")    
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class GroupView(ModelView):
    column_labels = dict(number_of_group='Номер группы', group_p='Параметр группы', cource="Курс")
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class UserView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

    column_labels = dict(
        telegram_id='Телеграмм id', 
        first_name='Имя', 
        last_name="Фамилия",
        username="username",
        group='группа')
