from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

tasdiqlash = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔴Qayta kiritish", callback_data="qayta")],
        [InlineKeyboardButton(text="♻️O'zgartirish", callback_data="o'zgartirish")],
        [InlineKeyboardButton(text="✅Tasdiqlash", callback_data="tasdiqlash")],
        [InlineKeyboardButton(text="◀️Ortga", callback_data="ortga")],
    ]
)
