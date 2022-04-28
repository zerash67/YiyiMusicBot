from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app
from Yukki.Database import (_get_authusers, delete_authuser, get_authuser,
                            get_authuser_count, get_authuser_names,
                            save_authuser)
from Yukki.Decorators.admins import AdminActual
from Yukki.Utilities.changers import (alpha_to_int, int_to_alpha,
                                      time_to_seconds)

__MODULE__ = "Auth Users"
__HELP__ = """

**Catatan:**
-Pengguna resmi dapat melewati, menjeda, menghentikan, melanjutkan Obrolan Suara bahkan tanpa Hak Admin.
/auth [Nama Pengguna atau Balas Pesan] 
- Tambahkan pengguna ke AUTH LIST Group.
/unauth [Nama Pengguna atau Balas Pesan] 
- Hapus pengguna dari AUTH LIST Group.
/authusers 
- Periksa AUTH LIST di Group.
"""


@app.on_message(filters.command("auth") & filters.group)
@AdminActual
async def auth(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Balas pesan pengguna atau berikan nama pengguna/id pengguna."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = 0
        for smex in _check:
            count += 1
        if int(count) == 20:
            return await message.reply_text(
                "Anda hanya dapat memiliki 20 Pengguna Di Daftar Pengguna Resmi Group Anda (AUL)"
            )
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            await save_authuser(message.chat.id, token, assis)
            await message.reply_text(
                f"Ditambahkan ke Daftar Pengguna resmi dari grup ini."
            )
            return
        else:
            await message.reply_text(f"Sudah ada di Daftar Pengguna resmi.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(
            "Anda hanya dapat memiliki 20 Pengguna Di Daftar Pengguna resmi Grup Anda (AUL)"
        )
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        await save_authuser(message.chat.id, token, assis)
        await message.reply_text(
            f"Ditambahkan ke Daftar Pengguna resmi dari grup ini."
        )
        return
    else:
        await message.reply_text(f"Sudah ada di Daftar Pengguna resmi.")


@app.on_message(filters.command("unauth") & filters.group)
@AdminActual
async def whitelist_chat_func(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Membalas pesan pengguna atau memberikan username/user_id."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        if deleted:
            return await message.reply_text(
                f"Dihapus dari Daftar Pengguna resmi Grup ini."
            )
        else:
            return await message.reply_text(f"Bukan Pengguna resmi.")
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if deleted:
        return await message.reply_text(
            f"Dihapus dari Daftar Pengguna resmi Grup ini."
        )
    else:
        return await message.reply_text(f"Bukan Pengguna resmi.")


@app.on_message(filters.command("authusers") & filters.group)
async def authusers(_, message: Message):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(
            f"Tidak ada Pengguna resmi di Grup ini.\n\nTambahkan pengguna resmi dengan /auth dan hapus dengan /unauth."
        )
    else:
        j = 0
        m = await message.reply_text(
            "Mengambil Pengguna Resmi... Mohon Tunggu"
        )
        msg = f"**Daftar Pengguna Resmi[AUL]:**\n\n"
        for note in _playlist:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            user_name = _note["auth_name"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            msg += f"{j}⌬ {user}[`{user_id}`]\n"
            msg += f"    ┗ Ditambahkan oleh:- {admin_name}[`{admin_id}`]\n\n"
        await m.edit_text(msg)
