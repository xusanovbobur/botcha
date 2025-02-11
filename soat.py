import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8030104495:AAE3UyPpRjBYIOaB8qMEEarmorIO6m9TXnI" 
USER_CODE = "9304"
bot = Bot(token=TOKEN)
dp = Dispatcher()

menu_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💳 Kartalar")],
        [KeyboardButton(text="📞 Nomer")]
    ],
    resize_keyboard=True
)
cards = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🟦💳 UzCard")],
        [KeyboardButton(text="💳🌍 Visa Card")],
        [KeyboardButton(text="💳🔴🟠 Master Card")],
        [KeyboardButton(text="💳🟣🟢 Humo")],
        [KeyboardButton(text="🔙 Orqaga")]
    ]
)
numbers = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔵 Telefon 1")],
        [KeyboardButton(text="🔴 Telefon 2")],
        [KeyboardButton(text="🔙 Orqaga")]
    ]
)
retry_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Qayta urinish", callback_data="retry")]
    ]
)
CARDS = {
    "🟦💳 UzCard": ["🙎‍♂️ Nuriddinov Mhammadiyor\nAmal qilish muddati : 06/29\n Uzcard", "5614682006072781"],
    "💳🌍 Visa Card": ["🙎‍♂️ Nuriddinov Mhammadiyor\nAmal qilish muddati : 01/28\n Visa Card", "4046320010155968"],
    "💳🔴🟠 Master Card": ["🙎‍♂️ Nuriddinov Mhammadiyor\nAmal qilish muddati : 01/28\n Master Card", "5174250020579389"],
    "💳🟣🟢 Humo": ["🙎‍♂️ Nuriddinov Mhammadiyor\nAmal qilish muddati : 01/28\n HUMO", "9860 2466 0227 7930"],
}
NUMBERS = {
    "🔵 Telefon 1": ["🙎‍♂️ Nuriddinov Mhammadiyor\n📞 Telefon raqami:\n\t\t 👇👇\n\t\t+998995179304 \n\t\t👆👆"],
    "🔴 Telefon 2": ["🙎‍♂️ Nuriddinov Mhammadiyor\n📞 Telefon raqami:\n\t\t 👇👇\n\t\t+998905379304 \n\t\t👆👆"],
}

user_states = {}

@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("🔹 Ma'lumotlaringizni saqlash uchun quyidagi tugmalardan foydalaning:", reply_markup=menu_buttons)

@dp.message(lambda message: message.text == "💳 Kartalar")
async def kartala(message: types.Message):
    await message.answer("💳 Qaysi kartani tanlamoqchisiz?", reply_markup=cards)

@dp.message(lambda message: message.text == "📞 Nomer")
async def nomerlar(message: types.Message):
    await message.answer("📞Raqamni nusxalab oling !", reply_markup=numbers)

@dp.message(lambda message: message.text == "🔙 Orqaga")
async def back_to_menu(message: types.Message):
    await message.answer("🔙 Asosiy menyuga qaytdingiz.", reply_markup=menu_buttons)

@dp.message(lambda message: message.text in CARDS.keys() or message.text in NUMBERS.keys())
async def request_code(message: types.Message):
    user_states[message.from_user.id] = message.text
    await message.answer("🔹 Kodni kiriting:")

@dp.message()
async def check_code(message: types.Message):
    user_id = message.from_user.id
    text = message.text
    action = user_states.get(user_id)

    if action:
        if action in CARDS:
            if text == USER_CODE:
                name, number = CARDS[action]
                msg = await message.answer(f"{name}\nNusxa olish uchun bosing\n\t👇👇\n<code>{number}</code>\n\t👆👆", parse_mode="HTML")
                await asyncio.sleep(10)
                await bot.delete_message(message.chat.id, msg.message_id)
                await message.answer("XABAR O'CHIRILDI 🟥")
            else:
                await message.answer("❌ Noto‘g‘ri kod! Qaytadan urinib ko‘ring.", reply_markup=retry_button)
        elif action in NUMBERS:
            if text == USER_CODE:
                name = NUMBERS[action][0]
                msg = await message.answer(f"{name}")
                await asyncio.sleep(10)
                await bot.delete_message(message.chat.id, msg.message_id)
                await message.answer("XABAR O'CHIRILDI 🟥")
            else:
                await message.answer("❌ Noto‘g‘ri kod! Qaytadan urinib ko‘ring.", reply_markup=retry_button)
        else:
            await message.answer("❌ Ma'lumot topilmadi.")
    else:
        await message.answer("❌ Avval kartani yoki raqamni tanlang!")

@dp.callback_query(lambda call: call.data == "retry")
async def retry(call: types.CallbackQuery):
    user_id = call.from_user.id
    if user_id in user_states:
        await call.message.answer("🔹 Kodni qaytadan kiriting:")
    else:
        await call.message.answer("❌ Qayta urinish mumkin emas. Avval kartani yoki raqamni tanlang!")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
