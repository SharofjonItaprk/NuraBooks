import asyncio
import logging
import json
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# === SOZLAMALAR ===
BOT_TOKEN = "8971804411:AAH6cESQFaAtsZkf9ci2ZLzSP7SoU1nBfbw"  # @BotFather bergan API token
ADMIN_ID = 8440649749 # Telegram ID-ngiz (buyurtmalar borishi uchun)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start buyrug'i
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    # Siz tasdiqlagan to'g'ri GitHub Pages havolasi
    web_app_url = "https://sharofjonitaprk.github.io/NuraBooks/"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Do'konni ochish", web_app=WebAppInfo(url=web_app_url))]
    ])

    await message.answer(
        f"Assalomu alaykum, {message.from_user.full_name}!\n"
        "NuraBooks do'koniga xush kelibsiz. Kitoblarni ko'rish uchun tugmani bosing:",
        reply_markup=kb
    )

# Mini App'dan kelgan buyurtmani qabul qilish
@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    data = json.loads(message.web_app_data.data)

    await message.answer(
        f"Rahmat! Buyurtmangiz qabul qilindi.\n\n"
        f"📚 Kitob: {data['book']}\n"
        f"💰 Summa: {data['totalPrice']:,} so'm\n\n"
        "Admin tez orada siz bilan bog'lanadi."
    )

    admin_text = (
        f"📥 **YANGI BUYURTMA!**\n\n"
        f"👤 Xaridor: {message.from_user.full_name} (@{message.from_user.username})\n"
        f"📚 Kitob: {data['book']}\n"
        f"🔢 Soni: {data['quantity']} ta\n"
        f"💰 Summa: {data['totalPrice']:,} so'm\n"
        f"📞 Telefon: `{data['phone']}`\n"
        f"📍 Manzil: {data['address']}"
    )

    await bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())