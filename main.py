import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class Client(commands.Bot):
  async def on_ready(self):
    print("Status Bot is ready and connected")
    # Sync the newly added commands
    try:
      guild = discord.Object(id = 777611696884678716)
      await self.tree.sync(guild=guild)
      print("Commands synced successfully!")
    except Exception as e:
      print("Error! Could not sync commands. " + str(e))

  # Ignore self message
  async def on_message(self, message):
    # Ignore self message
    if message.author == self.user:
      return

#  {
#   "user": userID,
#   "reason": "argument",
#   "duration": "argument",
#   "since": current date&time
#  }
users = []

intents = discord.Intents.default()
intents.message_content = True

client = Client(command_prefix = "/", intents = intents)

# mjls alsh3b server ID
GUILD_ID = discord.Object(id = 777611696884678716)

@client.tree.command(name = "afk", description = "Setup your status", guild = GUILD_ID)
async def setupStatus(interaction: discord.Interaction):
  await interaction.response.send_message("The feature is not fully implemented yet :>")

client.run('')