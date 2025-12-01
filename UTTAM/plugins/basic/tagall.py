import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from UTTAM.plugins.help import add_command_help

# --------------------------
# ACTIVE CHAT TRACKER
# --------------------------
spam_chats = []

# --------------------------
# RANDOM MESSAGES LIST
# --------------------------
RANDOM_MESSAGES = [
    "Kaise ho dear 🩷🌹",
    "Kya kar rahe ho abhi 💐",
    "Aaj kal kahan busy ho ✨",
    "Yaad aati hai tumhari 🩷",
    "Free ho kya baat karne ke liye 🌸",
    "Kya chal raha hai zindagi me 🌹",
    "Bahut din ho gaye baat kiye 🩷",
    "Kahan rehte ho aaj kal 💐",
    "Kya tum mujhe yaad karte ho 🌷",
    "Tumhari smile yaad aati hai 🩷",
    "Good morning dear 🌼",
    "Good night pyaare 🩷",
    "Aaj ka din kaisa raha tumhara 🌼",
    "Har roz tumhari soch me rehta hoon 🌸",
    "Tum meri khushi ka reason ho 💐",
    "Tum meri duaon ka hissa ho 🌹",
    "Tum meri life ki best feeling ho 🌹",
    "Tum meri sabse pyari feeling ho 🌼",
    "Bas tumse hi baat karne ka mann karta hai 🩷",
    "Aaj tum online ho to dil khush hai 🌸",
    "Tere bina sab suna lagta hai 🥺",
    "Tum meri zindagi ka sapna ho 🌸",
    "Tum meri muskaan ke peeche ka reason ho 🩷",
    "Good evening dear 🌹",
    "Tum meri duniya ki sabse khoobsurat cheez ho 💐",
    "Tere jaisa koi nahi 🩷",
    "Aaj tumhari photo dekhi 💐",
    "Bahut cute lagte ho tum 🌹",
    "Har lamha tum yaad aate ho 🌸",
    "Tum meri sabse pyaari yaad ho 💐",
    "Tum meri life ki sabse khoobsurat gift ho 🌹",
    "Aaj fir tumhari yaad satayi 💐",
    "Tum meri duaon ka sabse khoobsurat hissa ho 🌹",
    "Har roz tumhara intezaar rehta hai 🌸",
    "Tum meri har dua me ho 💐",
    "Bas tum meri duniya ho 🩷",
    "Har waqt tum mere dil me rehte ho 🌼",
    "Aaj tumhari yaad ne rula diya 💐",
]

# --------------------------
# HELPER TO EXTRACT TEXT
# --------------------------
def get_arg(message: Message):
    msg = message.text or ""
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

# --------------------------
# MAIN TAGGING FUNCTION
# --------------------------
async def tag_all_users(client, message, text):
    chat_id = message.chat.id
    reply_msg = message.reply_to_message
    spam_chats.append(chat_id)

    info_msg = await message.reply_text(f"**Starting tagging...**\nMessage: `{text}`")
    count = 0

    async for member in client.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break  # stopped manually

        user = member.user
        if not user or user.is_bot or not user.first_name:
            continue

        mention = f"[{user.first_name}](tg://user?id={user.id})"
        tag_text = f"{mention} {text}"

        try:
            if reply_msg:
                await reply_msg.reply(tag_text)
            else:
                await client.send_message(chat_id, tag_text)
            count += 1
            await asyncio.sleep(1.5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Error tagging {user.id}: {e}")
            await asyncio.sleep(1)

    try:
        spam_chats.remove(chat_id)
    except:
        pass

    await info_msg.edit(f"✅ **Tagging completed! Tagged {count} members.**")


# --------------------------
# .TAGALL COMMAND
# --------------------------
@Client.on_message(filters.command("tagall", ".") & filters.me)
async def tagall(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in spam_chats:
        return await message.reply_text("Already tagging... use `.cancel` to stop.")

    args = get_arg(message)
    if not args and not message.reply_to_message:
        return await message.reply_text("Send message or reply to one!")

    if args:
        text = args
    else:
        text = message.reply_to_message.text or message.reply_to_message.caption or ""

    await tag_all_users(client, message, text)


# --------------------------
# .GMTAG COMMAND
# --------------------------
@Client.on_message(filters.command("gmtag", ".") & filters.me)
async def gmtag(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in spam_chats:
        return await message.reply_text("Already tagging... use `.cancel` to stop.")
    text = "Good Morning 🌞"
    await tag_all_users(client, message, text)


# --------------------------
# .ONETAG COMMAND
# --------------------------
@Client.on_message(filters.command("onetag", ".") & filters.me)
async def onetag(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in spam_chats:
        return await message.reply_text("Already tagging... use `.cancel` to stop.")
    text = get_arg(message)
    if not text:
        return await message.reply_text("Example: `.onetag Hello ❤️`")
    await tag_all_users(client, message, text)


# --------------------------
# .RANDOMTAG COMMAND
# --------------------------
@Client.on_message(filters.command("randomtag", ".") & filters.me)
async def randomtag(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id in spam_chats:
        return await message.reply_text("Already tagging... use `.cancel` to stop.")

    spam_chats.append(chat_id)
    info = await message.reply_text("**Starting random tagging... 💞 (1.5s delay)**")

    count = 0
    async for member in client.get_chat_members(chat_id):
        if chat_id not in spam_chats:
            break

        user = member.user
        if not user or user.is_bot or not user.first_name:
            continue

        mention = f"[{user.first_name}](tg://user?id={user.id})"
        msg = f"{mention} {random.choice(RANDOM_MESSAGES)}"

        try:
            await client.send_message(chat_id, msg)
            count += 1
            await asyncio.sleep(1.5)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Random tag error for {user.id}: {e}")
            await asyncio.sleep(1)

    try:
        spam_chats.remove(chat_id)
    except:
        pass
    await info.edit(f"💫 **Random tagging finished — tagged {count} members!**")


# --------------------------
# .CANCEL COMMAND
# --------------------------
@Client.on_message(filters.command("cancel", ".") & filters.me)
async def cancel_tag(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in spam_chats:
        return await message.reply_text("No active tagging in this chat.")
    try:
        spam_chats.remove(chat_id)
    except:
        pass
    await message.reply_text("❌ Tagging cancelled successfully.")


# --------------------------
# HELP MENU REGISTRATION
# --------------------------
add_command_help(
    "tag_system",
    [
        ["tagall [text/reply]", "Tag everyone one by one with custom text."],
        ["gmtag", "Tag everyone with ‘Good Morning 🌞’ automatically."],
        ["onetag [text]", "Tag everyone with your custom message."],
        ["randomtag", "Tag everyone with random friendly messages 💞."],
        ["cancel", "Stop any ongoing tagging process."],
    ],
    )
