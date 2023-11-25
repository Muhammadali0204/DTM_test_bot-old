from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

variantlar = ["a", "b", "c", "d"]


def abcd_variant(var):
    variant = InlineKeyboardMarkup(row_width=3)
    for i in range(0, 4):
        if variantlar[i] != var:
            variant.insert(
                InlineKeyboardButton(
                    text=f"{variantlar[i].upper()}", callback_data=variantlar[i]
                )
            )
    variant.insert(InlineKeyboardButton(text="◀️Ortga", callback_data="ortga"))

    return variant
