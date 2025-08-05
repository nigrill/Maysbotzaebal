
from flask import Flask, request
import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
WEBSITE_URL = os.getenv("WEBSITE_URL")
PROMO_CODE = os.getenv("PROMO_CODE")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Webhook OK"

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.json
    if data.get("status") == "success":
        payload = data["payload"]
        if payload.startswith("nftvip_"):
            user_id = int(payload.split("_")[1])
            try:
                await bot.send_message(user_id, f"✅ Оплата получена! Добро пожаловать в клуб.\n\n🔗 Сайт регистрации: {WEBSITE_URL}\n🎁 Промокод: {PROMO_CODE}")
                await bot.add_chat_member(CHANNEL_ID, user_id)
            except Exception as e:
                print("Ошибка:", e)
    return "OK"
