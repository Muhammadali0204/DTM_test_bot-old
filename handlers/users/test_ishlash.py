from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.belgi import belgi
from keyboards.inline import fanlar_keyboard, testlar_keyboard, testni_boshlash
from keyboards.default import menu, test_turi
from loader import dp, db_users, db_tests, db_results, bot, db_temp
import datetime, pytz


@dp.message_handler(text="👨‍💻Test ishlash")
async def test(msg: types.Message, state: FSMContext):
    test_t = db_temp.select_temp(msg.from_user.id)
    if test_t != None:
        time_now = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
        test = db_tests.select_test(test_t[2])

        tugash_vaqti = test_t[1]
        soat_vaqt = tugash_vaqti.split(" ")
        vaqt = soat_vaqt[0].split(":")  # vaqt[0] = soat, vaqt[1] = minut
        sana = soat_vaqt[1].split(".")
        for i in range(0, 2):
            vaqt[i] = int(vaqt[i])
        for i in range(0, 3):
            sana[i] = int(sana[i])
        tugash_vaqti = datetime.datetime(
            sana[2],
            sana[1],
            sana[0],
            vaqt[0],
            vaqt[1],
            tzinfo=pytz.timezone("Etc/GMT-5"),
        )

        if time_now > tugash_vaqti:
            answer = f"<b>Siz avvalgi testni berilgan vaqt ichida javob yubormadingiz ❌\n<i>({test_t[1]} gacha javob yuborishingiz kerak edi)</i></b>"
            if test_t[4] == 1:
                answer += "<b>\n\nUshbu testdan olgan balingiz : 0️⃣</b>"
                db_results.add_result(msg.from_user.id, test[0], 0, test[2])
            db_temp.delete_temp(msg.from_user.id)
            await msg.answer(answer)
            await msg.answer(
                "<b>Qanday turdagi test ishlamoqchisiz ❓</b>",
                reply_markup=test_turi.test_ishlash,
            )
            await state.set_state("test turi")
        elif time_now <= tugash_vaqti:
            fan = db_tests.select_fan(test_t[3])
            if test[2] != 0:
                javob = f"<b>Siz hozirda {fan[1]} fanidan test ishlamoqdasiz ❗️\nAvval testni yakunlang, so`ngra boshqa testlarni ishlashingiz mumkin bo'ladi ✅\n⏱Amaldagi test uchun berilgan vaqt {test_t[1]} gacha</b>"
            else:
                javob = f"<b>Siz hozirda majburiy fanlardan test ishlamoqdasiz ❗️\nAvval  testni yakunlang, so`ngra boshqa testlarni ishlashingiz mumkin bo'ladi ✅\n⏱Amaldagi test uchun berilgan vaqt {test_t[1]} gacha</b>"
            await msg.answer(javob, reply_markup=menu.menu)
    else:
        await msg.answer(
            "<b>Qanday turdagi test ishlamoqchisiz ❓</b>",
            reply_markup=test_turi.test_ishlash,
        )
        await state.set_state("test turi")


@dp.message_handler(text="◀️Ortga", state=["test turi", "mening natijam bo'lim"])
async def salom(msg: types.Message, state: FSMContext):
    await msg.answer("<b><i>Menu : </i></b>", reply_markup=menu.menu)
    await state.finish()


@dp.message_handler(text="📕Asosiy fanlar", state="test turi")
async def test(msg: types.Message, state: FSMContext):
    data = db_tests.select_fanlar_by_turi(1)
    await msg.answer("<b>📕Asosiy fanlar</b>", reply_markup=types.ReplyKeyboardRemove())
    await msg.answer(
        "<b>Quyidagi fanlardan birini tanlang 👇🏻</b>",
        reply_markup=fanlar_keyboard.fanlar(data),
    )
    await state.set_state("111")


@dp.message_handler(text="📚Blok test (5 ta fan)", state="test turi")
async def test(msg: types.Message, state: FSMContext):
    data = db_tests.select_fanlar_by_turi(3)
    await msg.answer(
        "<b>📚Blok test (5 ta fan)</b>", reply_markup=types.ReplyKeyboardRemove()
    )
    await msg.answer(
        "<b>Quyidagi yo'nalishlardan birini tanlang 👇🏻</b>",
        reply_markup=fanlar_keyboard.fanlar(data),
    )
    await state.set_state("333")


@dp.callback_query_handler(state=["111", "333"], text="ortga")
async def ortga(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "<b>Qanday turdagi test ishlamoqchisiz ❓</b>",
        reply_markup=test_turi.test_ishlash,
    )
    await state.set_state("test turi")


# Test ro'yxatini yuborish


@dp.callback_query_handler(state="111")
async def test(call: types.CallbackQuery, state: FSMContext):
    data = db_tests.select_test_by_fan(call.data)
    if data != []:
        await call.message.delete()
        listt = []
        for i in data:
            salom = db_results.select_result(user_id=call.from_user.id, test_id=i[0])
            if salom == None:
                listt.append(0)
            else:
                listt.append(1)

        await call.message.answer(
            "<b>📕Asosiy fanlar\n\nYechmoqchi bo`lgan testingizni tanlang👇</b>",
            reply_markup=testlar_keyboard.testlar(data, listt),
        )
        await state.set_state("1 dan test tanlash")
    else:
        await call.answer(
            "Hozirda ushbu fan bo'yicha testlar mavjud emas ❌", show_alert=True
        )


@dp.callback_query_handler(state="333")
async def test(call: types.CallbackQuery, state: FSMContext):
    data = db_tests.select_test_by_fan(call.data)
    if data != []:
        await call.message.delete()
        listt = []
        for i in data:
            salom = db_results.select_result(user_id=call.from_user.id, test_id=i[0])
            if salom == None:
                listt.append(0)
            else:
                listt.append(1)

        await call.message.answer(
            "<b>📚Blok test (5 ta fan)\n\nYechmoqchi bo`lgan testingizni tanlang👇</b>",
            reply_markup=testlar_keyboard.testlar(data, listt),
        )
        await state.set_state("3 dan test tanlash")
    else:
        await call.answer(
            "Hozirda ushbu fan bo'yicha testlar mavjud emas ❌", show_alert=True
        )


@dp.message_handler(text="📗Majburiy fanlar", state="test turi")
async def test(msg: types.Message, state: FSMContext):
    data = db_tests.select_test_by_fan(0)
    if data != []:
        await msg.answer(
            "<b>📗Majburiy fanlar</b>", reply_markup=types.ReplyKeyboardRemove()
        )
        listt = []
        for i in data:
            salom = db_results.select_result(user_id=msg.from_user.id, test_id=i[0])
            if salom == None:
                listt.append(0)
            else:
                listt.append(1)

        await msg.answer(
            "<b>Yechmoqchi bo`lgan testingizni tanlang👇</b>",
            reply_markup=testlar_keyboard.testlar(data, listt),
        )
        await state.set_state("2 dan test tanlash")
    else:
        await msg.answer(
            "<b>Hozirda majburiy fanlar bo'yicha testlar mavjud emas ❌</b>"
        )


@dp.message_handler(
    state=["test turi", "mening natijam bo'lim"], content_types=types.ContentTypes.ANY
)
async def quyidagi_tugmaa(msg: types.Message):
    await msg.delete()
    await msg.answer(
        "<b>Quyidagi tugmalardan foydalaning 👇</b>", reply_markup=test_turi.test_ishlash
    )


# Test yuborish


@dp.callback_query_handler(
    state=["1 dan test tanlash", "2 dan test tanlash", "3 dan test tanlash"],
    text="ortga",
)
async def jhjrfg(call: types.CallbackQuery, state: FSMContext):
    son = await state.get_state()
    son = son[0]
    if son == "1":
        await call.message.delete()
        data = db_tests.select_fanlar_by_turi(1)
        await call.message.answer(
            "<b>Quyidagi fanlardan birini tanlang 👇🏻</b>",
            reply_markup=fanlar_keyboard.fanlar(data),
        )
        await state.set_state("111")
    elif son == "2":
        await call.message.delete()
        await call.message.answer(
            "<b>Qanday turdagi test ishlamoqchisiz ❓</b>",
            reply_markup=test_turi.test_ishlash,
        )
        await state.set_state("test turi")
    elif son == "3":
        await call.message.delete()
        data = db_tests.select_fanlar_by_turi(3)
        await call.message.answer(
            "<b>Quyidagi yo'nalishlardan birini tanlang 👇🏻</b>",
            reply_markup=fanlar_keyboard.fanlar(data),
        )
        await state.set_state("333")


@dp.callback_query_handler(
    state=["1 dan test tanlash", "2 dan test tanlash", "3 dan test tanlash"]
)
async def test_yuborish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    test_id = call.data
    test = db_tests.select_test(test_id)
    son = await state.get_state()
    son = son[0]
    answer = ""
    fan = db_tests.select_fan(test[2])
    result = db_results.select_result(call.from_user.id, test[0])
    foiz = 0
    if son == "1":
        answer += f"<b>📕Test turi : <i>Asosiy</i></b>\n"
        answer += f"<b>📗Fan nomi : <i>{fan[1]}</i></b>\n"
        answer += f"<b>🔢Savollar soni : <i>{len(test[3])}</i></b>\n\n"
        if result != None:
            foiz = result[2] / 93 * 100
    elif son == "2":
        answer += f"<b>📚Test turi : <i>Majburiy</i></b>\n"
        answer += f"<b>📗Fanlar : <i>Matematika, Ona tili, O'zb.Tarix</i></b>\n"
        answer += f"<b>🔢Savollar soni : <i>{len(test[3])}</i></b>\n\n"
        if result != None:
            foiz = result[2] / 33 * 100
    elif son == "3":
        answer += f"<b>📚Test turi : <i>Blok</i></b>\n"
        answer += f"<b>📗Yo'nalish : <i>{fan[1]}</i></b>\n"
        answer += f"<b>🔢Savollar soni : <i>{len(test[3])}</i></b>\n\n"
        if result != None:
            foiz = result[2] / 189 * 100

    answer = f"<b>{test[4]}</b>\n\n"

    if result != None:
        answer += f"<b>Ushbu testni ishlagansiz ❗️\nNatijangiz : <i>{result[2]} ball ({round(foiz, 1)}%)</i></b>\n\n"

    answer += f"<b>Ushbu testni boshlash uchun <code>🟢Testni boshlash</code> tugmasini bosing❗️</b>"

    await call.message.answer(
        answer, reply_markup=testni_boshlash.boshlash(test[0], son)
    )
    await state.set_state("testni yuborish")


@dp.callback_query_handler(text="ortga", state="testni yuborish")
async def hjdeiujgf(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "<b>Qanday turdagi test ishlamoqchisiz ❓</b>",
        reply_markup=test_turi.test_ishlash,
    )
    await state.set_state("test turi")


@dp.callback_query_handler(regexp="testni boshlash:+", state="testni yuborish")
async def testni_yubor(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = call.data.split(":")
    son = data[2]
    test_id = data[1]
    test = db_tests.select_test(test_id)
    if son == "1":
        caption = (
            f"<b>⏱Test yechish uchun berilgan vaqt : <i>1 soat 30 daqiqa</i></b>\n\n"
        )
        t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
        vaqt0 = t.strftime("%H:%M %d.%m.%Y")
        t = t + datetime.timedelta(seconds=5400)
        vaqt = t.strftime("%H:%M %d.%m.%Y")
        caption += f"<b>🕑Test boshlanish vaqti : <i>{vaqt0}</i></b>\n"
        caption += f"<b>🕓Test tugash vaqti : <i>{vaqt}</i></b>\n\n"
        result = db_results.select_result(call.from_user.id, test_id)
        if result == None:
            db_temp.add_temp(call.from_user.id, vaqt, test_id, test[2], 1)
            caption += f"<b><i>❗️Test javoblarini shu vaqt oralig'ida yubormasangiz, testdan olgan ballingiz 0 ball deb baholanadi</i></b>"
        else:
            db_temp.add_temp(call.from_user.id, vaqt, test_id, test[2], 2)
            caption += f"<b><i>❕Siz ushbu testni avval ishlagansiz va {result[2]} ball to'plagansiz</i></b>"
        await call.message.answer_document(
            test[1], caption=caption, reply_markup=menu.menu
        )
        await state.finish()

    elif son == "2":
        caption = f"<b>⏱Test yechish uchun berilgan vaqt : <i>1 soat.</i></b>\n\n"
        t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
        vaqt0 = t.strftime("%H:%M %d.%m.%Y")
        t = t + datetime.timedelta(seconds=3600)
        vaqt = t.strftime("%H:%M %d.%m.%Y")
        caption += f"<b>🕑Test boshlanish vaqti : <i>{vaqt0}</i></b>\n"
        caption += f"<b>🕓Test tugash vaqti : <i>{vaqt}</i></b>\n\n"
        result = db_results.select_result(call.from_user.id, test_id)
        if result == None:
            db_temp.add_temp(call.from_user.id, vaqt, test_id, 0, 1)
            caption += f"<b><i>❗️Test javoblarini shu vaqt oralig'ida yubormasangiz, testdan olgan ballingiz 0 ball deb baholanadi</i></b>"
        else:
            db_temp.add_temp(call.from_user.id, vaqt, test_id, 0, 2)
            caption += f"<b><i>❕Siz ushbu testni avval ishlagansiz va {result[2]} ball to'plagansiz</i></b>"
        await call.message.answer_document(
            test[1], caption=caption, reply_markup=menu.menu
        )
        await state.finish()

    elif son == "3":
        caption = (
            f"<b>⏱Test yechish uchun berilgan vaqt : <i>3 soat 30 daqiqa</i></b>\n\n"
        )
        t = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
        vaqt0 = t.strftime("%H:%M %d.%m.%Y")
        t = t + datetime.timedelta(seconds=12600)
        vaqt = t.strftime("%H:%M %d.%m.%Y")
        caption += f"<b>🕑Test boshlanish vaqti : <i>{vaqt0}</i></b>\n"
        caption += f"<b>🕓Test tugash vaqti : <i>{vaqt}</i></b>\n\n"
        result = db_results.select_result(call.from_user.id, test_id)
        if result == None:
            db_temp.add_temp(call.from_user.id, vaqt, test_id, test[2], 1)
            caption += f"<b><i>❗️Test javoblarini shu vaqt oralig'ida yubormasangiz, testdan olgan ballingiz 0 ball deb baholanadi</i></b>"
        else:
            db_temp.add_temp(call.from_user.id, vaqt, test_id, test[2], 2)
            caption += f"<b><i>❕Siz ushbu testni avval ishlagansiz va {result[2]} ball to'plagansiz</i></b>"
        await call.message.answer_document(
            test[1], caption=caption, reply_markup=menu.menu
        )
        await state.finish()
