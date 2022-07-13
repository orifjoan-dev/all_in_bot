
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
menu_kb.add('⛱ Ob-havo','💰 Kurs',"🎮 O'yin",'🎬 Youtube')


cities_kb = ReplyKeyboardMarkup(resize_keyboard=True)
cities_kb.add(' Andijan',' Bukhara',' Fergana',' Jizzakh',' Urgench',' Namangan',' Navoiy',' Qarshi',' Nukus',' Samarkand','Guliston',' Termez',' Tashkent','⬅️ Ortga')


currency_kb = ReplyKeyboardMarkup(resize_keyboard=True)
currency_kb.add('💲 Dollar','₽ Rubl','€ Yevro','₤ Lira','¥ Yuan','₸ Tenge','⬅️ Ortga')


play_kb = ReplyKeyboardMarkup(resize_keyboard=True)
play_kb.add('▶️ Play','⬅️ Ortga')


