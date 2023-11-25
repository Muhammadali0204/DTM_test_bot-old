from aiogram import types
from keyboards.default import menu
from aiogram.dispatcher import FSMContext

from loader import dp


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def delete(msg: types.Message):
    await msg.delete()
    await msg.answer(
        "<b>Quyidagi tugmalardan foydalaning 👇</b>", reply_markup=menu.menu
    )


@dp.callback_query_handler(state="*")
async def deletee(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
