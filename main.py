# Made by Quaron. Discord -> quaron
# imports. VERY IMPORTANT. Removing even one of these would break the entire code.
import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import random
# intents, newgen bs (important still)
intents = discord.Intents.all()

# defining the bot, extremely important
bot = commands.Bot(command_prefix="/", intents=intents)


# The beauty of Python (and pretty much any other programming language) is to reduce your work

# These are so-called 'helper functions' and they will make my work easier.
ECON_FILE = "econ.json"

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
        data[user_id] = {"balance": 0}

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
        data[user_id] = {"balance": 0}

    data[user_id]["balance"] -= amount
    if data[user_id]["balance"] < 0:
        data[user_id]["balance"] = 0

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Notifies when it's online.
@bot.event
async def on_ready():
    print(f"Successfully logged in as {bot.user}")
    await bot.tree.sync()
    print("Commands synced globally! (Synced to every server, though making the bot rejoin is recommanded. Rejoining the bot will NOT reset the economy. \nTo reset the economy, delete everything in the 'econ.json' file.")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name="the server"))
    print("Presence changed! It says 'Watching the server' as of now, with the idle status. (This message is not dynamic) \nInvite link: https://discord.com/oauth2/authorize?client_id=1415427601291284480&permissions=8&integration_type=0&scope=bot")
# test command
@bot.tree.command(name="wakeup", description="Is the bot alive?")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Awake! Latency is {round(bot.latency * 1000)}ms!")

# invite command sends the invite n stuff, recommanded to remove !!!
@bot.tree.command(name="invite", description="Fetches the invite link, though this bot isn't meant for public use.")
async def invite(interaction: discord.Interaction):
    await interaction.response.send_message(f"This is my invite link! \nhttps://discord.com/oauth2/authorize?client_id=1415427601291284480&permissions=8&integration_type=0&scope=bot")

# kick command
@bot.tree.command(name="kick", description="Kicks a user.")
@app_commands.describe(member="The member to kick", reason="Reason for the kick")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    # check permissions
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("Thy lack the permission to kicketh!", ephemeral=True)
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


# ban command
@bot.tree.command(name="ban", description="Bans a user.")
@app_commands.describe(member="The member to ban", reason="Reason for the ban.")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    # check permissions
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("Thy lack the permission to banish!", ephemeral=True)
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

SHOP_FILE = "shop.json"

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

@bot.tree.command(name="warn", description="Warns a user.")
@app_commands.describe(member="The member to warn", reason="Reason for the warn.")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if not interaction.user.guild_permissions.kick_members:
        await interaction.response.send_message("You lack the permission to warn!", ephemeral=True)
        return

    if member == interaction.user:
        await interaction.response.send_message("Thy cannot warn thee!", ephemeral=True)
        return
    if not os.path.exists(ECON_FILE) or os.stat(ECON_FILE).st_size == 0:
        data = {}
    else:
        with open(ECON_FILE, "r") as f:
            data = json.load(f)
        user_id = str(member.id)

    if user_id not in data:
        data[user_id] = {"balance": 0,
                         "warnings": 0}
    data[user_id]["warnings"] += 1
    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)
    await interaction.response.send_message(f"Warn has been issued to {member.mention}. Reason: {reason or 'No reason provided'}.")

# ---------------------------------------------------------------------------- ECONOMY ----------------------------------------------------------------------------
# Economy setup. Messes with the 'econ.json' file. (all the economy is preserved there)

@bot.tree.command(name="setup", description="Sets up the economy")
async def setup(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Administrator permissions are required to run this command.")
        return
    guild = interaction.guild

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
            data[user_id] = {"balance": 100,
                             "warnings": 0}
            added.append(member.name)

    await interaction.response.send_message(f"Added {len(added)} members to the economy: {', '.join(added)}")

    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)


# Event that detects whenever a new member joins. It connects them to the economy system! (BOT MUST BE ONLINE)
@bot.event
async def on_member_join(member):
    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    user_id = str(member.id)
    if member.bot:
        return


    if user_id not in data:
        data[user_id] = {"balance": 100,
                         "warnings": 0}

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
            data[user_id] = {"balance": 100, "warnings": 0}
        data[user_id]["balance"] = data[user_id].get("balance", 0) + amount


    with open(ECON_FILE, "w") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(f"Paycheck {role.mention}! Sent {amount} aureus.")

@bot.tree.command(name="paycheckglobal", description="PAYCHECK FOR EVERYONE!!")
async def paycheckglobal(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You need admin perms to do this!", ephemeral=True)
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
            data[user_id] = {"balance": 0, "warnings": 0}

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
        return

    with open(ECON_FILE, "r") as f:
        data = json.load(f)

    user_id = str(member.id)
    if user_id not in data:
        data[user_id] = {"balance": 0, "warnings": 0}


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
            data[user_id] = {"balance": 0, "warnings": 0}

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
    return [(name, name) for name in shop.keys()]  # tuple: (display, value)

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


# reads the 'token.txt' file and defines it as a variable called 'token' which is later implemented down below.
with open("token.txt", "r") as f:
    token=f.read().strip()
# connects the code to the bot itself. IMPORTANT !!!
bot.run(token)
