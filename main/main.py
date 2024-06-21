'''большинство информации о некоторых вещах можно найти в info'''

import sqlite3
from cfg import Config
import time
import telebot
from telebot import types
from telebot.types import InputMediaPhoto

global callbacks
bot = telebot.TeleBot(Config.token)

class SQLiteDB:
    def __init__(self, db_name='orders.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                username TEXT,
                                items TEXT,
                                total_amount INTEGER,
                                currency TEXT,
                                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )''')
        self.conn.commit()

    def save_order(self, user_id, username, items, total_amount, currency):
        self.cursor.execute('''INSERT INTO orders (user_id, username, items, total_amount, currency)
                            VALUES (?, ?, ?, ?, ?)''',
                            (user_id, username, items, total_amount, currency))
        self.conn.commit()
        order_id = self.cursor.lastrowid
        return order_id

    def get_all_orders(self):
        self.cursor.execute('SELECT * FROM orders')
        orders = self.cursor.fetchall()
        return orders

    def close(self):
        self.conn.close()

db = SQLiteDB()

db.init_db()

# словарь для корзины пользователя (чуть позже переделать добавив в базу данных, так же переделать все что работает с корзиной)
user_basket = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    global last_message_id

    # удаление начального сообщения если новое уже существует
    if last_message_id:
        try:
            bot.delete_message(message.chat.id, last_message_id)
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")

    markup = types.InlineKeyboardMarkup(row_width=2)
    shop = types.InlineKeyboardButton('Магазин.', callback_data='shop')
    faq = types.InlineKeyboardButton('FAQ.', callback_data='faq')
    about = types.InlineKeyboardButton('О нас.', callback_data='about')
    basket = types.InlineKeyboardButton('Корзина', callback_data='basket')
    markup.add(shop, faq, about, basket)

    # кнопка админ зонв для мдератора
    if message.chat.id == Config.admin_chat_id:
        admin = types.InlineKeyboardButton('Админка', callback_data='admin')
        markup.add(admin)

    photo_path = 'static/welcome_img.png'
    try:
        # начальное сообщение
        sent_message = bot.send_photo(message.chat.id, photo=open(photo_path, 'rb'), caption=f'Привет! {message.from_user.first_name}, Что вас интересует?', reply_markup=markup)
        last_message_id = sent_message.message_id 
    except Exception as e:
        print(f"Ошибка при отправке приветственного сообщения: {e}")
    
    try:
        time.sleep(0)
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")


last_message_id = None

# функция для обработки нажтий кнопок
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
    
    elif call.data == 'clear_basket':
        clear_basket(call)
        show_basket(call.message)
        last_message_id = call.message.message_id

    elif call.data in Config.all_items:
        add_to_cart(call)
        msg = bot.send_message(call.message.chat.id, f'Товар "{call.data}" был добавлен в корзину.')
        time.sleep(1)
        try:
            bot.delete_message(call.message.chat.id, msg.message_id)
        except Exception as e:
            print(f"Error while deleting message: {e}")
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

    elif call.data == 'admin':
        admin_panel(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'view_orders':
        view_orders(call.message)
        last_message_id = call.message.message_id

    elif call.data == 'del_msg':
        if admin_orders_msg_id:
            bot.delete_message(call.message.chat.id, admin_orders_msg_id)
    
    elif call.data == 'del_user_msg':
        if admin_orders_msg_id:
            bot.delete_message(call.message.chat.id, user_successful_payment_msg_id)

    elif call.data == 'back':
        if last_message_id:
            back_markup = types.InlineKeyboardMarkup(row_width=2)
            back_markup.add(types.InlineKeyboardButton('Магазин.', callback_data='shop'),
                            types.InlineKeyboardButton('FAQ.', callback_data='faq'),
                            types.InlineKeyboardButton('О нас.', callback_data='about'),
                            types.InlineKeyboardButton('Корзина', callback_data='basket'))
            
            if call.message.chat.id == Config.admin_chat_id:
                admin = types.InlineKeyboardButton('Админка', callback_data='admin')
                back_markup.add(admin)
            
            photo_path = 'static/welcome_img.png'
            bot.edit_message_media(chat_id=call.message.chat.id, message_id=last_message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption=f'Привет! {call.from_user.first_name}, Что вас интересует?'), reply_markup=back_markup)
            return

    else:
        msg = bot.send_message(call.message.chat.id, 'Пожалуйста, выберите один из вариантов в меню.')
        time.sleep(1)
        try:
            bot.delete_message(call.message.chat.id, msg.message_id)
        except Exception as e:
            print(f"Error while deleting message: {e}")

def admin_panel(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    view_orders_button = types.InlineKeyboardButton('Просмотр заказов', callback_data='view_orders')
    back_button = types.InlineKeyboardButton('Назад', callback_data='back')
    markup.add(view_orders_button, back_button)
    photo_path = 'static/welcome_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='Админ меню'), reply_markup=markup)

def view_orders(message):
    global admin_orders_msg_id

    markup = types.InlineKeyboardMarkup(row_width=2)
    hide_db = types.InlineKeyboardButton('Скрыть заказы', callback_data='del_msg')
    markup.add(hide_db)
    orders = db.get_all_orders()
    if not orders:
        bot.send_message(message.chat.id, f'Нет доступных заказов.', reply_markup=markup)
        return

    orders_text = ""
    for order in orders:
        orders_text += (
            f"Номер заказа: {order[0]}\n"
            f"ID пользователя: {order[1]}\n"
            f"Имя пользователя: {order[2]}\n"
            f"Товары: {order[3]}\n"
            f"Сумма: {order[4]} {order[5]}\n"
            f"Дата заказа: {order[6]}\n\n"
        )
    admin_orders_msg = f'Всего заказов:\n{orders_text}'
    send_message = bot.send_message(message.chat.id, admin_orders_msg, reply_markup=markup)
    admin_orders_msg_id = send_message.message_id

def add_to_cart(call):
    user_basket[call.data] = Config.all_items.get(call.data)

def clear_basket():
    user_basket.clear()

def calculate_total():
    total = sum(Config.all_items[item] for item in user_basket)
    return total

def show_basket(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    if not user_basket:
        back = types.InlineKeyboardButton('Назад', callback_data='back')
        markup.add(back)
        photo_path = 'static/cart_img.png'
        bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='Ваша корзина пуста.'), reply_markup=markup)
    else:
        clear = types.InlineKeyboardButton('Очистить корзину', callback_data='clear_basket')
        pay = types.InlineKeyboardButton('Оплатить', callback_data='pay_callback')
        back = types.InlineKeyboardButton('Назад', callback_data='back')
        markup.add(pay, clear, back)

        basket_text = "Ваша корзина:\n"
        total_price = 0
        for item, price in user_basket.items():
            basket_text += f"{item}: {price}\n"
            total_price += price
        basket_text += f"\nСумма: {total_price} рублей"
        photo_path = 'static/full_cart_img.png'
        bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption=basket_text), reply_markup=markup)

def shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Fortnite', callback_data='fortnite'),
               types.InlineKeyboardButton('VALORANT', callback_data='valorant'),
               types.InlineKeyboardButton('Назад', callback_data='back'))

    photo_path = 'static/shop_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='Выберите игру:'), reply_markup=markup)

def FAQ(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Назад', callback_data='back'))

    photo_path = 'static/faq_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='FAQ'), reply_markup=markup)

def about(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton('Назад', callback_data='back'))

    photo_path = 'static/about_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='about'), reply_markup=markup)

def fortnite_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Вбаксы', callback_data='vbucks'),
               types.InlineKeyboardButton('Наборы', callback_data='bundle'),
               types.InlineKeyboardButton('Назад', callback_data='back'))

    photo_path = 'static/fortnite_shop_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='Выберите вид товара:'), reply_markup=markup)

def vbucks_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('1000VB', callback_data='1000VB'),
               types.InlineKeyboardButton('2000VB', callback_data='2000VB'),
               types.InlineKeyboardButton('5000VB', callback_data='5000VB'),
               types.InlineKeyboardButton('13500VB', callback_data='13500VB'),
               types.InlineKeyboardButton('Назад', callback_data='back'))

    photo_path = 'static/vbucks_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='Выберите товар:'), reply_markup=markup)

def fortnite_bundle_shop(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton('Street Shadows', callback_data='StreetShadows'),
               types.InlineKeyboardButton('Rogue Spider Knight', callback_data='RogueSpiderKnight'),
               types.InlineKeyboardButton('The Last Laugh', callback_data='TheLastLaugh'),
               types.InlineKeyboardButton('Назад', callback_data='back'))

    photo_path = 'static/fortnite_bundle_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='Выберите товар:'), reply_markup=markup)

def clear_after_successful_payment(message):
    clear_basket()
    welcome(message)

def dsc_for_payment() -> str:
    basket_text = "\n"
    for item, price in user_basket.items():
        basket_text += f"{item}: {price}\n"

    return basket_text

def create_telegram_payment(message):
    total_price = types.LabeledPrice(label='Оплатить товар(ы)', amount=calculate_total()*100)
    
    bot.send_invoice(message.chat.id,
                    title='xenoqs shop',
                    description=dsc_for_payment(),
                    provider_token=Config.payment_provider_token,
                    prices=[total_price],
                    invoice_payload="test-invoice-payload",
                    currency='rub')

def pay(message):
    global last_message_id

    # Создание платежной ссылки
    create_telegram_payment(message)

    last_message_id = message.message_id  # последний айди сообщения

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message: types.Message):
    global user_successful_payment_msg_id
    print('SUCCESSFUL PAYMENT')

    # сохр заказ в базе и получение айдишки 
    order_id = db.save_order(message.from_user.id, message.from_user.username, dsc_for_payment(), calculate_total(), message.successful_payment.currency)

    # Отправка номера заказа и инф в чат с покупатлем
    markup = types.InlineKeyboardMarkup(row_width=2)
    hide_db = types.InlineKeyboardButton('Скрыть заказ)', callback_data='del_user_msg')
    markup.add(hide_db)

    user_basket_text = dsc_for_payment()
    user_message = (
        f'Оплата прошла успешно!\n'
        f'Ваш заказ: {user_basket_text}\n'
        f'Номер заказа: {order_id}\n'
        f'Скоро с вами свяжится наш модератор: {Config.admin_id}'
    )
    send_message = bot.send_message(message.chat.id, user_message, reply_markup=markup)
    user_successful_payment_msg_id = send_message.message_id
    
    # Получение информации о человеке
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Создание ссылки на профиль пользователя
    if username:
        user_link = f"https://t.me/{username}"
    else:
        user_link = f"https://t.me/user?id={user_id}"
    
    # Отправка сообщения модератору
    total_amount = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency
    moderator_message = (
        f'Оплата на сумму {total_amount} {currency} прошла успешно!\n'
        f'Ссылка на покупателя: {user_link}\n'
        f'Товары: {dsc_for_payment()}\n'
        f'Номер заказа: {order_id}'
    )
    bot.send_message(Config.admin_chat_id, moderator_message)
    clear_after_successful_payment(message)

bot.polling(non_stop=True)