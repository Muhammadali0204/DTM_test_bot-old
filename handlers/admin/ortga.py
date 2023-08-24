from loader import db_users, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import ortga, menu, admin_menu
import asyncio, time
from data.config import ADMINS
from keyboards.inline.forward_copy import inline_key



@dp.message_handler(text="◀️Ortga", state=["add fan1 blok","add fan1 asosiy","admin test turi1","reklama_turi", "forward", "copy", "admin test turi", "add test asosiy fayl", "add test blok fayl", "add test majburiy fayl", "add test asosiy javob", "add test blok javob", "add test majburiy javob", "javoblarni yuborishi kerak"], chat_id = ADMINS)
async def hsihdv(msg : types.Message, state : FSMContext):
    await msg.answer("<b><i>Menu : </i></b>", reply_markup=admin_menu.menu)
    await state.finish()
    
@dp.callback_query_handler(text="ortga", state=["add fan blok", "add fan asosiy"], chat_id = ADMINS)
async def hsihdv(call : types.CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.message.answer("<b><i>Menu : </i></b>", reply_markup=admin_menu.menu)
    await state.finish()