
import json
import logging
import datetime
from os import link
from time import sleep
import requests
import config
from pytube import YouTube
from config import open_weather_key
from aiogram import Bot,Dispatcher,types
from aiogram.utils import executor
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import Text
from asyncio import sleep
from keyboards import menu_kb,cities_kb,currency_kb,play_kb

bot=Bot(token=config.tg_bot_token)
dp=Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(text='⬅️ Ortga')
async def back(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,text='Ortga ⬅️',reply_markup=menu_kb,parse_mode=types.ParseMode.HTML)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,text=f"Tugmani bosing ⬇️",reply_markup=menu_kb,parse_mode=types.ParseMode.HTML)


@dp.message_handler(text='⛱ Ob-havo')
async def weather(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,text='Shaharni tanlang ⬇️',reply_markup=cities_kb,parse_mode=types.ParseMode.HTML)

CITIES = [  
'Andijan',
'Bukhara',
'Fergana',
'Jizzakh',
'Urgench',
'Namangan',
'Navoiy',
'Qarshi',
'Nukus',
'Samarkand',
'Guliston',
'Termez',
'Tashkent',
'⬅️ Ortga',
]

@dp.message_handler(filters.Text(equals=CITIES,ignore_case=True))  
async def get_weather(message: types.Message):
    code_to_weather = {
        "Clear": "Quyosh \U00002600",
        "Clouds": "Bulut \U00002601",
        "Rain": "Yomg'ir \U00002614",
        "Drizzle": "Yomg'ir\U00002614",
        "Thunderstorm": "Chaqmoq \U000026A1",
        "Snow": "Qor \U0001F328",
        "Mist": "Tuman \U0001F32B",

    } 
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_key}&units=metric"
        )
        data = r.json()


        shahar = data['name']
        namlik = data['main']['humidity']
        temperatura = data['main']['temp']
        shamol = data['wind']['speed']
        quyosh_chiqishi = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        quyosh_botishi = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        weather_decription = data['weather'][0]['main']
        if weather_decription in code_to_weather:
            wd = code_to_weather[weather_decription]
        else:
            wd = "Topib bo'lmadi"

        await message.answer(f"Shahar: {shahar} sh.\n"
              f"Namlik foizi: {namlik}%\n"
              f"Temperatura: {temperatura} C {wd}\n"
              f"Shamol tezligi: {shamol} km/h\n"
              f"Quyosh chiqishi: {quyosh_chiqishi}\n"
              f"Quyosh botishi: {quyosh_botishi}\n"
              )

    except:
        await message.answer("Xatolik shaharni nomini tekshiring !")

@dp.message_handler(text='💰 Kurs')
async def currency(message:types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,text="Valyutani tanlang ⬇️",reply_markup=currency_kb,parse_mode=types.ParseMode.HTML)

CURRENCY = {
  '💲 Dollar',
  '₽ Rubl',
  '€ Yevro',
  '₤ Lira',
  '¥ Yuan',
  '₸ Tenge',
  '⬅️ Ortga',
}

@dp.message_handler(filters.Text(equals=CURRENCY,ignore_case=True))
async def get_currency(message: types.Message):
    inputs = {'USD',
    'RUB',
    'EUR',
    'TRY',
    'CNY',
    'KZT',
    '⬅️ Ortga',
    }
    outputs = {'UZS'}
    text = message.text
    if text == '💲 Dollar':
        inputs = 'USD'
        outputs = 'UZS'
    elif text == '₽ Rubl':
        inputs = 'RUB'
        outputs = 'UZS'
    elif text == '€ Yevro':
        inputs = 'EUR'
        outputs = 'UZS'
    elif text == '₤ Lira':
        inputs = 'TRY'
        outputs = 'UZS'
    elif text == '¥ Yuan':
        inputs = 'CNY'
        outputs = 'UZS'
    elif text == '₸ Tenge':
        inputs = 'KZT'
        outputs = 'UZS'

    url = 'https://v6.exchangerate-api.com/v6/603ee02ddd20de47e5d983b3/latest/'+inputs
    response = requests.get(url)
    rest = json.loads(response.text)
    result = str(rest['conversion_rates'][outputs])
    await bot.send_message(message.chat.id,result)

@dp.message_handler(text="🎮 O'yin")
async def game(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,text=f"{message.from_user.username} O'yinni boshlash uchun ▶️ play tugmasini bosing",reply_markup=play_kb,parse_mode=types.ParseMode.HTML)

@dp.message_handler(text='▶️ Play')
async def start_game(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,text="O'yin boshlandi !!!")
    await sleep(1)
    

    bot_data = await bot.send_dice(message.from_user.id)
    bot_data = bot_data['dice']['value']
    await sleep(3)
    await dp.bot.send_message(chat_id=message.from_user.id,text=f'Botga {bot_data} raqami tushdi !!!')

    user_data = await bot.send_dice(message.from_user.id)
    user_data = user_data['dice']['value']
    await sleep(5)
    await dp.bot.send_message(chat_id=message.from_user.id,text=f'Sizga {user_data} raqami tushdi !!!')

    if bot_data > user_data:
        await dp.bot.send_message(chat_id=message.from_user.id,text='Siz yutqazdingiz !!!')
    elif bot_data < user_data:
        await dp.bot.send_message(chat_id=message.from_user.id,text='Siz yutdingiz !!!')
    else:
        await dp.bot.send_message(chat_id=message.from_user.id,text='Durrang !!!')

@dp.message_handler(text='🎬 Youtube')
async def youtube(message: types.Message):
    await dp.bot.send_message(chat_id=message.from_user.id,text="🔽 Youtubedan mp3 yuklash uchun URL manzilini kirgizing: ")

@dp.message_handler(Text(startswith="http"))
async def get_audio(message: types.Message):
    link = message.text
    from io import BytesIO
    buffer = BytesIO()
    url = YouTube(link)
    if url.check_availability() is None:
        file = url.streams.get_audio_only()
        file.stream_to_buffer(buffer=buffer)
        buffer.seek(0)
        filename = f"{url.title} \nMuvaffaqiyatli yakunlandi ✅"
        await dp.bot.send_audio(chat_id=message.from_user.id,audio=buffer,caption=filename)
    else:
        await dp.bot.send_message(chat_id=message.from_user.id,text="Manzil noto'g'ri ❌")

if __name__ == '__main__':
    executor.start_polling(dp)
