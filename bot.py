import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
import requests

# Настройки
TOKEN = "ВАШ_ТОКЕН_БОТА"
ADMIN_ID = 123456789  # Ваш ID в Telegram
LEADCONVERTER_WEBHOOK = "https://ваш_leadconverter_url/webhook"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

# Клавиатуры
def get_main_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📚 Бесплатный урок"))
    kb.add(types.KeyboardButton("💡 Консультация"))
    return kb

def get_buy_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Купить курс", callback_data="buy_course"))
    return kb

# Состояния для анкеты
class Form(StatesGroup):
    problem = State()
    email = State()

# Команда /start
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я бот школы [Название]. Помогу тебе освоить [тема курса].\n\n"
        "📌 Получи бесплатный урок или консультацию:",
        reply_markup=get_main_kb()
    )
    await send_sequence(message.from_user.id)

# Автоматическая серия сообщений
async def send_sequence(user_id):
    messages = [
        ("📌 Хочешь узнать, как избежать ошибок в [тема]?", None),
        ("🔍 Вот решение, которое работает:", "solution_video.mp4"),
    ]
    for text, media in messages:
        if media:
            await bot.send_video(user_id, types.InputFile(media), caption=text)
        else:
            await bot.send_message(user_id, text)
        await asyncio.sleep(3600)  # Интервал 1 час

# Отправка данных в LeadConverter
async def send_to_leadconverter(email, name, problem):
    payload = {
        "email": email,
        "name": name,
        "problem": problem,
        "source": "Telegram Bot"
    }
    requests.post(LEADCONVERTER_WEBHOOK, json=payload)

# Обработка анкеты
@dp.message_handler(Text(equals="
