from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.belgi import belgi
from keyboards.inline import viloyatlar
from keyboards.default import menu, sozlama, ortga
from loader import dp, db_users


@dp.message_handler(text="🛠Sozlamalar")
async def javob_berish(msg: types.Message, state: FSMContext):
    await msg.answer("<b>🛠Sozlamalar</b>", reply_markup=sozlama.sozlama)
    await state.set_state("sozlamalar")


@dp.message_handler(text="◀️Ortga", state="sozlamalar")
async def sozlama_back(msg: types.Message, state: FSMContext):
    await msg.answer("<b><i>Menu : </i></b>", reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(text="♻️Ismni tahrirlash", state="sozlamalar")
async def sozlama_back(msg: types.Message, state: FSMContext):
    await msg.answer(
        "<b>Yangi ism-familiyani yuboring : </b>", reply_markup=ortga.ortga
    )
    await state.set_state("ismini o'zgartirar emish")


@dp.message_handler(state="sozlamalar", content_types=types.ContentType.ANY)
async def jdei(msg: types.Message):
    await msg.delete()
    await msg.answer(
        "<b>Quyidagi tugmalardan foydalaning 👇</b>", reply_markup=sozlama.sozlama
    )


@dp.message_handler(text="◀️Ortga", state="ismini o'zgartirar emish")
async def djkfo(msg: types.Message, state: FSMContext):
    await msg.answer("<b>🛠Sozlamalar</b>", reply_markup=sozlama.sozlama)
    await state.set_state("sozlamalar")


@dp.message_handler(state="ismini o'zgartirar emish")
async def ismi(msg: types.Message, state: FSMContext):
    if all(x.isalpha() or belgi(x) for x in msg.text):
        if len(msg.text) > 5 and len(msg.text) < 31:
            db_users.update_ism(msg.from_user.id, msg.text)
            await msg.answer(
                "<b>Ismingiz muvaffaqiyatli o'zgartirildi ✅</b>", reply_markup=menu.menu
            )
            await state.finish()
        else:
            await msg.answer(
                "<b>Ism-familiya uzunligi 5 ta belgidan ko'p va 30 ta belgidan kam bo'lmasligi lozim !</b>\n\n<i>Qayta kiriting : </i>",
                reply_markup=ortga.ortga,
            )
    else:
        await msg.answer(
            "<b>Faqatgina lotin harflari, bo'sh joy va <code>' `</code> shu kabi belgilardan foydalanishingiz mumkin !</b>\n\n<i>Qayta kiriting : </i>",
            reply_markup=ortga.ortga,
        )
