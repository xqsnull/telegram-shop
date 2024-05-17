from cfg import all_items
from cfg import token
import time
import telebot
from telebot import types

bot = telebot.TeleBot(token)

# Словарь для корзины пользователя
user_basket = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    shop = types.InlineKeyboardButton('Магазин.', callback_data='shop')
    faq = types.InlineKeyboardButton('FAQ.', callback_data='faq')
    about = types.InlineKeyboardButton('О нас.', callback_data='about')
    basket = types.InlineKeyboardButton('Корзина', callback_data='basket')

    markup.add(shop, faq, about, basket)

    global last_message_id
    if last_message_id:
        bot.edit_message_text(chat_id=message.chat.id, message_id=last_message_id, text=f'Привет! {message.from_user.first_name}, Что вас интересует?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Привет! {message.from_user.first_name}, Что вас интересует?', reply_markup=markup)

last_message_id = None
<<<<<<< HEAD

# Функция для обработки нажатий кнопок
=======
>>>>>>> 4b921d761b5e2d60ae7a3f55d3d215c8434cb1b8
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

    elif call.data == 'basket':
        show_basket(call.message)
        last_message_id = call.message.message_id

    elif call.data in all_items:
        add_to_cart(call)
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

    elif call.data == 'pay_callback':
        pay(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'back':
        if last_message_id:
            back_markup = types.InlineKeyboardMarkup(row_width=2)
            back_markup.add(types.InlineKeyboardButton('Магазин.', callback_data='shop'),
                            types.InlineKeyboardButton('FAQ.', callback_data='faq'),
                            types.InlineKeyboardButton('О нас.', callback_data='about'),
                            types.InlineKeyboardButton('Корзина', callback_data='basket'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=last_message_id, text=f'Привет! {call.from_user.first_name}, Что вас интересует?')
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=last_message_id, reply_markup=back_markup)
            return

    else:
        msg = bot.send_message(call.message.chat.id, 'Пожалуйста, выберите один из вариантов в меню.')
        time.sleep(3)
        try:
            bot.delete_message(call.message.chat.id, msg.message_id)
        except Exception as e:
            print(f"Error while deleting message: {e}")

def add_to_cart(call):
    user_basket[call.data] = all_items.get(call.data)

def calculate_total():
    total = sum(all_items[item] for item in user_basket)
    return total

def show_basket(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    # pay = types.InlineKeyboardButton('Оплатить', callback_data='pay_callback')
    # back = types.InlineKeyboardButton('Назад', callback_data='back')

    # markup.add(pay, back)

    if not user_basket:
        back = types.InlineKeyboardButton('Назад', callback_data='back')
        markup.add(back)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Ваша корзина пуста.', reply_markup=markup)

    else:
        pay = types.InlineKeyboardButton('Оплатить', callback_data='pay_callback')
        back = types.InlineKeyboardButton('Назад', callback_data='back')
        markup.add(pay, back)

        basket_text = "Ваша корзина:\n"
        total_price = 0
        for item, price in user_basket.items():
            basket_text += f"{item}: {price}\n"
            total_price += price
        basket_text += f"\nИтого: {total_price} рублей"
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=basket_text, reply_markup=markup)

def shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Fortnite', callback_data='fortnite'),
               types.InlineKeyboardButton('VALORANT', callback_data='valorant'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите игру:', reply_markup=markup)

def FAQ(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='FAQ', reply_markup=markup)

def about(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='about', reply_markup=markup)

def fortnite_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Вбаксы', callback_data='vbucks'),
               types.InlineKeyboardButton('Наборы', callback_data='bundle'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите вид товара:', reply_markup=markup)

def vbucks_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('1000VB', callback_data='1000VB'),
               types.InlineKeyboardButton('2000VB', callback_data='2000VB'),
               types.InlineKeyboardButton('5000VB', callback_data='5000VB'),
               types.InlineKeyboardButton('13500VB', callback_data='13500VB'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите товар:', reply_markup=markup)

def fortnite_bundle_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Гремучие грёзы', callback_data='Гремучие грёзы'),
               types.InlineKeyboardButton('Аватар', callback_data='Аватар'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите товар:', reply_markup=markup)

def pay(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('QIWI', callback_data='QIWI'),
               types.InlineKeyboardButton('RU CARDS', callback_data='RU CARDS'),
               types.InlineKeyboardButton('Назад', callback_data='back'))
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Выберите вид оплаты:', reply_markup=markup)

bot.polling(non_stop=True)