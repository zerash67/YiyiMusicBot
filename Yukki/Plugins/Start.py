import asyncio
import random
import time
from sys import version as pyver
from typing import Dict, List, Union

import psutil
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from Yukki import ASSIDS, BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki import boottime as bot_start_time
from Yukki import db, random_assistant
from Yukki.Core.PyTgCalls import Yukki
from Yukki.Database import (add_nonadmin_chat, add_served_chat,
                            blacklisted_chats, get_assistant, get_authuser,
                            get_authuser_names, get_start, is_nonadmin_chat,
                            is_served_chat, remove_active_chat,
                            remove_nonadmin_chat, save_assistant, save_start)
from Yukki.Decorators.admins import ActualAdminCB
from Yukki.Decorators.permission import PermissionCheck
from Yukki.Inline import (custommarkup, dashmarkup, setting_markup,
                          setting_markup2, start_pannel, usermarkup, volmarkup)
from Yukki.Utilities.assistant import get_assistant_details
from Yukki.Utilities.ping import get_readable_time

welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == BOT_ID:
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        f"Hushh, Grup Anda[{message.chat.title}] telah masuk daftar hitam!\n\nMinta Pengguna Sudo untuk memasukkan Group Anda ke daftar putih"
                    )
                    return await app.leave_chat(chat_id)
                _assistant = await get_assistant(message.chat.id, "assistant")
                if not _assistant:
                    ran_ass = random.choice(random_assistant)
                    assis = {
                        "saveassistant": ran_ass,
                    }
                    await save_assistant(message.chat.id, "assistant", assis)
                else:
                    ran_ass = _assistant["saveassistant"]
                (
                    ASS_ID,
                    ASS_NAME,
                    ASS_USERNAME,
                    ASS_ACC,
                ) = await get_assistant_details(ran_ass)
                out = start_pannel()
                await message.reply_text(
                    f"""
┏━━━━•᪣•°• -𖣔- •°•᪣•━━━┓
   ┏━━┓┏━━┓┏━━┓┏━━┓ 
   ┗━┓┃┃┏┓┃┗━┓┃┗━┓┃ 
   ┏━┛┃┃┃┃┃┏━┛┃┏━┛┃
   𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝙺𝙰𝙼𝙸 𝚈𝙰 𝙶𝚄𝚈𝚂🙏
   ┃┗━┓┃┗┛┃┃┗━┓┃┗━┓
   ┗━━┛┗━━┛┗━━┛┗━━┛
┗━━━━•᪣•°• -𖣔- •°•᪣•━━━┛
👋 Selamat Datang Di {MUSIC_BOT_NAME}\n\nPromosikan saya sebagai administrator di grup Anda jika tidak, saya tidak akan berfungsi dengan baik.\n\nNama Pengguna Asisten:- @{ASS_USERNAME}\nID Asisten:- {ASS_ID}.\n\n **OWNER** @gausahsokablunyet""",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
            if member.id in ASSIDS:
                return await remove_active_chat(chat_id)
            if member.id in OWNER_ID:
                return await message.reply_text(
                    f"🥸 Pemilik Bot {MUSIC_BOT_NAME}[{member.mention}] baru saja bergabung digroup ini."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"⛑️ Admin Bot {MUSIC_BOT_NAME}[{member.mention}] baru saja bergabung dengan Group ini."
                )
            return
        except:
            return


@app.on_message(filters.command(["help", "start"]) & filters.group)
@PermissionCheck
async def useradd(_, message: Message):
    out = start_pannel()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"""
┏━━━━•᪣•°• -𖣔- •°•᪣•━━━┓
    ┏━━┓┏━━┓┏━━┓┏━━┓ 
    ┗━┓┃┃┏┓┃┗━┓┃┗━┓┃ 
    ┏━┛┃┃┃┃┃┏━┛┃┏━┛┃
    𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝙺𝙰𝙼𝙸 𝚈𝙰 𝙶𝚄𝚈𝚂🙏
    ┃┗━┓┃┗┛┃┃┗━┓┃┗━┓
    ┗━━┛┗━━┛┗━━┛┗━━┛
┗━━━━•᪣•°• -𖣔- •°•᪣•━━━┛
👋 Terima kasih telah memasukkan saya di {message.chat.title}

🤖 {MUSIC_BOT_NAME} Diaktifkan 🔥

📌 Untuk bantuan atau bantuan apa pun, periksa Group dan Channel dukungan kami.""",
            reply_markup=InlineKeyboardMarkup(out[1]),
        ),
    )


@app.on_message(filters.command("settings") & filters.group)
@PermissionCheck
async def settings(_, message: Message):
    c_id = message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    text, buttons = setting_markup2()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"{text}\n\n**Group:** {message.chat.title}\n**Tingkat Suara:** {volume}%",
            reply_markup=InlineKeyboardMarkup(buttons),
        ),
    )


@app.on_callback_query(filters.regex("okaybyee"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("Akan Kembali ...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"""
┏━━━━•᪣•°• -𖣔- •°•᪣•━━━┓
    ┏━━┓┏━━┓┏━━┓┏━━┓ 
    ┗━┓┃┃┏┓┃┗━┓┃┗━┓┃ 
    ┏━┛┃┃┃┃┃┏━┛┃┏━┛┃
    𝚂𝚄𝙿𝙿𝙾𝚁𝚃 𝙺𝙰𝙼𝙸 𝚈𝙰 𝙶𝚄𝚈𝚂🙏
    ┃┗━┓┃┗┛┃┃┗━┓┃┗━┓
    ┗━━┛┗━━┛┗━━┛┗━━┛
┗━━━━•᪣•°• -𖣔- •°•᪣•━━━┛
👋 Terima kasih telah memasukkan saya {CallbackQuery.message.chat.title}

🤖 {MUSIC_BOT_NAME} Diaktifkan 🔥

📌 Untuk bantuan atau bantuan apa pun, periksa Group dan Channel dukungan kami.""",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("Pengaturan Bot ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_start(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_start(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("Perubahan Tersimpan")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nMode Perintah Admin ke **Semuanya**\n\nSekarang, siapa pun yang ada di Group ini dapat melewati, menjeda, melanjutkan dan menghentikan musik.\n\nPerubahan dilakukan oleh @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "Mode Perintah Sudah Disetel Untuk SEMUANYA", show_alert=True
        )


@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "Mode Perintah Sudah Disetel Ke ADMIN SAJA", show_alert=True
        )
    else:
        await CallbackQuery.answer("Perubahan Tersimpan")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nSetel Mode Perintah ke **Admin**\n\nSekarang hanya Admin yang ada di grup ini yang dapat melewati, menjeda, melanjutkan, menghentikan musik.\n\nPerubahan Dilakukan Oleh @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("Sudah dalam Kualitas Terbaik", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("Pengaturan Bot ...")
        text, buttons = volmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("Pengaturan Bot...")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "Hanya Admin"
        else:
            current = "Semuanya"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n\nSaat ini siapa yang dapat menggunakan {MUSIC_BOT_NAME}:- **{current}**\n\n**⁉️ Apa ini?**\n\n**🫂 Semuanya :-**Semuanya dapat menggunakan {MUSIC_BOT_NAME} Perintah (melewati, menjeda, melanjutkan dsb) hadir di Group ini.\n\n**👷 Hanya Admin :-**  Hanya Admin dan Pengguna Resmi yang dapat menggunakan semua perintah dari {MUSIC_BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("Dashboard...")
        text, buttons = dashmarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n\nMemeriksa {MUSIC_BOT_NAME} Statistik Sistem di dashboard saat ini! Lebih banyak fungsi ditambahkan segera! Selalu periksa group dan channel kami.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("Pengaturan Bot ...")
        text, buttons = custommarkup()
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Mengatur Perubahan Suara ...")
        except:
            return await CallbackQuery.answer("Tidak Ada Obrolan Suara Aktif...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Mengatur Perubahan Suara ...")
        except:
            return await CallbackQuery.answer("Tidak Ada Obrolan Suara Aktif...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Mengatur Perubahan Suara ...")
        except:
            return await CallbackQuery.answer("Tidak Ada Obrolan Suara Aktif...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Mengatur Perubahan Suara ...")
        except:
            return await CallbackQuery.answer("Tidak Ada Obrolan Suara Aktif...")
        await save_start(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Mengatur Perubahan Suara...")
        except:
            return await CallbackQuery.answer("Tidak Ada Obrolan Suara Aktif...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Mengatur Perubahan Suara...")
        except:
            return await CallbackQuery.answer("Tidak Ada Obrolan Suara Aktif...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Tingkat Suara:** {volume}%\n**Kualitas Suara:** Bawaan Terbaik",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_start(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Yukki.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("Setting Audio Changes ...")
        except:
            return await CallbackQuery.answer("No active Group Call...")
        await save_start(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**Group:** {c_title}\n**Group ID:** {c_id}\n**Volume Level:** {volume}%\n**Audio Quality:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("Auth Users!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nNo Authorized Users Found\n\nYou can allow any non-admin to use my admin commands by /auth and delete by using /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "Fetching Authorised Users... Please Wait"
            )
            msg = f"**Authorised Users List[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
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
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    ┗ Added By:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"Bot's Uptime: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"Bot's Cpu Usage: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"Bot's Memory Usage: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"Yukki Disk Usage: {diske}%", show_alert=True
        )
