# Домашнее задание по теме "Инлайн клавиатуры".
# Задача "Ещё больше выбора"

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


api = ''  # api ключ
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
formula_txt = '10 х вес (кг) + 6,25 х рост (см) - 5 х возраст (г) -161'
info_txt = 'Рассчет нормы калорий по формуле Миффлина-Сан Жеора.'

# Клавиатура 1
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.row(
    button1, button2
)

# Клавиатура 2 (inline)
kb_in = InlineKeyboardMarkup(resize_keyboard=True)
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in.row(
    button3, button4
)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


# Обработчик кнопки button1
@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in)


# Обработчик кнопки button2
@dp.message_handler(text='Информация')
async def info(message):
    await message.answer(info_txt)


# Обработчик кнопки button4
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(formula_txt)
    await call.answer()  # Завершение вызова call и реактивация кнопки


# класс, описывающий состояние пользователя
class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()


# Обработчик кнопки button3
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()
    await call.answer()  # Завершение вызова call и реактивация кнопки


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост в см:')
    await UserState.height.set()


@dp.message_handler(state=UserState.height)
async def set_weight(message, state):
    await state.update_data(height=message.text)
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * float(data['weight']) + 6.25 * float(data['height']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваша норма калорий {calories:.2f}')
    await state.finish()


@ dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
