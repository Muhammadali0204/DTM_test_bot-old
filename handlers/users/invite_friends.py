from aiogram import types
from keyboards.inline import dustlar


from loader import dp


@dp.message_handler(text="👥Do'stlarni taklif qilish")
async def dustlar1(msg : types.Message):
    answer = f"<b>Quyidagi tugmani bosing va do'stlaringizni tanlang 😊</b>"
    await msg.answer(answer, reply_markup=dustlar.dustlar)
