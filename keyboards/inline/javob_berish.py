from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

javob_berish = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="❌Yo'q", callback_data="yo'q"),
            InlineKeyboardButton(text="✅Ha", callback_data="ha"),
        ]
    ]
)
