from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список доступных команд: ',
        '/start - Начать диалог',
        '/help - Список доступных команд',
        '/stats - Личная статистика',
        '/rating - Показывает рейтинг группы в которой выполняется команда',
        '/bonus - Получить бонус',
    ]
    await message.answer('\n'.join(text))
