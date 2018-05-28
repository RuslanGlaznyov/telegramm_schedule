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
    bot.send_message(msg.chat.id, " ", reply_markup=button)

			

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
    time_list = [
        '8:30-9:15<b>|</b>9:20-10:05',
        '10:15-11:00<b>|</b>10:05-11:50',
        '12:10-12:55<b>|</b>13:00-13:45',
        '13:55-14:40<b>|</b>14:45-15:30',
        '15:50-16:35<b>|</b>16:40-17:25',
        '17:35-18:20<b>|</b>18:25-19:10'
    ]
    if User.query.filter_by(telegram_id = msg.chat.id).count() != 0:
        user = User.query.filter_by(telegram_id = msg.chat.id).first()
        group = Group.query.filter_by(id = user.group_id).first()
        days = get_schedule(str(group.group_p), day)
        schedule_string = " "
        for key in days:
            if days[key] == 'нет пары':
                schedule_string += str(key)+" <b>нет пары</b> \n" +time_list[int(key)-1]+ "\n-------------------------\n"
            else:
                time = time_list[int(key)-1]
                para = str(key)
                subject = days[key]['subject']
                room = str(days[key]['room'])
                teacher = str(days[key]['teacher'])
                schedule_string += "пара: {} \n{} \n {} \n {} \n {} \n -------------------------\n"\
                .format(para,time, subject, room, teacher)
        
        return schedule_string


    else:
        key = main_menu()
        bot.send_message(msg.chat.id, "вы не подписаны на группу")
        bot.send_message(msg.chat.id, "Выберите факультет", reply_markup=key)
        return 
    
@bot.message_handler(func=lambda mess: "пн" == mess.text, content_types=['text'])
def mo(msg):
    schedule_string =  print_schedule(msg, 'mo')
    bot.send_message(msg.chat.id, schedule_string, parse_mode="HTML")

@bot.message_handler(func=lambda mess: "вт" == mess.text, content_types=['text'])
def tu(msg):
    schedule_string =  print_schedule(msg, 'tu')
    bot.send_message(msg.chat.id, schedule_string, parse_mode="HTML")

@bot.message_handler(func=lambda mess: "ср" == mess.text, content_types=['text'])
def we(msg):
    schedule_string =  print_schedule(msg, 'we')
    bot.send_message(msg.chat.id, schedule_string, parse_mode="HTML")

@bot.message_handler(func=lambda mess: "чт" == mess.text, content_types=['text'])
def th(msg):
    schedule_string =  print_schedule(msg, 'th')
    bot.send_message(msg.chat.id, schedule_string, parse_mode="HTML")

@bot.message_handler(func=lambda mess: "пт" == mess.text, content_types=['text'])
def fr(msg):
    schedule_string =  print_schedule(msg, 'fr')
    bot.send_message(msg.chat.id, schedule_string, parse_mode="HTML")

