from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_key = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Forward", callback_data="for"),
            InlineKeyboardButton(text="Copy", callback_data="copy"),
        ]
    ]
)
