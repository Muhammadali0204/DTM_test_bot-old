from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def testlar(testlar, listt):
    dbhtgnj = InlineKeyboardMarkup(
        row_width=3,
    )
    for i in range(0,len(testlar)):
        if listt[i] == 0:
            dbhtgnj.insert(InlineKeyboardButton(text=f"{i+1}-test", callback_data=testlar[i][0]))
        else:
            dbhtgnj.insert(InlineKeyboardButton(text=f"{i+1}-test ✔️", callback_data=testlar[i][0]))
            
    dbhtgnj.insert(InlineKeyboardButton(text='◀️Ortga', callback_data='ortga'))
    
    return dbhtgnj



