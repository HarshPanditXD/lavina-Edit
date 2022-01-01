# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from driver.utils import bash
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query: str):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'youtube-dl -g -f "{format}" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝐆𝐫𝐨𝐮𝐩 𝟏𝐬𝐭⭐️", url="t.me/UNIQUE_SOCIETY"),
                InlineKeyboardButton("𝐆𝐫𝐨𝐮𝐩 𝟐𝐬𝐭🌟", url="t.me/All_Dear_Comrade")
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"❔*𝐌𝐢𝐬𝐬𝐢𝐧𝐠 𝐀𝐝𝐦𝐢𝐧 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧*🌹*:\n\n» ✌️ __𝑫𝒆𝒍𝒆𝒕𝒆 𝑴𝒂𝒔𝒔𝒂𝒈𝒆__\n» ✌️ __𝑨𝒅𝒅 𝑼𝒔𝒆𝒓__\n» ✌️ __🌹𝑴𝒂𝒏𝒂𝒈𝒆 𝑽𝒐𝒊𝒄𝒆 𝑪𝒉𝒂𝒕✨__\n\n𝑫𝒂𝒕𝒂 𝒊𝒔 **✌️𝑼𝒑𝒅𝒂𝒕𝒆✨**💫𝑨𝒖𝒕𝒐𝒎𝒂𝒕𝒊𝒄𝒂𝒍𝒍𝒚 𝑨𝒇𝒕𝒆𝒓 𝒀𝒐𝒖✨ **𝑷𝒓𝒐𝒎𝒐𝒕𝒆 𝑴𝒆**"
        )
        return
    if not a.can_manage_voice_chats:
        await m.reply_text(
            "🔰𝐌𝐢𝐬𝐬𝐢𝐧𝐠 𝐀𝐝𝐦𝐢𝐧 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧❔:" + "\n\n» ✌️ __𝑴𝒂𝒏𝒂𝒈𝒆 𝑽𝒐𝒊𝒄𝒆 𝑪𝒉𝒂𝒕__"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "💫𝐌𝐢𝐬𝐬𝐢𝐧𝐠 𝐀𝐝𝐦𝐢𝐧 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧❔:" + "\n\n» 🗑️ __𝑫𝒆𝒍𝒆𝒕𝒆 𝑴𝒂𝒔𝒔𝒂𝒈𝒆__"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("⚡𝐌𝐢𝐬𝐬𝐢𝐧𝐠 𝐀𝐝𝐦𝐢𝐧 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧✨:" + "\n\n» ✌️ __𝑨𝒅𝒅 𝑼𝒔𝒆𝒓__")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **☠️ 𝐈𝐬 𝐁𝐚𝐧𝐧𝐞𝐝 🏜️ 𝐈𝐧 𝐆𝐫𝐨𝐮𝐩 🙀** {m.chat.title}**"
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"💫 *𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐅𝐚𝐢𝐥𝐞𝐝 ☠️ 𝐓𝐨 𝐉𝐨𝐢𝐧 🌟*\n\n**✌️ 𝐑𝐞𝐚𝐬𝐨𝐧 ✨**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"💫 *𝐔𝐬𝐞𝐫𝐛𝐨𝐭 𝐓𝐨 𝐉𝐨𝐢𝐧 💫**\n\n**⚡ 𝐑𝐞𝐚𝐬𝐨𝐧 ✨**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥🎸*𝐝𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐚𝐮𝐝𝐢𝐨☠️💫...**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"**𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💭 **𝐂𝐡𝐚𝐭:** `{chat_id}`\n🎧 **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
            else:
             try:
                await suhu.edit("*🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰ </𝐎ꜰꜰʟɪɴᴇ> ‌[𝐀ꜰᴋ] ☠️ ❱...*")
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"**𝐍𝐚𝐦𝐞:** [{songname}]({link})\n💭 **𝐂𝐡𝐚𝐭:** `{chat_id}`\n💡 **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲:** {requester}",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫𝐄𝐫𝐫𝐨𝐫❔:\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "**❔𝐀𝐮𝐝𝐢𝐨 𝐅𝐢𝐥𝐞✨** or **😂𝐆𝐢𝐯𝐞 𝐒𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 💫 𝐓𝐨 😇 𝐒𝐞𝐚𝐫𝐜𝐡 𝐒𝐨𝐧𝐠✨🙀.**"
                )
            else:
                suhu = await c.send_message(chat_id, "🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰</𝐎ꜰꜰʟɪɴᴇ> ‌[𝐀ꜰᴋ]☠️ ❱...**")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("*✌𝐖𝐡𝐚𝐭'𝐒 𝐓𝐡𝐞 ❤️ 𝐒𝐨𝐧𝐠 🎸 𝐘𝐨𝐮 🎧 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️*")
                else:
                    songname = search[0]
                    url = search[1]
                    duration = search[2]
                    thumbnail = search[3]
                    format = "bestaudio[ext=m4a]"
                    veez, ytlink = await ytdl(format, url)
                    if veez == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"**𝐍𝐚𝐦𝐞:** [{songname}]({url})\n**⏱ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:** `{duration}`\n🎧 **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await suhu.edit("*🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰ </𝐎ꜰꜰʟɪɴᴇ> ‌[𝐀ꜰᴋ]🌹 ☠️ ❱...*")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=thumbnail,
                                    caption=f"**𝐍𝐚𝐦𝐞:** [{songname}]({url})\n**⏱ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:** `{duration}`\n✌️ **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫єгг๏г❔: `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "*💫𝐆𝐢𝐯𝐞 𝐒𝐨𝐦𝐞𝐭𝐡𝐢𝐧𝐠 🎸 𝐓𝐨 🎧 𝐒𝐞𝐚𝐫𝐜𝐡 𝐒𝐨𝐧𝐠💫*"
            )
        else:
            suhu = await c.send_message(chat_id, "*🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 💫 𝐓𝐡𝐞 𝐒𝐨𝐧𝐠 ❤️ ❰ 𝐀 𝐋 𝐎 𝐍 𝐄 ♪ ☠️ ❱...*")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("*✌𝐖𝐡𝐚𝐭'𝐒 𝐓𝐡𝐞 ❤️ 𝐒𝐨𝐧𝐠 🎸 𝐘𝐨𝐮 🎧 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐏𝐥𝐚𝐲 ▶ ❤️*")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                format = "bestaudio[ext=m4a]"
                veez, ytlink = await ytdl(format, url)
                if veez == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=thumbnail,
                            caption=f"*𝐍𝐚𝐦𝐞:** [{songname}]({url})\n**⏱ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:** `{duration}`\n🎧 **𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit("*✌️𝐉𝐨𝐢𝐧𝐢𝐧𝐠 🎸 𝐯𝐜 💫 𝐒𝐨𝐧𝐠 ❤️ 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 🏜️*")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=thumbnail,
                                caption=f"**𝐍𝐚𝐦𝐞:** [{songname}]({url})\n**⏱ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:** `{duration}`\n💡**𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐁𝐲:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫ҽɾɾօɾ❔: `{ep}`")
