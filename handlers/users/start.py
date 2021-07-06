from aiogram.dispatcher.filters.builtin import CommandStart
from loader import bot
from config import POINTS, ADMIN_ID, client
from operator import itemgetter
from aiogram import types
from loader import dp
import re
from loguru import logger

db = client.counter
collection = db.counter


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}! Я бот для подсчета рейтинга "Пятюня\n'
                         f'Используй /help для отображения всех доступных команд')


@dp.message_handler(commands='rating')
async def rating_handler(message: types.Message):
    group = await collection.find_one({'group_id': message.chat.id})
    if group is None:
        await message.answer('В этой группе еще нет рейтинга')
    else:
        try:
            cursor = collection.find({'group_id': group['group_id']})
            text = '🏆Рейтинг участников🏆\n\n'
            new_list = sorted(await cursor.to_list(length=100), key=itemgetter('points'), reverse=True)
            for document in new_list:
                text += f'@{document["username"]} ' + f'({document["points"]})\n'
            await message.answer(text)
        except Exception as e:
            logger.error(e)


@dp.message_handler(commands='bonus')
async def bonus_handler(message: types.Message):
    result = await collection.find_one({'user_id': message.from_user.id, 'group_id': message.chat.id})
    if result is None:
        points = 0
    else:
        points = result['points']
    if points >= POINTS:
        await message.answer('Бонус ваш!Напишите, пожалуйста, куратору вашего чата для получения бонуса')
        await bot.send_message(ADMIN_ID, f'Пользователь получил бонус @{result["username"]}')
        await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        await collection.update_one({'user_id': message.from_user.id, 'group_id': message.chat.id},
                                    {'$set': {'points': points - POINTS}})
    else:
        await message.answer(f'Недостаточно баллов для получения бонуса. Осталось набрать {POINTS - points} баллов')


@dp.message_handler(commands='stats')
async def stats_handler(message: types.Message):
    result = collection.find({'user_id': message.from_user.id})
    text = ''
    result_list = await result.to_list(length=10)
    if not result_list:
        text = 'Вы еще не имеете рейтинга ни в одной группе'
    else:
        for doc in result_list:
            res = 0 if doc["points"] > POINTS else POINTS - doc["points"]
            text += f'Количество баллов «Пятюня» в группе {doc["group_name"]}: {doc["points"]}\n' \
                    f'Для получения бонуса осталось набрать: {res} баллов\n\n'
    await message.answer(text)


@dp.message_handler()
async def all_message_handler(message: types.Message):
    if message.reply_to_message is not None:
        user_id = message.reply_to_message.from_user.id
        username = message.reply_to_message.from_user.username
        group_name = message.chat.title
        group_id = message.chat.id
        if re.search(r'\+', message.text) and user_id != message.from_user.id:
            try:
                result = await collection.find_one({'user_id': user_id, 'group_id': group_id})
                if result is None:
                    data = {
                        "user_id": user_id,
                        "username": username,
                        "group_id": group_id,
                        "group_name": group_name,
                        "points": 1
                    }
                    await collection.insert_one(data)
                else:
                    await collection.update_one({'user_id': user_id, 'group_id': group_id},
                                                {'$set': {'points': result['points'] + 1,
                                                          'username': username}})
            except Exception as e:
                logger.error(e)
            await message.answer(f'{message.from_user.username} дал пятюню {message.reply_to_message.from_user.username}')