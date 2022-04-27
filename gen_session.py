import asyncio

from pyrogram import Client as c

API_ID = input("\nMasukkan API_ID kamu:\n > ")
API_HASH = input("\nMasukkan API_HASH kamu:\n > ")

print("\n\n Masukkan nomer telepon akun jika ditanyakan.\n\n")

i = c(":memory:", api_id=API_ID, api_hash=API_HASH)


async def main():
    await i.start()
    ss = await i.export_session_string()
    print("\nINI STRING SESSION KAMU, COPY INI, JANGAN DISEBARKAN!!\n")
    print(f"\n{ss}\n")


asyncio.run(main())
