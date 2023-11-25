from loader import db_users, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio, time
from keyboards.inline import fanlar_keyboard
from data.config import ADMINS
from keyboards.default import test_turi, ortga, admin_menu


from loader import dp, db_tests, temp


@dp.message_handler(text="Fan qo'shish", chat_id=ADMINS)
async def Add_test(msg: types.Message, state: FSMContext):
    await msg.answer("Test turini tanlang : ", reply_markup=test_turi.test_ishlash)
    await state.set_state("admin test turi1")


@dp.message_handler(text="📕Asosiy fanlar", state="admin test turi1", chat_id=ADMINS)
async def test(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Qo`shmoqchi bo`lgan fan nomini kiriting : (Asosiy fan uchun)",
        reply_markup=ortga.ortga,
    )
    await state.set_state("add fan1 asosiy")


@dp.message_handler(
    text="📚Blok test (5 ta fan)", state="admin test turi1", chat_id=ADMINS
)
async def test(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Qo`shmoqchi bo`lgan fan nomini kiriting : (Blok test uchun) ",
        reply_markup=ortga.ortga,
    )
    await state.set_state("add fan1 blok")


@dp.message_handler(state="add fan1 asosiy", chat_id=ADMINS)
async def add_asosiy_fan(msg: types.Message, state: FSMContext):
    try:
        db_tests.add_fan(msg.text, 1)
        await msg.answer(
            "<b>Muvaffaqiyatli qo'shildi ✅</b>", reply_markup=admin_menu.menu
        )
        await state.finish()
    except:
        await msg.answer("Bunday nomli fan mavjud ☹️", reply_markup=admin_menu.menu)
        await state.finish()


@dp.message_handler(state="add fan1 blok", chat_id=ADMINS)
async def add_asosiy_fan(msg: types.Message, state: FSMContext):
    try:
        db_tests.add_fan(msg.text, 3)
        await msg.answer(
            "<b>Muvaffaqiyatli qo'shildi ✅</b>", reply_markup=admin_menu.menu
        )
        await state.finish()
    except:
        await msg.answer("Bunday nomli fan mavjud ☹️", reply_markup=admin_menu.menu)
        await state.finish()
