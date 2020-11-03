from aiogram import types
from loader import dp
import re
from data.config import client


@dp.message_handler()
async def all_message_handler(message: types.Message):
    if message.reply_to_message is not None:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
        if (re.search(r'\+', message.text) or re.search(r'👍', message.text)) and user_id != message.from_user.id:
            result = await client.db.test_collection.find_one({'user_id': user_id})
            if result is None:
                data = {
                    "user_id": user_id,
                    "username": username,
                    "points": 1
                }
                res = await client.db.test_collection.insert_one(data)
            else:
                res = await client.db.test_collection.update_one({'user_id': user_id},
                                                                    {'$set': {'points': result['points'] + 1}})
            await message.answer(f'{message.from_user.username} дал пятюню {message.reply_to_message.from_user.username}')