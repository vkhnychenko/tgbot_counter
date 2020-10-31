from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


bonus = KeyboardButton('📌Получить бонус📌')
check_bonus = KeyboardButton('Проверить количество баллов «Пятюня»')

start = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
start.add(bonus, check_bonus)
