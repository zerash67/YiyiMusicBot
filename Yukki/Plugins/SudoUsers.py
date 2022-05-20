import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import LOG_SESSION, OWNER_ID
from Yukki import (ASSISTANT_PREFIX, BOT_ID, BOT_USERNAME, MUSIC_BOT_NAME,
                   OWNER_ID, SUDOERS, app)
from Yukki.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo,
                            set_video_limit)

__MODULE__ = "SudoUsers"
__HELP__ = f"""


**<u>TAMBAH & HAPUS SUDO USERS :</u>**
/addsudo [Username atau Balas ke pengguna]
/delsudo [Username atau Balas ke pengguna]

**<u>HEROKU:</u>**
/get_log - Log dari 100 baris terakhir dari Heroku.
/usage - Penggunaan Dyno.

**<u>KONFIGURASI VARIABEL:</u>**
/get_var - Dapatkan var konfigurasi dari Heroku atau .env.
/del_var - Hapus semua var di Heroku atau .env.
/set_var [Var Name] [Value] - Setel Var atau Perbarui Var di heroku atau .env. Pisahkan Var dan Nilainya dengan spasi.

**<u>PERINTAH BOT:</u>**
/restart - Memulai Ulang Bot. 
/update - Pembaruan Bot.
/clean - Bersihkan File Temp .
/maintenance [enable / disable] 
/logger [enable / disable] - Bot mencatat query yang dicari di Log Group.

**<u>PERINTAH STATISTIK:</u>**
/activevc - Periksa obrolan suara aktif di bot.
/activevideo - Periksa obrolan video aktif di bot.
/stats - Periksa Statistik Bot

**<u>FUNGSI DAFTAR HITAM:</u>**
/blacklistchat [CHAT_ID] - Menambahkan Group ke Daftar Hitam penggunaan Bot Musik
/whitelistchat [CHAT_ID] - Menambahkan Group ke Daftar Putih penggunaan Bot Musik

**<u>FUNGSI PESAN SIARAN:</u>**
/broadcast [Pesan atau Balas Pesan] - Siarkan pesan apa pun ke Group yang Dilayani Bot.
/broadcast_pin [Pesan atau Balas Pesan] - Siarkan pesan apa pun ke Group yang Dilayani Bot dengan pesan yang disematkan di Group [Notifikasi Dinonaktifkan].
/broadcast_pin_loud [Pesan atau Balas Pesan] - Siarkan pesan apa pun ke Group yang Dilayani Bot dengan pesan yang disematkan di Group [Notifikasi Diaktifkan].

**<u>FUNGSI GBAN:</u>**
/gban [Nama pengguna atau Balas ke pengguna] - Blokir pengguna secara global di Group yang Dilayani Bot dan cegah pengguna menggunakan perintah bot.
/ungban [Nama pengguna atau Balas ke pengguna] - Hapus pengguna dari Daftar GBan Bot.

**<u>FUNGSI BERGABUNG/MENINGGALKAN:</u>**
/joinassistant [Username Group atau ID Group] - Asisten Bergabung ke Group.
/leaveassistant [Username Group atau ID Group] - Asisten akan meninggalkan Group tertentu.
/leavebot [Username Group atau ID Group] - Bot akan meninggalkan Group tertentu.

**<u>FUNGSI VIDEOCALL:</u>**
/set_video_limit [Number of Chats] - Tetapkan Jumlah Obrolan maksimum yang diijinkan untuk Pemutaran Video sekaligus.

**<u>FUNGSI ASISTEN:</u>**
{ASSISTANT_PREFIX[0]}block [Membalas Pesan Pengguna] - Memblokir Pengguna dari Akun Asisten.
{ASSISTANT_PREFIX[0]}unblock [Membalas Pesan Pengguna] - Buka blokir Pengguna dari Akun Asisten.
{ASSISTANT_PREFIX[0]}approve [Membalas Pesan Pengguna] - Menyetujui Pengguna untuk Pesan Langsung.
{ASSISTANT_PREFIX[0]}disapprove [Membalas Pesan Pengguna] - Menolak Pengguna untuk Pesan Langsung.
{ASSISTANT_PREFIX[0]}pfp [Balas ke Foto] - Mengubah foto profil akun Asisten.
{ASSISTANT_PREFIX[0]}bio [Teks Bio] - Perubahan Bio Akun Asisten.
"""
# Add Sudo Users!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
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
        if user.id in SUDOERS:
            return await message.reply_text(
                f"{user.mention} Sudah menjadi Pengguna Sudo."
            )
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"Menambahkan **{user.mention}** ke Pengguna Sudo."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        else:
            await message.reply_text("Gagal")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"{message.reply_to_message.from_user.mention} Sudah menjadi Pengguna Sudo."
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            f"Menambahkan **{message.reply_to_message.from_user.mention}** ke Pengguna Sudo"
        )
        os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("Gagal")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
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
        from_user = message.from_user
        if user.id not in SUDOERS:
            return await message.reply_text(f"Bukan Pengguna Sudo.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(
                f"Menghapus **{user.mention}** Dari {MUSIC_BOT_NAME} Sudo."
            )
            return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        await message.reply_text(f"Sesuatu yang salah terjadi.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in SUDOERS:
        return await message.reply_text(
            f"Bukan bagian {MUSIC_BOT_NAME} Sudo."
        )
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(
            f"Menghapus **{mention}** dari {MUSIC_BOT_NAME} Sudo."
        )
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    await message.reply_text(f"Sesuatu yang salah terjadi.")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "🥸<u> **Pemilik:**</u>\n"
    sex = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            sex += 1
        except Exception:
            continue
        text += f"{sex}➤ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n👮‍♂<u> **Pengguna Sudo:**</u>\n"
                sex += 1
                text += f"{sex}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("Tidak Ada Pengguna Sudo")
    else:
        await message.reply_text(text)


### Video Limit


@app.on_message(
    filters.command(["set_video_limit", f"set_video_limit@{BOT_USERNAME}"])
    & filters.user(SUDOERS)
)
async def set_video_limit_kid(_, message: Message):
    if len(message.command) != 2:
        usage = "**usage:**\n/set_video_limit [Durasi yang diperbolehkan]"
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    try:
        limit = int(state)
    except:
        return await message.reply_text(
            "Silakan Gunakan Angka untuk Menetapkan Batas."
        )
    await set_video_limit(141414, limit)
    await message.reply_text(
        f"Batas Maksimum Memainkan Video ditetapkan ke {limit} Obrolan."
    )


## Maintenance Yukki


@app.on_message(filters.command("maintenance") & filters.user(SUDOERS))
async def maintenance(_, message):
    usage = "**usage:**\n/maintenance [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("Diaktifkan Untuk Pemeliharaan")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("Dimatikan Untuk Pemeliharaan")
    else:
        await message.reply_text(usage)


## Logger


@app.on_message(filters.command("logger") & filters.user(SUDOERS))
async def logger(_, message):
    if LOG_SESSION == "None":
        return await message.reply_text(
            "Tidak Ada Akun Pencatat yang Ditentukan.\n\nSilahkan Atur <code>LOG_SESSION</code> Var lalu mulai pencatatan."
        )
    usage = "**usage:**\n/logger [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 5
        await add_on(user_id)
        await message.reply_text("Log Diaktifkan digroup Log")
    elif state == "disable":
        user_id = 5
        await add_off(user_id)
        await message.reply_text("Log Dimatikan")
    else:
        await message.reply_text(usage)


## Gban Module


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**Usage:**\n/gban [USERNAME | USER_ID]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "Apakah kamu ingin Mengban diri sendiri? Stress!"
            )
        elif user.id == BOT_ID:
            await message.reply_text("Mau block bot ini?goblok!")
        elif user.id in SUDOERS:
            await message.reply_text("Mau block Pengguna Sudo? Bego")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Memulai Global Banned untuk {user.mention}**\n\nExpected Time : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Global Banned baru di{MUSIC_BOT_NAME}**__

**Asal:** {message.chat.title}
**Pengguna Sudo:** {from_user.mention}
**Blokir Pengguna:** {user.mention}
**Id Pengguna Terblokir:** `{user.id}`
**Chats:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Anda ingin memblokir diri sendiri? Betapa Bodohnya!")
    elif user_id == BOT_ID:
        await message.reply_text("Haruskah saya memblokir diri saya sendiri? Sangat gblk!")
    elif user_id in sudoers:
        await message.reply_text("Anda ingin memblokir Sudo User? Anda tidak waras")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("Sudah Digban.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Menginisialisasi Blokir Global pada {mention}**\n\nWaktu yang diperlukan : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.ban_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Blokir Global baru pada {MUSIC_BOT_NAME}**__

**Asal:** {message.chat.title}
**Pengguna Sudo:** {from_user_mention}
**Pengguna Diblokir:** {mention}
**Id Pengguna Terblokir:** `{user_id}`
**Chats:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**Usage:**\n/ungban [USERNAME | USER_ID]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("Anda ingin membuka blokir sendiri?")
        elif user.id == BOT_ID:
            await message.reply_text("Haruskah saya membuka blokir sendiri?")
        elif user.id in sudoers:
            await message.reply_text("Pengguna Sudo tidak dapat diblokir/dibuka blokirnya..")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("Dia sudah bebas, mengapa menggertaknya?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Dibuka Dari Blokir Global!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Anda ingin membuka blokir diri sendiri?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Haruskah saya membuka blokir sendiri? Tapi saya tidak diblokir."
        )
    elif user_id in sudoers:
        await message.reply_text("Pengguna Sudo tidak dapat diblokir/dibuka blokirnya.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("Dia sudah bebas, mengapa menggertaknya?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Dibuka Dari Blokir Global!")


# Broadcast Message


@app.on_message(filters.command("broadcast_pin") & filters.user(SUDOERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Pesan yang disiarkan dalam {sent}  Group dengan {pin} Sematan.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Pesan yang disiarkan dalam {sent} Group dengan {pin} Sematan.**"
    )


@app.on_message(filters.command("broadcast_pin_loud") & filters.user(SUDOERS))
async def broadcast_message_pin_loud(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Pesan yang disiarkan dalam {sent}  Group dengan {pin} Sematan.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Pesan yang disiarkan dalam {sent} Group dan {pin} Sematan.**"
    )


@app.on_message(filters.command("broadcast") & filters.user(SUDOERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**Pesan yang disiarkan dalam {sent} Group.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**Pesan yang disiarkan dalam {sent} Group.**")


# Clean


@app.on_message(filters.command("clean") & filters.user(SUDOERS))
async def clean(_, message):
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("Berhasil membersihkan semua **temp** direktori!")
