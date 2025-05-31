import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram import F


TOKEN = "7456695702:AAFbHDirnxMh0CaqeWASunF2rtzr_tGmuyY"  
INFOBIP_API_KEY = "38bff28b325d34b07e7008a4d769a295-28f9aa79-bcc8-4831-941f-c0857b5d0a1b"

PROJECT_URL = "https://openbudget.uz/boards/initiatives/initiative/50/0fa8928a-a03e-45d6-af2b-285084b84cde" 
PROJECT_NAME = "Xorazm viloyati Bog'ot tumani, Ma'naviyat MFYda Ichki Yo'llarni tamirlashga o'z hissangizni qo'shing!"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


voters = set()
user_phone_numbers = {}


request_phone_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="📱 Telefon raqam yuborish", request_contact=True)]],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start_command(message: types.Message):
    response_text = (f"📢 <b>{PROJECT_NAME}</b> loyihasiga ovoz bering!\n\n"
                     f"🔗 Batafsil: {PROJECT_URL}\n\n"
                     "Ovoz berish uchun telefon raqamingizni yuboring.\n\n")
    await message.answer(response_text, parse_mode="HTML", reply_markup=request_phone_keyboard)

@dp.message(F.contact)
async def handle_contact(message: types.Message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number.lstrip("+")
    user_phone_numbers[user_id] = phone_number
    await message.answer("📩 Telefon raqamingizni tasdiqlash uchun SMS yuborildi.", reply_markup=ReplyKeyboardRemove())

@dp.message(F.text)
async def handle_text(message: types.Message):
    user_id = message.from_user.id

    if message.text.startswith("CAPTCHA token: "):
        token = message.text[len("CAPTCHA token: "):]

        if verify_captcha(token):
            await message.answer(f"✅ Rahmat! Siz {PROJECT_NAME} loyihasiga ovoz berdingiz.\n\n📊 Jami ovozlar: {len(voters)}")
        else:
            await message.answer("❌ CAPTCHA tasdiqlashda xatolik yuz berdi. Iltimos, qaytadan urinib ko‘ring.")

    elif message.text == "🗳 Ovoz berish":
        if user_id not in user_phone_numbers:
            await message.answer("❌ Iltimos, avval telefon raqamingizni tasdiqlang!")
        elif user_id in voters:
            await message.answer("❌ Siz allaqachon ovoz bergansiz!")
        else:
            voters.add(user_id)
            await message.answer(f"✅ Rahmat! Siz {PROJECT_NAME} loyihasiga ovoz berdingiz.\n\n📊 Jami ovozlar: {len(voters)}")

def verify_captcha(token):
    url = "http://your-server.com/verify-captcha"  
    payload = {
        'token': token
    }
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get("success", False)  

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())