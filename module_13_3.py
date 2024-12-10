# Задача "Он мне ответил!"

from aiogram import Bot, Dispatcher, executor
# fsm_storage - блок работы с памятью:
from aiogram.contrib.fsm_storage.memory import MemoryStorage


api = ''  # api ключ
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

@ dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
