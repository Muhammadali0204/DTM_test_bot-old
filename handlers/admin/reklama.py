from loader import db_users, dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.default import ortga, menu, admin_menu
import asyncio, time
from data.config import ADMINS
from keyboards.inline.forward_copy import inline_key



@dp.message_handler(text="Reklama", chat_id = ADMINS)
async def sendmessage(msg : types.Message, state : FSMContext):
    await msg.answer(text="<b>Reklama yuborish : </b>\n<i>(Istalgan xabar)</i>", reply_markup=ortga.ortga)
    await msg.answer("<b>Forward yoki copy ? </b>", reply_markup=inline_key)
    await state.set_state("reklama_turi")
    
@dp.callback_query_handler(text="for", state="reklama_turi")
async def func(call : types.CallbackQuery, state : FSMContext):
    await call.message.answer("<b>Xabarni yuboring : <i>(Forward)</i></b>", reply_markup=ortga.ortga)
    await state.set_state("forward")
    await call.message.delete()
    
@dp.callback_query_handler(text="copy", state="reklama_turi")
async def func(call : types.CallbackQuery, state : FSMContext):
    await call.message.answer("<b>Xabarni yuboring : <i>(Copy)</i></b>", reply_markup=ortga.ortga)
    await state.set_state("copy")
    await call.message.delete()
    
@dp.message_handler(state="forward", content_types=types.ContentType.ANY)
async def func(msg : types.Message, state : FSMContext):
    users = db_users.select_all_users()
    n = 0
    for i in range(0, len(users)):
        try:
            await bot.forward_message(users[i][0], msg.from_user.id, msg.message_id)
            n+=1
            await asyncio.sleep(0.05)
        except:
            pass
        
    await msg.answer(f"<b>{n} ta foydalanuvchiga xabar yuborildi ✅</b>\n<b>{len(users) - n} taga yuborilmadi ❌</b>", reply_markup=admin_menu.menu)
    await state.finish()
    
@dp.message_handler(state="copy", content_types=types.ContentType.ANY)
async def func(msg : types.Message, state : FSMContext):
    users = db_users.select_all_users()
    n = 0
    for i in range(0, len(users)):
        try:
            await bot.copy_message(users[i][0], msg.from_user.id, msg.message_id)
            n+=1
            await asyncio.sleep(0.05)
        except:
            pass
        
    await msg.answer(f"<b>{n} ta foydalanuvchiga xabar yuborildi ✅</b>\n<b>{len(users) - n} taga yuborilmadi ❌</b>", reply_markup=admin_menu.menu)
    await state.finish()