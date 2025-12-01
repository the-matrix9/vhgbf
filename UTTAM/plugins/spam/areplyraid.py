import random
from pyrogram import Client, filters
from pyrogram.types import Message
from UTTAM import SUDO_USER
from UTTAM.database.rraid import get_rraid_users, rraid_user, unrraid_user
from .replyraid import RAIDS  # Global list of users under raid
from UTTAM.plugins.basic.profile import extract_user

DEVS = 7432319742
SUDO_USERS = SUDO_USER if isinstance(SUDO_USER, (list, set)) else [SUDO_USER]

# 💀 10–20 funny / desi gaali lines
GAALIS = [
"ᴍᴀᴅᴀʀᴄʜᴏᴅ ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ɢʜᴜᴛᴋᴀ ᴋʜᴀᴀᴋᴇ ᴛʜᴏᴏᴋ ᴅᴜɴɢᴀ 🤣🤣",
"ᴛᴇʀᴇ ʙᴇʜᴇɴ ᴋ ᴄʜᴜᴛ ᴍᴇ ᴄʜᴀᴋᴜ ᴅᴀᴀʟ ᴋᴀʀ ᴄʜᴜᴛ ᴋᴀ ᴋʜᴏᴏɴ ᴋᴀʀ ᴅᴜɢᴀ",
"ᴛᴇʀɪ ᴠᴀʜᴇᴇɴ ɴʜɪ ʜᴀɪ ᴋʏᴀ? 9 ᴍᴀʜɪɴᴇ ʀᴜᴋ ꜱᴀɢɪ ᴠᴀʜᴇᴇɴ ᴅᴇᴛᴀ ʜᴜ 🤣🤣🤩",
"ᴛᴇʀɪ ᴍᴀᴀ ᴋ ʙʜᴏꜱᴅᴇ ᴍᴇ ᴀᴇʀᴏᴘʟᴀɴᴇᴘᴀʀᴋ ᴋᴀʀᴋᴇ ᴜᴅᴀᴀɴ ʙʜᴀʀ ᴅᴜɢᴀ ✈️🛫",
"ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ꜱᴜᴛʟɪ ʙᴏᴍʙ ꜰᴏᴅ ᴅᴜɴɢᴀ ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴊʜᴀᴀᴛᴇ ᴊᴀʟ ᴋᴇ ᴋʜᴀᴀᴋ ʜᴏ ᴊᴀʏᴇɢɪ💣",
"ᴛᴇʀɪ ᴍᴀᴀᴋɪ ᴄʜᴜᴛ ᴍᴇ ꜱᴄᴏᴏᴛᴇʀ ᴅᴀᴀʟ ᴅᴜɢᴀ👅",
"ᴛᴇʀᴇ ʙᴇʜᴇɴ ᴋ ᴄʜᴜᴛ ᴍᴇ ᴄʜᴀᴋᴜ ᴅᴀᴀʟ ᴋᴀʀ ᴄʜᴜᴛ ᴋᴀ ᴋʜᴏᴏɴ ᴋᴀʀ ᴅᴜɢᴀ",
"ᴛᴇʀᴇ ʙᴇʜᴇɴ ᴋ ᴄʜᴜᴛ ᴍᴇ ᴄʜᴀᴋᴜ ᴅᴀᴀʟ ᴋᴀʀ ᴄʜᴜᴛ ᴋᴀ ᴋʜᴏᴏɴ ᴋᴀʀ ᴅᴜɢᴀ",
"ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ ᴋᴀᴋᴛᴇ 🤱 ɢᴀʟɪ ᴋᴇ ᴋᴜᴛᴛᴏ 🦮 ᴍᴇ ʙᴀᴀᴛ ᴅᴜɴɢᴀ ᴘʜɪʀ 🍞 ʙʀᴇᴀᴅ ᴋɪ ᴛᴀʀʜ ᴋʜᴀʏᴇɴɢᴇ ᴡᴏ ᴛᴇʀɪ ᴍᴀᴀ ᴋɪ ᴄʜᴜᴛ",
"ᴅᴜᴅʜ ʜɪʟᴀᴀᴜɴɢᴀ ᴛᴇʀɪ ᴠᴀʜᴇᴇɴ ᴋᴇ ᴜᴘʀ ɴɪᴄʜᴇ 🆙🆒😙",
"ᴛᴇʀɪ ʀᴀɴᴅɪ ʙᴀʜᴀɴ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ᴛʜᴏᴍᴀs ᴘᴀᴘᴀ ᴋᴀ ʟᴀɴᴅ",
"ᴛᴇʀɪ ᴍᴀ ᴋɪ ᴄʜᴜᴛ ᴍᴇ ʀᴀᴅʜᴇ ᴋᴀ ʟᴀɴᴅ",
"ꜱᴜᴀʀ ᴋᴇ ᴘɪʟʟᴇ ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ꜱᴀᴅᴀᴋ ᴘʀ ʟɪᴛᴀᴋᴇ ᴄʜᴏᴅ ᴅᴜɴɢᴀ 😂😆🤤",
"ᴀʙᴇ ᴛᴇʀɪ ᴍᴀᴀᴋᴀ ʙʜᴏꜱᴅᴀ ᴍᴀᴅᴇʀᴄʜᴏᴏᴅ ᴋʀ ᴘɪʟʟᴇ ᴘᴀᴘᴀ ꜱᴇ ʟᴀᴅᴇɢᴀ ᴛᴜ 😼😂🤤",
"ɢᴀʟɪ ɢᴀʟɪ ɴᴇ ꜱʜᴏʀ ʜᴇ ᴛᴇʀɪ ᴍᴀᴀ ʀᴀɴᴅɪ ᴄʜᴏʀ ʜᴇ 💋💋💦",
"ᴀʙᴇ ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴏ ᴄʜᴏᴅᴜ ʀᴀɴᴅɪᴋᴇ ᴘɪʟʟᴇ ᴋᴜᴛᴛᴇ ᴋᴇ ᴄʜᴏᴅᴇ 😂👻🔥",
"ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴀɪꜱᴇ ᴄʜᴏᴅᴀ ᴀɪꜱᴇ ᴄʜᴏᴅᴀ ᴛᴇʀɪ ᴍᴀᴀᴀ ʙᴇᴅ ᴘᴇʜɪ ᴍᴜᴛʜ ᴅɪᴀ 💦💦💦💦",
"ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴇ ʙʜᴏꜱᴅᴇ ᴍᴇ ᴀᴀᴀɢ ʟᴀɢᴀᴅɪᴀ ᴍᴇʀᴀ ᴍᴏᴛᴀ ʟᴜɴᴅ ᴅᴀʟᴋᴇ 🔥🔥💦😆😆",
"ʀᴀɴᴅɪᴋᴇ ʙᴀᴄʜʜᴇ ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴄʜᴏᴅᴜ ᴄʜᴀʟ ɴɪᴋᴀʟ",
"ᴋɪᴛɴᴀ ᴄʜᴏᴅᴜ ᴛᴇʀɪ ʀᴀɴᴅɪ ᴍᴀᴀᴋɪ ᴄʜᴜᴛʜ ᴀʙʙ ᴀᴘɴɪ ʙᴇʜᴇɴ ᴋᴏ ʙʜᴇᴊ 😆👻🤤",
"ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴏᴛᴏ ᴄʜᴏᴅ ᴄʜᴏᴅᴋᴇ ᴘᴜʀᴀ ꜰᴀᴀᴅ ᴅɪᴀ ᴄʜᴜᴛʜ ᴀʙʙ ᴛᴇʀɪ ɢꜰ ᴋᴏ ʙʜᴇᴊ 😆💦🤤",
"ᴛᴇʀɪ ɢꜰ ᴋᴏ ᴇᴛɴᴀ ᴄʜᴏᴅᴀ ʙᴇʜᴇɴ ᴋᴇ ʟᴏᴅᴇ ᴛᴇʀɪ ɢꜰ ᴛᴏ ᴍᴇʀɪ ʀᴀɴᴅɪ ʙᴀɴɢᴀʏɪ ᴀʙʙ ᴄʜᴀʟ ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴄʜᴏᴅᴛᴀ ꜰɪʀꜱᴇ ♥️💦😆😆😆😆",
"ʜᴀʀɪ ʜᴀʀɪ ɢʜᴀᴀꜱ ᴍᴇ ᴊʜᴏᴘᴅᴀ ᴛᴇʀɪ ᴍᴀᴀᴋᴀ ʙʜᴏꜱᴅᴀ 🤣🤣💋💦",
"ᴄʜᴀʟ ᴛᴇʀᴇ ʙᴀᴀᴘ ᴋᴏ ʙʜᴇᴊ ᴛᴇʀᴀ ʙᴀꜱᴋᴀ ɴʜɪ ʜᴇ ᴘᴀᴘᴀ ꜱᴇ ʟᴀᴅᴇɢᴀ ᴛᴜ",
"ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋɪ ᴄʜᴜᴛʜ ᴍᴇ ʙᴏᴍʙ ᴅᴀʟᴋᴇ ᴜᴅᴀ ᴅᴜɴɢᴀ ᴍᴀᴀᴋᴇ ʟᴀᴡᴅᴇ",
"ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴛʀᴀɪɴ ᴍᴇ ʟᴇᴊᴀᴋᴇ ᴛᴏᴘ ʙᴇᴅ ᴘᴇ ʟɪᴛᴀᴋᴇ ᴄʜᴏᴅ ᴅᴜɴɢᴀ ꜱᴜᴀʀ ᴋᴇ ᴘɪʟʟᴇ 🤣🤣💋💋",
"ᴛᴇʀɪ ᴍᴀᴀᴀᴋᴇ ɴᴜᴅᴇꜱ ɢᴏᴏɢʟᴇ ᴘᴇ ᴜᴘʟᴏᴀᴅ ᴋᴀʀᴅᴜɴɢᴀ ʙᴇʜᴇɴ ᴋᴇ ʟᴀᴇᴡᴅᴇ 👻🔥",
"ᴛᴇʀɪ ᴍᴀᴀᴀᴋᴇ ɴᴜᴅᴇꜱ ɢᴏᴏɢʟᴇ ᴘᴇ ᴜᴘʟᴏᴀᴅ ᴋᴀʀᴅᴜɴɢᴀ ʙᴇʜᴇɴ ᴋᴇ ʟᴀᴇᴡᴅᴇ 👻🔥",
"ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴏ ᴄʜᴏᴅ ᴄʜᴏᴅᴋᴇ ᴠɪᴅᴇᴏ ʙᴀɴᴀᴋᴇ xɴxx.ᴄᴏᴍ ᴘᴇ ɴᴇᴇʟᴀᴍ ᴋᴀʀᴅᴜɴɢᴀ ᴋᴜᴛᴛᴇ ᴋᴇ ᴘɪʟʟᴇ 💦💋",
"ᴛᴇʀɪ ᴍᴀᴀᴀᴋɪ ᴄʜᴜᴅᴀɪ ᴋᴏ ᴘᴏʀɴʜᴜʙ.ᴄᴏᴍ ᴘᴇ ᴜᴘʟᴏᴀᴅ ᴋᴀʀᴅᴜɴɢᴀ ꜱᴜᴀʀ ᴋᴇ ᴄʜᴏᴅᴇ 🤣💋💦",
"ᴀʙᴇ ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴏ ᴄʜᴏᴅᴜ ʀᴀɴᴅɪᴋᴇ ʙᴀᴄʜʜᴇ ᴛᴇʀᴇᴋᴏ ᴄʜᴀᴋᴋᴏ ꜱᴇ ᴘɪʟᴡᴀᴠᴜɴɢᴀ ʀᴀɴᴅɪᴋᴇ ʙᴀᴄʜʜᴇ 🤣🤣",
"ᴛᴇʀɪ ᴍᴀᴀᴋɪ ᴄʜᴜᴛʜ ꜰᴀᴀᴅᴋᴇ ʀᴀᴋᴅɪᴀ ᴍᴀᴀᴋᴇ ʟᴏᴅᴇ ᴊᴀᴀ ᴀʙʙ ꜱɪʟᴡᴀʟᴇ 👄👄",
"ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋɪ ᴄʜᴜᴛʜ ᴍᴇ ᴍᴇʀᴀ ʟᴜɴᴅ ᴋᴀᴀʟᴀ",
"ᴛᴇʀɪ ʙᴇʜᴇɴ ʟᴇᴛɪ ᴍᴇʀɪ ʟᴜɴᴅ ʙᴀᴅᴇ ᴍᴀꜱᴛɪ ꜱᴇ ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴏ ᴍᴇɴᴇ ᴄʜᴏᴅ ᴅᴀʟᴀ ʙᴏʜᴏᴛ ꜱᴀꜱᴛᴇ ꜱᴇ",
"ʙᴇᴛᴇ ᴛᴜ ʙᴀᴀᴘ ꜱᴇ ʟᴇɢᴀ ᴘᴀɴɢᴀ ᴛᴇʀɪ ᴍᴀᴀᴀ ᴋᴏ ᴄʜᴏᴅ ᴅᴜɴɢᴀ ᴋᴀʀᴋᴇ ɴᴀɴɢᴀ 💦💋",
"ʜᴀʜᴀʜᴀʜ ᴍᴇʀᴇ ʙᴇᴛᴇ ᴀɢʟɪ ʙᴀᴀʀ ᴀᴘɴɪ ᴍᴀᴀᴋᴏ ʟᴇᴋᴇ ᴀᴀʏᴀ ᴍᴀᴛʜ ᴋᴀᴛ ᴏʀ ᴍᴇʀᴇ ᴍᴏᴛᴇ ʟᴜɴᴅ ꜱᴇ ᴄʜᴜᴅᴡᴀʏᴀ ᴍᴀᴛʜ ᴋᴀʀ",
"ᴄʜᴀʟ ʙᴇᴛᴀ ᴛᴜᴊʜᴇ ᴍᴀᴀꜰ ᴋɪᴀ 🤣 ᴀʙʙ ᴀᴘɴɪ ɢꜰ ᴋᴏ ʙʜᴇᴊ",
"ꜱʜᴀʀᴀᴍ ᴋᴀʀ ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴀ ʙʜᴏꜱᴅᴀ ᴋɪᴛɴᴀ ɢᴀᴀʟɪᴀ ꜱᴜɴᴡᴀʏᴇɢᴀ ᴀᴘɴɪ ᴍᴀᴀᴀ ʙᴇʜᴇɴ ᴋᴇ ᴜᴘᴇʀ",
"ᴀʙᴇ ʀᴀɴᴅɪᴋᴇ ʙᴀᴄʜʜᴇ ᴀᴜᴋᴀᴛ ɴʜɪ ʜᴇᴛᴏ ᴀᴘɴɪ ʀᴀɴᴅɪ ᴍᴀᴀᴋᴏ ʟᴇᴋᴇ ᴀᴀʏᴀ ᴍᴀᴛʜ ᴋᴀʀ ʜᴀʜᴀʜᴀʜᴀ",
"ᴋɪᴅᴢ ᴍᴀᴅᴀʀᴄʜᴏᴅ ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴄʜᴏᴅ ᴄʜᴏᴅᴋᴇ ᴛᴇʀʀ ʟɪʏᴇ ʙʜᴀɪ ᴅᴇᴅɪʏᴀ",
"ᴊᴜɴɢʟᴇ ᴍᴇ ɴᴀᴄʜᴛᴀ ʜᴇ ᴍᴏʀᴇ ᴛᴇʀɪ ᴍᴀᴀᴋɪ ᴄʜᴜᴅᴀɪ ᴅᴇᴋᴋᴇ ꜱᴀʙ ʙᴏʟᴛᴇ ᴏɴᴄᴇ ᴍᴏʀᴇ ᴏɴᴄᴇ ᴍᴏʀᴇ 🤣🤣💦💋",
"ɢᴀʟɪ ɢᴀʟɪ ᴍᴇ ʀᴇʜᴛᴀ ʜᴇ ꜱᴀɴᴅ ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴄʜᴏᴅ ᴅᴀʟᴀ ᴏʀ ʙᴀɴᴀ ᴅɪᴀ ʀᴀɴᴅ 🤤🤣",
"ꜱᴀʙ ʙᴏʟᴛᴇ ᴍᴜᴊʜᴋᴏ ᴘᴀᴘᴀ ᴋʏᴏᴜɴᴋɪ ᴍᴇɴᴇ ʙᴀɴᴀᴅɪᴀ ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴘʀᴇɢɴᴇɴᴛ 🤣🤣",
"ꜱᴜᴀʀ ᴋᴇ ᴘɪʟʟᴇ ᴛᴇʀɪ ᴍᴀᴀᴋɪ ᴄʜᴜᴛʜ ᴍᴇ ꜱᴜᴀʀ ᴋᴀ ʟᴏᴜᴅᴀ ᴏʀ ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋɪ ᴄʜᴜᴛʜ ᴍᴇ ᴍᴇʀᴀ ʟᴏᴅᴀ",
"ᴄʜᴀʟ ᴄʜᴀʟ ᴀᴘɴɪ ᴍᴀᴀᴋɪ ᴄʜᴜᴄʜɪʏᴀ ᴅɪᴋᴀ",
"ʜᴀʜᴀʜᴀʜᴀ ʙᴀᴄʜʜᴇ ᴛᴇʀɪ ᴍᴀᴀᴀᴋᴏ ᴄʜᴏᴅ ᴅɪᴀ ɴᴀɴɢᴀ ᴋᴀʀᴋᴇ",
"ᴛᴇʀɪ ɢꜰ ʜᴇ ʙᴀᴅɪ ꜱᴇxʏ ᴜꜱᴋᴏ ᴘɪʟᴀᴋᴇ ᴄʜᴏᴏᴅᴇɴɢᴇ ᴘᴇᴘꜱɪ",
"2 ʀᴜᴘᴀʏ ᴋɪ ᴘᴇᴘꜱɪ ᴛᴇʀɪ ᴍᴜᴍᴍʏ ꜱᴀʙꜱᴇ ꜱᴇxʏ 💋💦",
"ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴄʜᴇᴇᴍꜱ ꜱᴇ ᴄʜᴜᴅᴡᴀᴠᴜɴɢᴀ ᴍᴀᴅᴇʀᴄʜᴏᴏᴅ ᴋᴇ ᴘɪʟʟᴇ 💦🤣",
"ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋɪ ᴄʜᴜᴛʜ ᴍᴇ ᴍᴜᴛʜᴋᴇ ꜰᴀʀᴀʀ ʜᴏᴊᴀᴠᴜɴɢᴀ ʜᴜɪ ʜᴜɪ ʜᴜɪ",
"ꜱᴘᴇᴇᴅ ʟᴀᴀᴀ ᴛᴇʀɪ ʙᴇʜᴇɴ ᴄʜᴏᴅᴜ ʀᴀɴᴅɪᴋᴇ ᴘɪʟʟᴇ 💋💦🤣",
"ᴀʀᴇ ʀᴇ ᴍᴇʀᴇ ʙᴇᴛᴇ ᴋʏᴏᴜɴ ꜱᴘᴇᴇᴅ ᴘᴀᴋᴀᴅ ɴᴀ ᴘᴀᴀᴀ ʀᴀʜᴀ ᴀᴘɴᴇ ʙᴀᴀᴘ ᴋᴀ ʜᴀʜᴀʜ🤣🤣",
"ꜱᴜɴ ꜱᴜɴ ꜱᴜᴀʀ ᴋᴇ ᴘɪʟʟᴇ ᴊʜᴀɴᴛᴏ ᴋᴇ ꜱᴏᴜᴅᴀɢᴀʀ ᴀᴘɴɪ ᴍᴜᴍᴍʏ ᴋɪ ɴᴜᴅᴇꜱ ʙʜᴇᴊ",
"ᴀʙᴇ ꜱᴜɴ ʟᴏᴅᴇ ᴛᴇʀɪ ʙᴇʜᴇɴ ᴋᴀ ʙʜᴏꜱᴅᴀ ꜰᴀᴀᴅ ᴅᴜɴɢᴀ",
"ᴛᴇʀɪ ᴍᴀᴀᴋᴏ ᴋʜᴜʟᴇ ʙᴀᴊᴀʀ ᴍᴇ ᴄʜᴏᴅ ᴅᴀʟᴀ 🤣🤣💋",
]
    
# Activate replyraid
@Client.on_message(filters.command(["replyraid"], ".") & (filters.me | filters.user(SUDO_USERS)))
async def replyraid_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    status_msg = await message.edit_text("⚙️ Processing...")

    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await status_msg.edit("❌ Invalid user specified.")
    elif reply:
        user = reply.from_user
    else:
        return await status_msg.edit("❌ Please reply to a user or give their ID.")

    # Safety checks
    if user.id == client.me.id:
        return await status_msg.edit("😐 Bhai apne aap pe raid nahi karte.")
    if user.id in SUDO_USERS or user.id == DEVS:
        return await status_msg.edit("🚫 Ye banda protected hai (SUDO/DEV).")

    rraid_users = await get_rraid_users()
    if user.id in rraid_users:
        return await status_msg.edit(f"⚡ ReplyRaid already active for [{user.first_name}](tg://user?id={user.id}).")

    await rraid_user(user.id)
    RAIDS.append(user.id)
    await status_msg.edit(
        f"✅ **ReplyRaid Activated!**\n"
        f"👤 Target: [{user.first_name}](tg://user?id={user.id})\n"
        f"💀 Reply Mode: Desi Gaali Active"
    )


# Deactivate replyraid
@Client.on_message(filters.command(["rraidoff"], ".") & (filters.me | filters.user(SUDO_USERS)))
async def rraidoff_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    status_msg = await message.edit_text("♻️ Turning off ReplyRaid...")

    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            return await status_msg.edit("❌ Invalid user.")
    elif reply:
        user = reply.from_user
    else:
        return await status_msg.edit("❌ Reply to a user or provide their ID.")

    if user.id not in await get_rraid_users():
        return await status_msg.edit("⚠️ ReplyRaid is not active for this user.")

    await unrraid_user(user.id)
    if user.id in RAIDS:
        RAIDS.remove(user.id)

    await status_msg.edit(
        f"🛑 **ReplyRaid Deactivated!**\n"
        f"👤 Target: [{user.first_name}](tg://user?id={user.id})"
    )


# List all raided users
@Client.on_message(filters.command(["rraidlist"], ".") & (filters.me | filters.user(SUDO_USERS)))
async def list_replyraids(client: Client, message: Message):
    users = await get_rraid_users()
    if not users:
        return await message.edit("😎 No active ReplyRaids right now.")
    text = "🔥 **Active ReplyRaid Targets:**\n\n"
    for uid in users:
        try:
            user = await client.get_users(uid)
            text += f"• [{user.first_name}](tg://user?id={uid}) — `{uid}`\n"
        except Exception:
            text += f"• `{uid}` (User not found)\n"
    await message.edit(text)


# Auto reply gaalis if user under raid sends a message
@Client.on_message(filters.text & ~filters.me)
async def auto_replyraid(client: Client, message: Message):
    if not message.from_user:
        return
    user_id = message.from_user.id
    if user_id in await get_rraid_users():
        gaali = random.choice(GAALIS)
        try:
            await message.reply_text(gaali)
        except Exception as e:
            print(f"ReplyRaid error: {e}")
