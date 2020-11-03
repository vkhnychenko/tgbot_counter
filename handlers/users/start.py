from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import keyboards.default.reply_keyboards as reply_kb
from loader import dp, bot
from data.config import POINTS, ADMIN_ID, client
from operator import itemgetter


@dp.message_handler(lambda message: message.chat.type != 'group', CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=reply_kb.start)


@dp.message_handler(commands='rating')
async def rating_handler(message: types.Message):
    cursor = client.db.test_collection.find()
    text = '🏆Рейтинг участников🏆\n'
    new_list = sorted(await cursor.to_list(length=100), key=itemgetter('points'), reverse=True)
    for document in new_list:
        print(document)
        text += f'@{document["username"]}' + f'({document["points"]})\n'
    await message.answer(text)


@dp.message_handler(lambda message: message.chat.type != 'group', text='📌Получить бонус📌')
async def bonus_handler(message: types.Message):
    result = await client.db.test_collection.find_one({'user_id': message.from_user.id})
    if result is None:
        points = 0
    else:
        points = result['points']
    print(points)
    if points >= POINTS:
        await message.answer('Бонус получен!Куратор свяжется с вами в ближайшее время.')
        await bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        await client.db.test_collection.update_one({'user_id': message.from_user.id},
                                                         {'$set': {'points': points - POINTS}})
    else:
        await message.answer(f'Недостаточно баллов для получения бонуса. Осталось набрать {POINTS - points} баллов')


@dp.message_handler(lambda message: message.chat.type != 'group', text='Проверить количество баллов «Пятюня»')
async def bonus_handler(message: types.Message):
    result = await client.db.test_collection.find_one({'user_id': message.from_user.id})
    if result is not None:
        points = result['points']
    else:
        points = 0
    res = 0 if points > POINTS else POINTS - points
    await message.answer(f'Количество баллов «Пятюня»: {points}\n'
                         f'Для получения бонуса осталось набрать: {res} баллов')
