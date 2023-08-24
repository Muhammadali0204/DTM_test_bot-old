from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

andi = InlineKeyboardButton(text='Andijon', callback_data='Andijon')
bux = InlineKeyboardButton(text='Buxoro', callback_data='Buxoro')
far = InlineKeyboardButton(text='Farg`ona', callback_data="Farg'ona")
jiz = InlineKeyboardButton(text='Jizzax', callback_data='Jizzax')
nam = InlineKeyboardButton(text='Namangan', callback_data='Namangan')
nav = InlineKeyboardButton(text='Navoiy', callback_data='Navoiy')
nuk = InlineKeyboardButton(text="Qoraqolpog'iston", callback_data="Qoraqolpog'iston")
qash = InlineKeyboardButton(text='Qashqadaryo', callback_data='Qashqadaryo')
sam = InlineKeyboardButton(text='Samarqand', callback_data='Samarqand')
sir = InlineKeyboardButton(text='Sirdaryo', callback_data='Sirdaryo')
sur = InlineKeyboardButton(text='Surxondaryo', callback_data='Surxondaryo')
xor = InlineKeyboardButton(text='Xorazm', callback_data='Xorazm')
tosh_sh = InlineKeyboardButton(text='Toshknet shahri', callback_data='Toshkent shahri')
tosh_v = InlineKeyboardButton(text='Toshkent viloyati', callback_data='Toshkent viloyati')


viloyat_keyboard = InlineKeyboardMarkup(row_width=2).add(andi,bux,far,jiz,nam,qash,nuk,sam,sir,sur,xor,nav,tosh_sh,tosh_v)