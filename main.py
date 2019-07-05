import telebot
import os
from datetime import datetime


bot = telebot.TeleBot('789281149:AAEsBcRQLYX5-WMGoUEE9SOZpy0UAHZZtGg')
date_text = 'Could you send me your birthday *ONLY* in _month/day/year_ format \nEx: 08/08/08'


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, 'Welcome to the BirthdayAlarmBot \U0001F973'
                                           '\n• Add a birthday /add \U0001F389'
                                           '\n• Send me an excel file with birthdays /send \U0001F381'
                                           '\n• Force me to sleep /stop \U0001F644')


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    bot.send_message(message.from_user.id, 'Bye Bye \U0001F634')


@bot.message_handler(commands=['add'])
def handle_add(message):
    markup = telebot.types.ForceReply(selective=True)

    bot.send_chat_action(message.from_user.id, 'typing')

    bot.send_message(message.from_user.id,
                     date_text,
                     parse_mode='Markdown',
                     reply_markup=markup)


@bot.message_handler(commands=['send'])
def handle_send(message):
    cwd = os.getcwd()

    doc = open('{}/Birthdays.xlsx'.format(cwd), 'rb')

    bot.send_chat_action(message.from_user.id, 'typing')

    bot.send_document(message.from_user.id, doc)


@bot.message_handler(content_types=['text'])
def handle_birthday(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    global reply_message
    try:
        reply_message = message.reply_to_message.text

    except AttributeError:
        exit()

    pure_date_text = date_text.replace('*', '').replace('_', '')

    if reply_message == pure_date_text:
        try:
            datetime.strptime(message.text, '%m/%d/%y')

            bot.send_chat_action(message.from_user.id, 'typing')

            bot.send_message(message.from_user.id, 'Saved \U0001F38A \nThank you \U0001F60A')

            bot.send_message(message.from_user.id, 'First Name: %s'
                                                   '\nLast Name: %s'
                                                   '\nUsername: %s'
                                                   '\nBirthday: %s' % (first_name, last_name, username, message.text))

        except ValueError:
            markup = telebot.types.ForceReply(selective=True)

            bot.send_chat_action(message.from_user.id, 'typing')

            bot.send_message(message.from_user.id,
                             date_text,
                             parse_mode='Markdown',
                             reply_markup=markup)


bot.polling(none_stop=True, interval=0)
