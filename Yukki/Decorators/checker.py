from Yukki import BOT_USERNAME, LOG_GROUP_ID, app
from Yukki.Database import blacklisted_chats, is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "Kamu adalah__Admin Anonim__Di Group Chat ini!\nKembalikan ke Akun Pengguna Dari Hak Admin."
            )
        blacklisted_chats_list = await blacklisted_chats()
        if message.chat.id in blacklisted_chats_list:
            await message.reply_text(
                f"**Daftar Hitam Chat**\n\nObrolan kamu masuk daftar hitam oleh Pengguna Sudo.Tanya __SUDO USER__ untuk ke Daftar Putih.\nPeriksa daftar Pengguna Sudo [Disini](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
            return await app.leave_chat(message.chat.id)
        if await is_on_off(1):
            if int(message.chat.id) != int(LOG_GROUP_ID):
                return await message.reply_text(
                    f"Bot sedang dalam Pemeliharaan. Maaf untuk ketidaknyamanannya 🙏!"
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**Gban Pengguna**\n\nAnda dilarang menggunakan Bot.Tanya __SUDO USER__ untuk Ungban.\nPeriksa Daftar Pengguna Sudo [Disini](https://t.me/{BOT_USERNAME}?start=sudolist)"
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        blacklisted_chats_list = await blacklisted_chats()
        if CallbackQuery.message.chat.id in blacklisted_chats_list:
            return await CallbackQuery.answer(
                "Daftar Hitam Chat", show_alert=True
            )
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOG_GROUP_ID):
                return await CallbackQuery.answer(
                    "Bot sedang dalam Pemeliharaan. Maaf untuk ketidaknyamanannya 🙏!",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "Kamu telah di Gban", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
