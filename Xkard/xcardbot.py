import telebot
from telebot import types

from PIL import Image, ImageDraw, ImageFont
#im = Image.open('MO.png')
#image = Image.new('RGB', (1000, 900), (255, 255, 255))
image  = Image.open('p.jpg')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('arial.ttf', size=45)

import random
import os
import datetime
import qrcode

token = "1861564936:AAElg28kmf6Z1zG7X03MZF280KtKrS5e0cs"

d_date = datetime.datetime.now()

bot = telebot.TeleBot(token) 

#flag = False

@bot.message_handler(commands=['start'])
def welcome(message):

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton("Зарегистрировать карту.")
    item2 = types.KeyboardButton("Узнать свой QR.")
    item3 = types.KeyboardButton("Наше приложение.")
    markup.add(item1, item2,item3)
 
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}. Данный бот создан, что бы каждый житель города имел возможность быстро получить доступ к функциям Xcard. <a href='https://yandex.ru/'>Ссылка на приложение</a>",
        parse_mode='html', reply_markup=markup)

    
@bot.message_handler(content_types=['text'])
def func(message):

    chatId = message.chat.id

    #global flag

    if message.chat.type == 'private':
        if message.text == 'Зарегистрировать карту.':
            #if flag == False:
            (x, y) = (600, 75)
            idno = random.randint(10000000, 90000000)
            message = str('ID ' + str(idno))
            color = 'rgb(0, 0, 0)'  # black color
            font = ImageFont.truetype('arial.ttf', size=60)
            draw.text((x, y), message, fill=color, font=font)

            img = qrcode.make(str(idno))  # this info. is added in QR code, also add other things
            img.save(str(idno) + '.jpg')

            qr_code = open(str(idno) + '.jpg', 'rb')
            bot.send_photo(chatId, qr_code, f"Ваша ID карта сгенерированна, и имеет уникальный номер ID{idno}")
            #flag = True
            #else:
                #bot.send_message(chatId, f"Прошу прощения {message.from_user.first_name}, но вы уже имеете зарегистрированную на вас ID карту.")


        elif message.text == 'Узнать свой QR.':
            bot.send_message(message.chat.id, f"Прошу прощения {message.from_user.first_name}. На текущий момент данная функция не активна.")
        elif message.text == 'Наше приложение.':
            bot.send_message(message.chat.id, f"Для получение более подробной информации, а так же выбора места отдыха, вы можете посетить <a href='https://yandex.ru/'>наше приложение</a>.", parse_mode='html')
        else:
            bot.send_message(message.chat.id, f"Прошу прощения {message.from_user.first_name}, но ваша команда не корректна!")




# RUN
bot.polling(none_stop=True)