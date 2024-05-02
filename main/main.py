# импорт моих доп. файлов
import cfg
import func
# импорт нужных библиотек
import time
import telebot
from telebot import types

bot = telebot.TeleBot(cfg.token)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    shop = types.InlineKeyboardButton('Магазин.', callback_data='shop')
    faq = types.InlineKeyboardButton('FAQ.', callback_data='faq')
    about = types.InlineKeyboardButton('О нас.', callback_data='about')

    markup.add(shop, faq, about)

    if last_message_id:
        bot.edit_message_text(chat_id=message.chat.id, message_id=last_message_id, text=f'Привет! {message.from_user.first_name}, Что вас интересует?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}, Что вас интересует?', reply_markup=markup)

last_message_id = None
@bot.callback_query_handler(func=lambda call: True)
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_callback(call):
    global last_message_id

    if call.data == 'shop':
        shop(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'faq':
        FAQ(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'about':
        about(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'fortnite':
        fortnite_shop(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'vbucks':
        vbucks_shop(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'bundle':
        fortnite_bundle_shop(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'valorant':
        bot.send_message(call.message.chat.id, 'Вы выбрали VALORANT.')
        bot.send_message(call.message.chat.id, 'Что дальше?', reply_markup=None)

    elif call.data == 'back':
        if last_message_id:
            back_markup = types.InlineKeyboardMarkup(row_width=2)
            back_markup.add(types.InlineKeyboardButton('Магазин.', callback_data='shop'),
                            types.InlineKeyboardButton('FAQ.', callback_data='faq'),
                            types.InlineKeyboardButton('О нас.', callback_data='about'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=last_message_id, text=f'Привет! {call.from_user.first_name}, Что вас интересует?')
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=last_message_id, reply_markup=back_markup)
            return  # Выходим из функции после редактирования разметки

    else:
        msg = bot.send_message(call.message.chat.id, 'Пожалуйста, выберите один из вариантов в меню.')
        time.sleep(3)  # Ждем 3 секунды
        try:
            bot.delete_message(call.message.chat.id, msg.message_id)
        except Exception as e:
            print(f"Error while deleting message: {e}")


def shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Добавляем кнопки
    markup.add(types.InlineKeyboardButton('Fortnite', callback_data='fortnite'),
               types.InlineKeyboardButton('VALORANT', callback_data='valorant'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите игру:', reply_markup=markup)

def FAQ(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Добавляем кнопку
    markup.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='FAQ', reply_markup=markup)

def about(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Добавляем кнопку
    markup.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='about', reply_markup=markup)

# shop of games
def fortnite_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Добавляем кнопки
    markup.add(types.InlineKeyboardButton('Вбаксы', callback_data='vbucks'),
               types.InlineKeyboardButton('Наборы', callback_data='bundle'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите вид товара:', reply_markup=markup)

def vbucks_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Добавляем кнопки
    markup.add(types.InlineKeyboardButton('1000VB', callback_data='1000VB'),
               types.InlineKeyboardButton('2000VB', callback_data='2000VB'),
               types.InlineKeyboardButton('5000VB', callback_data='5000VB'),
               types.InlineKeyboardButton('13500VB', callback_data='13500VB'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите товар:', reply_markup=markup)

def fortnite_bundle_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    # Добавляем кнопки
    markup.add(types.InlineKeyboardButton('Гремучие грёзы', callback_data='rattling dreams'),
               types.InlineKeyboardButton('Аватар', callback_data='avatar'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите товар:', reply_markup=markup)

bot.polling(non_stop=True)
