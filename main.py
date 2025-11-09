import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load bot token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Enable intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    print("Bot is online and ready to DM members!")

# 📨 Command: DM all members
@bot.command()
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, message: str = None):
    if not message:
        return await ctx.send("❌ Please provide a message.\nExample: `?dmall Hello everyone!`")

    await ctx.send("📨 Sending DMs to all members...")

    count = 0
    for member in ctx.guild.members:
        if member.bot:
            continue
        try:
            await member.send(message)
            count += 1
        except discord.Forbidden:
            continue  # Can't DM this user
        except Exception as e:
            print(f"Error sending to {member}: {e}")

    await ctx.send(f"✅ Sent DMs to **{count}** members!")

# 📨 Command: DM members of a specific role
@bot.command()
@commands.has_permissions(administrator=True)
async def drole(ctx, role: discord.Role = None, *, message: str = None):
    if not role or not message:
        return await ctx.send("❌ Usage: `?drole @Role Your message here`")

    await ctx.send(f"📨 Sending DMs to members with role **{role.name}**...")

    count = 0
    for member in role.members:
        if member.bot:
            continue
        try:
            await member.send(message)
            count += 1
        except discord.Forbidden:
            continue
        except Exception as e:
            print(f"Error sending to {member}: {e}")

    await ctx.send(f"✅ Sent DMs to **{count}** members with role `{role.name}`!")

# ⚠️ Error Handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need Administrator permission to use this command.")
    else:
        print(error)

bot.run(TOKEN)
