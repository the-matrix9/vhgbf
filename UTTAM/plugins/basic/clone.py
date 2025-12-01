import os

from pyrogram import Client, filters
from pyrogram.types import Message

from UTTAM.helper.basic import get_text, get_user
from UTTAM.plugins.help import add_command_help


# -----------------------------------------------
#  YOUR FIXED OWNER NAME + BIO WITH CLICKABLE LINK
# -----------------------------------------------

OWNER = os.environ.get("OWNER", "ʀᴀᴅʜᴇ")
BIO = os.environ.get(
    "BIO",
    "I am part of [BOTMINE TECH](https://t.me/BOTMINE_TECH)"
)


# -----------------------------------------------
#  CLONE COMMAND
# -----------------------------------------------
@Client.on_message(filters.command("clone", ".") & filters.me)
async def clone(client: Client, message: Message):
    text = get_text(message)
    msg = await message.edit_text("`Cloning profile...`")

    # extract user
    user_id = get_user(message, text)[0]
    user = await client.get_users(user_id)
    if not user:
        return await msg.edit("`Whom should I clone?`")

    # get bio + name + photo
    chat_info = await client.get_chat(user.id)
    bio = chat_info.bio or ""
    name = user.first_name or "User"

    # download profile pic
    if user.photo:
        photo = await client.download_media(user.photo.big_file_id)
        await client.set_profile_photo(photo=photo)

    # update name + bio
    await client.update_profile(first_name=name, bio=bio)

    await msg.edit(f"**Successfully cloned:** `{name}`")


# -----------------------------------------------
#  REVERT COMMAND (BACK TO NORMAL)
# -----------------------------------------------
@Client.on_message(filters.command("revert", ".") & filters.me)
async def revert(client: Client, message: Message):
    msg = await message.edit("`Reverting profile...`")

    # reset name + bio
    await client.update_profile(
        first_name=OWNER,
        bio=BIO
    )

    # delete cloned photo
    photos = [p async for p in client.get_chat_photos("me")]
    if photos:
        await client.delete_profile_photos(photos[0].file_id)

    await msg.edit("`I am back to normal!`")


# -----------------------------------------------
#  ADD HELP
# -----------------------------------------------
add_command_help(
    "clone",
    [
        ["clone <reply/user>", "Clone someone’s profile."],
        ["revert", "Restore your original profile."],
    ],
)
