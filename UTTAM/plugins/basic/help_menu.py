from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

# ───────────────────────────────
# SMALL-CAPS COMMANDS + USED TEXT
# ───────────────────────────────

COMMANDS = {
    "ᴛᴀɢᴀʟʟ": "ᴜꜱᴇᴅ ғᴏʀ ᴛᴀɢɢɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ (1.5ꜱ ᴅᴇʟᴀʏ , ᴇxᴀᴍᴘʟᴇ:- .tagall radhe krishna 🚩).",
    "ᴏɴᴇᴛᴀɢ": "ᴏɴᴇ-ʟɪɴᴇ ᴛᴀɢ ᴛᴏ ᴀʟʟ (1.5s ᴅᴇʟᴀʏ, ᴇxᴀᴍᴘʟᴇ:- .onetag hello 👋).",
    "ɢᴍᴛᴀɢ": "ɢᴏᴏᴅ-ᴍᴏʀɴɪɴɢ ᴛᴀɢ ( ᴘᴇʀ ᴛᴀɢ 𝟷.𝟻s, ᴇxᴀᴍᴘʟᴇ:- .gmtag).",
    "ʀᴀɴᴅᴏᴍᴛᴀɢ": "ʀᴀɴᴅᴏᴍ ꜱᴛʏʟᴇ ᴛᴀɢꜱ ( ᴘᴇʀ ᴛᴀɢ 𝟷.𝟻s,ᴇxᴀᴍᴘʟᴇ:-.randomtag ).",
    "ᴄᴀɴᴄᴇʟ": "ꜱᴛᴏᴘ ᴛᴀɢ ᴘʀᴏᴄᴇꜱꜱ ( .cancel ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴜsᴇᴅ ᴛᴏ sᴛᴏᴘ .tagall, .onetag, .gmtag, .randomtag).",

    "ʀᴀɪᴅ": "ʜᴇᴀᴠʏ ʀᴀɪᴅ ꜱᴘᴀᴍ.",
    "ʀᴇᴘʟʏʀᴀɪᴅ": "ᴀᴜᴛᴏ ɢᴀᴀᴀʟɪ ʀᴇᴘʟʏ.",
    "ʀʀᴀɪᴅᴏꜰꜰ": "ꜱᴛᴏᴘ ʀᴇᴘʟʏ ʀᴀɪᴅ.",
    "ʀʀᴀɪᴅʟɪꜱᴛ": "ʀᴇᴘʟʏ ʀᴀɪᴅ ᴜꜱᴇʀꜱ.",
    "ᴅᴍʀᴀɪᴅ": "ᴅᴍ ʀᴀɪᴅ ꜱᴘᴀᴍ.",
    "ᴅᴍꜱᴘᴀᴍ": "ᴅᴍ ꜱᴘᴀᴍꜱ.",

    "ꜱᴘᴀᴍ": "ꜰᴀꜱᴛ ꜱᴘᴀᴍ.",
    "ꜰᴀꜱᴛꜱᴘᴀᴍ": "ᴜʟᴛʀᴀꜰᴀꜱᴛ ꜱᴘᴀᴍ.",
    "ꜱʟᴏᴡꜱᴘᴀᴍ": "1ꜱ ᴅᴇʟᴀʏ ꜱᴘᴀᴍ.",
    "ꜱᴛᴀᴛꜱᴘᴀᴍ": "ꜱᴘᴀᴍ + ᴀᴜᴛᴏ ᴅᴇʟ.",
    "ᴅꜱᴘᴀᴍ": "ʙᴇᴛᴡᴇᴇɴ ᴅᴇʟᴀʏ.",
    "ꜱᴛɪᴄᴋᴇʀꜱᴘᴀᴍ": "ꜱᴘᴀᴍ ꜱᴛɪᴄᴋᴇʀꜱ.",

    "ꜱᴜᴅᴏʟɪꜱᴛ": "ꜱʜᴏᴡ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ.",
    "ʙᴀɴᴀʟʟ": "ʙᴀɴ ᴀʟʟ ᴍᴇᴍʙᴇʀꜱ ɪɴ ɢʀᴏᴜᴘ.",

    "ᴡᴇᴀᴛʜᴇʀ": "ᴄɪᴛʏ ᴡᴇᴀᴛʜᴇʀ.",
    "ɢᴏᴏɢʟᴇ": "ɢᴏᴏɢʟᴇ ꜱᴇᴀʀᴄʜ.",
    "ᴛʀᴀɴꜱʟᴀᴛᴇ": "ᴛᴇxᴛ ᴛʀᴀɴꜱʟᴀᴛᴇ.",
    "ʟʏʀɪᴄꜱ": "ꜱᴏɴɢ ʟʏʀɪᴄꜱ.",
    "ᴍᴜꜱɪᴄ": "ᴍᴜꜱɪᴄ ᴅᴏᴡɴʟᴏᴀᴅ.",
    "ᴜɴꜱᴘʟᴀꜱʜ": "ʜᴅ ᴀᴇꜱᴛʜᴇᴛɪᴄ ᴘɪᴄꜱ.",

    "ɪɴꜰᴏ": "ᴜꜱᴇʀ ɪɴꜰᴏ.",
    "ᴄʜᴀᴛɪɴꜰᴏ": "ɢʀᴏᴜᴘ ɪɴꜰᴏ.",
    "ꜱᴛᴀʀᴛᴠᴄ": "ꜱᴛᴀʀᴛ ᴠᴄ.",
    "ꜱᴛᴏᴘᴠᴄ": "ꜱᴛᴏᴘ ᴠᴄ.",

    "ᴘᴍɢᴜᴀʀᴅ": "ᴘᴍ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ.",
    "ꜱᴇᴛᴘᴍᴍꜱɢ": "ꜱᴇᴛ ᴘᴍᴍꜱɢ.",
    "ꜱᴇᴛʟɪᴍɪᴛ": "ꜱᴇᴛ ᴘᴍ ʟɪᴍɪᴛ.",
    "ᴀʟʟᴏᴡ": "ᴀʟʟᴏᴡ ᴜꜱᴇʀ.",
    "ᴅᴇɴʏ": "ᴅᴇɴʏ ᴘᴍ.",
}

PAGE_1_COMMANDS = list(COMMANDS.keys())[:18]
PAGE_2_COMMANDS = list(COMMANDS.keys())[18:36]

# ───────────────────────────────
# BUILD PAGE
# ───────────────────────────────
def build_page(commands, page_no: int) -> InlineKeyboardMarkup:
    rows, row = [], []
    for i, cmd in enumerate(commands, 1):
        row.append(InlineKeyboardButton(f"{cmd}", callback_data=f"CMD.{cmd}"))
        if i % 3 == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)

    # Page switch buttons
    if page_no == 1:
        rows.append([InlineKeyboardButton("⏭ ɴᴇxᴛ", callback_data="PAGE.2")])
    else:
        rows.append([InlineKeyboardButton("⏮ ʙᴀᴄᴋ", callback_data="PAGE.1")])

    # Home button
    rows.append([InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="START_HOME")])
    return InlineKeyboardMarkup(rows)

# ───────────────────────────────
# HELP MAIN
# ───────────────────────────────
HELP_HEADER = (
    "**💠 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴜꜱᴇʀʙᴏᴛ 💠**\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "✨ ᴇᴀᴄʜ ᴄᴏᴍᴍᴀɴᴅ ʜᴇʀᴇ ɪꜱ ʙᴜɪʟᴛ ғᴏʀ ꜱᴘᴇᴇᴅ + ᴘᴏᴡᴇʀ.\n"
    "⚙️ ᴍᴀꜱᴛᴇʀ ᴛᴀɢɢɪɴɢ · ꜱᴘᴀᴍ · ʀᴀɪᴅ · ᴘᴍɢᴜᴀʀᴅ.\n"
    "🚀 ᴜꜱᴇʀʙᴏᴛ ꜱᴘᴇᴇᴅ: **ʜɪɢʜ ᴘᴇʀꜰᴏʀᴍᴀɴᴄᴇ ᴇɴɢɪɴᴇ**.\n"
    "━━━━━━━━━━━━━━━━━━━━"
)

@Client.on_message(filters.command("help", "."))
async def help_main(client, message: Message):
    await message.reply_text(
        HELP_HEADER,
        reply_markup=build_page(PAGE_1_COMMANDS, 1)
    )

# ───────────────────────────────
# PAGE SWITCH
# ───────────────────────────────
@Client.on_callback_query(filters.regex("PAGE.1"))
async def page_1(client, query):
    await query.message.edit_text(
        HELP_HEADER,
        reply_markup=build_page(PAGE_1_COMMANDS, 1)
    )
    await query.answer()

@Client.on_callback_query(filters.regex("PAGE.2"))
async def page_2(client, query):
    await query.message.edit_text(
        HELP_HEADER,
        reply_markup=build_page(PAGE_2_COMMANDS, 2)
    )
    await query.answer()

# Optional: "📜 Help & Commands" ko ye handle karega
@Client.on_callback_query(filters.regex("HELP_PAGE_1"))
async def help_page_from_home(client, query):
    await query.message.edit_text(
        HELP_HEADER,
        reply_markup=build_page(PAGE_1_COMMANDS, 1)
    )
    await query.answer("Help & Commands 🔰")

# ───────────────────────────────
# HOME PANEL → START STYLE
# ───────────────────────────────

join_button_1 = InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/BOTMINE_TECH")
join_button_2 = InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/BOTMINE_SUPPORT")
mini_web_button_pyrogram = InlineKeyboardButton(
    " ⌯ ɢєηєꝛᴧᴛє ᴘʏꝛσɢꝛᴧϻ sᴇssɪᴏɴ ⌯ ",
    web_app=WebAppInfo(url="https://telegram.tools/session-string-generator#pyrogram,user")
)

HOME_MARKUP = InlineKeyboardMarkup([
    [mini_web_button_pyrogram],
    [join_button_1, join_button_2],
    [InlineKeyboardButton("📜 Help & Commands", callback_data="HELP_PAGE_1")]
])

@Client.on_callback_query(filters.regex("START_HOME"))
async def go_start(client, query):
    user = query.from_user
    HOME = f"""**╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ────•  
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
    await query.message.edit_text(
        HOME,
        reply_markup=HOME_MARKUP,
        disable_web_page_preview=True
    )
    await query.answer("Home Panel ❤️")

# ───────────────────────────────
# COMMAND DETAILS
# ───────────────────────────────
@Client.on_callback_query(filters.regex(r"CMD\.(.*)"))
async def cmd_detail(client, query):
    cmd = query.data.split(".", 1)[1]
    info = COMMANDS.get(cmd, "ɴᴏ ɪɴꜰᴏ ʏᴇᴛ.")

    await query.message.edit_text(
        f"**🔹 ᴄᴏᴍᴍᴀɴᴅ:** `{cmd}`\n\n**🔸 ᴜꜱᴇᴅ:** {info}",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⬅ ʙᴀᴄᴋ", callback_data="PAGE.1"),
                InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="START_HOME")
            ]
        ])
    )
    await query.answer()