from app import app

from flask import request
import telebot
from telebot import types
import time

from app.const import WEBHOOK_PATH, TOKEN 

bot = telebot.TeleBot(TOKEN, threaded=False)

bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url=WEBHOOK_PATH)

@app.route('/{}'.format(TOKEN), methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "ok", 200


@bot.message_handler(content_types=['text'])
def startCommand(msg):
    # keyboard = types.InlineKeyboardMarkup()
    # for i in range(10):
    #     callback_button = types.InlineKeyboardButton(text="test"+str(i), callback_data="test"+str(i))
    #     keyboard.add(callback_button)
    

    
    bot.send_message(msg.chat.id, "msg successful")

    # keyboard =types.InlineKeyboardMarkup()
    # keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['test1', 'test2','test3', 'test4']])
    # bot.send_message(msg.chat.id,"test?",reply_markup=keyboard)
    # bot.send_message(message.chat.id, 'Hi *' + message.chat.first_name + '*!' , parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
# @bot.callback_query_handler(func=lambda c: True)
# def inline(c):
#     if c.data == 'test5':
#         bot.send_message(c.message.chat.id,'OK')

