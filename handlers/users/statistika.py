from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.belgi import belgi
from keyboards.inline import viloyatlar
from keyboards.default import test_turi, menu
from loader import dp, db_users, db_results, db_tests


@dp.message_handler(text="🧮Umumiy statistika")
async def javob_berish(msg: types.Message, state: FSMContext):
    users_count = db_users.count_users()[0]
    tests_count = db_tests.count_tests()[0]
    results_count = db_results.count_results()[0]

    answer = f"<b>👤Botning foydalanuvchilari soni : <i>{users_count}</i> ta</b>\n"
    answer += f"<b>📂Botda mavjud testlar soni : <i>{tests_count}</i> ta</b>\n"
    answer += f"<b>📝Foydalanuvchilar ishlagan testlar soni : <i>{results_count}</i> ta</b>\n\n"
    answer += f"<b>👨‍💻Admin : @javob_tekshir_admin_bot\n\n🤖Boshqa botlarimiz :\n1. <i>@javob_tekshir_bot</i>\n2. <i>@trend_music_bot</i></b>"

    await msg.answer(answer)


@dp.message_handler(text="👤Mening natijam")
async def my_result(msg: types.Message, state: FSMContext):
    await msg.answer(
        text=f"<b>Quyidagi bo'limlardan birini tanlang 👇</b>",
        reply_markup=test_turi.test_ishlash,
    )
    await state.set_state("mening natijam bo'lim")


@dp.message_handler(text="📕Asosiy fanlar", state="mening natijam bo'lim")
async def asosiy_fan(msg: types.Message, state: FSMContext):
    fanlar = db_tests.select_fanlar_by_turi(1)  # fan = [id, nom, tur]
    answer = "<b>📕Asosiy fanlardan natijalaringiz 👇\n\n</b>"
    for i in range(0, len(fanlar)):
        results = db_results.select_result_fan_id(msg.from_user.id, fanlar[i][0])
        umumiy_ball = 0
        if results != []:
            for j in range(0, len(results)):
                umumiy_ball += results[j][2]
            answer += f"<b>{i+1}. {fanlar[i][1]} - <i>{round(umumiy_ball * 100/ (len(results) * 93), 1)} %</i></b>\n"
        else:
            answer += f"<b>{i+1}. {fanlar[i][1]} - <i>0 %</i></b>\n"
    await msg.answer(answer, reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(text="📗Majburiy fanlar", state="mening natijam bo'lim")
async def asosiy_fan(msg: types.Message, state: FSMContext):
    answer = ""
    results = db_results.select_result_fan_id(msg.from_user.id, 0)
    umumiy_ball = 0
    if results != []:
        for j in range(0, len(results)):
            umumiy_ball += results[j][2]
        answer += f"<b>📕Majburiy fanlar - <i>{round(umumiy_ball * 100/ (len(results) * 33), 1)} %</i></b>\n"
    else:
        answer += f"<b>📕Majburiy fanlar - <i>0 %</i></b>\n"
    await msg.answer(answer, reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(text="📚Blok test (5 ta fan)", state="mening natijam bo'lim")
async def asosiy_fan(msg: types.Message, state: FSMContext):
    fanlar = db_tests.select_fanlar_by_turi(3)  # fan = [id, nom, tur]
    answer = "<b>📕Blok testlardan natijalaringiz 👇\n\n</b>"
    for i in range(0, len(fanlar)):
        results = db_results.select_result_fan_id(msg.from_user.id, fanlar[i][0])
        umumiy_ball = 0
        if results != []:
            for j in range(0, len(results)):
                umumiy_ball += results[j][2]
            answer += f"<b>{i+1}. {fanlar[i][1]} - <i>{round(umumiy_ball * 100/ (len(results) * 93), 1)} %</i></b>\n"
        else:
            answer += f"<b>{i+1}. {fanlar[i][1]} - <i>0 %</i></b>\n"
    await msg.answer(answer, reply_markup=menu.menu)
    await state.finish()
