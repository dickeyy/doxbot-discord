import discord
from discord.ext import commands
import os
import requests
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Define stuff
client = commands.Bot(command_prefix = 'h$', intents=intents)
client.remove_command('help')
response = requests.get('https://doxbot-discord.herokuapp.com/')
code = int(response.status_code)
off = discord.Embed(title = ":red_circle: Outage Detected", color = discord.Color.red())
off.add_field(name = 'DoxBot is Offline!', value = 'We have detected that DoxBot is down for everyone please be patient! (Automatic detections are not 100% accurate)', inline = False)
liv = discord.Embed(title=":green_circle: DoxBot Online",color=discord.Color.green())
liv.add_field(name="Back Online", value="DoxBot is online, if you are still having issues please reach out for support!")


# online command 
@client.command()
async def live(ctx):
  liv = discord.Embed(
    title=":green_circle: DoxBot Online",
    color=discord.Color.green()
  )
  liv.add_field(name="Back Online", value="DoxBot is online, if you are still having issues please reach out for support!"
  )
  await ctx.send(embed = liv)

# startup stuff
@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="DoxBot - doxbot.xyz"))
  my_loop.start()

# ping loop
@tasks.loop(seconds=300)
async def my_loop():
    my_channel = client.get_channel(801363821390200853)
    if code != 200:
        await my_channel.send(embed = off)
    else:
        print('Dox Online')

#rules command
@client.command()
async def rules(ctx):
  rul = discord.Embed(title = "DoxBot Support Rules!", color = discord.Color.gold())
  rul.add_field(name = "1. Cursing is fine but racism/discrimination is not", value = "Don't be a jerk basically", inline = False)
  rul.add_field(name = "2. Listen to mods", value = "They are cooler than you so listen", inline = False)
  rul.add_field(name = "3. Respect the channel topics", value = "Basically dont start a convo in #support", inline = False)
  rul.add_field(name = "4. Spamming will result in a mute/ban (this includes mention spamming", value = "It's annoying. Don't be annoying", inline = False)
  rul.add_field(name = "5. No NSFW of any kind including media", value = "Gross bro don't do that", inline = False)
  await ctx.send(embed = rul)


# stuff to ping counting bot on twitter
cbtresponse = requests.get('https://count-twitter-bot.herokuapp.com/')
cbtcode = int(cbtresponse.status_code)

@client.command()
async def pingcbt(ctx):
  if cbtcode != 200:
    await ctx.send('Counting Bot appears to be offline!')
  else:
    await ctx.send('Counting Bot is online!')

@client.command()
async def stats(ctx):

  scount = str(len(client.guilds))
  users = str(len(client.users))
  ping = round(client.latency * 1000,2)

  st = discord.Embed(title = 'Bot Stats', color = discord.Color.green())
  st.add_field(name = 'Server Count ~ ', value = f"`{scount}`", inline = True)
  st.add_field(name = 'User Count ~ ', value = f"`{users}`", inline = True)
  st.add_field(name = 'Ping', value = f"`{ping}ms`", inline = True)

  await ctx.send(embed = st)
  print(f'{users}')

@client.event
async def on_member_update(before, after):
  my_channel = client.get_channel(801363821390200853)
  if str(before.status) == "online" and after.id == 800636967317536778:
    if str(after.status) == "offline":
      await my_channel.send(embed = off)

  elif str(before.status) == "offline" and after.id == 800636967317536778:
    if str(after.status) == "online":
      await my_channel.send(embed = liv)
            
# web server / run
client.run(os.getenv('TOKEN'))