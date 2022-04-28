from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from config import MUSIC_BOT_NAME, SUPPORT_CHANNEL, SUPPORT_GROUP
from Yukki import BOT_USERNAME


def setting_markup2():
    buttons = [
        [
            InlineKeyboardButton(text="🔈 ᴋᴜᴀʟɪᴛᴀs sᴜᴀʀᴀ", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 ᴠᴏʟᴜᴍᴇ sᴜᴀʀᴀ", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 ᴘᴇʀɪᴊɪɴᴀɴ", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 ᴅᴀsʜʙᴏᴀʀᴅ", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ ᴛᴜᴛᴜᴘ", callback_data="close"),
        ],
    ]
    return f"⚙️  **{MUSIC_BOT_NAME} ᴘᴇɴɢᴀᴛᴜʀᴀɴ**", buttons


def start_pannel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="📋 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ᴘᴇɴɢᴀᴛᴜʀᴀɴ", callback_data="settingm"
                )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="📋 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ᴘᴇɴɢᴀᴛᴜʀᴀɴ", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨ɢʀᴏᴜᴘ", url=f"{SUPPORT_GROUP}"
                ),
            ],
            [
                 InlineKeyboardButton(
                    text="🥸 ᴏᴡɴᴇʀ 🥸", 
                url=f"https://t.me/gausahsokablunyet",
               )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="📋 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ᴘᴇɴɢᴀᴛᴜʀᴀɴ", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢ᴄʜᴀɴɴᴇʟ", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
            [
                 InlineKeyboardButton(
                    text="🥸 ᴏᴡɴᴇʀ 🥸", 
                url=f"https://t.me/gausahsokablunyet",
               )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="📋 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ", callback_data="shikhar"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔧 ᴘᴇɴɢᴀᴛᴜʀᴀɴ", callback_data="settingm"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢ᴄʜᴀɴɴᴇʟ", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨ɢʀᴏᴜᴘ", url=f"{SUPPORT_GROUP}"
                ),
            ],
            [
                 InlineKeyboardButton(
                    text="🥸 ᴏᴡɴᴇʀ 🥸", 
                url=f"https://t.me/gausahsokablunyet",
               )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}**", buttons


def private_panel():
    if not SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ɢʀᴏᴜᴘ",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}**", buttons
    if not SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ɢʀᴏᴜᴘ",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📨ɢʀᴏᴜᴘ", url=f"{SUPPORT_GROUP}"
                ),
            ],
            [
                 InlineKeyboardButton(
                    text="🥸 ᴏᴡɴᴇʀ 🥸", 
                url=f"https://t.me/gausahsokablunyet",
               )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}*", buttons
    if SUPPORT_CHANNEL and not SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ɢʀᴏᴜᴘ",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢ᴄʜᴀɴɴᴇʟ", url=f"{SUPPORT_CHANNEL}"
                ),
            ],
            [
                 InlineKeyboardButton(
                    text="🥸 ᴏᴡɴᴇʀ 🥸", 
                url=f"https://t.me/gausahsokablunyet",
               )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}**", buttons
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons = [
            [
                InlineKeyboardButton(
                    text="🗂 ᴍᴇɴᴜ ᴘᴇʀɪɴᴛᴀʜ",
                    callback_data="search_helper_mess",
                ),
            ],
            [
                InlineKeyboardButton(
                    "➕ ᴛᴀᴍʙᴀʜᴋᴀɴ sᴀʏᴀ ᴋᴇ ɢʀᴏᴜᴘ",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📢ᴄʜᴀɴɴᴇʟ", url=f"{SUPPORT_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="📨ɢʀᴏᴜᴘ", url=f"{SUPPORT_GROUP}"
                ),
            ],
            [
                 InlineKeyboardButton(
                    text="🥸 ᴏᴡɴᴇʀ 🥸", 
                url=f"https://t.me/gausahsokablunyet",
               )
            ],
        ]
        return f"🎛  **sᴀʏᴀ ᴀᴅᴀʟᴀʜ {MUSIC_BOT_NAME}**", buttons


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="🔈 ᴋᴜᴀʟɪᴛᴀs sᴜᴀʀᴀ", callback_data="AQ"),
            InlineKeyboardButton(text="🎚 ᴠᴏʟᴜᴍᴇ sᴜᴀʀᴀ", callback_data="AV"),
        ],
        [
            InlineKeyboardButton(
                text="👥 ᴘᴇʀɪᴊɪɴᴀɴ", callback_data="AU"
            ),
            InlineKeyboardButton(
                text="💻 ᴅᴀsʜʙᴏᴀʀᴅ", callback_data="Dashboard"
            ),
        ],
        [
            InlineKeyboardButton(text="✖️ ᴛᴜᴛᴜᴘ", callback_data="close"),
            InlineKeyboardButton(text="≼ ᴋᴇᴍʙᴀʟɪ", callback_data="okaybhai"),
        ],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ᴘᴇɴɢᴀᴛᴜʀᴀɴ**", buttons


def volmarkup():
    buttons = [
        [
            InlineKeyboardButton(
                text="🔄 ᴀᴛᴜʀ ᴜʟᴀɴɢ ᴠᴏʟᴜᴍᴇ 🔄", callback_data="HV"
            )
        ],
        [
            InlineKeyboardButton(text="🔈 ᴠᴏʟ ʀᴇɴᴅᴀʜ", callback_data="LV"),
            InlineKeyboardButton(text="🔉 ᴠᴏʟ sᴇᴅᴀɴɢ", callback_data="MV"),
        ],
        [
            InlineKeyboardButton(text="🔊 ᴠᴏʟ ᴛɪɴɢɢɪ", callback_data="HV"),
            InlineKeyboardButton(text="🔈 ᴠᴏʟ sᴇɪᴍʙᴀɴɢ", callback_data="VAM"),
        ],
        [
            InlineKeyboardButton(
                text="🔽 ᴠᴏʟᴜᴍᴇ ᴋᴜsᴛᴏᴍ 🔽", callback_data="Custommarkup"
            )
        ],
        [InlineKeyboardButton(text="≼ ᴋᴇᴍʙᴀʟɪ", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ᴘᴇɴɢᴀᴛᴜʀᴀɴ**", buttons


def custommarkup():
    buttons = [
        [
            InlineKeyboardButton(text="+10", callback_data="PTEN"),
            InlineKeyboardButton(text="-10", callback_data="MTEN"),
        ],
        [
            InlineKeyboardButton(text="+25", callback_data="PTF"),
            InlineKeyboardButton(text="-25", callback_data="MTF"),
        ],
        [
            InlineKeyboardButton(text="+50", callback_data="PFZ"),
            InlineKeyboardButton(text="-50", callback_data="MFZ"),
        ],
        [InlineKeyboardButton(text="🔼 ᴠᴏʟᴜᴍᴇ ᴋᴜsᴛᴏᴍ 🔼", callback_data="AV")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ᴘᴇɴɢᴀᴛᴜʀᴀɴ**", buttons


def usermarkup():
    buttons = [
        [
            InlineKeyboardButton(text="👥 sᴇᴍᴜᴀ", callback_data="EVE"),
            InlineKeyboardButton(text="🤴 ᴀᴅᴍɪɴ", callback_data="AMS"),
        ],
        [
            InlineKeyboardButton(
                text="📖 ᴅᴀғᴛᴀʀ ᴘᴇʀɪᴊɪɴᴀɴ", callback_data="USERLIST"
            )
        ],
        [InlineKeyboardButton(text="≼ ᴋᴇᴍʙᴀʟɪ", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ᴘᴇɴɢᴀᴛᴜʀᴀɴ**", buttons


def dashmarkup():
    buttons = [
        [
            InlineKeyboardButton(text="✔️ Uptime", callback_data="UPT"),
            InlineKeyboardButton(text="💾 Ram", callback_data="RAT"),
        ],
        [
            InlineKeyboardButton(text="💻 Cpu", callback_data="CPT"),
            InlineKeyboardButton(text="💽 Disk", callback_data="DIT"),
        ],
        [InlineKeyboardButton(text="≼ ᴋᴇᴍʙᴀʟɪ", callback_data="settingm")],
    ]
    return f"🔧  **{MUSIC_BOT_NAME} ᴘᴇɴɢᴀᴛᴜʀᴀɴ**", buttons
