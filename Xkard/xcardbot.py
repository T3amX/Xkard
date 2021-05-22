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
import time

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
     
    msg = bot.send_message(message.chat.id, f"Добро пожаловать, {message.from_user.first_name}. Данный бот создан, что бы каждый житель города имел возможность быстро получить доступ к функциям Xkard. <a href='https://yandex.ru/'>Ссылка на приложение</a>",
        parse_mode='html', reply_markup=markup)

    bot.register_next_step_handler(msg, func)


@bot.message_handler(content_types=['text'])
def func(message):

    chatId = message.chat.id

    #global flag

    if message.chat.type == 'private':
        if message.text == 'Зарегистрировать карту.':

            def start(message):
                msg = bot.send_message(message.chat.id, 'Укажите ваш пол (м/ж) : ')
                bot.register_next_step_handler(msg, start_2)

            msg = bot.send_message(message.chat.id, 'Введите ФИО : ')
            bot.register_next_step_handler(msg, start)

            def start_2(message):
                msg = bot.send_message(message.chat.id, 'Укажите полный возраст : ')
                bot.register_next_step_handler(msg, start_3)

                
            def start_3(message):
                msg = bot.send_message(message.chat.id, 'Из какого вы города? : ')
                bot.register_next_step_handler(msg, start_4)

            def start_4(message):
                msg = bot.send_message(message.chat.id, 'Укажите свой номер телефона (формат: 7xxxxxxxxxx) : ')
                bot.register_next_step_handler(msg, start_5)

            def start_5(message):
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
                #bot.send_message(chatId, f"Прошу прощения {message.from_user.first_name}, но вы уже имеете зарегистрированную на вас ID карту.")\


        elif message.text == 'Узнать свой QR.':
            bot.send_message(message.chat.id, f"Прошу прощения {message.from_user.first_name}. На текущий момент данная функция не активна.")
        elif message.text == 'Наше приложение.':
            bot.send_message(message.chat.id, f"Для получение более подробной информации, а так же выбора места отдыха, вы можете посетить <a href='https://yandex.ru/'>наше приложение</a>.", parse_mode='html')
        else:
            bot.send_message(message.chat.id, f"Прошу прощения {message.from_user.first_name}, но ваша команда не корректна!")
        
   # RUN
bot.polling(none_stop=True)