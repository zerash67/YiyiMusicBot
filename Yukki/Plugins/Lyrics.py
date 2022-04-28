import os
import re

import lyricsgenius
from pyrogram import Client, filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch

from Yukki import MUSIC_BOT_NAME, app

__MODULE__ = "Lyrics"
__HELP__ = """

/Lyrics [Nama Musik]
- Mencari Lirik untuk Musik tertentu di web.
**Catatan**:
Tombol sebaris Lirik memiliki beberapa bug. Pencarian hanya 50% hasil. Anda dapat menggunakan perintah sebagai gantinya jika Anda ingin lirik untuk musik apa pun yang diputar.
"""


@app.on_callback_query(filters.regex(pattern=r"lyrics"))
async def lyricssex(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    try:
        id, user_id = callback_request.split("|")
    except Exception as e:
        return await CallbackQuery.message.edit(
            f"Terjadi Kesalahan\n**Kemungkinan Alasannya Bisa**:{e}"
        )
    url = f"https://www.youtube.com/watch?v={id}"
    print(url)
    try:
        results = VideosSearch(url, limit=1)
        for result in results.result()["result"]:
            title = result["title"]
    except Exception as e:
        return await CallbackQuery.answer(
            "Suara tidak ditemukan. Masalah YouTube.", show_alert=True
        )
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    t = re.sub(r"[^\w]", " ", title)
    y.verbose = False
    S = y.search_song(t, get_full_info=False)
    if S is None:
        return await CallbackQuery.answer(
            "Lirik tidak ditemukan 🥺", show_alert=True
        )
    await CallbackQuery.message.delete()
    userid = CallbackQuery.from_user.id
    usr = f"[{CallbackQuery.from_user.first_name}](tg://user?id={userid})"
    xxx = f"""
**Pencarian Lirik Dipersembahkan oleh {MUSIC_BOT_NAME}**

**Dicari Oleh:-** {usr}
**Lagu yang dicari:-** __{title}__

**Menemukan Lirik Untuk:-** __{S.title}__
**Penyanyi:-** {S.artist}

**__Lirik:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await CallbackQuery.message.reply_document(
            document=filename,
            caption=f"**KELUARAN:**\n\n`Lirik`",
            quote=False,
        )
        os.remove(filename)
    else:
        await CallbackQuery.message.reply_text(xxx)


@app.on_message(filters.command("lyrics"))
async def lrsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**Penggunaan:**\n\n/lirik [ Nama Musik]")
    m = await message.reply_text("Pencarian Lirik")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("Lirik tidak ditemukan 🥺")
    xxx = f"""
**Pencarian Lirik dipersembahkan oleh {MUSIC_BOT_NAME}**

**Lagu yang dicari:-** __{query}__
**Menemukan Lirik untuk:-** __{S.title}__
**Penyanyi:-** {S.artist}

**__Lirik:__**

{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**KELUARAN:**\n\n`Lirik`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)
