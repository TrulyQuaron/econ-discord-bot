# Made by Quaron. Discord -> @quaron
# imports. VERY IMPORTANT. Removing even one of these would break the entire code.
import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import random
import asyncio
from datetime import timedelta
import time
import discord
# intents, newgen bs (important still)
intents = discord.Intents.all()

# defining the bot, extremely important
bot = commands.Bot(command_prefix="/", intents=intents)

active_executions = {}

# The beauty of Python (and pretty much any other programming language) is to reduce your work

# These are so-called 'helper functions' and they will make my work easier.
ECON_FILE = "econ.json"
# ---- gambling helpers ----
MIN_BET = 10

def _validate_bet(interaction: discord.Interaction, amount: int) -> str | None:
    if amount < MIN_BET:
        return f"Bet must be at least {MIN_BET}."
    if get_balance(interaction.user.id) < amount:
        return "You don't have enough aureus for that bet. Beg on the street, gambler."
    return None

def get_balance(user_id):
    with open(ECON_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), {}).get("balance", 0)  # default to 0

def add_balance(user_id, amount):
    user_id = str(user_id)
    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

    data[user_id]["balance"] += amount

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def remove_balance(user_id, amount):
    user_id = str(user_id)
    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

    data[user_id]["balance"] -= amount
    if data[user_id]["balance"] < 0:
        data[user_id]["balance"] = 0

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_points(user_id):
    with open(ECON_FILE, "r") as f:
        data = json.load(f)
    return data.get(str(user_id), {}).get("points", 0)  # default to 0

def add_points(user_id, amount):
    user_id = str(user_id)
    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

    data[user_id]["points"] += amount

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

def remove_points(user_id, amount):
    user_id = str(user_id)
    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

    data[user_id]["points"] -= amount
    if data[user_id]["points"] < 0:
        data[user_id]["points"] = 0

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)




# Notifies when it's online.
@bot.event
async def on_ready():
    print(f"Successfully logged in as {bot.user}")
    await bot.tree.sync()
    print("Commands synced globally! (Synced to every server, though making the bot rejoin is recommanded. Rejoining the bot will NOT reset the economy. \nTo reset the economy, delete everything in the 'econ.json' file.")
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="I use slash commands! Type /help for all commands."))
    print("Presence changed! It says 'Playing I use slash commands! Type /help for all commands.' as of now, with the online status. (This message is not dynamic) \nInvite link: https://discord.com/oauth2/authorize?client_id=1415427601291284480&permissions=8&integration_type=0&scope=bot")
# test command
@bot.tree.command(name="ping", description="Is the bot alive?")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Awake! Latency is {round(bot.latency * 1000)}ms!")

@bot.tree.command(name="code", description="Link to source code on GitHub!")
async def code(interaction: discord.Interaction):
    await interaction.response.send_message(f"Source code available and free to use on https://github.com/TrulyQuaron/econ-discord-bot/releases/ !")

# kick command
@bot.tree.command(name="kick", description="Kicks a user.")
@app_commands.describe(member="The member to kick", reason="Reason for the kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    # check permissions
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("Thy lack the permission to kicketh!", ephemeral=True)
        print(f"Kick command attempted usage by {member.name}. Forbidden.")
        return
    
    if member == interaction.user:
        await interaction.response.send_message("Thy cannot banish thee!", ephemeral=True)
        return
    
    if member == interaction.guild.me:
        await interaction.response.send_message("I shall NOT removeth myself!", ephemeral=True)
        return

    # KICK
    await member.kick(reason=reason)
    await interaction.response.send_message(f"{member.name} has been kicked. Reason: {reason or 'No reason provided.'}")
    await user.send(f"You have been kicked in {interaction.guild.name}. Reason: {reason or 'No reason provided'}")


# ban command
@bot.tree.command(name="ban", description="Bans a user.")
@app_commands.describe(member="The member to ban", reason="Reason for the ban.")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    # check permissions
    if not interaction.user.guild_permissions.ban_members:
        await interaction.response.send_message("Thy lack the permission to banish!", ephemeral=True)
        print(f"Ban command attempted usage by {member.name}. Forbidden.")
        return

    if member == interaction.user:
        await interaction.response.send_message("Thy cannot kicketh thee!", ephemeral=True)
        return

    if member == interaction.guild.me:
        await interaction.response.send_message("I shall NOT removeth myself!", ephemeral=True)
        return

    # ban
    await member.ban(reason=reason)
    await interaction.response.send_message(f"{member.name} has been banned. Reason: {reason or 'No reason provided.'}")
    await user.send(f"You have been banned in {interaction.guild.name}. Reason: {reason or 'No reason provided'}")

SHOP_FILE = "shop.json"
# helper function again
def load_shop():
    if not os.path.exists(SHOP_FILE) or os.stat(SHOP_FILE).st_size == 0:
        return {"shop": {}}
    with open(SHOP_FILE, "r") as f:
        return json.load(f)

@bot.tree.command(name="shop", description="View the items available in the shop")
async def shop(interaction: discord.Interaction):
    data = load_shop()
    shop_items = data.get("shop", {})

    if not shop_items:
        await interaction.response.send_message("The shop is currently empty!", ephemeral=True)
        return

    msg = "** Shop Items:**\n"
    for item_id, info in shop_items.items():
        msg += f"**{info['name']}** — {info['price']} aureus\n"

    await interaction.response.send_message(msg, ephemeral=True)

# Warn command

from datetime import datetime

@bot.tree.command(name="warn", description="Warns a user.")
@app_commands.describe(member="The member to warn", reason="Reason for the warning.")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("You lack the permission to warn!", ephemeral=True)
        print(f"Warn command attempted usage by {interaction.user.name}. Forbidden.")
        return

    if member == interaction.user:
        await interaction.response.send_message("You cannot warn yourself!", ephemeral=True)
        return

    if member.bot:
        await interaction.response.send_message("You can’t warn a bot.", ephemeral=True)
        return

    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    user_id = str(member.id)


    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

    if not isinstance(data[user_id].get("warnings"), list):
        data[user_id]["warnings"] = []


    new_warn = {
        "reason": reason or "No reason provided.",
        "moderator": interaction.user.name
    }

    data[user_id]["warnings"].append(new_warn)


    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(
        f"Warn issued to {member.mention}. Reason: {reason or 'No reason provided.'}"
    )



@bot.tree.command(name="timeout", description="Times out a user for a set amount of minutes (0 removes timeout).")
@app_commands.describe(member="The member to timeout",minutes="Duration in minutes (0 = remove timeout)",warn="Also add a warning to their record?",reason="Reason (optional)")
async def timeout_cmd(interaction: discord.Interaction,member: discord.Member,minutes: int,warn: bool = False,reason: str | None = None):
    # Permission checks
    if not interaction.user.guild_permissions.moderate_members:
        await interaction.response.send_message("You lack the **Moderate Members** permission.", ephemeral=True)
        return
    if not interaction.guild.me.guild_permissions.moderate_members:
        await interaction.response.send_message("I’m missing the **Moderate Members** permission.", ephemeral=True)
        return

    if member.id == interaction.user.id:
        await interaction.response.send_message("You can’t timeout yourself.", ephemeral=True)
        return
    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("Their top role is higher or equal to mine. I can’t timeout them.", ephemeral=True)
        return


    until = None if minutes <= 0 else (discord.utils.utcnow() + timedelta(minutes=minutes))


    try:
        if hasattr(member, "timeout"):  # modern
            await member.timeout(until, reason=reason or f"Timeout by {interaction.user}")
        else:
            await member.timeout(until, reason=reason or f"Timeout by {interaction.user}")
    except discord.Forbidden:
        await interaction.response.send_message("I don’t have permission or role position to timeout that member.", ephemeral=True)
        return
    except TypeError:
        # In case kwargs mismatch on some versions, try the other method
        try:
            await member.timeout(until, reason=reason or f"Timeout by {interaction.user}")
        except Exception as e:
            await interaction.response.send_message(f"Failed to apply timeout: {e}", ephemeral=True)
            return
    except Exception as e:
        await interaction.response.send_message(f"Failed to apply timeout: {e}", ephemeral=True)
        return

    if warn:
        if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
            data = {}
        else:
            with open(ECON_FILE, "r") as f:
                data = json.load(f)

        uid = str(member.id)
        if uid not in data:
            data[uid] = {"balance": 0, "warnings": []}
            new_warn = {
        "reason": "Timed out.",
        "moderator": interaction.user.name
    }

        data[user_id]["warnings"].append(new_warn)

        with open(ECON_FILE, "w") as f:
            json.dump(data, f, indent=4)


    if until is None:
        msg = f"Removed timeout for {member.mention}."
    else:
        msg = f"Timed out {member.mention} for **{minutes}** minute(s)."
    if reason:
        msg += f" Reason: {reason}"
    if warn:
        msg += " A warning was also issued."

    await interaction.response.send_message(msg)
@bot.tree.command(name="clearwarnings", description="Clears all or specific warnings for a user.")
@app_commands.describe(
    member="The member whose warnings you want to clear",
    index="Optional: which warning number to clear (leave empty to clear all)"
)
async def clearwarnings(interaction: discord.Interaction, member: discord.Member, index: int = None):
    # permission check
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("You lack permission to clear warnings!", ephemeral=True)
        return

    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        await interaction.response.send_message("No economy file found.", ephemeral=True)
        return

    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    user_id = str(member.id)
    if user_id not in data or not data[user_id].get("warnings"):
        await interaction.response.send_message(f"{member.name} has no warnings to clear.", ephemeral=True)
        return

    warnings_list = data[user_id]["warnings"]

    # clear a specific warning
    if index is not None:
        if index < 1 or index > len(warnings_list):
            await interaction.response.send_message(f"Invalid warning index. {member.name} only has {len(warnings_list)} warning(s).", ephemeral=True)
            return

        removed = warnings_list.pop(index - 1)
        reason = removed.get("reason", "Unknown reason")
        moderator = removed.get("moderator", "Unknown moderator")
        await interaction.response.send_message(
            f"🧹 Removed warning #{index} from {member.mention}.\n> **Reason:** {reason}\n> **Issued by:** {moderator}",
            ephemeral=False
        )

    # clear all warnings
    else:
        data[user_id]["warnings"] = []
        await interaction.response.send_message(f"🧹 Cleared all warnings for {member.mention}.")

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.tree.command(name="warnings", description="Shows all warnings for a user.")
async def warnings(interaction: discord.Interaction, member: discord.Member):
    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    user_id = str(member.id)
    user_data = data.get(user_id, {})
    warnings_list = user_data.get("warnings", [])

    if not warnings_list:
        await interaction.response.send_message(f"{member.name} has no warnings.", ephemeral=True)
        return

    formatted = "\n".join(
        [f"⚠️ **{i+1}.** {w['reason']} — by *{w['moderator']}*" for i, w in enumerate(warnings_list)]
    )

    await interaction.response.send_message(f"**{member.name}’s Warnings:**\n{formatted}")

# ---------------------------------------------------------------------------- ECONOMY ----------------------------------------------------------------------------
# Economy setup. Messes with the 'econ.json' file. (all the economy is preserved there)
# also this file is actually extremely not sorted at all ignore the big bar

@bot.tree.command(name="setup", description="Sets up the economy")
async def setup(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Administrator permissions are required to run this command.")
        print(f"Setup command attempted usage by {interaction.user.name}. Forbidden.")
        return

    guild = interaction.guild

    # load or create econ file
    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    added = []
    for member in guild.members:
        if member.bot:
            continue

        user_id = str(member.id)
        if user_id not in data:
            data[user_id] = {"balance": 0, "points": 0, "warnings": []}
            added.append(member.name)

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(
        f"Added {len(added)} members to the economy."
    )




@bot.tree.command(name="coinflip", description="Flip a coin for aureus.")
@app_commands.describe(side="Pick heads or tails", amount="Your bet (aureus)")
@app_commands.choices(
    side=[
        app_commands.Choice(name="Heads", value="heads"),
        app_commands.Choice(name="Tails", value="tails"),
    ]
)
@app_commands.checks.cooldown(rate=1, per=5)
async def coinflip(interaction: discord.Interaction, side: app_commands.Choice[str], amount: int):
    err = _validate_bet(interaction, amount)
    if err:
        await interaction.response.send_message(err, ephemeral=True)
        return

    remove_balance(interaction.user.id, amount)

    import random
    result = random.choice(["heads", "tails"])
    win = (side.value == result)

    if win:
        add_balance(interaction.user.id, amount * 2)
        await interaction.response.send_message(
            f"🪙 It landed **{result}**! You won **+{amount}** (total returned {amount*2})."
        )
    else:
        await interaction.response.send_message(
            f"🪙 It landed **{result}**. You lost **-{amount}**."
        )

# Event that detects whenever a new member joins. It connects them to the economy system! (BOT MUST BE ONLINE and if it's not just run /setup)
@bot.event
async def on_member_join(member):
    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    user_id = str(member.id)
    if member.bot:
        return


    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Displays balance
@bot.tree.command(name="balance", description="Displays your balance.")
@app_commands.describe(member="Whose balance do you want to check (if empty it checks yours).")
async def balance(interaction: discord.Interaction, member: discord.Member = None):

    if member is None:
        user_id = interaction.user.id
        bal = get_balance(user_id)
        await interaction.response.send_message(f"Your balance is {bal} aureus.", ephemeral=True)
    else:
        user_id = member.id
        member_bal = get_balance(user_id)
        await interaction.response.send_message(f"{member.name}'s balance is {member_bal} aureus.", ephemeral=True)

# mining for balls :3
# @bot.tree.command(name="mine", description="Mine for balls.")
# @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
# async def mine(interaction: discord.Interaction):
#     with open(ECON_FILE, "r") as f:
#         data = json.load(f)
#     amount = random.randint(10, 50)
#     choice = random.randint(0,1)
#     if choice == 0:
#         remove_balance(interaction.user.id, amount)
#         await interaction.response.send_message(f"You went to the balls mine... however you dropped {amount} balls lmao")
#     else:
#         add_balance(interaction.user.id, amount)
#         await interaction.response.send_message(f"You went to the balls mine and mined out {amount} balls!!!!")

@bot.tree.command(name="execution", description="Start a vote to publicly execute someone.")
@app_commands.describe(member="The member to publicly execute", reason="Reason for public execution.")
async def execution(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    global active_executions
    if member == interaction.user:
        await interaction.response.send_message("You can't execute yourself 💀", ephemeral=True)
        return
    if member == interaction.guild.me:
        await interaction.response.send_message("why me :cry:", ephemeral=True)
        return

    guild_id = str(interaction.guild.id)
    if guild_id in active_executions:
        await interaction.response.send_message(
            "There’s already an active public execution vote! Cancel it first with `/cancelexecution`.",
            ephemeral=True
        )
        return

    votes_needed = 10
    embed = discord.Embed(
        title="! ! PUBLIC EXECUTION INITIATED ! !",
        description=f"Vote to publicly execute {member.mention} for **{reason or 'absolutely NOTHING!!!'}**.\nReact with 👍 to vote yes.\n⏳ Ends in 1 hour!",
        color=discord.Color.red()
    )
    embed.set_footer(text=f"Started by {interaction.user.display_name}")

    await interaction.response.send_message(embed=embed)
    msg = await interaction.original_response()
    await msg.add_reaction("👍")

    active_executions[guild_id] = {
        "message_id": msg.id,
        "target": member,
        "starter": interaction.user.id,
        "votes": set(),
        "ended": False
    }

    def check(reaction, user):
        return (
            str(reaction.emoji) == "👍"
            and reaction.message.id == msg.id
            and not user.bot
        )

    try:
        while True:
            reaction, user = await bot.wait_for("reaction_add", timeout=3600, check=check)
            if guild_id not in active_executions or active_executions[guild_id]["ended"]:
                return  # cancelled or expired

            active_executions[guild_id]["votes"].add(user.id)
            current_votes = len(active_executions[guild_id]["votes"])

            if current_votes >= votes_needed:
                await msg.reply(f"✅ EXECUTION VOTE PASSED ({current_votes} votes)! Public execution of {member.mention} begins in 1 minute.")
                await asyncio.sleep(60)

                await msg.reply(f"WELCOME TO {member.mention}'S PUBLIC EXECUTION!!, {member.name}, any last words?")
                await asyncio.sleep(3)
                await msg.reply(f"i don't care!!!!! commence execution!!!!!!")
                
                executed_balance = get_balance(member.id)
                remove_balance(member.id, executed_balance)

                try:
                    until = discord.utils.utcnow() + timedelta(minutes=5)
                    await member.timeout(until, reason=reason or "Public execution complete.")
                    await msg.reply(f"{member.mention} has been publicly executed. You can see their face, like you know they'll appear convinently in 5 minutes")
                except discord.Forbidden:
                    await msg.reply(f"THEY RESIST THE DEATH??? then i'll just rob them of their money haha goodbye")
                
                active_executions.pop(guild_id, None)
                return

    except asyncio.TimeoutError:
        if guild_id not in active_executions or active_executions[guild_id]["ended"]:
            return
        total_votes = len(active_executions[guild_id]["votes"])
        await msg.reply(f"❌ Execution expired after 1 hour. Total votes: {total_votes}")
        active_executions.pop(guild_id, None)


@bot.tree.command(name="cancelexecution", description="Cancel your active public execution vote.")
async def cancelexecution(interaction: discord.Interaction):
    global active_executions
    guild_id = str(interaction.guild.id)

    if guild_id not in active_executions:
        await interaction.response.send_message("There is no active public execution vote to cancel.", ephemeral=True)
        return

    execution_data = active_executions[guild_id]
    starter_id = execution_data["starter"]

    if interaction.user.id != starter_id and not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Only the person who started the execution (or an admin) can cancel it.", ephemeral=True)
        return

    active_executions[guild_id]["ended"] = True
    target = execution_data["target"]
    active_executions.pop(guild_id, None)

    await interaction.response.send_message(f"🛑 The public execution of {target.mention} has been cancelled by {interaction.user.mention}.")





# pay command
@bot.tree.command(name="pay", description="Pays a user a certain amount.")
async def pay(interaction: discord.Interaction, member: discord.Member, amount: int):
    payerBalance=get_balance(interaction.user.id)
    if payerBalance < amount:
        await interaction.response.send_message("You don't have enough money!", ephemeral=True)
    else:
        remove_balance(interaction.user.id, amount)
        add_balance(member.id, amount)
        await interaction.response.send_message(f"Payment complete! Sent {amount} aureus to {member.mention}!")
# Setpay command

@bot.tree.command(name="setpay", description="Sets the paycheck amount for a specified role. Users get paid based off their highest paying role.")
async def setpay(interaction: discord.Interaction, role: discord.Role, amount: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You lack the permission to issue this command.", ephemeral=True)
        print(f"Setpay command attempted usage by {member.name}. Forbidden.")
        return

    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    role_id = str(role.id)

    if "roles" not in data:
        data["roles"] = {}
    data["roles"][role_id] = amount


    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(f"Success! Set the pay for the role **{role.name}** ({role.id}) to {amount} aureus.")

@bot.tree.command(name="paycheck", description="Paycheck time!")
async def paycheck(interaction: discord.Interaction, role: discord.Role):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Administrator permissions are required to set give out a paycheck.", ephemeral=True)
        print(f"Paycheck command attempted usage by {member.name}. Forbidden.")
        return
    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    members_with_role = [m for m in interaction.guild.members if role in m.roles]
    role_id = str(role.id)
    amount = data["roles"].get(role_id, 0)
    
    for member in members_with_role:
        user_id = str(member.id)
    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}
        data[user_id]["balance"] = data[user_id].get("balance", 0) + amount


    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(f"Paycheck {role.mention}! Sent {amount} aureus.")

@bot.tree.command(name="givepoints", description="Gives a user points.")
async def givepoints(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Administrator permissions are required for this command!", ephemeral=True)
        print(f"Givepoints command attempted usage by {member.name}. Forbidden.")
        return
    else:
        memberid=member.id
        add_points(memberid, amount)
        await interaction.response.send_message(f"{amount} points have been given to {member.mention}!")

@bot.tree.command(name="removepoints", description="Removes a user points.")
async def removepoints(interaction: discord.Interaction, member: discord.Member, amount: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Administrator permissions are required for this command!", ephemeral=True)
        print(f"Removepoints command attempted usage by {member.name}. Forbidden.")
        return
    else:
        memberid=member.id
        remove_points(memberid, amount)
        await interaction.response.send_message(f"{amount} points have been removed to {member.mention}!")

@bot.tree.command(name="points", description="Gives a user points.")
async def points(interaction: discord.Interaction, member: discord.Member = None):
    if member == None:
        points = get_points(interaction.user.id)
        await interaction.response.send_message(f"{interaction.user.mention} points balance: {points}.", ephemeral=True)
    else:
        points = get_points(member.id)
        await interaction.response.send_message(f"{member.mention} points balance: {points}.", ephemeral=True)

@bot.tree.command(name="paycheckglobal", description="PAYCHECK FOR EVERYONE!!")
async def paycheckglobal(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin perms to do this!", ephemeral=True)
        print(f"Paycheckglobal command attempted usage by {member.name}. Forbidden.")
        return

    guild = interaction.guild


    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    role_pays = data.get("roles", {})

    updated = []
    for member in guild.members:
        if member.bot:
            continue

        user_id = str(member.id)


    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

        highest_pay = 0
        for role in member.roles:
            rpay = role_pays.get(str(role.id))
            if rpay and rpay > highest_pay:
                highest_pay = rpay


        data[user_id]["balance"] = data[user_id].get("balance", 0) + highest_pay

        updated.append(f"{member.name} (+{highest_pay})")

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(
        f"Paid everyone!\n" +
        "\n".join(updated[:10]) +
        (f"\n...and {len(updated)-10} more." if len(updated) > 10 else "")
    )
# setting taxes
@bot.tree.command(name="settax", description="Sets the tax amount for a role. Users are taxed based off their highest taxing role.")
async def settax(interaction: discord.Interaction, role: discord.Role, amount: int):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You lack admin permissions.", ephemeral=True)
        print(f"Settax command attempted usage by {member.name}. Forbidden.")
        return

    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)

    if "taxes" not in data:
        data["taxes"] = {}

    data["taxes"][str(role.id)] = amount

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(f"Set tax for role **{role.name}** ({role.id}) to {amount} aureus.")
# taxing
@bot.tree.command(name="tax", description="Taxes a specified user.")
async def tax(interaction: discord.Interaction, member: discord.Member):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You lack admin permissions.", ephemeral=True)
        print(f"Tax command attempted usage by {member.name}. Forbidden.")
        return

    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    user_id = str(member.id)
    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}


    highest_tax = 0
    role_taxes = data.get("taxes", {})
    for role in member.roles:
        t = role_taxes.get(str(role.id))
        if t and t > highest_tax:
            highest_tax = t

    data[user_id]["balance"] = max(0, data[user_id].get("balance", 0) - highest_tax)

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(f"{member.name} was taxed {highest_tax} aureus.")

# global taxing
@bot.tree.command(name="taxglobal", description="Taxes all users based off their highest taxing role.")
async def taxglobal(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You lack admin permissions.", ephemeral=True)
        print(f"Taxglobal command attempted usage by {member.name}. Forbidden.")
        return

    guild = interaction.guild

    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    role_taxes = data.get("taxes", {})
    updated = []

    for member in guild.members:
        if member.bot:
            continue

        user_id = str(member.id)
    if user_id not in data:
        data[user_id] = {"balance": 0, "points": 0, "warnings": []}

        highest_tax = 0
        for role in member.roles:
            t = role_taxes.get(str(role.id))
            if t and t > highest_tax:
                highest_tax = t

        data[user_id]["balance"] = max(0, data[user_id].get("balance", 0) - highest_tax)
        updated.append(f"{member.name} (-{highest_tax})")

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(
        f"Taxed everyone!\n" +
        "\n".join(updated[:10]) +
        (f"\n...and {len(updated)-10} more." if len(updated) > 10 else "")
    )

# begging, just to test if adding aureus works.
@bot.tree.command(name="beg", description="Get on the street and beg for money.")
@app_commands.checks.cooldown(rate=1, per=5)
async def beg(interaction: discord.Interaction):
    with open(ECON_FILE, "r") as f:
        data = json.load(f)
    amount = random.randint(10, 50)
    choice = random.randint(0, 1)
    if choice == 0:
        remove_balance(interaction.user.id, amount)
        await interaction.response.send_message(
            f"You got on the street to beg... And someone stole {amount} aureus from you! You tried to run, but didn't want to leave your current pile..."
        )
    else:
        add_balance(interaction.user.id, amount)
        await interaction.response.send_message(
            f"You got on the street to beg... And someone donated {amount} aureus to you!"
        )

@bot.tree.command(name="leaderboard", description="Shows the richest members on the server.")
async def leaderboard(interaction: discord.Interaction):
    guild = interaction.guild
    bal_list = []


    for member in guild.members:
        if member.bot:
            continue

        balance = get_balance(member.id)
        bal_list.append({
            "name": member.display_name,
            "balance": balance
        })


    bal_list.sort(key=lambda x: x["balance"], reverse=True)

    top10 = bal_list[:10]
    formatted = "\n".join([f"{i+1}. {entry['name']} — {entry['balance']} aureus"
                           for i, entry in enumerate(top10)])

    await interaction.response.send_message(f"** Leaderboard:**\n{formatted}")

@bot.tree.command(name="pointsleaderboard", description="Shows who has the most points on the server.")
async def pointsleaderboard(interaction: discord.Interaction):
    guild = interaction.guild
    bal_list = []


    for member in guild.members:
        if member.bot:
            continue

        balance = get_points(member.id)
        bal_list.append({
            "name": member.display_name,
            "balance": balance
        })


    bal_list.sort(key=lambda x: x["balance"], reverse=True)

    top10 = bal_list[:10]
    formatted = "\n".join([f"{i+1}. {entry['name']} — {entry['balance']} points"
                           for i, entry in enumerate(top10)])

    await interaction.response.send_message(f"** Leaderboard:**\n{formatted}")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"Slow down! Try again in {round(error.retry_after, 1)} seconds.", ephemeral=True
        )
    elif isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message(
            "That command does not exist! Use `/help` to see all commands.", ephemeral=True
        )
    else:
        raise error
# add role command
@bot.tree.command(name="addrole", description="Adds a role to a specified user.")
@app_commands.describe(member="The member to give the role", role="The role to add")
async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("You lack manage roles permissions.", ephemeral=True)
        print(f"Addrole command attempted usage by {member.name}. Forbidden.")
        return
    
    try:
        await member.add_roles(role)
        await interaction.response.send_message(f"Successfully added **{role.name}** to {member.mention}!")
    except Exception as e:
        await interaction.response.send_message(f"Failed to add role: {e}", ephemeral=True)


# remove role command
@bot.tree.command(name="removerole", description="Removes a role from a specified user.")
@app_commands.describe(member="The member to remove the role from", role="The role to remove")
async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("You lack manage roles permissions.", ephemeral=True)
        print(f"Removerole command attempted usage by {member.name}. Forbidden.")
        return
    
    try:
        await member.remove_roles(role)
        await interaction.response.send_message(f"Successfully removed **{role.name}** from {member.mention}!")
    except Exception as e:
        await interaction.response.send_message(f"Failed to remove role: {e}", ephemeral=True)


# create role command
@bot.tree.command(name="createrole", description="Create a new role in the server")
@app_commands.describe(name="The name of the role to create", color="The color of the role (hex, optional)")
async def createrole(interaction: discord.Interaction, name: str, color: str = None):
    # check permissions
    if not interaction.user.guild_permissions.manage_roles:
        await interaction.response.send_message("You lack the permission to create roles.", ephemeral=True)
        print(f"Createrole command attempted usage by {member.name}. Forbidden.")
        return

    guild = interaction.guild
    try:
        role_color = discord.Color.default()
        if color:
            try:
                role_color = discord.Color(int(color.replace("#", ""), 16))
            except ValueError:
                await interaction.response.send_message("Invalid color format! Use a hex code like #ff0000.", ephemeral=True)
                return

        new_role = await guild.create_role(name=name, color=role_color, reason=f"Created by {interaction.user}")
        await interaction.response.send_message(f"Role **{new_role.name}** has been created!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to create roles.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
# helper function to get items from shop.json
def get_shop_items():
    if not os.path.exists("shop.json") or os.stat("shop.json").st_size == 0:
        return []
    with open("shop.json", "r") as f:
        shop = json.load(f)
    return [(name, name) for name in shop.keys()]

@bot.tree.command(name="clear", description="Clears a number of messages from a channel.")
@app_commands.describe(
    amount="How many messages to delete (max 100 at once)",
    user="Optionally delete messages only from this user"
)
async def clear(interaction: discord.Interaction, amount: int, user: discord.User = None):
    # check perms
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("You lack permission to manage messages!", ephemeral=True)
        return

    if amount <= 0:
        await interaction.response.send_message("You must specify a positive number of messages.", ephemeral=True)
        return

    if amount > 100:
        amount = 100

    await interaction.response.defer(ephemeral=True)

    def check(msg: discord.Message):
        if msg.pinned:
            return False
        if user is not None:
            return msg.author.id == user.id
        return True

    # purge the messages
    deleted = await interaction.channel.purge(limit=amount, check=check)
    count = len(deleted)

    await interaction.followup.send(
        f"Cleared **{count}** message(s){' from ' + user.mention if user else ''} in {interaction.channel.mention}.",
        ephemeral=True)

# /buy command with dynamic choices
@bot.tree.command(name="buy", description="Buy an item from the shop.")
@app_commands.describe(item="The item you want to buy")
async def buy(interaction: discord.Interaction, item: str):
    # load shop
    if not os.path.exists("shop.json"):
        await interaction.response.send_message("The shop is empty!", ephemeral=True)
        return

    with open("shop.json", "r") as f:
        shop = json.load(f)

    if item not in shop:
        await interaction.response.send_message("That item does not exist!", ephemeral=True)
        return

    price = shop[item]["price"]
    user_balance = get_balance(interaction.user.id)

    if user_balance < price:
        await interaction.response.send_message(f"You don’t have enough aureus! ({price} needed)", ephemeral=True)
        return

    remove_balance(interaction.user.id, price)


    inventory_file = "inventory.json"
    if os.path.exists(inventory_file) and os.stat(inventory_file).st_size > 0:
        with open(inventory_file, "r") as f:
            inventory = json.load(f)
    else:
        inventory = {}

    user_id = str(interaction.user.id)
    if user_id not in inventory:
        inventory[user_id] = []

    inventory[user_id].append(item)

    with open(inventory_file, "w") as f:
        json.dump(inventory, f, indent=4)

    await interaction.response.send_message(f"You bought **{item}** for {price} aureus!")

# dynamic autocomplete for the 'item' argument
@buy.autocomplete("item")
async def buy_autocomplete(interaction: discord.Interaction, current: str):
    items = get_shop_items()
    return [app_commands.Choice(name=name, value=value) for name, value in items if current.lower() in name.lower()]
# HELP COMMAND
@bot.tree.command(name="help", description="Displays all commands")
async def help(interaction: discord.Interaction):
    commands_list = "\n".join([f"/{cmd.name} - {cmd.description}" for cmd in bot.tree.walk_commands()])
    await interaction.response.send_message(f"Commands:\n{commands_list} \nTo find out how to use a command, type '/' and the name of the command! \n`Made by Quaron! Discord: quaron`", ephemeral=True)
    
# in case someone writes a command that doesn't exist
@bot.event
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandNotFound):
        await interaction.response.send_message(
            "That command does not exist! Use `/help` to see all commands. (If you still see the slash command, you should probably contact the owner or an administrator (or quaron)", ephemeral=True
        )
    else:
        raise error
# in case someone writes an unknown command
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command does not exist! Try `/help` to see all commands.")
    else:
        raise error  # re-raise other errors so you can debug them


token=os.getenv("TOKEN")
# connects the code to the bot itself. IMPORTANT !!!
bot.run(token)







