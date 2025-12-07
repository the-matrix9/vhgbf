from UTTAM import app
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, FloodWait
import time
from flask import Flask
import pymongo
import random

# Bot details
CHANNEL_1_USERNAME = "BOTMINE_TECH"       # Updates Channel
CHANNEL_2_USERNAME = "BOTMINE_SUPPORT"    # Support Channel
ADMIN_ID = int(os.getenv("ADMIN_ID", "5738579437"))

# Flask app for uptime check
flask_app = Flask(__name__)
start_time = time.time()

# MongoDB setup
mongo_client = pymongo.MongoClient(os.getenv("MONGO_URL"))
db = mongo_client[os.getenv("MONGO_DB_NAME", "Rishtu-free-db")]
users_collection = db[os.getenv("MONGO_COLLECTION_NAME", "users")]

# -------------------- FORCE JOIN CHECK -------------------- #
async def is_user_in_channel(client, user_id: int, channel_username: str) -> bool:
    try:
        member = await client.get_chat_member(channel_username, user_id)
        return member.status not in ["kicked", "left"]
    except UserNotParticipant:
        return False
    except ChatAdminRequired:
        return False
    except Exception as e:
        print(f"Error checking {channel_username}: {e}")
        return False


async def send_join_prompt(client, chat_id):
    join_button_1 = InlineKeyboardButton("♡ Join Updates ♡", url=f"https://t.me/{CHANNEL_1_USERNAME}")
    join_button_2 = InlineKeyboardButton("♡ Join Support ♡", url=f"https://t.me/{CHANNEL_2_USERNAME}")
    markup = InlineKeyboardMarkup([[join_button_1, join_button_2]])
    await client.send_message(
        chat_id,
        "♡ You need to join both channels to use this bot ♡",
        reply_markup=markup,
    )

# -------------------- FLASK ROUTE -------------------- #
@flask_app.route('/hh')
def home():
    uptime_minutes = (time.time() - start_time) / 60
    user_count = users_collection.count_documents({})
    return f"Bot uptime: {uptime_minutes:.2f} minutes\nUnique users: {user_count}"


# -------------------- START COMMAND -------------------- #
@app.on_message(filters.command("start"))
async def start_message(client, message):
    user_id = message.from_user.id
    user = message.from_user

    # Progress animation
    baby = await message.reply_text("[□□□□□□□□□□] 0%")
    progress = [
        "[■□□□□□□□□□] 10%", "[■■□□□□□□□□] 20%", "[■■■□□□□□□□] 30%", "[■■■■□□□□□□] 40%",
        "[■■■■■□□□□□] 50%", "[■■■■■■□□□□] 60%", "[■■■■■■■□□□] 70%", "[■■■■■■■■□□] 80%",
        "[■■■■■■■■■□] 90%", "[■■■■■■■■■■] 100%"
    ]
    for step in progress:
        await baby.edit_text(f"**{step}**")
        await asyncio.sleep(0.25)

    await baby.edit_text("**❖ Jᴀʏ Sʜʀᴇᴇ Rᴀᴍ 🚩...**")
    await asyncio.sleep(1)
    await baby.delete()

    # Force join check
    if not (await is_user_in_channel(client, user_id, CHANNEL_1_USERNAME)
            and await is_user_in_channel(client, user_id, CHANNEL_2_USERNAME)):
        await send_join_prompt(client, message.chat.id)
        return

    # Store new user
    if users_collection.count_documents({'user_id': user_id}) == 0:
        users_collection.insert_one({'user_id': user_id})
        await client.send_message(
            chat_id=ADMIN_ID,
            text=(f"╔═══ ⋆ʟᴏᴠᴇ ᴡɪᴛʜ⋆ ══╗\n\n💡 **New User Alert**:\n\n"
                  f"👤 **User:** {message.from_user.mention}\n"
                  f"🆔 **User ID:** `{user_id}`\n"
                  f"📊 **Total Users:** `{users_collection.count_documents({})}`\n\n╚═════ ⋆★⋆ ═════╝")
        )

    # Random welcome image
    image_urls = [
        "https://graph.org/file/f76fd86d1936d45a63c64.jpg",
        "https://graph.org/file/a0893f3a1e6777f6de821.jpg",
        "https://graph.org/file/a13e9733afdad69720d67.jpg",
        "https://graph.org/file/692e89f8fe20554e7a139.jpg",
        "https://graph.org/file/a4a8f0e5c0e6b18249ffc.jpg",
    ]
    random_image = random.choice(image_urls)

    # Buttons — only 3 + help button added
    join_button_1 = InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/BOTMINE_TECH")
    join_button_2 = InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/BOTMINE_SUPPORT")
    mini_web_button_pyrogram = InlineKeyboardButton(
        " ⌯ ɢєηєꝛᴧᴛє ᴘʏꝛσɢꝛᴧϻ sᴇssɪᴏɴ ⌯ ",
        web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#pyrogram,user")
    )

    markup = InlineKeyboardMarkup([
        [mini_web_button_pyrogram],
        [join_button_1, join_button_2],
        [InlineKeyboardButton("📜 Help & Commands", callback_data="HELP_PAGE_1")]   # <<<< ADDED
    ])

    await client.send_photo(
        chat_id=message.chat.id,
        photo=random_image,
        caption=(
            f"""**╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ────•  
┆⚘ ʜᴇʏ {user.mention} 
┆⚘ ɪ ᴀᴍ : [˹ 𝐔sᴇʀʙᴏᴛ ˼](https://t.me/BOTMINE_TECH)  
┆⚘ ᴍᴏʀᴇ ᴀɴɪᴍᴀᴛɪᴏɴ, ғᴜɴ  
┊⚘ ᴘᴏᴡᴇʀғᴜʟ & ᴜsᴇғᴜʟ ᴜsᴇʀʙᴏᴛ  
╰─────────────────────•  
❍ ʜσᴡ ᴛσ υsє ᴛʜɪs ʙσᴛ - [ᴛɪᴘs ʜᴇʀᴇ](https://t.me/BOTMINE_TECH)  
❍ sᴛʀɪɴɢ sєᴄᴛɪση ʙσᴛ ⁚ [sᴇssɪᴏɴ-ʙᴏᴛ](https://t.me/STRING_SESSION_GENN_BOT)  
•──────────────────────•  
❍ ᴄʟᴏɴᴇ ⁚ /clone [ sᴛʀɪɴɢ sᴇssɪᴏɴ ]  
•──────────────────────•  
❍ ᴘᴏᴡᴇʀᴇᴅ ʙʏ ⏤‌‌‌‌ [ʙᴏᴛᴍɪɴᴇ ᴛᴇᴄʜ](https://t.me/BOTMINE_TECH)  
•──────────────────────•**"""
        ),
        reply_markup=markup
    )


# -------------------- BROADCAST COMMAND -------------------- #
@app.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast_message(client, message):
    if not (message.reply_to_message or len(message.command) > 1):
        await message.reply_text(
            "Please reply to a message or provide text to broadcast.\n\nUsage:\n"
            "/broadcast <text>\nOR\nReply to any media with /broadcast"
        )
        return

    broadcast_content = message.reply_to_message if message.reply_to_message else message
    users = users_collection.find()
    sent_count = 0
    failed_count = 0

    status = await message.reply_text("Starting the broadcast...")

    for user in users:
        try:
            user_id = user["user_id"]

            if broadcast_content.photo:
                await client.send_photo(user_id, broadcast_content.photo.file_id, caption=broadcast_content.caption or "")
            elif broadcast_content.video:
                await client.send_video(user_id, broadcast_content.video.file_id, caption=broadcast_content.caption or "")
            elif broadcast_content.document:
                await client.send_document(user_id, broadcast_content.document.file_id, caption=broadcast_content.caption or "")
            elif broadcast_content.text:
                await client.send_message(user_id, broadcast_content.text)

            sent_count += 1
            await asyncio.sleep(0.5)

        except FloodWait as e:
            print(f"FloodWait {e.value}s")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Failed to send to {user_id}: {e}")
            failed_count += 1

    await status.edit_text(f"�████ Broadcast Completed! \n\n📤 Sent: {sent_count}\n❌ Failed: {failed_count}")
