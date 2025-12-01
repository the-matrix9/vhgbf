import asyncio
from prettytable import PrettyTable
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from UTTAM import app, CMD_HELP
from UTTAM.helper.PyroHelpers import ReplyCheck
from UTTAM.helper.utility import split_list

# --- Acceptable prefixes for commands ---
COMMAND_PREFIXES = [".", "/", "!"]


async def edit_or_reply(message: Message, *args, **kwargs) -> Message:
    """
    Use message.edit_text if the message was sent by self (outgoing),
    otherwise reply to the message (or reply_to_message if present).
    """
    is_outgoing = bool(
        (hasattr(message, "from_user") and message.from_user and message.from_user.is_self)
        or getattr(message, "outgoing", False)
    )

    if is_outgoing:
        func = message.edit_text
    else:
        func = (message.reply_to_message or message).reply_text

    return await func(*args, **kwargs)


# ---------------------- HELP COMMAND ---------------------- #
@app.on_message(filters.command(["help", "helpme"], prefixes=COMMAND_PREFIXES) & filters.me)
async def module_help(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    # get bot username only when needed (avoid raising if bot not started)
    try:
        bot_username = (await app.get_me()).username or ""
    except Exception:
        bot_username = ""

    # .help <module> → direct
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:]).strip()

    # .help → show all modules or inline panel
    elif not message.reply_to_message and len(cmd) == 1:
        await message.edit_text("⏳ Loading help menu...")
        # Try inline bot results first (fancy panel)
        try:
            if bot_username:
                nice = await client.get_inline_bot_results(bot=bot_username, query="helper")
                # send the first inline result
                await asyncio.gather(
                    message.delete(),
                    client.send_inline_bot_result(message.chat.id, nice.query_id, nice.results[0].id),
                )
                return
        except Exception as e:
            # fallback to text table if inline fails
            print(f"[HELP INLINE ERROR] {e}")

        # Fallback → show table list
        try:
            ac = PrettyTable()
            ac.header = False
            ac.title = "BOTMINE TECH PLUGINS"
            ac.align = "l"
            for x in split_list(sorted(CMD_HELP.keys()), 2):
                ac.add_row([x[0], x[1] if len(x) >= 2 else None])

            xx = await client.send_message(
                message.chat.id,
                f"```{str(ac)}```\n• @BOTMINE_TECH × @BOTMINE_SUPPORT •",
                reply_to_message_id=ReplyCheck(message),
            )
            await xx.reply_text("**Usage:** `.help module_name` — to view command details.")
            return
        except Exception as e:
            # if even fallback fails, show a minimal message
            print(f"[HELP FALLBACK ERROR] {e}")
            return await message.edit_text("❌ Failed to load help. Try again later.")

    # show help for a specific module
    if help_arg:
        help_key = help_arg.lower()
        if help_key in CMD_HELP:
            commands: dict = CMD_HELP[help_key]
            this_command = f"──「 **Help for {help_key.upper()}** 」──\n\n"
            for x in commands:
                # show all accepted prefixes in the output
                prefix_forms = " / ".join([f"{p}{x}" for p in COMMAND_PREFIXES])
                this_command += f"  • **Command:** `{prefix_forms}`\n  • **Function:** `{commands[x]}`\n\n"
            this_command += "\n© [BOTMINE SUPPORT](https://t.me/BOTMINE_SUPPORT)"
            await edit_or_reply(message, this_command, parse_mode=enums.ParseMode.MARKDOWN)
        else:
            await edit_or_reply(message, f"❌ `{help_arg}` is not a valid module name.")


# ---------------------- MODULE LIST COMMAND ---------------------- #
@app.on_message(filters.command(["plugins", "modules"], prefixes=COMMAND_PREFIXES) & filters.me)
async def module_helper(client: Client, message: Message):
    cmd = message.command
    help_arg = ""
    if len(cmd) > 1:
        help_arg = " ".join(cmd[1:]).strip()
    elif message.reply_to_message and len(cmd) == 1:
        help_arg = message.reply_to_message.text

    # Show all modules
    if not message.reply_to_message and len(cmd) == 1 and not help_arg:
        ac = PrettyTable()
        ac.header = False
        ac.title = "BOTMINE USERBOT PLUGINS"
        ac.align = "l"
        for x in split_list(sorted(CMD_HELP.keys()), 2):
            ac.add_row([x[0], x[1] if len(x) >= 2 else None])
        await edit_or_reply(
            message, f"```{str(ac)}```\n• @BOTMINE_TECH × @BOTMINE_SUPPORT •"
        )
        await message.reply_text("**Usage:** `.help <module>` — to see command details.")
        return

    # Show module details
    if help_arg:
        help_key = help_arg.lower()
        if help_key in CMD_HELP:
            commands: dict = CMD_HELP[help_key]
            this_command = f"──「 **Help for {help_key.upper()}** 」──\n\n"
            for x in commands:
                prefix_forms = " / ".join([f"{p}{x}" for p in COMMAND_PREFIXES])
                this_command += f"  • **Command:** `{prefix_forms}`\n  • **Function:** `{commands[x]}`\n\n"
            this_command += "© [BOTMINE SUPPORT](https://t.me/BOTMINE_SUPPORT)"
            await edit_or_reply(message, this_command, parse_mode=enums.ParseMode.MARKDOWN)
        else:
            await edit_or_reply(message, f"❌ `{help_arg}` is not a valid module name.")


# ---------------------- ADD COMMAND HELP ---------------------- #
def add_command_help(module_name, commands):
    """
    Register new commands to the global CMD_HELP dict.
    usage: add_command_help("module", [["cmd", "desc"], ["cmd2","desc2"]])
    """
    key = module_name.lower()
    if key not in CMD_HELP:
        CMD_HELP[key] = {}

    for command, desc in commands:
        # store command in lowercase for consistent lookup
        CMD_HELP[key][command] = desc
