import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta, time
import os
from dotenv import load_dotenv
load_dotenv()

class Client(commands.Bot):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  async def setup_hook(self):
    self.clearAllStatus.start()

  async def on_ready(self):
    print("Status Bot is ready and connected")
    # Sync the newly added commands
    try:
      guild = discord.Object(id = os.getenv("SERVER_ID"))
      await self.tree.sync(guild=guild)
      print("Commands synced successfully!")
    except Exception as e:
      print("Error! Could not sync commands. " + str(e))

  @tasks.loop(time = time(hour = 0, minute = 0, tzinfo = timezone(timedelta(hours = 3))))
  async def clearAllStatus(self):
    embed = discord.Embed(title="Status Log", color=discord.Color.blue())
    for i in users:
      if i["since"] != -1:
        # status list
        list = "".join(f'<@{i["user"]}> **Reason:** {i["reason"]} **Duration:** {i["duration"]} **Since:** {i["since"]}')
        embed.add_field(name = "", value = list, inline = False)
    channel = self.get_channel(int(os.getenv("CHANNEL_ID")))
    await channel.send(embed = embed)
    for i in users:
      i["since"] = -1

  # wait until bot initialize before starting schedule, avoid race condition.
  @clearAllStatus.before_loop
  async def before_clearAllStatus(self):
    await self.wait_until_ready()

  # Ignore self message
  async def on_message(self, message):
    if message.author == self.user:
      return

#  {
#   "user": userID,
#   "reason": "String",
#   "duration": "String ends with h or m",
#   "since": current date&time
#  }
users = []

intents = discord.Intents.default()
intents.message_content = True

# commands start with '/'
client = Client(command_prefix = "/", intents = intents)

# server ID
GUILD_ID = discord.Object(id = os.getenv("SERVER_ID"))

@client.tree.command(name = "afk", description = "Setup your status", guild = GUILD_ID)
async def setupStatus(interaction: discord.Interaction, reason: str, duration: str):
  found = False
  validDuration = False
  # only accept input that ends with 'h' or 'm'
  if duration.endswith('h') or duration.endswith('m'):
    validDuration = True

  if validDuration:
    # Will ignore for first user as len(users) == 0
    for i in users:
      if interaction.user.id == i["user"]:
        i["reason"] = reason
        i["duration"] = duration
        # time UTC+3
        i["since"] = datetime.now(timezone(timedelta(hours = 3))).strftime("%Y-%m-%d %H:%M")
        found = True
        break
    if not found:
      users.append(
        {
          "user": interaction.user.id,
          "reason": reason,
          "duration": duration,
          # time UTC+3
          "since": datetime.now(timezone(timedelta(hours = 3))).strftime("%Y-%m-%d %H:%M"),
        }
      )
    await interaction.response.send_message("Status updated successfully!", ephemeral=True)
  else:
    await interaction.response.send_message("Please enter the duration as number followed by 'm' for minutes and 'h' for hours", ephemeral = True)

@client.tree.command(name = "status", description = "Show users status list", guild = GUILD_ID)
async def printStatus(interaction: discord.Interaction):
  embed = discord.Embed(title="Status List", color=discord.Color.blue())
  for i in users:
    if i["since"] != -1:
      # status list
      list = "".join(f'<@{i["user"]}> **Reason:** {i["reason"]} **Duration:** {i["duration"]} **Since:** {i["since"]}')
      embed.add_field(name = "", value = list, inline = False)
  await interaction.response.send_message(embed = embed)

@client.tree.command(name = "clear", description = "Clear user status", guild = GUILD_ID)
async def clearStatus(interaction: discord.Interaction):
  for i in users:
    # set "since" to -1, invalid input.
    if i["user"] == interaction.user.id:
      i["since"] = -1
      break
  await interaction.response.send_message("Status cleared successfully!", ephemeral = True)

client.run(os.getenv("DISCORD_TOKEN"))