from flask_admin.contrib.sqla import ModelView

class FacultyView(ModelView):
     column_labels = dict(name='Название факультета', spec='Специальность')    

class SpecialtyView(ModelView):
    column_labels = dict(name='Название спецальности', course='курс', faculty="Факультет")    

class CourseView(ModelView):
    column_labels = dict(number_of_course='Номер курса', group='группа', spec="Спицальность")    

class GroupView(ModelView):
    column_labels = dict(number_of_group='Номер группы', group_p='Параметр группы', cource="Курс")

class UserView(ModelView):
    column_labels = dict(
        telegram_id='Телеграмм id', 
        first_name='Имя', 
        last_name="Фамилия",
        username="username",
        group='группа')
