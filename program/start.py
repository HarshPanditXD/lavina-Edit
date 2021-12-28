from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.veez import user
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **Welcome {message.from_user.mention()} !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **Allows you to play music and video on groups through the new Telegram's video chats!**

🔖 **To know how to use this bot, please click on the » ❓ Basic Guide button!**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕𝐀𝐃𝐃 𝐌𝐄 𝐓𝐎 𝐆𝐑𝐎𝐔𝐏➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],                
                [
                    InlineKeyboardButton("❔𝐂𝐎𝐌𝐌𝐀𝐍𝐃🔐", callback_data="cbcmds"),
                    InlineKeyboardButton("📣𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑💫", url=f"https://t.me/log_afk"),
                ],
                [
                    InlineKeyboardButton(
                        "🍀𝐒𝐔𝐏𝐏𝐎𝐑𝐓📪", url=f"https://t.me/UNIQUE_SOCIETY"
                    ),
                    InlineKeyboardButton(
                        "📩 𝐆𝐑𝐎𝐔𝐏 📩", url=f"https://t.me/ALL_DEAR_COMRADE"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🍀𝐎𝐖𝐍𝐄𝐑✨", url="https://t.me/EVIL_XD_BOY"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🍀𝐒𝐔𝐏𝐏𝐎𝐑𝐓📪", url=f"https://t.me/UNIQUE_SOCIETY"),
                InlineKeyboardButton(
                    "📩 𝐆𝐑𝐎𝐔𝐏 📩", url=f"https://t.me/All_Dear_comrade"
                ),
            ]
        ]
    )

    alive = f"**𝗛𝗲𝗹𝗹𝗼 {message.from_user.mention()}, i'm {BOT_NAME}**\n\n✨ 𝗕𝗼𝘁 𝗶𝘀 𝘄𝗼𝗿𝗸𝗶𝗻𝗴 𝗻𝗼𝗿𝗺𝗮𝗹𝗹𝘆\n🍀 My Master: [𝐋𝐎𝐆 𝐀𝐅𝐊](https://t.me/Log_afk)\n✨ Bot Version: `v{__version__}`\n🍀 Pyrogram Version: `{pyrover}`\n✨ Python Version: `{__python_version__}`\n🍀 PyTgCalls version: `{pytover.__version__}`\n✨ Uptime Status: `{uptime}`\n\n**𝗧𝗵𝗮𝗻𝗸𝘀 𝗳𝗼𝗿 𝗔𝗱𝗱𝗶𝗻𝗴 𝗺𝗲 𝗵𝗲𝗿𝗲, 𝗳𝗼𝗿 𝗽𝗹𝗮𝘆𝗶𝗻𝗴 𝘃𝗶𝗱𝗲𝗼 & 𝗺𝘂𝘀𝗶𝗰 𝗼𝗻 𝘆𝗼𝘂𝗿 𝗚𝗿𝗼𝘂𝗽'𝘀 𝗔𝘂𝗱𝗶𝗼 𝗰𝗵𝗮𝘁** ❤"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 bot status:\n"
        f"• **uptime:** `{uptime}`\n"
        f"• **start time:** `{START_TIME_ISO}`"
    )


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ **𝑻𝒉𝒂𝒏𝒌𝒔 𝒇𝒐𝒓 𝒂𝒅𝒅𝒊𝒏𝒈 𝒎𝒆 𝒕𝒐 𝒕𝒉𝒆 𝑮𝒓𝒐𝒖𝒑 !**\n\n"
                "**✤Promote✤ ✤me✤ ✤as✤ ✤administrator✤ ✤of✤ ✤the✤ ✤Group✤, ❁otherwise❁ ❁I❁ ❁will❁ ❁not❁ ❁be❁ ❁able❁ ❁to❁ ❁work❁ ❁properly❁, ✤and✤ ✤don't✤ ✤forget✤ ✤to✤ ✤type✤ /userbotjoin ❀for❀ ❀invite❀ ❀the❀ ❀assistant❀.**\n\n"
                "**Once done, type** /reload",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🍀𝐒𝐔𝐏𝐏𝐎𝐑𝐓📪", url=f"https://t.me/UNIQUE_SOCIETY"),
                            InlineKeyboardButton("📩𝐆𝐑𝐎𝐔𝐏📩", url=f"https://t.me/ALL_DEAR_COMRADE")
                        ],
                        [
                            InlineKeyboardButton("👤𝐀𝐒𝐒𝐈𝐒𝐓𝐀𝐍𝐓💫", url=f"https://t.me/{ass_uname}")
                        ]
                    ]
                )
            )
