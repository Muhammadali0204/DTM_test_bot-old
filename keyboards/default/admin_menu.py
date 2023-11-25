from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Reklama")],
        [KeyboardButton("Fan qo'shish"), KeyboardButton(text="Test qo'shish")],
    ],
    resize_keyboard=True,
)
