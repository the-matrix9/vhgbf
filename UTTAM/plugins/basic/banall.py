import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError

from config import OWNER_ID  # to skip owner
from UTTAM import app        # your main client


async def safe_ban(client, chat_id, user_id):
    try:
        await client.ban_chat_member(chat_id, user_id)
        return True

    except FloodWait as fw:
        wait = getattr(fw, "value", getattr(fw, "x", 5))
        await asyncio.sleep(wait + 1)
        try:
            await client.ban_chat_member(chat_id, user_id)
            return True
        except:
            return False

    except:
        return False


@app.on_message(filters.command("banall", ".") & filters.me)
async def banall_cmd(client: Client, message: Message):
    chat_id = message.chat.id
    me = await client.get_me()

    await message.edit("🔥 **BanAll started...**")

    async for member in client.get_chat_members(chat_id):

        user = member.user

        # SKIPS
        if user.id == me.id:
            continue

        if user.id == OWNER_ID:
            continue

        if user.is_bot:
            continue

        if member.status in ("administrator", "creator"):
            continue

        # BAN NOW
        ok = await safe_ban(client, chat_id, user.id)

        if ok:
            await message.edit(f"🚫 Banned `{user.id}`")
        else:
            await message.edit(f"❌ Failed `{user.id}`")

        await asyncio.sleep(1.2)  # flood safe

    await message.edit("✔️ **BanAll Completed!**")
