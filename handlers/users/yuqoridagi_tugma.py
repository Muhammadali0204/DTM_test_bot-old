from aiogram import types
from loader import dp, bot
import asyncio


@dp.message_handler(
    state=[
        "testni yuborish",
        "viloyat",
        "111",
        "333",
        "1 dan test tanlash",
        "2 dan test tanlash",
        "3 dan test tanlash",
        "javob berishni tasdiqlash",
    ],
    content_types=types.ContentTypes.ANY,
)
async def funcc(msg: types.Message):
    await msg.delete()
    await msg.answer("<b>Yuqoridagi tugmalardan foydalaning 👆</b>")
    await asyncio.sleep(3)
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id + 1)
    except:
        pass
