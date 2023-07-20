import telebot
import config as conf
from telebot import types
import get_gold_prices
from core import save_in_gspread

bot = telebot.TeleBot(conf.API_KEY)
prices = get_gold_prices.get_prices()
d = {}


@bot.message_handler(commands=['new_fix'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text=f'Ֆիքսել 995', callback_data='price_995')
    btn2 = types.InlineKeyboardButton(text=f'Ֆիքսել 999', callback_data='price_999')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f"Ոսկու գներ՝\n999 - {prices[0]['sell']}$\n995 - {prices[1]['sell']}$",
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

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if call.data == 'price_995':
        btn1 = types.KeyboardButton(text='10')
        btn2 = types.KeyboardButton(text='20')
        btn3 = types.KeyboardButton(text='50')
        btn4 = types.KeyboardButton(text='100')
        btn5 = types.KeyboardButton(text='200')
        btn6 = types.KeyboardButton(text='300')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(call.message.chat.id, "Մուտքագրեք կամ Ընտրեք քաշը՝", reply_markup=markup)
    if call.data == 'price_999':
        btn1 = types.KeyboardButton(text='10')
        btn2 = types.KeyboardButton(text='20')
        btn3 = types.KeyboardButton(text='50')
        btn4 = types.KeyboardButton(text='100')
        btn5 = types.KeyboardButton(text='200')
        btn6 = types.KeyboardButton(text='300')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(call.message.chat.id, "Մուտքագրեք կամ Ընտրեք քաշը՝", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_user_input(message):
    try:
        user_input = message.text
        if ',' in user_input:
            user_input = user_input.replace(',', '.')
        float_input = float(user_input) or int(user_input)
        print(float_input)
        if float_input < 10:
            bot.send_message(message.chat.id, "You input must be more than 10\nEnter /new_fix command for start again")
        price999 = float(prices[0]['sell']) - 0.1
        price995 = float(prices[1]['sell']) - 0.1
        if d['gold'] == '999':
            total_price = float_input * price999
            d['total price'] = int(round(total_price))
            d['current_price'] = prices[0]['sell']
            markup_1 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text=f'✅ Այո', callback_data='yes')
            btn2 = types.InlineKeyboardButton(text=f'❌ Ոչ', callback_data='no')
            markup_1.add(btn1, btn2)
            bot.send_message(message.chat.id,
                             f"Ընդհանուր գումար՝{round(total_price)}$\n {float_input} "
                             f"* ({float(prices[0]['sell'])} - {0.1}) = {round(total_price)}$",
                             )
            bot.send_message(message.chat.id, "Ֆիքսենք❓", reply_markup=markup_1)
            d['weight'] = float(user_input)

        if d['gold'] == '995':
            total_price = float_input * price995
            d['total price'] = int(round(total_price))
            d['current_price'] = prices[1]['sell']
            markup_1 = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton(text=f'✅ Այո', callback_data='yes')
            btn2 = types.InlineKeyboardButton(text=f'❌ Ոչ', callback_data='no')
            markup_1.add(btn1, btn2)
            bot.send_message(message.chat.id,
                             f"Ընդհանուր գումար՝{round(total_price)}$\n {float_input} "
                             f"* ({float(prices[1]['sell'])} - {0.1}) = {round(total_price)}$",
                             )
            bot.send_message(message.chat.id, "Ֆիքսենք❓", reply_markup=markup_1)

            d['weight'] = user_input
        print(d)

    except Exception:
        bot.send_message(message.chat.id, "🚫Սխալ\nԴուք պետք է  մութքագրեք միայն թվանշան\n"
                                          "Սեխմեք /new_fix հրահանգը կրկին փորցելու համար")


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def yes_answer(call):
    data = [d]
    save_in_gspread.save_orders_data(data)
    channel_username = 'goldcenter_fix'
    bot.send_message(call.message.chat.id, "Շնորհակալություն, ֆիքսելու համար! Կարող եք մոտենալ։\n"
                                           "Սեխմեք /new_fix նոր քաշ ֆիքսելու համար")
    message = bot.send_message(chat_id='@' + channel_username, text=f'Նոր Ֆիքս՝ https://t.me/{d["username"]}\n'
                                                                    f'{d["gold"]},{d["weight"]} * '
                                                                    f'{d["current_price"]} = {d["total price"]}$'
                               )
    channel_id = message.chat.id
    print(f'Channel ID: {channel_id}')


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def yes_answer(call):
    print(call.data)
    bot.send_message(call.message.chat.id, "Սեխմեք /new_fix հրահանգը կրկին փորցելու համար")


bot.polling(none_stop=True, interval=0)
