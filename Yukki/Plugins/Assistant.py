import random

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import ASSISTANT_PREFIX, SUDOERS, app, random_assistant
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details

ass_num_list = ["1", "2", "3", "4", "5"]


@app.on_message(filters.command("changeassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Penggunaan:**\n/changeassistant [ASS_NO]\n\nPilih dari Mereka\n{' | '.join(ass_num_list)}"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    num = message.text.split(None, 1)[1].strip()
    if num not in ass_num_list:
        return await message.reply_text(usage)
    ass_num = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Asisten Tidak Ditemukan.\n\nKamu dapat mengatur Asisten melalui /setassistant"
        )
    else:
        ass = _assistant["saveassistant"]
    assis = {
        "saveassistant": ass_num,
    }
    await save_assistant(message.chat.id, "assistant", assis)
    await message.reply_text(
        f"**Merubah Asisten**\n\nAkun Asisten berubah dari **{ass}** menjadi Asisten nomer **{ass_num}**"
    )


ass_num_list2 = ["1", "2", "3", "4", "5", "Random"]


@app.on_message(filters.command("setassistant") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Penggunaan:**\n/setassistant [ASS_NO or Random]\n\nPilih dari mereka\n{' | '.join(ass_num_list2)}\n\nGunakan 'Random' untuk mengatur Asisten secara acak"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    query = message.text.split(None, 1)[1].strip()
    if query not in ass_num_list2:
        return await message.reply_text(usage)
    if str(query) == "Random":
        ran_ass = random.choice(random_assistant)
    else:
        ran_ass = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        await message.reply_text(
            f"**__Asisten Ndi Music Bot diberikan__**\n\nNo. Asisten **{ran_ass}**"
        )
        assis = {
            "saveassistant": ran_ass,
        }
        await save_assistant(message.chat.id, "assistant", assis)
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Nomer Asisten tersimpan sebelumnya {ass} ditemukan.\n\nKamu bisa mengubah asisten melalui /changeassistant"
        )


@app.on_message(filters.command("checkassistant") & filters.group)
async def check_ass(_, message: Message):
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Asisten Tidak Ditemukan.\n\nKamu bisa mengatur Asisten melalui /play"
        )
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Asisten yang tersimpan sebelumnya ditemukan\n\nNomer Asisten {ass} "
        )
