import cfg
import time
import telebot
from telebot import types
from telebot.types import InputMediaPhoto

bot = telebot.TeleBot(cfg.token)

# Словарь для корзины пользователя
user_basket = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    #admin zone
    global last_message_id
    if message.chat.id == 1638573890:
        markup = types.InlineKeyboardMarkup(row_width=2)
        shop = types.InlineKeyboardButton('Магазин.', callback_data='shop')
        faq = types.InlineKeyboardButton('FAQ.', callback_data='faq')
        about = types.InlineKeyboardButton('О нас.', callback_data='about')
        basket = types.InlineKeyboardButton('Корзина', callback_data='basket')
        admin = types.InlineKeyboardButton('Админка', callback_data='admin')
        markup.add(shop, faq, about, basket, admin)
        photo_path = 'static/welcome_img.png'
        if last_message_id:
            bot.edit_message_media(chat_id=message.chat.id, message_id=last_message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption=f'Привет! {message.from_user.first_name}, Что вас интересует?'), reply_markup=markup)
        else:
            bot.send_photo(message.chat.id, photo=open(photo_path, 'rb'), caption=f'Привет! {message.from_user.first_name}, Что вас интересует?', reply_markup=markup)
        

    else:
        markup = types.InlineKeyboardMarkup(row_width=2)

        shop = types.InlineKeyboardButton('Магазин.', callback_data='shop')
        faq = types.InlineKeyboardButton('FAQ.', callback_data='faq')
        about = types.InlineKeyboardButton('О нас.', callback_data='about')
        basket = types.InlineKeyboardButton('Корзина', callback_data='basket')

        markup.add(shop, faq, about, basket)

        photo_path = 'static/welcome_img.png'
        if last_message_id:
            bot.edit_message_media(chat_id=message.chat.id, message_id=last_message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption=f'Привет! {message.from_user.first_name}, Что вас интересует?'), reply_markup=markup)
        else:
            bot.send_photo(message.chat.id, photo=open(photo_path, 'rb'), caption=f'Привет! {message.from_user.first_name}, Что вас интересует?', reply_markup=markup)

last_message_id = None

# Функция для обработки нажатий кнопок
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
        last_message_id = call.message.message_id
        show_basket(call.message)
        last_message_id = call.message.message_id

    elif call.data in cfg.all_items:
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

    elif call.data == 'back':
        if last_message_id:
            back_markup = types.InlineKeyboardMarkup(row_width=2)
            back_markup.add(types.InlineKeyboardButton('Магазин.', callback_data='shop'),
                            types.InlineKeyboardButton('FAQ.', callback_data='faq'),
                            types.InlineKeyboardButton('О нас.', callback_data='about'),
                            types.InlineKeyboardButton('Корзина', callback_data='basket'))
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

def add_to_cart(call):
    user_basket[call.data] = cfg.all_items.get(call.data)

def clear_basket(call):
    user_basket.clear()

def calculate_total():
    total = sum(cfg.all_items[item] for item in user_basket)
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
    markup.add(types.InlineKeyboardButton('Гремучие грёзы', callback_data='Гремучие грёзы'),
               types.InlineKeyboardButton('Аватар', callback_data='Аватар'),
               types.InlineKeyboardButton('Назад', callback_data='back'))

    photo_path = 'static/fortnite_bundle_img.png'
    bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=InputMediaPhoto(open(photo_path, 'rb'), caption='Выберите товар:'), reply_markup=markup)

def dsc_for_payment() -> str:
    basket_text = "\n"
    for item, price in user_basket.items():
        basket_text += f"{item}: {price}\n"

    return basket_text

def create_telegram_payment(message):
    total_price = types.LabeledPrice(label='Оплатить товар(ы)', amount=calculate_total()*100)

    if cfg.payment_provider_token.split(':')[1] == 'TEST':
        print('test pay')
    
    bot.send_invoice(message.chat.id,
                    title='xenoqs shop',
                    description=dsc_for_payment(),
                    provider_token=cfg.payment_provider_token,
                    prices=[total_price],  # Преобразуем total_price в список
                    invoice_payload="test-invoice-payload",
                    currency='rub')

def pay(message):
    global last_message_id

    # Создание платежной ссылки через Telegram Payments API
    create_telegram_payment(message)

    last_message_id = message.message_id  # Обновляем последний ID сообщения

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout(query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message: types.Message):
    print('SUCCESSFUL PAYMENT')
    
    # Получение информации о пользователе
    user_id = message.from_user.id
    username = message.from_user.username
    
    # Создание ссылки на профиль пользователя
    if username:
        user_link = f"https://t.me/{username}"
    else:
        user_link = f"https://t.me/user?id={user_id}"
    
    # Отправка сообщения с информацией об оплате и ссылкой на пользователя
    total_amount = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency
    bot.send_message(
        1638573890,
        f'Оплата на сумму {total_amount} {currency} прошла успешно!\n'
        f'Ссылка на покупателя: {user_link}')
    
# def successful_payment(message: types.Message):
#     user = message.from_user.first_name
#     print('SUCCESSFUL PAYMENT')
#     invoice_payload = message.successful_payment.invoice_payload
#     if invoice_payload is not None:
#         print('Invoice Payload:', invoice_payload)
#         bot.send_message(message.chat.id, f'Оплата на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошла успешно!')
#         bot.send_message(1638573890, f'{user}, ОПЛАТА ПРОШЛА\n\nТОВАРЫ: {dsc_for_payment()}\nСУММА: {calculate_total()}')
#     else:
#         bot.send_message(message.chat.id, f'Оплата не прошла')
#         print('Invoice payload is not available.')



bot.polling(non_stop=True)
