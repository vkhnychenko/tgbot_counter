from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import keyboards.default.reply_keyboards as reply_kb
from utils.redis.consts import redis
from loader import dp, bot
from data.config import POINTS, ADMIN_ID


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=reply_kb.start)


@dp.message_handler(text='📌Получить бонус📌')
async def bonus_handler(message: types.Message):
    result = await redis.get(f'{message.from_user.id}')
    if result is not None:
        result = int(result)
    else:
        result = 0
    if result >= POINTS:
        await message.answer('Бонус получен!Куратор свяжется с вами в ближайшее время.')
        await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        result = result - POINTS
        await redis.set(f'{message.chat.id}', f'{result}')
    else:
        await message.answer(f'Недостаточно баллов для получения бонуса. Осталось набрать {POINTS - int(result)} баллов')


@dp.message_handler(text='Проверить количество баллов «Пятюня»')
async def bonus_handler(message: types.Message):
    result = await redis.get(f'{message.from_user.id}')
    if result is not None:
        result = int(result)
    else:
        result = 0
    await message.answer(f'Количество баллов «Пятюня»: {result}\n'
                         f'Для получения бонуса осталось набрать: {POINTS - result} баллов')
