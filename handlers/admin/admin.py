from loader import db_users, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
import asyncio, time
from keyboards.default import admin_menu
from data.config import ADMINS
from keyboards.inline.forward_copy import inline_key

from loader import dp


@dp.message_handler(text=["admin", "Admin"], chat_id=ADMINS)
async def admin(msg: types.Message):
    await msg.answer("Admin panel : ", reply_markup=admin_menu.menu)
