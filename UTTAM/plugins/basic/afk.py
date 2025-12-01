import asyncio
from datetime import datetime

import humanize
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from UTTAM.helper.PyroHelpers import GetChatID, ReplyCheck
from UTTAM.plugins.help import add_command_help


# ==============================
#  GLOBAL VARIABLES
# ==============================
AFK = False
AFK_REASON = ""
AFK_TIME = ""
USERS = {}
GROUPS = {}


# ==============================
#  TIME FORMATTER
# ==============================
def subtract_time(start, end):
    return humanize.naturaltime(start - end)


# ==============================
#  AUTO REPLY WHEN AFK
# ==============================
@Client.on_message(
    ((filters.group & filters.mentioned) | filters.private) & ~filters.me & ~filters.service,
    group=3
)
async def afk_auto_reply(bot: Client, message: Message):

    if not AFK:
        return

    last_seen = subtract_time(datetime.now(), AFK_TIME)
    is_group = message.chat.type in ["group", "supergroup"]
    STORAGE = GROUPS if is_group else USERS
    chat_id = GetChatID(message)

    # First message from user/group
    if chat_id not in STORAGE:
        text = (
            f"**⚠️ ᴀꜰᴋ ᴀʟᴇʀᴛ**\n"
            f"━━━━━━━━━━━━━━\n"
            f"💤 **ɪ'ᴍ ᴀꜰᴋ ʀɪɢʜᴛ ɴᴏᴡ**\n"
            f"⌛ **ʟᴀꜱᴛ ꜱᴇᴇɴ:** `{last_seen}`\n"
            f"📝 **ʀᴇᴀꜱᴏɴ:** `{AFK_REASON or '—'}`\n"
            f"━━━━━━━━━━━━━━"
        )
        await bot.send_message(chat_id, text, reply_to_message_id=ReplyCheck(message))
        STORAGE[chat_id] = 1
        return

    # Limit spam
    STORAGE[chat_id] += 1

    if STORAGE[chat_id] in [5, 10, 20, 50]:
        text = (
            f"**🔔 ꜱᴛɪʟʟ ᴀꜰᴋ!**\n"
            f"⌛ `{last_seen}`\n"
            f"📝 `{AFK_REASON or '—'}`"
        )
        await bot.send_message(chat_id, text, reply_to_message_id=ReplyCheck(message))


# ==============================
#  AFK SET (.afk / /afk / !afk)
# ==============================
@Client.on_message(filters.command("afk", prefixes=[".", "/", "!"]) & filters.me, group=3)
async def afk_on(bot: Client, message: Message):
    global AFK, AFK_REASON, AFK_TIME

    reason = " ".join(message.command[1:]) if len(message.command) > 1 else ""

    AFK = True
    AFK_REASON = reason
    AFK_TIME = datetime.now()

    await message.edit("**💤 ᴀꜰᴋ ᴍᴏᴅᴇ ᴀᴄᴛɪᴠᴀᴛᴇᴅ...**")
    await asyncio.sleep(1)
    await message.delete()


# ==============================
#  AUTO AFK UNSET (You Send Msg)
# ==============================
@Client.on_message(filters.me, group=3)
async def auto_afk_off(bot: Client, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if not AFK:
        return

    last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
    total_msgs = sum(USERS.values()) + sum(GROUPS.values())
    total_chats = len(USERS) + len(GROUPS)

    reply = await message.reply(
        f"**🟢 ᴀꜰᴋ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ**\n"
        f"━━━━━━━━━━━━━━\n"
        f"⏳ **ᴅᴜʀᴀᴛɪᴏɴ:** {last_seen}\n"
        f"💬 **ᴍᴇꜱꜱᴀɢᴇꜱ:** `{total_msgs}`\n"
        f"👥 **ᴄʜᴀᴛꜱ:** `{total_chats}`\n"
        f"━━━━━━━━━━━━━━"
    )

    # RESET DATA
    AFK = False
    AFK_TIME = ""
    AFK_REASON = ""
    USERS = {}
    GROUPS = {}

    await asyncio.sleep(5)
    await reply.delete()


# ==============================
#  HELP MENU
# ==============================
add_command_help(
    "afk",
    [
        [".afk /afk !afk <reason>", "ᴇɴᴀʙʟᴇꜱ ᴀꜰᴋ ᴍᴏᴅᴇ ᴡɪᴛʜ ᴏᴘᴛɪᴏɴᴀʟ ʀᴇᴀꜱᴏɴ."],
        ["ᴀꜰᴋ ᴏꜰꜰ", "ᴀᴜᴛᴏ ᴅɪꜱᴀʙʟᴇꜱ ᴡʜᴇɴ ʏᴏᴜ ꜱᴇɴᴅ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ."],
    ],
)
