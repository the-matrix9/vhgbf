
import html
import asyncio
from typing import List

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from UTTAM.helper.parser import mention_html, mention_markdown
from UTTAM.plugins.help import add_command_help

# supported prefixes
CMD_PREFIXES = [".", "/", "!"]


# ──────────────────────────────────────────
#   GET ADMIN LIST
# ──────────────────────────────────────────
@Client.on_message(filters.me & filters.command(["admins", "adminlist"], CMD_PREFIXES))
async def adminlist(client: Client, message: Message):
    replyid = message.reply_to_message.id if message.reply_to_message else None

    try:
        # Group selection (id/username optional)
        if len(message.command) >= 2:
            chat_arg = message.command[1]
            grup = await client.get_chat(chat_arg)
            chat_id = grup.id
        else:
            chat_id = message.chat.id
            grup = await client.get_chat(chat_id)

        creator: List[str] = []
        admins: List[str] = []
        bot_admins: List[str] = []

        async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            user = member.user
            name = ((user.first_name or "") + " " + (user.last_name or "")).strip()
            if not name:
                name = "☠️ Deleted Account"

            if member.status == enums.ChatMemberStatus.OWNER:
                creator.append(mention_markdown(user.id, name))
            elif member.status == enums.ChatMemberStatus.ADMINISTRATOR and not user.is_bot:
                admins.append(mention_markdown(user.id, name))
            elif user.is_bot:
                bot_admins.append(mention_markdown(user.id, name))

        admins.sort()
        bot_admins.sort()

        header = f"**Admins in** `{grup.title}`\n\n"
        lines = []
        lines.append("╒═══「 Creator 」")
        if creator:
            for x in creator:
                lines.append(f"│ • {x}")
        else:
            lines.append("│ • —")

        lines.append(f"╞══「 {len(admins)} Human Admins 」")
        if admins:
            for x in admins:
                lines.append(f"│ • {x}")
        else:
            lines.append("│ • —")

        lines.append(f"╞══「 {len(bot_admins)} Bot Admins 」")
        if bot_admins:
            for x in bot_admins:
                lines.append(f"│ • {x}")
        else:
            lines.append("│ • —")

        total = len(creator) + len(admins) + len(bot_admins)
        lines.append(f"╘══「 Total {total} Admins 」")

        text = header + "\n".join(lines)

        # split if too long for a single message
        MAX = 4000
        if len(text) <= 4096:
            if replyid:
                await client.send_message(chat_id, text, reply_to_message_id=replyid)
            else:
                await message.edit(text)
        else:
            # chunk safely
            chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]
            for c in chunks:
                if replyid:
                    await client.send_message(chat_id, c, reply_to_message_id=replyid)
                    replyid = None
                else:
                    await client.send_message(chat_id, c)

    except Exception as e:
        await message.edit(f"**ERROR (adminlist):** `{html.escape(str(e))}`")


# ──────────────────────────────────────────
#      REPORT ADMINS
# ──────────────────────────────────────────
@Client.on_message(filters.me & filters.command(["reportadmin", "report", "reportadmins"], CMD_PREFIXES))
async def report_admin(client: Client, message: Message):
    try:
        # delete command to keep chat clean
        await message.delete()

        # text may be absent
        text = None
        if len(message.command) > 1:
            text = " ".join(message.command[1:])

        admin_mentions = ""
        # build mention placeholders for all admins (non-bots)
        async for member in client.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not member.user.is_bot:
                # a zero-width char mention so admins get notified
                admin_mentions += mention_html(member.user.id, "\u200b")

        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
            if text:
                msg = f"{html.escape(text)}{admin_mentions}"
            else:
                who = mention_html(target_user.id, html.escape(target_user.first_name or "User"))
                msg = f"{who} reported to admins.{admin_mentions}"
        else:
            msg = (html.escape(text) if text else "Calling admins…") + admin_mentions

        await client.send_message(message.chat.id, msg, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        # best effort notify original author via PM if cannot post in group
        try:
            await client.send_message(message.from_user.id, f"**REPORT FAILED:** `{html.escape(str(e))}`")
        except Exception:
            pass


# ──────────────────────────────────────────
#        TAG EVERYONE (SAFE)
# ──────────────────────────────────────────
@Client.on_message(filters.me & filters.command(["everyone", "mentionall"], CMD_PREFIXES))
async def tag_all(client: Client, message: Message):
    # Remove command message to keep chat clean
    try:
        await message.delete()
    except Exception:
        pass

    custom = "Hi all 👋"
    if len(message.command) > 1:
        # preserve original spacing text (after command)
        custom = message.text.split(None, 1)[1]

    sent = 0
    try:
        async for member in client.get_chat_members(message.chat.id):
            # skip bots and deleted
            if getattr(member.user, "is_bot", False):
                continue
            try:
                mention = mention_html(member.user.id, member.user.first_name or "User")
                await client.send_message(
                    message.chat.id,
                    f"{html.escape(custom)} {mention}",
                    parse_mode=enums.ParseMode.HTML
                )
                sent += 1
                await asyncio.sleep(0.5)  # floodwait-safe
            except Exception:
                # ignore single-user failure and continue
                await asyncio.sleep(0.2)
                continue
    except Exception as e:
        await client.send_message(message.chat.id, f"**ERROR (tag_all):** `{html.escape(str(e))}`")
        return

    # optional summary (no reply to avoid spam)
    try:
        await client.send_message(message.chat.id, f"✅ Tagged {sent} users (delay-safe).")
    except Exception:
        pass


# ──────────────────────────────────────────
#        GET BOT LIST
# ──────────────────────────────────────────
@Client.on_message(filters.me & filters.command(["botlist", "bots"], CMD_PREFIXES))
async def get_bots(client: Client, message: Message):
    replyid = message.reply_to_message.id if message.reply_to_message else None

    try:
        if len(message.command) > 1:
            grup = await client.get_chat(message.command[1])
            chat_id = grup.id
        else:
            chat_id = message.chat.id
            grup = await client.get_chat(chat_id)

        bots = []
        async for m in client.get_chat_members(chat_id):
            if m.user.is_bot:
                name = m.user.first_name or "Bot"
                bots.append(mention_markdown(m.user.id, name))

        text = f"**Bots in {grup.title}:**\n\n"
        if bots:
            for x in bots:
                text += f"• {x}\n"
        else:
            text += "• —\n"
        text += f"\nTotal Bots: {len(bots)}"

        if replyid:
            await client.send_message(chat_id, text, reply_to_message_id=replyid)
        else:
            await message.edit(text)
    except Exception as e:
        await message.edit(f"**ERROR (botlist):** `{html.escape(str(e))}`")


# ──────────────────────────────────────────
# ADD HELP MENU
# ──────────────────────────────────────────
add_command_help(
    "tag",
    [
        [".admins / /admins / !admins", "Show admin list"],
        [".botlist / /botlist / !botlist", "Show list of bots"],
        [".everyone / /everyone / !everyone", "Tag everyone (safe delay)"],
        [".reportadmin / /reportadmin / !reportadmin", "Report someone to admins"],
    ],
                )
