from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
from UTTAM.helper.PyroHelpers import get_ub_chats
from UTTAM.plugins.basic.profile import extract_user, extract_user_and_reason
from UTTAM.database import gbandb as UTTAM
from UTTAM.database import gmutedb as Gmute
from UTTAM.plugins.help import add_command_help
from config import OWNER_ID
from UTTAM import SUDO_USER

DEVS = [7432319742]
GLOBAL_ACTIVE = True


# ===================== AUTH CHECKER ===================== #

def is_sudo_or_owner(user_id: int):
    return user_id == OWNER_ID or user_id in SUDO_USER


# ===================== GBAN USER ===================== #

@Client.on_message(filters.command("gban", "."))
async def gban_user(client: Client, message: Message):

    if not is_sudo_or_owner(message.from_user.id):
        return await message.reply("❌ You are not authorized to use this command.")

    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ex = await message.reply("`Gbanning user...`")

    if not user_id:
        return await ex.edit("I can't find that user.")

    if user_id == client.me.id:
        return await ex.edit("**You cannot gban yourself 😂**")

    if user_id in DEVS:
        return await ex.edit("**Baap ko mat sikha 🗿**")

    try:
        user = await client.get_users(user_id)
    except:
        return await ex.edit("`Invalid user!`")

    if await UTTAM.gban_info(user.id):
        return await ex.edit("User is already **GBANNED**.")

    chats = await get_ub_chats(client)
    done = 0

    for chat in chats:
        try:
            await client.ban_chat_member(chat, user.id)
            done += 1
        except:
            pass

    await UTTAM.gban_user(user.id)

    text = (
        "**#GBANNED_USER**\n\n"
        f"**Name:** [{user.first_name}](tg://user?id={user.id})\n"
        f"**User ID:** `{user.id}`\n"
        f"**Affected Chats:** `{done}`\n"
    )

    if reason:
        text += f"**Reason:** `{reason}`"

    await ex.edit(text)


# ===================== UNGBAN USER ===================== #

@Client.on_message(filters.command("ungban", "."))
async def ungban_user(client: Client, message: Message):

    if not is_sudo_or_owner(message.from_user.id):
        return await message.reply("❌ You are not authorized to use this command.")

    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    ex = await message.reply("`Ungbanning user...`")

    if not user_id:
        return await ex.edit("I can't find that user.")

    try:
        user = await client.get_users(user_id)
    except:
        return await ex.edit("`Invalid user!`")

    if not await UTTAM.gban_info(user.id):
        return await ex.edit("User is already **UNGBANNED**.")

    chats = await get_ub_chats(client)
    done = 0

    for chat in chats:
        try:
            await client.unban_chat_member(chat, user.id)
            done += 1
        except:
            pass

    await UTTAM.ungban_user(user.id)

    text = (
        "**#UNGBANNED_USER**\n\n"
        f"**Name:** [{user.first_name}](tg://user?id={user.id})\n"
        f"**User ID:** `{user.id}`\n"
        f"**Affected Chats:** `{done}`\n"
    )

    if reason:
        text += f"**Reason:** `{reason}`"

    await ex.edit(text)


# ===================== LIST GBAN ===================== #

@Client.on_message(filters.command("listgban", "."))
async def gbanlist(client: Client, message: Message):

    if not is_sudo_or_owner(message.from_user.id):
        return await message.reply("❌ You are not authorized to use this command.")

    users = await UTTAM.gban_list()
    ex = await message.reply("`Fetching list...`")

    if not users:
        return await ex.edit("No GBanned users.")

    txt = "**🔥 GLOBAL BAN LIST:**\n\n"
    for i, data in enumerate(users, start=1):
        txt += f"**{i}.** `{data.sender}`\n"

    await ex.edit(txt)


# ===================== GMUTE ===================== #

@Client.on_message(filters.command("gmute", "."))
async def gmute_user(client: Client, message: Message):

    if not is_sudo_or_owner(message.from_user.id):
        return await message.reply("❌ You are not authorized to use this command.")

    user_id = await extract_user(message)
    ex = await message.reply("`Processing gmute...`")

    if not user_id:
        return await ex.edit("Invalid user")

    user = await client.get_users(user_id)

    if user.id == client.me.id:
        return await ex.edit("**You cannot gmute yourself 😂**")

    if user.id in DEVS:
        return await ex.edit("**Baap ko mat sikha 🗿**")

    if await Gmute.is_gmuted(user.id):
        return await ex.edit("User already **GMUTED**.")

    await Gmute.gmute(user.id)

    try:
        chats = await client.get_common_chats(user.id)
        for chat in chats:
            await chat.restrict_member(user.id, ChatPermissions())
    except:
        pass

    await ex.edit(f"**Globally Muted:** {user.mention}")


# ===================== UNGMUTE ===================== #

@Client.on_message(filters.command("ungmute", "."))
async def ungmute_user(client: Client, message: Message):

    if not is_sudo_or_owner(message.from_user.id):
        return await message.reply("❌ You are not authorized to use this command.")

    user_id = await extract_user(message)
    ex = await message.reply("`Processing ungmute...`")

    if not user_id:
        return await ex.edit("Invalid user")

    user = await client.get_users(user_id)

    if not await Gmute.is_gmuted(user.id):
        return await ex.edit("User is already UNGMUTED.")

    await Gmute.ungmute(user.id)

    try:
        chats = await client.get_common_chats(user.id)
        for chat in chats:
            await chat.unban_member(user.id)
    except:
        pass

    await ex.edit(f"**Globally Unmuted:** {user.mention}")


# ===================== LIST GMUTE ===================== #

@Client.on_message(filters.command("listgmute", "."))
async def gmutelist(client: Client, message: Message):

    if not is_sudo_or_owner(message.from_user.id):
        return await message.reply("❌ You are not authorized to use this command.")

    users = await Gmute.gmute_list()
    ex = await message.reply("`Processing...`")

    if not users:
        return await ex.edit("No GMUTED users.")

    txt = "**🔇 GLOBAL MUTE LIST:**\n\n"
    for i, data in enumerate(users, start=1):
        txt += f"**{i}.** `{data.sender}`\n"

    await ex.edit(txt)


# ===================== GLOBAL AUTO CHECK ===================== #

@Client.on_message(filters.incoming & filters.group)
async def global_checker(client: Client, message: Message):

    if not GLOBAL_ACTIVE:
        return

    user = message.from_user
    if not user:
        return

    uid = user.id
    cid = message.chat.id

    # GBAN
    if await UTTAM.gban_info(uid):
        try:
            await client.ban_chat_member(cid, uid)
        except:
            pass

    # GMUTE
    if await Gmute.is_gmuted(uid):
        try:
            await message.delete()
        except:
            pass
        try:
            await client.restrict_chat_member(cid, uid, ChatPermissions())
        except:
            pass


# ===================== HELP ===================== #

add_command_help(
    "globals",
    [
        ["gban <user>", "Global ban (OWNER + SUDO ONLY)"],
        ["ungban <user>", "Remove global ban"],
        ["listgban", "Show all gbanned users"],
        ["gmute <user>", "Global mute"],
        ["ungmute <user>", "Remove gmute"],
        ["listgmute", "Show all gmuted users"],
    ],
)
