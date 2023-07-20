import telebot
import config as conf
from telebot import types
import get_gold_prices
from core import save_in_gspread

bot = telebot.TeleBot(conf.API_KEY)
prices = get_gold_prices.get_prices()
d = {}


@bot.message_handler(commands=['start'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=f'Fix 995', callback_data='price_995')
    btn2 = types.InlineKeyboardButton(text=f'Fix 999', callback_data='price_999')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f"Today's Gold Prices\n999 - {prices[0]['sell']}$\n995 - {prices[1]['sell']}$",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('price_'))
def handle_callback(call):
    username = call.from_user.username
    if username is not None:
        print(prices[0]['sell'])
        d['username'] = username
        d['gold'] = call.data.split('_')[1]
        print(d)
        print('Username:', username)
    else:
        print('No username available.')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок

    if call.data == 'price_995':
        btn1 = types.KeyboardButton(text='10')
        btn2 = types.KeyboardButton(text='20')
        btn3 = types.KeyboardButton(text='50')
        btn4 = types.KeyboardButton(text='100')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(call.message.chat.id, "What weight do you want for 995?", reply_markup=markup)
    if call.data == 'price_999':
        btn1 = types.KeyboardButton(text='10')
        btn2 = types.KeyboardButton(text='20')
        btn3 = types.KeyboardButton(text='50')
        btn4 = types.KeyboardButton(text='100')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(call.message.chat.id, "What weight do you want for 999?", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    try:
        user_input = message.text[:-1]
        print(user_input)
        print(type(user_input))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        float_input = int(user_input)
        print(type(float_input))
        price999 = float(prices[0]['sell']) - 0.01
        price995 = float(prices[1]['sell']) - 0.01
        if d['gold'] == '999':
            total_price = float_input * price999
            d['total price'] = round(total_price)
            d['current_price'] = prices[0]['sell']
            markup_1 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text=f'✅ Yes', callback_data='yes')
            btn2 = types.InlineKeyboardButton(text=f'❌ No', callback_data='no')
            markup_1.add(btn1, btn2)
            bot.send_message(message.chat.id,
                             f"Fix Price for 50g and price: {round(price999)}$ -> {round(total_price)}$?",
                             reply_markup=markup)
            bot.send_message(message.chat.id, "Fix it?", reply_markup=markup_1)

        if d['gold'] == '995':
            total_price = float_input * price995
            d['total price'] = round(total_price)
            d['current_price'] = prices[1]['sell']
            markup_1 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text=f'Yes', callback_data='yes')
            btn2 = types.InlineKeyboardButton(text=f'No', callback_data='no')
            markup_1.add(btn1, btn2)
            bot.send_message(message.chat.id,
                             f"Fix Price for 50g and price: {round(price995)}$ -> {round(total_price)}$?",
                             )
            bot.send_message(message.chat.id, "Fix it?", reply_markup=markup_1)

            d['weight'] = user_input
        print(d)

    except Exception:
        bot.send_message(message.chat.id, "You input must be integer\nEnter /start command for start again")


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def yes_answer(call):
    data = [d]
    save_in_gspread.save_orders_data(data)
    bot.send_message(call.message.chat.id, "Thank you for your order!\nEnter /start command for order again")


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def yes_answer(call):
    print(call.data)
    bot.send_message(call.message.chat.id, "Enter /start command for order again")


bot.polling(none_stop=True, interval=0)
