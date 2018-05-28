from app import db
from app.route import bot 
from telebot import types
from app.models import Faculty, Specialty, Course, Group, User
from app.scraping import  get_schedule
@bot.message_handler(commands=['start', 'reset'])
def start(msg):
    key = main_menu()
    bot.send_message(msg.chat.id, "Выберите факультет", reply_markup=key)

def button_menu(msg):
    button = types.ReplyKeyboardMarkup(True)
    button.row('пн','вт','ср','чт','пт')
    button.row('/reset')
    bot.send_message(msg.chat.id, "меню", reply_markup=button)

			

def main_menu():
    facs = Faculty.query.all()
    key = types.InlineKeyboardMarkup()
    for fac in facs: 
        key.add(types.InlineKeyboardButton(text=fac.name, callback_data=str(fac.id)+"|"+fac.entity))
    return key

@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    entity_id = split_entity(c.data)
    if entity_id[1] == 'faculty':
        specs_by_fac = Specialty.query.filter_by(faculty_id=int(entity_id[0]))
        if specs_by_fac.count() == 0:
            key = main_menu()
            empty_category(c, key)
            return 
        key = types.InlineKeyboardMarkup()
        for spec in specs_by_fac:
            key.add(types.InlineKeyboardButton(text=spec.name, callback_data=str(spec.id)+"|"+spec.entity))

        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Выберите специальность",
            parse_mode="markdown",
            reply_markup=key)
    
    if entity_id[1] == 'specialty':
        specs_by_fac = Course.query.filter_by(spec_id=int(entity_id[0]))
        if specs_by_fac.count() == 0:
            key = main_menu()
            empty_category(c, key)
            return 
        key = types.InlineKeyboardMarkup()
        for spec in specs_by_fac:
            key.add(types.InlineKeyboardButton(text=str(spec.number_of_course), callback_data=str(spec.id)+"|"+spec.entity))

        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Выберите курс",
            parse_mode="markdown",
            reply_markup=key)
    
    if entity_id[1] == 'course':
        specs_by_fac = Group.query.filter_by(cource_id=int(entity_id[0]))
        if specs_by_fac.count() == 0:
            key = main_menu()
            empty_category(c, key)
            return 
        key = types.InlineKeyboardMarkup()
        for spec in specs_by_fac:
            key.add(types.InlineKeyboardButton(text=str(spec.number_of_group), callback_data=str(spec.id)+"|"+spec.entity))

        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Выберите группу",
            parse_mode="markdown",
            reply_markup=key)
   
    if entity_id[1] == 'group':
        user = User.query.filter_by(telegram_id = c.message.chat.id).first()
        if user:
            user.group_id = int(entity_id[0])
            db.session.commit()
        else: 
            new_user = User(
                telegram_id=c.message.chat.id,
                first_name=c.message.chat.first_name,
                last_name=c.message.chat.last_name,
                username=c.message.chat.username,
                group_id=int(entity_id[0])
                )
            db.session.add(new_user)
            db.session.commit()
        
        
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="вы подписаны на группу",
            parse_mode="markdown",
            )
        button_menu(c.message)
            
def empty_category(c, key):
    bot.edit_message_text(
    chat_id=c.message.chat.id,
    message_id=c.message.message_id,
    text="пустая котегория \nвыбирите факультет",
    parse_mode="markdown",
    reply_markup=key)


def split_entity(string):
    try:
        string  = string.split('|')
        return string
    except Exception as e:
        return None


def print_schedule(msg, day):
    if User.query.filter_by(telegram_id = msg.chat.id).count() != 0:
        user = User.query.filter_by(telegram_id = msg.chat.id).first()
        group = Group.query.filter_by(id = user.group_id).first()
        days = get_schedule(str(group.group_p), day)
        schedule_string = " "
        for key in days:
            if days[key] == 'нет пары':
                schedule_string += str(key)+" нет пары \n" + "-------------------------\n"
            else:
                para = str(key)
                subject = days[key]['subject']
                room = str(days[key]['room'])
                teacher = str(days[key]['teacher'])
                schedule_string += "пара: {} \n {} \n {} \n {} \n -------------------------\n"\
                .format(para, subject, room, teacher)
        
        return schedule_string


    else:
        key = main_menu()
        bot.send_message(msg.chat.id, "вы не подписаны на группу")
        bot.send_message(msg.chat.id, "Выберите факультет", reply_markup=key)
        return 
    
@bot.message_handler(func=lambda mess: "пн" == mess.text, content_types=['text'])
def mo(msg):
    schedule_string =  print_schedule(msg, 'mo')
    bot.send_message(msg.chat.id, schedule_string)

@bot.message_handler(func=lambda mess: "вт" == mess.text, content_types=['text'])
def tu(msg):
    schedule_string =  print_schedule(msg, 'tu')
    bot.send_message(msg.chat.id, schedule_string)

@bot.message_handler(func=lambda mess: "ср" == mess.text, content_types=['text'])
def we(msg):
    schedule_string =  print_schedule(msg, 'we')
    bot.send_message(msg.chat.id, schedule_string)

@bot.message_handler(func=lambda mess: "чт" == mess.text, content_types=['text'])
def th(msg):
    schedule_string =  print_schedule(msg, 'th')
    bot.send_message(msg.chat.id, schedule_string)

@bot.message_handler(func=lambda mess: "пт" == mess.text, content_types=['text'])
def fr(msg):
    schedule_string =  print_schedule(msg, 'fr')
    bot.send_message(msg.chat.id, schedule_string)



#sample menu 
# @bot.message_handler(commands=['start', 'update'])
# def startCommand(msg):
#     print(msg.text + 'fac_step')
#     facs = Faculty.query.all()
#     keyboard = types.ReplyKeyboardMarkup(True)
#     for fac in facs:
#         keyboard.row(str(fac.id) + "|" + fac.name)
#     # callback_button = types.InlineKeyboardButton(text=fac.name, callback_data=fac.id)
#     # keyboard.add(callback_button)
#     bot.send_message(msg.chat.id, "Выберите факультет", reply_markup=keyboard)
#     if msg.text != '/start' or msg.text != '/update':
#         bot.register_next_step_handler(msg, process_spec_step)

    
# def process_spec_step(msg):
#     # if msg.text=='/start' or msg.text=='/update':
#     #     bot.register_next_step_handler(msg, startCommand)
#     # print(msg.text + 'spec_step')
#     id_fac = split_id(msg.text)
#     if id_fac:
#         specs_by_fac = Specialty.query.filter_by(faculty_id=id_fac)
#         keyboard = types.ReplyKeyboardMarkup(True)
#         for spec in specs_by_fac:
#             keyboard.row(spec.name)
#         bot.send_message(msg.chat.id, "Выберите специальность", reply_markup=keyboard)

# def split_id(string):
#     try:
#         string  = string.split('|')
#         id = string[0]
#         id = int(id)
#         return id
#     except Exception as e:
#         return None 

# @bot.message_handler(content_types=['text'])
# def startCommand(msg):
    # keyboard = types.InlineKeyboardMarkup()
    # for i in range(10):
    #     callback_button = types.InlineKeyboardButton(text="test"+str(i), callback_data="test"+str(i))
    #     keyboard.add(callback_button)
    

    
#     bot.send_message(msg.chat.id, "msg successful")

    # keyboard =types.InlineKeyboardMarkup()
    # keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['test1', 'test2','test3', 'test4']])
    # bot.send_message(msg.chat.id,"test?",reply_markup=keyboard)
    # bot.send_message(message.chat.id, 'Hi *' + message.chat.first_name + '*!' , parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())

# from flask_admin import form, expose
