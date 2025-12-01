from asyncio import gather
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import Message

from UTTAM.helper.PyroHelpers import ReplyCheck
from UTTAM.plugins.basic.profile import extract_user
from UTTAM.plugins.help import add_command_help


# Allowed prefixes
PREFIX = ["!", "/", "."]


def multi_cmd(commands):
    return filters.command(commands, PREFIX)


# ============================================
#  ᴜꜱᴇʀ ɪɴꜰᴏ  — (.ɪɴꜰᴏ / !ɪɴꜰᴏ / /ɪɴꜰᴏ)
# ============================================

@Client.on_message(multi_cmd(["whois", "info"]) & filters.me)
async def who_is(client: Client, message: Message):

    # Auto detect:
    # reply → that user
    # argument → that user
    # none → yourself
    user_id = await extract_user(message)
    if not user_id:
        user_id = message.from_user.id   # auto self

    ex = await message.edit_text("`ᴘʀᴏᴄᴇꜱꜱɪɴɢ...`")

    try:
        user = await client.get_users(user_id)

        username = f"@{user.username}" if user.username else "—"
        first_name = user.first_name or "—"
        last_name = user.last_name or "—"
        fullname = f"{first_name} {last_name}".strip()

        bio = (await client.get_chat(user.id)).bio or "—"
        status_raw = f"{user.status}"

        status = (
            status_raw.replace("UserStatus.", "").capitalize()
            if "UserStatus" in status_raw else "—"
        )

        dc_id = user.dc_id or "—"
        mutual = await client.get_common_chats(user.id)

        out = f"""
<b>🚩 ᴜꜱᴇʀ ɪɴꜰᴏ 🚩</b>
━━━━━━━━━━━━━━━━━━

◆ <b>ᴜꜱᴇʀ ɪᴅ:</b> <code>{user.id}</code>
◆ <b>ɴᴀᴍᴇ:</b> {fullname}
◆ <b>ᴜꜱᴇʀɴᴀᴍᴇ:</b> {username}
◆ <b>ᴅᴄ ɪᴅ:</b> <code>{dc_id}</code>

◆ <b>ᴘʀᴇᴍɪᴜᴍ:</b> <code>{user.is_premium}</code>
◆ <b>ᴠᴇʀɪꜰɪᴇᴅ:</b> <code>{user.is_verified}</code>
◆ <b>ꜱᴄᴀᴍ:</b> <code>{user.is_scam}</code>
◆ <b>ʀᴇꜱᴛʀɪᴄᴛᴇᴅ:</b> <code>{user.is_restricted}</code>
◆ <b>ʙᴏᴛ ᴜꜱᴇʀ:</b> <code>{user.is_bot}</code>

◆ <b>ʟᴀꜱᴛ ꜱᴇᴇɴ:</b> <code>{status}</code>
◆ <b>ᴍᴜᴛᴜᴀʟ ɢʀᴏᴜᴘꜱ:</b> <code>{len(mutual)}</code>

◆ <b>ʙɪᴏ:</b> <code>{bio}</code>

━━━━━━━━━━━━━━━━━━
🔗 <b>ᴘʀᴏꜰɪʟᴇ ʟɪɴᴋ:</b> <a href='tg://user?id={user.id}'>{fullname}</a>
"""

        await ex.edit(out, disable_web_page_preview=True)

    except Exception as e:
        return await ex.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


# ============================================
#  ɢʀᴏᴜᴘ ɪɴꜰᴏ (.ᴄʜᴀᴛɪɴꜰᴏ / !ᴄʜᴀᴛɪɴꜰᴏ / /ᴄʜᴀᴛɪɴꜰᴏ)
# ============================================

@Client.on_message(multi_cmd(["chatinfo", "cinfo", "ginfo"]) & filters.me)
async def chatinfo_handler(client: Client, message: Message):

    ex = await message.edit_text("`ᴘʀᴏᴄᴇꜱꜱɪɴɢ...`")

    try:
        if len(message.command) > 1:
            chat = await client.get_chat(message.command[1])
        else:
            if message.chat.type == ChatType.PRIVATE:
                return await ex.edit("**ᴜꜱᴇ ɪɴ ᴀ ɢʀᴏᴜᴘ ᴏʀ ᴘᴀꜱꜱ ɢʀᴏᴜᴘ ɪᴅ!**")

            chat = await client.get_chat(message.chat.id)

        chat_type = str(chat.type).replace("ChatType.", "").capitalize()
        username = f"@{chat.username}" if chat.username else "—"
        description = chat.description or "—"
        dc_id = chat.dc_id or "—"

        out = f"""
<b>🏛️ ɢʀᴏᴜᴘ ɪɴꜰᴏ ᴘᴀɴᴇʟ 🏛️</b>
━━━━━━━━━━━━━━━━━━

◎ <b>ɢʀᴏᴜᴘ ɪᴅ:</b> <code>{chat.id}</code>
◎ <b>ᴛɪᴛʟᴇ:</b> {chat.title}
◎ <b>ᴜꜱᴇʀɴᴀᴍᴇ:</b> {username}
◎ <b>ᴛʏᴘᴇ:</b> <code>{chat_type}</code>

◎ <b>ᴅᴄ ɪᴅ:</b> <code>{dc_id}</code>
◎ <b>ꜱᴄᴀᴍ:</b> <code>{chat.is_scam}</code>
◎ <b>ꜰᴀᴋᴇ:</b> <code>{chat.is_fake}</code>
◎ <b>ᴠᴇʀɪꜰɪᴇᴅ:</b> <code>{chat.is_verified}</code>

◎ <b>ʀᴇꜱᴛʀɪᴄᴛᴇᴅ:</b> <code>{chat.is_restricted}</code>
◎ <b>ᴘʀᴏᴛᴇᴄᴛᴇᴅ:</b> <code>{chat.has_protected_content}</code>
◎ <b>ᴍᴇᴍʙᴇʀꜱ:</b> <code>{chat.members_count}</code>

◎ <b>ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ:</b>
<code>{description}</code>

━━━━━━━━━━━━━━━━━━
"""

        await ex.edit(out, disable_web_page_preview=True)

    except Exception as e:
        return await ex.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


# ============================================
#  ʜᴇʟᴘ ᴍᴇɴᴜ
# ============================================

add_command_help(
    "info",
    [
        ["info / whois / !info", "ᴀᴜᴛᴏ-ᴅᴇᴛᴇᴄᴛ ᴜꜱᴇʀ · ꜱᴇʟꜰ ɪɴꜰᴏ ᴀᴜᴛᴏ"],
        ["chatinfo / cinfo / !chatinfo", "ɢᴇᴛ ɢʀᴏᴜᴘ ɪɴꜰᴏ"],
    ],
)
