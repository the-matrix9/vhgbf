import asyncio
from datetime import datetime
from platform import python_version

from pyrogram import __version__, filters, Client
from pyrogram.types import Message
from config import ALIVE_PIC, ALIVE_TEXT
from UTTAM import START_TIME, SUDO_USER
from UTTAM.helper.PyroHelpers import ReplyCheck
from UTTAM.plugins.help import add_command_help
from UTTAM.plugins.bot.inline import get_readable_time


# Default Alive Image
alive_logo = ALIVE_PIC or "https://files.catbox.moe/svssj2.jpg"

# Alive text with your updated links
if ALIVE_TEXT:
    txt = ALIVE_TEXT
else:
    txt = (
        f"**🌸 ʀᴀᴅʜᴇ ᴋʀɪꜱʜɴᴀ 🌸**\n\n"
        f"❏ **ᴠᴇʀsɪᴏɴ:** `2.1`\n"
        f"├• **ᴜᴘᴛɪᴍᴇ:** `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"├• **ᴘʏᴛʜᴏɴ:** `{python_version()}`\n"
        f"├• **ᴘʏʀᴏɢʀᴀᴍ:** `{__version__}`\n"
        f"├• **sᴜᴘᴘᴏʀᴛ:** [ʙᴏᴛᴍɪɴᴇ sᴜᴘᴘᴏʀᴛ](https://t.me/BOTMINE_SUPPORT)\n"
        f"├• **ᴜᴘᴅᴀᴛᴇs:** [ʙᴏᴛᴍɪɴᴇ ᴛᴇᴄʜ](https://t.me/BOTMINE_TECH)\n"
        f"└• **ᴍᴀsᴛᴇʀ:** [ʀᴀᴅʜᴇ](https://t.me/Overloadego)"
    )


# ALIVE COMMAND
@Client.on_message(
    filters.command(["alive", "python"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def alive(client: Client, message: Message):
    xx = await message.reply_text("⚡️")
    try:
        await message.delete()
    except:
        pass

    send = client.send_video if alive_logo.endswith(".mp4") else client.send_photo
    caption = txt

    try:
        await asyncio.gather(
            xx.delete(),
            send(
                message.chat.id,
                alive_logo,
                caption=caption,
                reply_to_message_id=ReplyCheck(message),
            ),
        )
    except BaseException:
        await xx.edit(caption, disable_web_page_preview=True)


# REPO COMMAND
@Client.on_message(filters.command("repo", ".") & filters.me)
async def repo(bot: Client, message: Message):
    await message.edit("⚡")
    await asyncio.sleep(1)
    await message.edit("Fetching Source Code.....")
    await asyncio.sleep(1)
    await message.edit("Sorry meri jaan, repo chahiye to DM kar lo 👉 [Overloadego](https://t.me/Overloadego)")


# CREATOR COMMAND
@Client.on_message(filters.command("creator ", ".") & filters.me)
async def creator(bot: Client, message: Message):
    await message.edit("Creator: [Overloadego](https://t.me/Overloadego)", disable_web_page_preview=True)


# UPTIME COMMAND
@Client.on_message(filters.command(["uptime", "up"], ".") & filters.me)
async def uptime(bot: Client, message: Message):
    now = datetime.now()
    current_uptime = now - START_TIME
    await message.edit(f"**Uptime ⚡**\n```{str(current_uptime).split('.')[0]}```")


# ID COMMAND
@Client.on_message(filters.command("id", ".") & filters.me)
async def get_id(bot: Client, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"**File ID:** `{rep.audio.file_id}`\n**File Type:** `audio`"
        elif rep.document:
            file_id = f"**File ID:** `{rep.document.file_id}`\n**File Type:** `{rep.document.mime_type}`"
        elif rep.photo:
            file_id = f"**File ID:** `{rep.photo.file_id}`\n**File Type:** `photo`"
        elif rep.sticker:
            file_id = f"**Sticker ID:** `{rep.sticker.file_id}`\n"
            file_id += f"**Set:** `{rep.sticker.set_name}`\n**Emoji:** `{rep.sticker.emoji}`"
        elif rep.video:
            file_id = f"**File ID:** `{rep.video.file_id}`\n**File Type:** `video`"
        elif rep.animation:
            file_id = f"**File ID:** `{rep.animation.file_id}`\n**File Type:** `GIF`"
        elif rep.voice:
            file_id = f"**File ID:** `{rep.voice.file_id}`\n**File Type:** `Voice Note`"
        elif rep.video_note:
            file_id = f"**File ID:** `{rep.video_note.file_id}`\n**File Type:** `Video Note`"
        elif rep.location:
            file_id = (
                f"**Location:**\n"
                f"Longitude: `{rep.location.longitude}`\n"
                f"Latitude: `{rep.location.latitude}`"
            )
        elif rep.venue:
            file_id = (
                f"**Venue:**\n"
                f"Title: `{rep.venue.title}`\n"
                f"Address: `{rep.venue.address}`\n"
                f"Longitude: `{rep.venue.location.longitude}`\n"
                f"Latitude: `{rep.venue.location.latitude}`"
            )

        if rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        user_detail = f"**User ID:** `{user_id}`\n**Message ID:** `{message.reply_to_message.id}`"
        if file_id:
            user_detail += f"\n\n{file_id}"
        await message.edit(user_detail)
    elif file_id:
        await message.edit(file_id)
    else:
        await message.edit(f"**Chat ID:** `{message.chat.id}`")


# HELP SECTION
add_command_help(
    "radhe",
    [
        [".alive", "Check if Radhe bot is alive or not."],
        [".repo", "Get repo info of Radhe bot."],
        [".creator", "Show the creator of Radhe bot."],
        [".id", "Fetch IDs of user or files."],
        [".uptime", "Check Radhe bot uptime."],
    ],
)

add_command_help(
    "restart",
    [
        [".restart", "Restart Radhe bot instantly."],
    ],
)
