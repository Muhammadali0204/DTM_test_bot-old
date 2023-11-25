from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👨‍💻Test ishlash")],
        [KeyboardButton(text="🏁Javoblarni tekshirish")],
        [
            KeyboardButton(text="🛠Sozlamalar"),
            KeyboardButton(text="👥Do'stlarni taklif qilish"),
        ],
        [
            KeyboardButton(text="👤Mening natijam"),
            KeyboardButton(text="🧮Umumiy statistika"),
        ],
    ],
    resize_keyboard=True,
)
