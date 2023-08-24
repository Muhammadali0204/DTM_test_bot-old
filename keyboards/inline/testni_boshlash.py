from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def boshlash(test_id, tur):
    boshlash1 = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢Testni boshlash", callback_data=f"testni boshlash:{test_id}:{tur}")
            ],
            [
                InlineKeyboardButton(text='◀️Ortga', callback_data='ortga')
            ]
        ]
    )
    
    return boshlash1