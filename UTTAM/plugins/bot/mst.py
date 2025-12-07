import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from UTTAM import app

#--------------------------
MUST_JOIN = "rishucoder"  # your main join channel
#--------------------------

# 🎴 Random image list
JOIN_IMAGES = [
    "https://files.catbox.moe/zfy8qm.jpg",
    "https://graph.org/file/f86b71018196c5cfe7344.jpg",
    "https://graph.org/file/a3db9af88f25bb1b99325.jpg",
    "https://graph.org/file/5b344a55f3d5199b63fa5.jpg",
    "https://graph.org/file/84de4b440300297a8ecb3.jpg",
    "https://graph.org/file/ed92cada78099c9c3a4f7.jpg",
    "https://graph.org/file/16b1a2828cc507f8048bd.jpg",
    "https://graph.org/file/cacbdddee77784d9ed2b7.jpg",
]

# 💬 Random caption list
CAPTIONS = [
    "๏ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ʏᴇᴛ, ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ sᴛᴀʀᴛ ᴀɢᴀɪɴ 💫",
    "๏ ᴊᴏɪɴ ᴛʜᴇ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ 💥",
    "๏ ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ᴜsɪɴɢ ᴍᴇ 💖",
    "๏ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ғᴀᴍɪʟʏ ʏᴇᴛ 🌸",
    "๏ ᴊᴏɪɴ ᴀɴᴅ ᴄᴏɴᴛɪɴᴜᴇ ᴛᴏ ᴇɴᴊᴏʏ ᴍʏ ғᴇᴀᴛᴜʀᴇs 🌹",
    "๏ ᴡɪᴛʜᴏᴜᴛ ᴊᴏɪɴɪɴɢ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜsᴇ ᴍᴇ 🥺",
    "๏ ᴊᴏɪɴ ɴᴏᴡ ᴀɴᴅ ʜᴀᴠᴇ ғᴜɴ ᴡɪᴛʜ ᴍᴇ 💫",
]


# 🔹 Helper to check join status
async def is_joined(app: Client, user_id: int):
    try:
        member = await app.get_chat_member(MUST_JOIN, user_id)
        return member.status not in ("left", "kicked")
    except UserNotParticipant:
        return False
    except Exception:
        return False


# 🔹 Main must join check
@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    if not MUST_JOIN:
        return

    # Check if user joined
    if await is_joined(app, msg.from_user.id):
        return  # already joined, continue normally

    try:
        # Prepare join link
        if MUST_JOIN.isalpha():
            link = "https://t.me/" + MUST_JOIN
        else:
            chat_info = await app.get_chat(MUST_JOIN)
            link = chat_info.invite_link

        # Random image and caption
        photo = random.choice(JOIN_IMAGES)
        caption = random.choice(CAPTIONS)

        # Send join message with button + I Joined button
        await msg.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("๏Jᴏɪɴ๏", url=link)],
                    [
                        InlineKeyboardButton("๏ ᴜᴘᴅᴀᴛᴇs ๏", url="https://t.me/BOTMINE_TECH"),
                        InlineKeyboardButton("๏ sᴜᴘᴘᴏʀᴛ ๏", url="https://t.me/BOTMINE_SUPPORT")
                    ],
                    [InlineKeyboardButton("✅ I Joined", callback_data="check_joined")]
                ]
            )
        )
        await msg.stop_propagation()
    except ChatWriteForbidden:
        pass
    except ChatAdminRequired:
        print(f"⚠️ Promote me as admin in must join chat: {MUST_JOIN}")


# 🔹 Callback: When user clicks “✅ I Joined”
@app.on_callback_query(filters.regex("check_joined"))
async def recheck_joined(app: Client, query: CallbackQuery):
    user_id = query.from_user.id
    if await is_joined(app, user_id):
        await query.message.edit_caption(
            caption="✅ **Thank you for joining!**\n\nYou can now start using the bot ✨",
            reply_markup=None,
        )
        # Optional: Auto-start message after join confirmation
        await app.send_message(
            user_id,
            "✨ **Welcome!**\n\nNow you have full access to my features 💫",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🌐 ᴜᴘᴅᴀᴛᴇs", url="https://t.me/BOTMINE_TECH"),
                        InlineKeyboardButton("💬 sᴜᴘᴘᴏʀᴛ", url="https://t.me/BOTMINE_SUPPORT"),
                    ],
                ]
            ),
        )
    else:
        await query.answer("❌ You haven't joined yet!", show_alert=True)
