import discord
from discord.ext import commands
import os

LOG_CHANNEL_NAME = "logs"

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

def get_log_channel(guild: discord.Guild):
    return discord.utils.get(guild.text_channels, name=LOG_CHANNEL_NAME)

@bot.event
async def on_message_delete(message: discord.Message):
    if not message.guild or message.author.bot:
        return
    log_channel = get_log_channel(message.guild)
    if not log_channel:
        return
    content = message.content if message.content else "[no text – maybe attachment/embed]"
    await log_channel.send(
        f"🗑️ Message deleted in #{message.channel.name} by {message.author}:\n> {content}"
    )

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if not before.guild or before.author.bot:
        return
    if before.content == after.content:
        return
    log_channel = get_log_channel(before.guild)
    if not log_channel:
        return
    await log_channel.send(
        f"✏️ Message edited in #{before.channel.name} by {before.author}:\n"
        f"**Before:** {before.content}\n"
        f"**After:**  {after.content}"
    )

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

