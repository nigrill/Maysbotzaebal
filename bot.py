
import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import requests

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
CRYPTOBOT_TOKEN = os.getenv("CRYPTOBOT_API_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
WEBSITE_URL = os.getenv("WEBSITE_URL")
PROMO_CODE = os.getenv("PROMO_CODE")
PAY_AMOUNT = os.getenv("PAY_AMOUNT")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

users_waiting_payment = {}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("🚀 Начать"))
    await message.answer("Привет! Добро пожаловать в VIP NFT Lab от Паши Мэйса.\n\nГотов пройти опрос?", reply_markup=kb)

@dp.message_handler(lambda message: message.text == "🚀 Начать")
async def start_poll(message: types.Message):
    await message.answer("1. Какой у тебя опыт в NFT?")
    users_waiting_payment[message.from_user.id] = {"step": 1}

@dp.message_handler(lambda message: message.from_user.id in users_waiting_payment)
async def handle_poll(message: types.Message):
    user_data = users_waiting_payment[message.from_user.id]
    step = user_data["step"]

    if step == 1:
        user_data["experience"] = message.text
        user_data["step"] = 2
        await message.answer("2. Сколько ты готов инвестировать в NFT?")
    elif step == 2:
        user_data["budget"] = message.text
        user_data["step"] = 3
        await message.answer("3. Какие проекты тебе интересны?")
    elif step == 3:
        user_data["interests"] = message.text
        await send_payment_link(message)

async def send_payment_link(message):
    user_id = message.from_user.id
    payload = f"nftvip_{user_id}"
    url = f"https://t.me/CryptoBot?start=payment-{payload}"
    await message.answer(f"💸 Оплати {PAY_AMOUNT} USDT через CryptoBot:\n\n{url}\n\nПосле оплаты ты будешь автоматически добавлен в приватный канал.")

@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if str(message.from_user.id) in os.getenv("ADMINS", ""):
        await message.answer("Админ-панель: Пока базовая версия.")
    else:
        await message.answer("⛔ Доступ запрещён.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
