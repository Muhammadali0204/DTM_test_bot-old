from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.belgi import belgi
from keyboards.inline import viloyatlar
from data.config import ADMINS
from keyboards.default import menu
from loader import dp, db_users, bot


@dp.message_handler(text="/menu", state="*")
async def menuu(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Menu : </b>", reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(CommandStart())
async def bot_start(msg: types.Message, state: FSMContext):
    user = db_users.select_user_by_id(msg.from_user.id)
    if user == None:
        db_users.add_user(msg.from_user.id, msg.from_user.full_name, None)
        for admin in ADMINS:
            try:
                await bot.send_message(
                    admin,
                    f"<b>➕Yangi foydalanuvchi qo'shildi, {msg.from_user.get_mention(msg.from_user.first_name)}</b>",
                )
            except:
                pass
        await msg.answer(
            f"<b>Assalomu alaykum {msg.from_user.get_mention(msg.from_user.full_name)}, botimizga xush kelibsiz !\n\nUshbu bot orqali testlarimizni ishlab, o'z bilimingizni sinab ko'rishingiz mumkin 😊</b>"
        )
        await msg.answer("<b><i>Ism-familiyangizni kiriting : </i></b>")
        await state.set_state("ism kiritadi")
    else:
        await msg.answer(f"<b><i>Menu : </i></b>", reply_markup=menu.menu)


@dp.message_handler(state="ism kiritadi")
async def ism_olish(msg: types.Message, state: FSMContext):
    if all(x.isalpha() or belgi(x) for x in msg.text):
        if len(msg.text) > 5 and len(msg.text) < 31:
            db_users.update_ism(msg.from_user.id, msg.text)
            await msg.answer(
                "<b>Qayerda istiqomat qilasiz : </b>",
                reply_markup=viloyatlar.viloyat_keyboard,
            )
            await state.set_state("viloyat")
        else:
            await msg.answer(
                "<b>Ism-familiya uzunligi 5 ta belgidan ko'p va 30 ta belgidan kam bo'lmasligi lozim !</b>\n\n<i>Qayta kiriting : </i>"
            )
    else:
        await msg.answer(
            "<b>Faqatgina lotin harflari, bo'sh joy va <code>' `</code> shu kabi belgilardan foydalanishingiz mumkin !</b>\n\n<i>Qayta kiriting : </i>"
        )


@dp.callback_query_handler(state="viloyat")
async def viloyat(call: types.CallbackQuery, state: FSMContext):
    viloyat = call.data
    db_users.update_vil(call.from_user.id, viloyat)
    await call.message.delete()
    await call.message.answer("🎊")
    await call.message.answer(
        "<b>Botimizga xush kelibsiz 😊\n\n<i>Menu : </i></b>", reply_markup=menu.menu
    )
    await state.finish()
