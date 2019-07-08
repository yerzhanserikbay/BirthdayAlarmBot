import telebot
from datetime import datetime
import data_manager as dm
import os

bot = telebot.TeleBot(os.environ['TOKEN'])
date_text = 'Could you send me your birthday *ONLY* in _year-month-day_ format \nEx: 1996-08-13'


@bot.message_handler(commands=['start'])
def handle_start(message):

    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Welcome to the BirthdayAlarmBot \U0001F973'
                                      '\n• Add a birthday /add \U0001F389'
                                      '\n• Send me an excel file with birthdays /send \U0001F381'
                                      '\n• Send me a message with list of the birthdays/list \U0001F605'
                                      '\n• Force me to sleep /stop \U0001F644')


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Bye Bye \U0001F634')


@bot.message_handler(commands=['add'])
def handle_add(message):
    markup = telebot.types.ForceReply(selective=True)

    bot.send_chat_action(message.chat.id, 'typing')

    bot.send_message(message.chat.id,
                     date_text,
                     parse_mode='Markdown',
                     reply_markup=markup)


@bot.message_handler(commands=['send'])
def handle_send(message):
    doc = dm.get_file(message.chat.id)

    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Trying \U0001F975')
    bot.send_document(message.chat.id, doc)
    bot.send_message(message.chat.id, 'Done \U0001F60A')


@bot.message_handler(commands=['list'])
def handle_list(message):
    msg = dm.get_elements(str(message.chat.id))
    bot.send_chat_action(message.chat.id, 'typing')
    bot.send_message(message.chat.id, 'Trying \U0001F975')
    bot.send_message(message.chat.id, msg)
    bot.send_message(message.chat.id, 'Done \U0001F60A')


@bot.message_handler(content_types=['text'])
def handle_birthday(message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id
    group_id = message.chat.id

    global reply_message
    try:
        reply_message = message.reply_to_message.text

    except AttributeError:
        exit()

    pure_date_text = date_text.replace('*', '').replace('_', '')

    if reply_message == pure_date_text:
        try:
            datetime.strptime(message.text, '%Y-%m-%d')

            bot.send_chat_action(message.chat.id, 'typing')

            bot.send_message(message.chat.id, 'Saved \U0001F38A \nThank you \U0001F60A')

            bot.send_message(message.chat.id, 'First Name: %s'
                                              '\nLast Name: %s'
                                              '\nUsername: %s'
                                              '\nBirthday: %s' % (first_name, last_name, username, message.text))

            data = [first_name, last_name, username, message.text, user_id, group_id]

            dm.insert_element(data)

        except ValueError:
            markup = telebot.types.ForceReply(selective=True)

            bot.send_chat_action(message.chat.id, 'typing')

            bot.send_message(message.chat.id,
                             date_text,
                             parse_mode='Markdown',
                             reply_markup=markup)


bot.polling(none_stop=True, interval=0)
