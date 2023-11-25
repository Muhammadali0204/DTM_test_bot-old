from loader import db_users, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio, time
from keyboards.inline import fanlar_keyboard
from data.config import ADMINS
from keyboards.default import test_turi, ortga, admin_menu


from loader import dp, db_tests, temp


@dp.message_handler(text="Test qo'shish", chat_id=ADMINS)
async def Add_test(msg: types.Message, state: FSMContext):
    await msg.answer("Test turini tanlang : ", reply_markup=test_turi.test_ishlash)
    await state.set_state("admin test turi")


@dp.message_handler(text="📕Asosiy fanlar", state="admin test turi")
async def test(msg: types.Message, state: FSMContext):
    data = db_tests.select_fanlar_by_turi(1)
    await msg.answer(
        "Qaysi fan uchun qo'shmoqchisiz : ", reply_markup=fanlar_keyboard.fanlar(data)
    )
    await state.set_state("add fan asosiy")


@dp.message_handler(text="📚Blok test (5 ta fan)", state="admin test turi")
async def test(msg: types.Message, state: FSMContext):
    data = db_tests.select_fanlar_by_turi(3)
    await msg.answer(
        "Qaysi fan uchun qo'shmoqchisiz : ", reply_markup=fanlar_keyboard.fanlar(data)
    )
    await state.set_state("add fan blok")


@dp.message_handler(text="📗Majburiy fanlar", state="admin test turi")
async def test(msg: types.Message, state: FSMContext):
    await msg.answer(
        "Test faylini va javoblarni caption da yuboring : ", reply_markup=ortga.ortga
    )
    await state.set_state("add test majburiy fayl")


@dp.callback_query_handler(state="add fan asosiy")
async def jhsijfh(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    temp[f"{call.from_user.id} add test asosiy fan_id"] = call.data
    await call.message.answer(
        "Test faylini va javoblarini caption da yuboring : ", reply_markup=ortga.ortga
    )
    await state.set_state("add test asosiy fayl")


@dp.callback_query_handler(state="add fan blok")
async def jhsijfh(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    temp[f"{call.from_user.id} add test blok fan_id"] = call.data
    await call.message.answer(
        "Test faylini va javoblarini caption da yuboring : ", reply_markup=ortga.ortga
    )
    await state.set_state("add test blok fayl")


@dp.message_handler(
    state="add test asosiy fayl", content_types=types.ContentTypes.DOCUMENT
)
async def kjnheikvnb(msg: types.Message, state: FSMContext):
    temp[f"{msg.from_user.id} asosiy file_id"] = msg.document.file_id
    temp[f"{msg.from_user.id} asosiy javoblar"] = msg.caption.lower()
    await msg.answer("Endi bu testning ta`rifini yuboring : ", reply_markup=ortga.ortga)
    await state.set_state("add test asosiy javob")


@dp.message_handler(
    state="add test blok fayl", content_types=types.ContentTypes.DOCUMENT
)
async def kjnheikvnb(msg: types.Message, state: FSMContext):
    temp[f"{msg.from_user.id} blok file_id"] = msg.document.file_id
    temp[f"{msg.from_user.id} blok javoblar"] = msg.caption.lower()
    await msg.answer("Endi bu testning ta`rifini yuboring : ", reply_markup=ortga.ortga)
    await state.set_state("add test blok javob")


@dp.message_handler(
    state="add test majburiy fayl", content_types=types.ContentTypes.DOCUMENT
)
async def kjnheikvnb(msg: types.Message, state: FSMContext):
    temp[f"{msg.from_user.id} majburiy file_id"] = msg.document.file_id
    temp[f"{msg.from_user.id} majburiy javoblar"] = msg.caption.lower()
    await msg.answer("Endi bu testning ta`rifini yuboring : ", reply_markup=ortga.ortga)
    await state.set_state("add test majburiy javob")


@dp.message_handler(state="add test asosiy javob")
async def ihevif(msg: types.Message, state: FSMContext):
    db_tests.add_test(
        temp[f"{msg.from_user.id} asosiy file_id"],
        temp[f"{msg.from_user.id} add test asosiy fan_id"],
        temp[f"{msg.from_user.id} asosiy javoblar"],
        msg.html_text,
    )
    temp[f"{msg.from_user.id} asosiy file_id"] = None
    temp[f"{msg.from_user.id} add test asosiy fan_id"] = None
    temp[f"{msg.from_user.id} asosiy javoblar"] = None
    await msg.answer("Qo'shildi ✅", reply_markup=admin_menu.menu)
    await state.finish()


@dp.message_handler(state="add test blok javob")
async def ihevif(msg: types.Message, state: FSMContext):
    db_tests.add_test(
        temp[f"{msg.from_user.id} blok file_id"],
        temp[f"{msg.from_user.id} add test blok fan_id"],
        temp[f"{msg.from_user.id} blok javoblar"],
        msg.html_text,
    )
    temp[f"{msg.from_user.id} blok file_id"] = None
    temp[f"{msg.from_user.id} add test blok fan_id"] = None
    temp[f"{msg.from_user.id} blok javoblar"] = None
    await msg.answer("Qo'shildi ✅", reply_markup=admin_menu.menu)
    await state.finish()


@dp.message_handler(state="add test majburiy javob")
async def ihevif(msg: types.Message, state: FSMContext):
    db_tests.add_test(
        temp["majburiy file_id"],
        0,
        temp[f"{msg.from_user.id} majburiy javoblar"],
        msg.html_text,
    )
    temp[f"{msg.from_user.id} majburiy file_id"] = None
    temp[f"{msg.from_user.id} majburiy javoblar"] = None
    await msg.answer("Qo'shildi ✅", reply_markup=admin_menu.menu)
    await state.finish()
