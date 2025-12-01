from pyrogram import Client, filters
from pyrogram.types import Message
from UTTAM.plugins.help import add_command_help
from UTTAM.plugins.basic.profile import extract_user
from UTTAM import SUDO_USER
from config import OWNER_ID

# -----------------------------------------
#  SUDO ADD / REMOVE / LIST  –  FULL FIXED
# -----------------------------------------

@Client.on_message(filters.command("sudolist", ".") & filters.me)
async def sudo_list(client: Client, message: Message):
    ex = await message.edit("`Fetching sudo list...`")

    if not SUDO_USER:
        return await ex.edit("`No sudo users added yet!`")

    text = "**🔥 SUDO USERS LIST:**\n\n"
    for i, user_id in enumerate(SUDO_USER, start=1):
        text += f"**{i}.** `{user_id}`\n"

    await ex.edit(text)


# ---------------------- ADD SUDO ----------------------

@Client.on_message(filters.command("addsudo", ".") & filters.user(OWNER_ID))
async def add_sudo(client: Client, message: Message):
    ex = await message.reply("`Processing...`")

    user_id = await extract_user(message)

    if not user_id:
        return await ex.edit("`Please reply to a user or give username/userid!`")

    if user_id == client.me.id:
        return await ex.edit("`I cannot sudo myself 🤦‍♂️`")

    if user_id in SUDO_USER:
        return await ex.edit("`User is already a sudo user!`")

    SUDO_USER.append(user_id)
    await ex.edit(f"**Successfully added to SUDO:** `{user_id}`") 


# ---------------------- REMOVE SUDO ----------------------

@Client.on_message(filters.command("rmsudo", ".") & filters.user(OWNER_ID))
async def remove_sudo(client: Client, message: Message):
    ex = await message.reply("`Processing...`")

    user_id = await extract_user(message)

    if not user_id:
        return await ex.edit("`Please reply to a user or give username/userid!`")

    if user_id not in SUDO_USER:
        return await ex.edit("`This user is not in sudo list!`")

    SUDO_USER.remove(user_id)
    await ex.edit(f"**Removed from SUDO:** `{user_id}`")


# ---------------------- HELP MENU ----------------------

add_command_help(
    "sudos",
    [
        ["addsudo <reply/user>", "Add a user as sudo"],
        ["rmsudo <reply/user>", "Remove sudo user"],
        ["sudolist", "Show all sudo users"],
    ],
)
