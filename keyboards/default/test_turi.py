from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


asosiy_fanlar = KeyboardButton(text="📕Asosiy fanlar")
majburiy_fanlar = KeyboardButton(text="📗Majburiy fanlar")
blok_test = KeyboardButton(text="📚Blok test (5 ta fan)")
ortga = KeyboardButton(text="◀️Ortga")

test_ishlash = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(
    asosiy_fanlar, majburiy_fanlar, blok_test, ortga
)
