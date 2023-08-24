from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def fanlar(fanlar):
    subjects = InlineKeyboardMarkup(
        row_width = 2
    )
    for fan in fanlar:
        subjects.insert(InlineKeyboardButton(text=f'{fan[1]}', callback_data=fan[0]))
    subjects.insert(InlineKeyboardButton(text='◀️Ortga', callback_data='ortga'))
    
    return subjects