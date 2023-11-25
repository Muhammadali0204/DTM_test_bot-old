from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.belgi import belgi
from keyboards.inline import viloyatlar, javob_berish, tasdiqlash, abcd_variant
from keyboards.default import menu, ortga
from utils.misc import abcd
from utils import raqam
from loader import dp, db_users, test_time, db_tests, db_results, temp, bot, db_temp
import datetime, pytz


# test_time[user_id] = [datetime, test_id, fan_id, status]


@dp.message_handler(text="🏁Javoblarni tekshirish")
async def javob_berish1(msg: types.Message, state: FSMContext):
    try:
        # test_t = (id, datetime, test_id, fan_id, status)
        # datetime = "00:00 01.01.2000"
        test_t = db_temp.select_temp(msg.from_user.id)
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

        test_time[msg.from_user.id] = [tugash_vaqti, test_t[2], test_t[3], test_t[4]]

        data = test_time[msg.from_user.id]
        if data != None:
            time_now = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
            last_time = test_t[1]
            if time_now > data[0]:
                answer = f"<b>Siz berilgan vaqt ichida javob yubormadingiz.\n<i>({last_time} gacha javob yuborishingiz kerak edi)</i>\n\nUshbu testdan olgan balingiz : 0</b>"
                if data[3] == 1:
                    db_results.add_result(msg.from_user.id, data[1], 0, data[2])
                await msg.answer(answer, reply_markup=menu.menu)
            else:
                answer = f"<b>Test javoblarini <code>{last_time}</code> gacha yuborishingiz mumkin ❗️\n\nJavoblarni haqiqatdan ham yubormoqchimisiz ❓</b>"
                await msg.answer(answer, reply_markup=javob_berish.javob_berish)
                await state.set_state("javob berishni tasdiqlash")
        elif data == None:
            await msg.answer("<b>Sizda faol test mavjud emas ❗️</b>")
    except:
        await msg.answer("<b>Sizda faol test mavjud emas ❗️</b>")


@dp.callback_query_handler(text="ha", state="javob berishni tasdiqlash")
async def javob_olish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = test_time[call.from_user.id]
    test = db_tests.select_test(data[1])
    answer = f"<b>Yaxshi, savollar soni <i>{len(test[3])}</i> ta ✅\n\nJavoblarni quyidagi ko'rinishda yuboring : \n\nabcdabcd... ({len(test[3])} ta)\n\n(Katta harflar bo'lishi ham mumkin)\n\n<i>Misol uchun : \n1 - savolning javobi a\n2 - savolning javobi b\n3 - savolning javobi c bo'lsin.\nYuborishingiz kerak bo'lgan javob : <code>abc</code> ko'rinishida bo'ladi ❗️</i></b>"
    await call.message.answer(answer, reply_markup=ortga.ortga)
    await state.set_state("javoblarni yuborishi kerak user")


@dp.callback_query_handler(text="yo'q", state="javob berishni tasdiqlash")
async def javob_olish_yuq(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    time_now = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
    if time_now < test_time[call.from_user.id][0]:
        time_delta = test_time[call.from_user.id][0] - time_now
        seconds = time_delta.seconds
        soat = 0
        minut = 0
        answer = ""

        if seconds > 3599:
            soat = seconds // 3600
            seconds = seconds - soat * 3600
        if seconds > 59:
            minut = seconds // 60
            seconds = seconds - minut * 60

        if soat != 0:
            answer += f"<b>Yaxshi, sizda yana {soat} soat, </b>"
            if minut != 0:
                answer += f"<b>{minut+1} daqiqa </b>"
            answer += f"<b>vaqtingiz bor 🕑\n\nBemalol barcha testlarni bajarib, javob yuborishingiz mumkin 😊</b>"
        elif minut != 0:
            answer += f"<b>Yaxshi, sizda yana {minut+1} daqiqa </b>"
            answer += f"<b>vaqtingiz bor 🕑\n\nBarcha testlarni bajarib, tezroq javob yuborishni maslahat beramiz 😉</b>"
        else:
            answer += "<b>Menu : </b>"

        await call.message.answer(answer, reply_markup=menu.menu)
        await state.finish()

    else:
        answer += "<b>Menu : </b>"
        await call.message.answer(answer, reply_markup=menu.menu)
        await state.finish()


@dp.message_handler(text="◀️Ortga", state="javoblarni yuborishi kerak user")
async def ortga1(msg: types.Message, state: FSMContext):
    await state.finish()
    await msg.answer("<b>Menu : </b>", reply_markup=menu.menu)


@dp.callback_query_handler(text="ortga", state="javoblarni tasdiqlash")
async def ortga1(call: types.CallbackQuery, state: FSMContext):
    temp[call.from_user.id] = None
    try:
        temp[f"{call.from_user.id}:raqam"] = None
    except:
        pass
    await call.message.delete()
    await state.finish()
    await call.message.answer("<b>Menu : </b>", reply_markup=menu.menu)


# test_time[user_id] = [datetime, test_id, fan_id, status]
@dp.message_handler(state="javoblarni yuborishi kerak user")
async def lkblk(msg: types.Message, state: FSMContext):
    if all(abcd.abcd(x) for x in msg.text):
        data = test_time[msg.from_user.id]
        test = db_tests.select_test(data[1])
        if len(test[3]) == len(msg.text):
            temp[msg.from_user.id] = [msg.text.lower(), msg.message_id + 1]
            answer = "<b>Diqqat ❗️\n\nJavoblaringiz to'g'ri ekanligiga ishonch hosil qiling ❗️\n\n\n</b>"
            javob = msg.text.lower()
            for i in range(1, len(javob) + 1):
                answer += f"<i>{i}  --  {javob[i-1]}</i>\n"
            answer += "\n\n<b><i>Agar javoblarni qayta kiritmoqchi bo'lsangiz <code>🔴Qayta kiritish</code> tugmasini bosing\nBiror savolning javobini o'zgartirmoqchi bo'lsangiz <code>♻️O'zgartirish</code> tugmasini bosing\nJavoblaringiz to'g'riligiga ishonch hosil qilganingizdan so'ng <code>✅Tasdiqlash</code> tugmasini bosing</i></b>"
            await msg.answer(answer, reply_markup=tasdiqlash.tasdiqlash)
            await state.set_state("javoblarni tasdiqlash")
        else:
            await msg.answer(
                f"<b>Xatolik ❗️\n\nJavoblar soni {len(test[3])} ta bo'lishi kerak edi, ammo siz {len(msg.text)} ta javob yubordingiz❗️\n\nJavoblarni qayta yuboring : </b>",
                reply_markup=ortga.ortga,
            )
    else:
        await msg.answer(
            "<b>Xatolik ❗️\n\nJavoblar faqat a,b,c,d harflaridan iborat bo'lsin ❗️\n\nJavoblarni qayta yuboring : </b>",
            reply_markup=ortga.ortga,
        )


@dp.callback_query_handler(text="qayta", state="javoblarni tasdiqlash")
async def qayta_kiritish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(
        "<b>Yaxshi, javobingizni qayta yuboring : </b>", reply_markup=ortga.ortga
    )
    await state.set_state("javoblarni yuborishi kerak user")


@dp.callback_query_handler(text="o'zgartirish", state="javoblarni tasdiqlash")
async def ozgartirish(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer(
        "<b>Nechanchi savolga bergan javobingizni almashtirmoqchisiz ❓</b>"
    )
    await state.set_state("savolning raqami")


@dp.message_handler(text="◀️Ortga", state="savolning raqami")
async def ortga1(msg: types.Message, state: FSMContext):
    text = temp[msg.from_user.id][0]
    answer = "<b>Diqqat ❗️\n\nJavoblaringiz to'g'ri ekanligiga ishonch hosil qiling ❗️\n\n\n</b>"
    for i in range(1, len(text) + 1):
        answer += f"<i>{i}  --  {text[i-1]}</i>\n"
    answer += "\n\n<b><i>Agar javoblarni qayta kiritmoqchi bo'lsangiz <code>🔴Qayta kiritish</code> tugmasini bosing\nBiror savolning javobini o'zgartirmoqchi bo'lsangiz <code>♻️O'zgartirish</code> tugmasini bosing\nJavoblaringiz to'g'riligiga ishonch hosil qilganingizdan so'ng <code>✅Tasdiqlash</code> tugmasini bosing</i></b>"
    try:
        await bot.delete_message(msg.chat.id, temp[msg.from_user.id][1])
    except:
        pass
    temp[msg.from_user.id][1] = msg.message_id + 1
    await msg.answer(answer, reply_markup=tasdiqlash.tasdiqlash)
    await state.set_state("javoblarni tasdiqlash")


@dp.message_handler(state="savolning raqami")
async def javobni_uzgartirish(msg: types.Message, state: FSMContext):
    if msg.text.isnumeric():
        raqam = int(msg.text)
        if len(temp[msg.from_user.id][0]) >= raqam:
            temp[f"{msg.from_user.id}:raqam"] = raqam
            await msg.answer(
                f"<b>{raqam} - savolning javobiga {temp[msg.from_user.id][0][raqam - 1]} variantini kiritgansiz❗️\nQaysi variantga almashtirmoqchisiz❓(Tanlang 👇)</b>",
                reply_markup=abcd_variant.abcd_variant(
                    temp[msg.from_user.id][0][raqam - 1]
                ),
            )
            await state.set_state("yangi variant")
        else:
            await msg.answer(
                f"<b>{raqam} - savol mavjud emas ❗️\nSavollar soni {len(temp[msg.from_user.id][0])} ta ❗️\n\nSavolning tartib raqamini qayta yuboring : </b>",
                reply_markup=ortga.ortga,
            )

    else:
        await msg.answer(
            f"<b>Savolning tartib raqami natural son❗️\n\nSavolning tartib raqamini qayta yuboring : </b>",
            reply_markup=ortga.ortga,
        )


@dp.callback_query_handler(text="ortga", state="yangi variant")
async def ortgaaa(call: types.CallbackQuery, state: FSMContext):
    text = temp[call.from_user.id][0]
    answer = "<b>Diqqat ❗️\n\nJavoblaringiz to'g'ri ekanligiga ishonch hosil qiling ❗️\n\n\n</b>"
    for i in range(1, len(text) + 1):
        answer += f"<i>{i}  --  {text[i-1]}</i>\n"
    answer += "\n\n<b><i>Agar javoblarni qayta kiritmoqchi bo'lsangiz <code>🔴Qayta kiritish</code> tugmasini bosing\nBiror savolning javobini o'zgartirmoqchi bo'lsangiz <code>♻️O'zgartirish</code> tugmasini bosing\nJavoblaringiz to'g'riligiga ishonch hosil qilganingizdan so'ng <code>✅Tasdiqlash</code> tugmasini bosing</i></b>"
    try:
        await bot.delete_message(call.message.chat.id, temp[call.from_user.id][1])
    except:
        pass
    temp[call.from_user.id][1] = call.message.message_id + 1
    await call.message.delete()
    await call.message.answer(answer, reply_markup=tasdiqlash.tasdiqlash)
    await state.set_state("javoblarni tasdiqlash")


@dp.callback_query_handler(state="yangi variant")
async def yangi_variant(call: types.CallbackQuery, state: FSMContext):
    # temp[user_id] = [javob, message_id]
    variant = call.data
    tartib = temp[f"{call.from_user.id}:raqam"]
    temp[f"{call.from_user.id}:raqam"] = None
    try:
        await bot.delete_message(call.message.chat.id, temp[call.from_user.id][1])
    except:
        pass
    javob = temp[call.from_user.id][0]
    lis = list(javob)
    lis[tartib - 1] = variant
    javob = "".join(lis)
    temp[call.from_user.id][0] = javob
    await call.answer(
        f"{tartib} - savolning javobi {variant} variantiga o'zgartirildi ✅",
        show_alert=True,
    )
    await call.message.delete()
    text = temp[call.from_user.id][0]
    answer = "<b>Diqqat ❗️\n\nJavoblaringiz to'g'ri ekanligiga ishonch hosil qiling ❗️\n\n\n</b>"
    for i in range(1, len(text) + 1):
        answer += f"<i>{i}  --  {text[i-1]}</i>\n"
    answer += "\n\n<b><i>Agar javoblarni qayta kiritmoqchi bo'lsangiz <code>🔴Qayta kiritish</code> tugmasini bosing\nBiror savolning javobini o'zgartirmoqchi bo'lsangiz <code>♻️O'zgartirish</code> tugmasini bosing\nJavoblaringiz to'g'riligiga ishonch hosil qilganingizdan so'ng <code>✅Tasdiqlash</code> tugmasini bosing</i></b>"
    temp[call.from_user.id][1] = call.message.message_id + 1
    await call.message.answer(answer, reply_markup=tasdiqlash.tasdiqlash)
    await state.set_state("javoblarni tasdiqlash")


@dp.callback_query_handler(state="javoblarni tasdiqlash", text="tasdiqlash")
async def tekshirishh(call: types.CallbackQuery, state: FSMContext):
    # test_time[user_id] = [datetime, test_id, fan_id, status]
    data = test_time[call.from_user.id]
    time_now = datetime.datetime.now(pytz.timezone("Asia/Tashkent"))
    last_time = data[0].strftime("%H:%M %d.%m.%Y")
    if time_now > data[0]:
        answer = f"<b>Siz berilgan vaqt ichida javob yubormadingiz ❌\n<i>({last_time} gacha javob yuborishingiz kerak edi)</i></b>"
        if data[3] == 1:
            answer += "<b>\n\nUshbu testdan olgan balingiz : 0️⃣</b>"
            db_results.add_result(call.from_user.id, data[1], 0)
        db_temp.delete_temp(call.from_user.id)
        temp[call.from_user.id] = None
        test_time[call.from_user.id] = None
        await call.message.delete()
        await call.answer(answer, reply_markup=menu.menu)
        await state.finish()
    else:
        await call.answer("Javoblaringiz qabul qilindi ✅", show_alert=True)
        if data[2] == 0:
            # Majburiy fanlar
            test = db_tests.select_test(data[1])
            berilgan_javob = temp[call.from_user.id][0]
            ona_tili = []
            count1 = 0
            count2 = 0
            count3 = 0
            matematika = []
            tarix = []
            for i in range(0, 10):
                if test[3][i] == berilgan_javob[i]:
                    ona_tili.append("✅")
                    count1 += 1
                else:
                    ona_tili.append("❌")
            for i in range(10, 20):
                if test[3][i] == berilgan_javob[i]:
                    matematika.append("✅")
                    count2 += 1
                else:
                    matematika.append("❌")
            for i in range(20, 30):
                if test[3][i] == berilgan_javob[i]:
                    tarix.append("✅")
                    count3 += 1
                else:
                    tarix.append("❌")
            balll = await raqam.digit_to_emoji(round(count1 * 1.1, 1))
            answer = f"<b>#Majburiy_fanlar\n\n\n📚Fanlar : \nOna tili\nMatematika\nO'zbekiston tarixi\n\n\n📕Ona tili -- <i>{balll}</i> ball <i>({count1} ta, 1.1 ball)</i>\n\n</b>"
            for i in range(0, 10):
                answer += f"<i>{i+1} - {ona_tili[i]}</i> "
                if i == 4:
                    answer += "\n"
            balll = await raqam.digit_to_emoji(round(count2 * 1.1, 1))
            answer += f"<b>\n\n📗Matematika() -- <i>{balll}</i> ball <i>({count2} ta, 1.1 ball)</i>\n\n</b>"
            for i in range(0, 10):
                answer += f"<i>{i+11} - {matematika[i]}</i> "
                if i == 4:
                    answer += "\n"
            balll = await raqam.digit_to_emoji(round(count3 * 1.1, 1))
            answer += f"<b>\n\n\n📘O'zbekiston tarixi -- <i>{balll}</i> ball <i>({count3} ta, 1.1 ball)</i>\n\n</b>"
            for i in range(0, 10):
                answer += f"<i>{i+21} - {tarix[i]}</i> "
                if i == 4:
                    answer += "\n"
            balll = await raqam.digit_to_emoji(
                round((count1 + count2 + count3) * 1.1, 1)
            )
            answer += f"<b>\n\n\✅Umumiy ball : <i>{balll}</i> ball <i>({count1 + count2 + count3} ta)</i></b>"
            if data[3] == 1:
                db_results.add_result(
                    call.from_user.id,
                    data[1],
                    round((count1 + count2 + count3) * 1.1, 1),
                    0,
                )
            await call.message.delete()
            await call.message.answer(answer, reply_markup=menu.menu)
        else:
            tur = db_tests.select_fan(data[2])
            if tur[2] == 1:
                # Asosiy
                test = db_tests.select_test(data[1])
                fan = db_tests.select_fan(test[2])
                berilgan_javob = temp[call.from_user.id][0]
                natija = []
                ball = 0
                for i in range(0, 30):
                    if test[3][i] == berilgan_javob[i]:
                        natija.append("✅")
                        ball += 1
                    else:
                        natija.append("❌")
                balll = await raqam.digit_to_emoji(round(ball * 3.1, 1))
                answer = f"<b>#Asosiy_fan\n\n\n{fan[1]} -- <i>{balll}</i> ball <i>({ball} ta, 3.1 ball)</i>\n\n</b>"
                for i in range(0, 30):
                    answer += f"<i>{i+1} - {natija[i]}</i> "
                    if i in [4, 9, 14, 19, 24]:
                        answer += "\n\n"

                if data[3] == 1:
                    db_results.add_result(
                        call.from_user.id, test[0], round(ball * 3.1, 1), data[2]
                    )
                await call.message.delete()
                await call.message.answer(answer, reply_markup=menu.menu)

            elif tur[2] == 3:
                # Blok test
                # data = test_time[user_id] = [datetime, test_id, fan_id, status]
                test = db_tests.select_test(data[1])
                fan = db_tests.select_fan(data[2])[1]
                berilgan_javob = temp[call.from_user.id][0]
                natija = []
                for i in range(0, len(berilgan_javob)):
                    if test[3][i] == berilgan_javob[i]:
                        natija.append("✅")
                    else:
                        natija.append("❌")
                ona_tili = []
                matem = []
                tarix = []
                birinchi = []
                ikkinchi = []
                temp1 = ""
                ball = 0
                for i in range(0, 10):
                    temp1 += f"<i>{i+1} - {natija[i]}</i> "
                    if natija[i] == "✅":
                        ball += 1
                    if i == 4:
                        temp1 += "\n"

                ona_tili.append(ball)
                ona_tili.append(temp1)
                ball = 0
                temp1 = ""

                for i in range(10, 20):
                    temp1 += f"<i>{i+1} - {natija[i]}</i> "
                    if natija[i] == "✅":
                        ball += 1
                    if i == 14:
                        temp1 += "\n"

                matem.append(ball)
                matem.append(temp1)
                ball = 0
                temp1 = ""

                for i in range(20, 30):
                    temp1 += f"<i>{i+1} - {natija[i]}</i> "
                    if natija[i] == "✅":
                        ball += 1
                    if i == 24:
                        temp1 += "\n"

                tarix.append(ball)
                tarix.append(temp1)
                ball = 0
                temp1 = ""

                for i in range(30, 60):
                    temp1 += f"<i>{i+1} - {natija[i]}</i> "
                    if natija[i] == "✅":
                        ball += 1
                    if i in [34, 39, 44, 49, 54]:
                        temp1 += "\n\n"

                birinchi.append(ball)
                birinchi.append(temp1)
                ball = 0
                temp1 = ""

                for i in range(60, 90):
                    temp1 += f"<i>{i+1} - {natija[i]}</i> "
                    if natija[i] == "✅":
                        ball += 1
                    if i in [64, 69, 74, 79, 84]:
                        temp1 += "\n\n"

                ikkinchi.append(ball)
                ikkinchi.append(temp1)

                fan_list = fan.split(" va ")
                balll = await raqam.digit_to_emoji(round(ona_tili[0] * 1.1, 1))
                answer = f"<b>#Blok_test\n\n\n📚Majburiy fanlar\n1️⃣{fan_list[0]}\n2️⃣{fan_list[1]}\n\n\n📕Ona tili -- <i>{balll}</i> ball <i>({ona_tili[0]} ta, 1.1 ball)</i>\n\n</b>{ona_tili[1]}\n\n"
                balll = await raqam.digit_to_emoji(round(matem[0] * 1.1, 1))
                answer += f"<b>📗Matematika -- <i>{balll}</i> ball <i>({matem[0]} ta, 1.1 ball)</i>\n\n</b>{matem[1]}\n\n"
                balll = await raqam.digit_to_emoji(round(tarix[0] * 1.1, 1))
                answer += f"<b>📘O'zbekiston tarixi -- <i>{balll}</i> ball <i>({tarix[0]} ta, 1.1 ball)</i>\n\n</b>{tarix[1]}\n\n"
                balll = await raqam.digit_to_emoji(round(birinchi[0] * 3.1, 1))
                answer += f"<b>1️⃣{fan_list[0]} -- <i>{balll}</i> ball <i>({birinchi[0]} ta, 3.1 ball)</i>\n\n</b>{birinchi[1]}\n\n"
                balll = await raqam.digit_to_emoji(round(ikkinchi[0] * 3.1, 1))
                answer += f"<b>2️⃣{fan_list[1]} -- <i>{balll}</i> ball <i>({ikkinchi[0]} ta, 2.1 ball)</i>\n\n</b>{ikkinchi[1]}\n\n"
                balll = await raqam.digit_to_emoji(
                    round(
                        birinchi[0] * 3.1
                        + ikkinchi[0] * 2.1
                        + (ona_tili[0] + tarix[0] + matem[0]) * 1.1,
                        1,
                    )
                )
                answer += f"<b>✅Umumiy ball : <i>{balll}</i> ball</b>\n\n"
                if data[3] == 1:
                    db_results.add_result(
                        call.from_user.id,
                        test[0],
                        round(
                            birinchi[0] * 3.1
                            + ikkinchi[0] * 2.1
                            + (ona_tili[0] + tarix[0] + matem[0]) * 1.1,
                            1,
                        ),
                        data[2],
                    )
                await call.message.delete()
                await call.message.answer(answer, reply_markup=menu.menu)

        await state.finish()
        db_temp.delete_temp(call.from_user.id)
        temp[call.from_user.id] = None
        test_time[call.from_user.id] = None
