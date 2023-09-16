async def digit_to_emoji(number):
    # number = 175.2
    emoji = ""
    number = str(number)
    for a in number:
        if a == "1":
            emoji += "1️⃣"
        elif a == "2":
            emoji += "2️⃣"
        elif a == "3":
            emoji += "3️⃣"
        elif a == "4":
            emoji += "4️⃣"
        elif a == "5":
            emoji += "5️⃣"
        elif a == "6":
            emoji += "6️⃣"
        elif a == "7":
            emoji += "7️⃣"
        elif a == "8":
            emoji += "8️⃣"
        elif a == "9":
            emoji += "9️⃣"
        elif a == "0":
            emoji += "0️⃣"
        elif a == ".":
            emoji += "."
    
    return emoji