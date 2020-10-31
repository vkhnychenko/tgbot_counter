from aiogram import types
from loader import dp
import re
from utils.redis.consts import redis


@dp.message_handler()
async def all_message_handler(message: types.Message):
    if message.reply_to_message is not None:
        user_id = message.reply_to_message.from_user.id
        # print(message.text)
        # print(message.reply_to_message.from_user.id)
        if (re.search(r'\+', message.text) or re.search(r'👍', message.text)) and user_id != message.from_user.id:
            result = await redis.get(f'{user_id}')
            print(result)
            if result is not None:
                res = int(result) + 1
            else:
                res = 1
            await redis.set(f'{user_id}', f'{res}')
            await message.answer('Найдено совпадение')