from io import StringIO
from re import X
import discord
from discord import embeds
from discord import Intents
import random

prefix = "s!"
color = 0x7B00FF


afkList = []
with open("afkList.txt", "r") as f:
  afkList = f.read()
  afkList = afkList.split("||")
  afkList.remove("")
  for i in range(len(afkList)):
    afkList[i] = afkList[i].split(",") 

intents = Intents.default()
intents.members = True
client = discord.Client(intents=intents)

def getuser_id(id):
  if id[0] != "<":
    return id
  user = id[2:][:-1]
  if user[0] == "!":
    user = user[1:]
  return int(user)

def message_spliter(message, parts):
  final_message = message.split(" ", parts)
  for i in range(parts):
    if final_message[i] == " ":
      final_message.pop(i)
  return final_message

def save_afkList(reason, id):
  with open("afkList.txt", "a") as f:
    f.write(f"||{reason},{id}")

def clearitem_afkList(id):
  reason = None
  for i in afkList:
    if i[0] == str(id):
      reason = i[1]

  with open('afkList.txt', 'r') as file :
    filedata = file.read()

  filedata = filedata.replace(f"||{id},{reason}", '')

  with open('afkList.txt', 'w') as file:
    file.write(filedata)


@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game('with squishy cats'))
  print(f"Logged in as {client.user.name}")

@client.event
async def on_message(message):

  # Makes sure its not replying it its self
  if message.author == client.user:
    return

  # Gets users that are afk if the bot goes down
  if afkList:
    for i in afkList:
      if i[0] in message.content:
        await message.reply(f"They are afk for **{i[1]}**", mention_author=True)

  # -----------  Help command -------------
  if message.content.lower().startswith("s!help"):
    embedMessage = discord.Embed(title="Heres a list of my commands!", color=color)
    embedMessage.add_field(name="Fun:", value="s!pfp @user,\ns!ship", inline=True)
    embedMessage.add_field(name="Utilities:", value="s!ping\ns!afk (reason)\ns!unafk", inline=True)
    embedMessage.add_field(name="Bot hisotry", value="This is for my baby Naomi\nWritten by Apple", inline=False)
    embedMessage.set_footer(text=f"Requested by {message.author.name}")
    await message.channel.send(embed=embedMessage)

  # ------- UTILITIES -------
  if message.content.lower().startswith("s!ping"):
    await message.channel.send("pong")

  if message.content.lower().startswith("s!afk"):
    if "[AFK]" in message.author.display_name:
      await message.reply("You are aready afk", mention_author=True)
      return
    try:
      await message.author.edit(nick=f"[AFK] {message.author.display_name}")
    except:
      pass

    afkList.append([str(message.author.id), message_spliter(message.content, 1)[1]])
    save_afkList(str(message.author.id), message_spliter(message.content, 1)[1])
    await message.reply(f"Your afk was set for, **{message_spliter(message.content, 1)[1]}**", mention_author=True)
  
  if message.content.lower().startswith("s!unafk"):
    if "[AFK]" in message.author.display_name:
      clearitem_afkList(message.author.id)
      for i in range(len(afkList)):
        if afkList[i][1] == str(message.author.id):
          afkList.pop(i)
        
      await message.author.edit(nick=None)
      await message.reply("You are no longer afk!", mention_author=True)

  # ------ FUN -------
  if message.content.lower().startswith("s!pfp"):
    split = message.content.split(" ")
    
    user = await client.fetch_user(getuser_id(split[1]))

    embedMessage = discord.Embed(title=f"{user.name}'s profile picture", color=color)
    embedMessage.set_image(url=user.avatar_url)
    embedMessage.set_footer(text=f"Requested by {message.author.name}")
    await message.channel.send(embed=embedMessage)
  
  if message.content.lower().startswith("s!ship"):
      members = await message.guild.fetch_members().flatten()
      choice = members[random.randint(0, len(members)-1)]

      embedMessage = discord.Embed(title=f"💞{message.author.name} & {choice.name}💞", color=color)
      embedMessage.set_image(url=choice.avatar_url)
      embedMessage.set_thumbnail(url=message.author.avatar_url)
      embedMessage.set_footer(text=f"Requested by {message.author.name}")

      if choice.name == message.author.name:
         embedMessage.add_field(name="\u200b", value="OwO you got your self congrats")
      else:
        embedMessage.add_field(name="\u200b", value="I can smell the love")

      await message.channel.send(embed=embedMessage)

  if message.content.lower().startswith("s!kick"):
    splitMessage = message_spliter(message.content, 2)
    splitMessage[1] = getuser_id(splitMessage[1])
    await client.(int(splitMessage[1])).kick(splitMessage[2])


client.run("ODY0MzMwMTkwNTAyODg3NDY0.YOz4Nw.y7xfMQ-MHVADA7-FdJXZIjjZ8bI")
