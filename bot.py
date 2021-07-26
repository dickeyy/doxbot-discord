import discord
from discord.ext import commands
import json
from discord.voice_client import VoiceClient
import youtube_dl
import os
import time
import requests
from discord.ext import tasks
import random
import math
import aiohttp
from discord.utils import get
import asyncio
import functools
import itertools
import youtube_dl
from async_timeout import timeout
import giphy_client
from giphy_client.rest import ApiException
import datetime
import mysql.connector
import sys
import psutil
import numbers
from dadjokes import Dadjoke
import googletrans
from fng_api import *
from PIL import Image
from io import BytesIO
from datetime import date
from discord import DMChannel
from thispersondoesnotexist import get_online_person
from dotenv import load_dotenv
from web import web_server
import statcord
import tweepy
import akinator 
from discord_buttons_plugin import *
from discord_slash import SlashCommand

load_dotenv()

# database stuff
db = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE")
)
cursor = db.cursor(buffered=True)

# get prefix
def get_prefix(bot, message):
    guildID = message.guild.id
    cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {guildID}")
    result = cursor.fetchone()
    for tuple1 in result:
      str = ''.join(tuple1)
      prefix = str
    return prefix

# Define stuff
intents = discord.Intents.default()
intents.members = True
owner_id = 489264179472236557
bot = commands.Bot(command_prefix = get_prefix, intents=intents, owner_id=489264179472236557)
bot.remove_command('help')
buttons = ButtonsClient(bot)
slash = SlashCommand(bot, sync_commands=True)

# Run startup stuff
@bot.event
async def on_ready():
  my_channel = bot.get_channel(801363821390200853)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="$help - doxbot.xyz"))

# statcord api
StatCordkey = os.getenv('STATCORDAPI')
StatCordapi = statcord.Client(bot,StatCordkey)
StatCordapi.start_loop()

@bot.event
async def on_command(ctx):
    StatCordapi.command_run(ctx)

# twitter bot
consumer_key = os.getenv("TWITKEY")
consumer_secret = os.getenv("TWITSEC")
access_token = os.getenv("TWITTOKEN")
access_token_secret = os.getenv("TWITTOKSEC")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(access_token, access_token_secret)

TwitApi = tweepy.API(auth)

@tasks.loop(hours=24, reconnect=True)
async def pub_tweet():
    cursor.execute("SELECT number FROM twitterbot")
    number = cursor.fetchall()
    for number1 in number:
        for number_tweet in number1:
            TwitApi.update_status(number_tweet)
            number_tweet += 1
            cursor.execute(f"UPDATE `twitterbot` SET `number`= {number_tweet}")
            db.commit()
            number_tweet -= 1
            print(f'Tweeted -- {number_tweet}')

# cooldown messages 
coolDown_list = ['Chill Tf Out', 'CHILLLLL', 'Stop.', 'Take a Breather', 'ok', 'Spamming commands is cringe', 'Slow it down', 'Wee-Woo-Wee-Woo Pull Over', 'No smile', '-_-', 'Why tho...', 'Yikes U Should Like Not', 'Slow it Cowboy', 'Take a Break Bro', 'Go Touch Some Grass']

# Dox Command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def dox(ctx, member: discord.Member=None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'dox'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    identity = getIdentity()

    if member == None:
        userName = ctx.author.name
    else:
        userName = member.name

    embed = discord.Embed(title=f"Doxing {userName}...", color=discord.Color.red())
    embed.add_field(name="Full Name:", value=identity.name, inline=False)
    embed.add_field(name="Height:", value=identity.height + " / " + identity.heightcm + " cm", inline=False)
    embed.add_field(name="Weight:", value=identity.weight + "lbs / " + identity.weightkg + "kg", inline=False)
    embed.add_field(name="Birthday:", value=identity.birthday, inline=False)
    embed.add_field(name="Address:", value=identity.address, inline=False)
    embed.add_field(name="Coordinates:", value=identity.coords, inline=False)
    embed.add_field(name="Email:", value=identity.email, inline=False)
    embed.add_field(name="Phone Number:", value=identity.phone, inline=False)
    embed.add_field(name="Discord Password:", value=identity.password, inline=False)
    embed.add_field(name="SSN:", value=identity.ssn, inline=False)
    embed.add_field(name="Credit Card:", value="Num: " + identity.card + " Exp: " + identity.expiration + " CVV: " + identity.cvv2, inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"Requested by: {ctx.author} \u200b")

    await ctx.send(embed = embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'dox'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'dox'")
        db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Dox -- {cupGuild} by {cupUser}")

@dox.error
async def dox_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# help command 3.0
@bot.group(name='help', invoke_without_command=True)
@commands.cooldown(1,1,commands.BucketType.guild)
async def help_cmd(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        
        embed = discord.Embed(title="DoxBot Help", description=f"For more info on any command simply do `{pre}help [command]`. Example: `{pre}help dox`", color=0xff6666)
        embed.add_field(name="Music:", value="`play [song]`, `music`, `sfx [sound name]`", inline=False)
        embed.add_field(name="Moderation (Under Development):", value="`disable [command]`, `enable [command]`, `disabledcmds`, `setnote [user] [note]`, `notes [user]`, `deletenote [note id]`, `clearnotes [user]`")
        embed.add_field(name="Economy (Under Development):", value="`balance [optional user]`, `beg`, `daily`, `slots [amount]`, `fish`, `shop`, `buy [shop number]`, `mine`, `rob [user]`, `gift [user] [amount]`, `highlow`, `richest`, `leaderboard coins`, `rps [bet] [move]`", inline=False)
        embed.add_field(name="Starboard:", value="`setstarboard [channel]`, `starthresh [number]`, `highstar`", inline=False)
        embed.add_field(name="Server Stats:", value="`statsetup`, `statsreset`, `removecounter [counter]`, `addcounter [counter]`, `counters`", inline=False)
        embed.add_field(name="Utility:", value="`botidea [idea]`, `bugreport [bug]`, `stats`, `setprefix [prefix]`, `prefix`, `setcountchannel [channel]`, `countinfo`, `setwordchan [channel]`, `wordinfo`, `poll [option 1] or [option 2]`, `cstats [command]`, `lfg [game]`, `tictactoe [player 1] [player2]`, `coinflip`, `avatar [user]`, `support`, `ping`, `server`, `vote`, `invite`, `math`, `donate`, `afk [reason]`, `translate [to lang] [message]`, `languages`, `weather [location]`, `shorturl [url]`, `qr [url]`, `rcolor`", inline=False)
        embed.add_field(name="Fun:", value="`dox [optional user]`, `aki`, `doesntexist`, `pp [user]`, `hate [user]`, `love [user]`, `set [socialmedia] [username]`, `socialsinfo`, `meme`, `virgin [user]`, `reddit [subreddit]`, `nsfw`, `iq [user]`, `embarrass [user]`, `8ball [question]`, `dog`, `cat`, `gif [search]`, `dadjoke`, `affirmation`, `say [message]`, `roast [optional user]`, `wanted [optional user]`, `todayinhistory`, `lovetest [user]`, `sex [user]`, `cringe [optional user]`, `urban [word]`")
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"Prefix for this server: {pre}  |  {ctx.author} \u200b")
        await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'help'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'help'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Help -- {cupGuild} by {cupUser}")

@help_cmd.command(name='aki')
async def aki_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Aki Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}aki [command]", value=f"Use this to get a list of available Akinator commands. The most common one is `aki start` which will start a game", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='urban')
async def urban_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Urban Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}urban [word]", value=f"Use this to look up a word on Urban Dictionary. Please only use one word", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='cringe')
async def cringe_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Cringe Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}cringe [optional user]", value=f"Use this to cringe, you can just cringe or you can cringe at someone", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='leaderboard')
async def leaderboard_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Leaderboard Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}leaderboard [name]", value=f"Use this command to see the leaderboard for a variety of different things. Use `leaderboard` to get a list of available leaderboards", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='rob')
async def rob_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Rob Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}rob [user]", value=f"Use this command to rob another user. There's a chance you will get away with a lot of money but you could also lose quite a bit. This command can only be used once every 48 hours", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='mine')
async def mine_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Mine Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}mine", value=f"Use this to mine for some blocks then sell them for DXC! Requires you to have a pickaxe so use the `{pre}shop` command! Also be careful there's a 0.0001% chance of falling in lava!", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='sfx')
async def sfx_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="SFX Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}sfx [sound]", value=f"Use this command to get a list of all available sounds, or put in a sound to play it in whatever VC you are in", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='counters')
async def counters_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Counters Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}counters", value=f"Use this command to get a list of all available counters, and how to spell the counters for the {pre}addcounter and {pre}removecounter commands", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='addcounter')
async def addcounter_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Addcounter Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}addcounter [counter]", value=f"Use this command to add a Server Stats Counter. Please make sure the [counter] is spelled exactly as it appears in {pre}counters", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='removecounter')
async def removecounter_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Removecounter Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}removecounter", value=f"Use this command to remove a specific Server Stats Counter. Please make sure the [counter] is spelled exactly as it appears in {pre}counters", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='statsreset')
async def statsreset_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Statsreset Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}statsreset", value="Use this command to delete all Server Stats Counters", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='statsetup')
async def statsetup_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Statsetup Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}statsetup", value="Use this command to setup the Server Stats Counters", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='highstar')
async def highstar_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Highstar Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}highstar", value="Use this command to see the highest stars ever received in your server", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='starthresh')
async def starthresh_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Starthresh Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}starthresh [number]", value="Use this command to set the minimum amount of stars required for a message to be posted to the starboard", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='setstarboard')
async def setstarboard_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Setstarboard Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}setstarboard [channel]", value="Use this command to set the channel for the starboard", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='rps')
async def rps_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="RPS Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}rps [bet > 10] [move]", value="Use this command to play Rock Paper Scissors with DoxBot. [move] Must be 'rock', 'paper', or 'scissors' and [bet] must be more than 10", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='bugreport')
async def bugreport_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Bugreport Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}bugreport [bug]", value="Use this command to report any bugs you find. A Dev / Mod will DM you and likely ask you for a screenshot of the bug", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='slots')
async def slots_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Slots Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}slots [amount > 10]", value="Use this to play the slot machine! The amount bet must me more than 10 Dox Coins (DXC). If you get 2 emojis in a row, your prize is how much you bet times 1.5, if you get 3 emojis in a row (jackpot) your prize is however much you bet times 3", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='richest')
async def gift_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Richest Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}richest", value="Use this to see who has the most Dox Coins in the server", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='highlow')
async def highlow_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="highlow Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}highlow", value="Use this to play the high / low game and predict whether a number is higher or lower than a hint number. If you guess right you will receive DXC (Dox Coin)", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='gift')
async def gift_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Gift Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}gift [user] [amount]", value="Use this to gift anyone in the server some DXC (Dox Coin). Warning this is non-refundable.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='buy')
async def buy_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Buy Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}buy [shop number]", value=f"Use this to buy a specifc store item. To get the shop number, use {pre}shop", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='shop')
async def shop_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Shop Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}shop", value="Use this to get access to the DoxBot Store to spend your DXC (Dox Coin)", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='fish')
async def fish_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Fish Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}fish", value="Use this to fish in the great Dox ocean. You may or may not catch a variety of things giving DXC (Dox Coin)", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='daily')
async def daily_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Daily Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}daily", value="Use this to get your daily free 1000 DXC (Dox Coin)", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='beg')
async def beg_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Beg Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}beg", value="Use this to beg DoxBot for some DXC (Dox Coin). He will give you anywhere from 1-200 DXC.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='balance')
async def balance_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Balance Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}balance [optional user]", value=f"Use this to get the DXC (Dox Coin) balance of any user. If [optional user] is left blank it will give you your balance. Alias {pre}bal", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='dox')
async def dox_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Dox Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}dox [optional user]", value="Use this to get 100% real info about someone *wink wink*.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='setprefix')
async def setprefix_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Setprefix Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}setprefix [prefix]", value="Set a custom prefix for your server, [prefix] must be less than or equal to 8 characters", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='prefix')
async def prefix_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Prefix Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}prefix", value="Forgot prefix? Use this to get the prefix for the server", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='setcountchannel')
async def setcountchannel_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Setcountchannel Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}setcountchannel [channel]", value=f"Set a specified counting channel for the counting game. Alias: {pre}secoca", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='countinfo')
async def countinfo_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Counting Game Info",description="The counting game is a game where all you have to do is (in the specified channel) send the number that comes after the last number sent. *Example:* If I were to send **1** then Dox would send **2** and so on.", color=0xff6666)
        embed.add_field(name=f"{pre}setcountchannel [channel]", value=f"Set a specified channel for the counting game (Must have the 'Administrator' permission). Alias: {pre}secoca", inline=False)
        embed.add_field(name=f"{pre}countrules", value="See all of the rules for the counting game", inline=False)
        embed.add_field(name=f"{pre}counthigh", value="See the highscore for your server", inline=False)
        embed.add_field(name=f"{pre}countchannel", value="Forgot the counting channel? Don't worry this command will remind you what it is", inline=False)
        embed.set_footer(text=f"For info about the rules use {pre}countrules")
        await ctx.send(embed=embed)

@help_cmd.command(name='set')
async def set_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Set Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}set [social medaia] [account]", value="Add a social media to your socials profile", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='socialsinfo')
async def socialsinfo_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Socials Info", description="Socials is a system to display your social media's to everyone in the server", color=discord.Color.orange())
        embed.add_field(name=f"{pre}set [social media] [account name]", value="Add a social media to your socials profile", inline=False)
        embed.add_field(name=f"{pre}socials [user]", value=f"Get the socials profile for anyone in the server. Aliases: {pre}soc", inline=False)
        embed.add_field(name=f"{pre}socialdelete [social media]", value=f"Delete one of your social media's from your profile. Aliases: {pre}socdel", inline=False)
        embed.add_field(name=f"{pre}supportedsocials", value=f"See a list of the supported social media's. Aliases: {pre}suso", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='play')
async def play_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Play Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}play [song]", value=f"Play music using DoxBot, [song] can be the name or a YouTube URL, for more info do {pre}help music", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='music')
async def music_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Music Help", color=0xff6666)
        embed.add_field(name=f"{pre}play [song]", value="Play a song in a voice channel using DoxBot", inline=False)
        embed.add_field(name=f"{pre}queue", value="Display the queue", inline=False)
        embed.add_field(name=f"{pre}skip", value="Skip the current song and play the next in queue", inline=False)
        embed.add_field(name=f"{pre}remove [queue number]", value="Remove a specific song in queue", inline=False)
        embed.add_field(name=f"{pre}join", value="Make DoxBot join the voice channel you are in", inline=False)
        embed.add_field(name=f"{pre}leave", value="Make DoxBot leave the current VC", inline=False)
        embed.add_field(name=f"{pre}summon [channel id]", value="Tell Dox to join a specific channel (User must have Manage Channel permission)", inline=False)
        embed.add_field(name=f"{pre}pause", value="Pauses the song currently playing", inline=False)
        embed.add_field(name=f"{pre}resume", value="Resumes playing the paused song", inline=False)
        embed.add_field(name=f"{pre}stop", value="Stops the song playing", inline=False)
        embed.add_field(name=f"{pre}volume [number 1-100]", value="Sets the volume of the player", inline=False)
        embed.add_field(name=f"{pre}loop", value="Loop the song currently playing", inline=False)
        embed.add_field(name=f"{pre}shuffle", value="Shuffles the queue", inline=False)
        embed.add_field(name=f"{pre}now", value="Displays the song currently playing", inline=False)
        embed.set_footer(text="Note: Some of these commands will in the future be a premium feature so enjoy them now :)")
        await ctx.send(embed=embed)

@help_cmd.command(name='weather')
async def weather_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Weather Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}weather [location]", value="Use this to get detailed weather info about a given city or country", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='roast')
async def roast_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Roast Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}roast [optional user]", value=f"Use this to roast yourself (if you leave [user] blank), or someone else. Alias= {pre}insult", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='pp')
async def pp_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="PP Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}pp [user]", value="Find out someones pp size.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='hate')
async def hate_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Hate Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}hate [user]", value="Tell everyone who you hate!", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='love')
async def love_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Love Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}love [user]", value="Tell everyone who you love!", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='meme')
async def meme_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Meme Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}meme", value="Ask Dox to send a random meme from Reddit.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='virgin')
async def virgin_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Virgin Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}virgin [user]", value="Find out if someones a virgin or not.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='poll')
async def poll_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Poll Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}poll [option 1] or [option 2]", value="Start a poll for users to vote on.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='reddit')
async def reddit_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Reddit Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}reddit [subreddit]", value="Get a random picture from a specified subreddit.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='iq')
async def iq_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="IQ Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}iq [user]", value="Get the IQ of anyone.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='cstats')
async def cstats_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Cstats Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}cstats [command]", value="Get the number of times a command has been used in any server since Febuary 29, 2021.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='todayinhistory')
async def todayinhistory_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Todayinhistory Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}todayinhistory", value=f"Use this to get a fact about something that happpened today in history. Aliases: {pre}tih, {pre}datefact")
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='translate')
async def translate_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Translate Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}translate [to language] [message]", value=f"Translate text, the [to language] is the language you want to translate to, the original language will be auto-detected. Alias: {pre}tr", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='affirmation')
async def affirmation_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Affirmation Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}affirmation", value=f"If your feelin' down use this to get a little boost. Aliases: {pre}aff, {pre}isad", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='lfg')
async def lfg_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="LFG Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}lfg [game]", value="Let people know that your Looking For (a) Gamer to play with!", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='afk')
async def afk_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="AFK Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}afk [reason]", value="Let everyone know that you are AFK and why", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='tictactoe')
async def tictactoe_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Tictactoe Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}tictactoe [user] [user]", value=f"Play TicTacToe with someone! To get more tictactoe info do {pre}help tttinfo", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='tttinfo')
async def tttinfo_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Tictactoe Help", color=0xff6666)
        embed.add_field(name = f"{pre}tictactoe [user][user]", value = "Use this command to start a TicTacToe game, be sure one of the users is you!", inline = False)
        embed.add_field(name = f"{pre}place [integer]", value = "Use this command to place your marker, the integer is the tile number counting from left to right, for instance top left corner is intger 1 and bottom right corner is integer 9, or use...", inline = False)
        embed.add_field(name = f"{pre}tictemplate", value = "Use ths to get a template board so you can see which place is what number", inline = False)
        embed.add_field(name = f"{pre}endgame", value = "Use this to end a game if innactive, only people with the **Administrator** role can use this", inline = False)
        await ctx.send(embed = embed)

@help_cmd.command(name='embarrass')
async def embarrass_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Embarrass Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}embarrass [user]", value="Get some embarrassing info about someone.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='coinflip')
async def coinflip_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Coinflip Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}coinflip", value="Ask Dox to flip a coin.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='avatar')
async def avatar_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Avatar Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}avatar [user]", value="View someones profile picture.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='math')
async def math_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title = "Math Commands Help", color = 0xff6666)
        embed.add_field(name = f"`{pre}mathadd [number] [number]`", value="Ask Dox to add two numbers together", inline=False)
        embed.add_field(name = f"`{pre}mathsub [number] [number]`", value="Ask Dox to subtract two numbers", inline=False)
        embed.add_field(name = f"`{pre}math [number] [number]`", value="Ask Dox to pick a number between the two given numbers", inline=False)
        embed.add_field(name = f"`{pre}mathdiv [number] [number]`", value="Ask Dox to divide two numbers", inline=False)
        embed.add_field(name = f"`{pre}mathmulti [number] [number]`", value="Ask Dox to multiply two numbers", inline=False)
        embed.add_field(name = f"`{pre}mathsqrt [number]`", value="Ask Dox to find the square root of a number", inline=False)
        await ctx.send(embed = embed)

@help_cmd.command(name='numfact')
async def numfact_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Numfact Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}numfact [number]", value="Use this to get a fact about a given number", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='qr')
async def qr_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="QR Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}qr [url]", value="Use this to generate a QR code for a website", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='wanted')
async def wanted_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Wanted Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}wanted [optional user]", value="Use this to get a wanted poster with the users avatar on it. If you leave user blank it will default to you", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='shorturl')
async def shorturl_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Shorurl Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}shorturl [url]", value=f"Shorten a specified URL. Alias: {pre}surl", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='say')
async def say_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Say Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}say [message]", value="Get DoxBot to say whatever you want", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='support')
async def support_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Support Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}support", value="Get the link to our support server.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='nsfw')
async def nsfw_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="NSFW Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}nsfw", value="Ask Dox to send an NSFW picture. This comand must be used in an NSFW channel.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='ping')
async def nsfw_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Ping Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}ping", value="Get the latency for the bot.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)  

@help_cmd.command(name='server')
async def server_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Server Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}server", value="Get info about the server.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)     

@help_cmd.command(name='vote')
async def vote_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Vote Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}vote", value="Upvote DoxBot on some bot lists.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed) 

@help_cmd.command(name='rcolor')
async def rcolor_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Rcolor Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}rcolor", value="Use this to get a random hex color code", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed) 

@help_cmd.command(name='lovetest')
async def lovetest_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Lovetest Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}lovetest [user]", value="Check if you and someone else are compatible as lovers", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='dadjoke')
async def dadjoke_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Dadjoke Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}dadjoke", value="Take a wild guess at what this does", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='invite')
async def invite_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Invite Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}invite", value="Invite DoxBot to your server.", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='donate')
async def donate_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Donate Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}donate", value="Donate to DoxBot to help support the bot!", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='8ball')
async def eightball_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="8ball Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}8ball [question]", value="Ask Dox to shake the Magic 8Ball", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='dog')
async def dog_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Dog Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}dog", value="Get a random picture of a dog", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='cat')
async def cat_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Cat Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}cat", value="Get a random picture of a cat", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='gif')
async def gif_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="GIF Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}gif [search]", value="Search GIPHY for a GIF, if no [search] is specified then it will send a random GIF", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='setnote')
async def setnote_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Setnote Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}setnote [user] [note]", value="Use this to set notes on users for all mods to see. Currently each user has a max of 10 notes that can be put on their profile, but this limit will increase as time goes on.  Requires the 'Administrator Permission'", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='notes')
async def notes_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Notes Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}notes [user]", value="Use this to see the notes on a user. Requires the 'Administrator Permission'", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='deletenote')
async def deletenote_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Deletenote Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}deletenote [note id]", value="Use this to delete a specific note off a users profile. To get the note ID use the notes command. Requires the 'Administrator Permission'", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='clearnotes')
async def clearnotes_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Clearnotes Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}clearnotes [user]", value="Use this to clear all the notes from a user. Requires the 'Administrator Permission'", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='botidea')
async def botidea_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Botidea Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}botidea [idea]", value=f"Use this to suggest a feature for the bot. Alias: {pre}bi. *Note: Your Discord name and profile picture will be shared publicly in the support server. You will also receive a DM from the bot if your idea gets approved or denied.*", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='doesntexist')
async def doesntexist_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Doesntexist Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}doesntexist", value=f"Use this to get an AI generated image of a person who does not exist. [SOURCE](https://thispersondoesnotexist.com/)", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)
        
@help_cmd.command(name='sex')
async def sex_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Sex Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}sex [user]", value=f"Use this to ask someone in the server to have sex...", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='setwordchan')
async def setwordchan_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Setwordchan Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}setwordchan [channel]", value=f"Use this to set the channel for the word game. Requires the 'Administrator' Permission For more info on the game use `{pre}wordinfo`. Alias: {pre}sewoch", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='wordinfo')
async def wordinfo_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Word Game Info", description="The word game is simple, in the designated channel (found with `wordchan`) one user will send a word then the next user will have to start their word with the last letter of the word before. Example: PapaRaG3: Dog DoxBot: God PapaRaG3: Dude. And so on", color=discord.Color.random())
        embed.add_field(name=f"Commands (for more info use `{pre}help [command]`)", value="`setwordchan [channel]`, `wordchan`, `wordhigh`")
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='wordchan')
async def wordchan_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Wordchan Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}wordchan", value=f"Use this if you forgot the channel for the word game", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='wordhigh')
async def wordhigh_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Wordhigh Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}wordhigh", value=f"Use this to get the high score for the word game for the server", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='disable')
async def disable_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Disable Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}disable [command]", value=f"Use this to disable a specific command. Please write out the desired [command] as it appears in the help command. For commands like `aki` where there are different subcommands, just use the base command i.e. `aki`. Requires 'Administrator' permission", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='enable')
async def enable_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Enable Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}enable [command]", value=f"Use this command to enable a previously disabled command. To see a list of disabled commands use {pre}disabledcmds. Requires 'Administrator' permission", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

@help_cmd.command(name='disabledcmds')
async def disabledcmds_subcom(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Disabledcmds Command Help", color=0xff6666)
        embed.add_field(name=f"{pre}disabledcmds", value=f"Use this to get a list of disabled commands for the server", inline=False)
        embed.add_field(name="Links", value="[🌐 Website](https://doxbot.xyz) | [<:invite:823987169978613851> Invite](https://doxbot.xyz/invite) | [<:upvote:823988328306049104> Upvote](https://top.gg/bot/800636967317536778/vote) | [<:discord:823989269626355793> Support](https://discord.com/invite/zs7UwgBZb9) | [<:paypal:824766297685491722> Donate](https://doxbot.xyz/donate)", inline=False)
        await ctx.send(embed=embed)

# Ping Command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def ping(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'ping'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await ctx.send(f'Pong! **{round(bot.latency * 1000,2)}ms**')
    cursor.execute("SELECT used FROM commands WHERE name = 'ping'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'ping'")
        db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Ping -- {cupGuild} by {cupUser}")

@ping.error
async def ping_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# support Command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def support(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'support'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await ctx.channel.send("Support Server  https://discord.gg/zs7UwgBZb9")
    cursor.execute("SELECT used FROM commands WHERE name = 'support'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'support'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Support -- {cupGuild} by {cupUser}")

@support.error
async def support_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# Embarrass Command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def embarrass(ctx, member : discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'embarrass'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    embarrass_list = ['They peed the bed last night' , 'They havent showered in 3 weeks' , 'Their favorite movie is "Cuties" uhhh' , 'They collect their belly button lint' , 'They tried to slide in my DMs last night' , 'Got friendzoned by 4 different people in one day' , 'Says "bababoey" unironically' , 'Doesnt wipe after they poop' , 'Still sleeps in their moms bed' , 'Some how managed to fail study hall' , 'Their destiny is to be a 40 year old virgin']
    emb = random.choice(embarrass_list)
    await ctx.channel.send(f"{emb}")
    cursor.execute("SELECT used FROM commands WHERE name = 'embarrass'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'embarrass'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Embarrass -- {cupGuild} by {cupUser}")

# Embarrass Error Handler
@embarrass.error
async def embarrass_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention someone to embarrass")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# Chad Command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def chad(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'chad'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await ctx.send('<:chad:799588502454796319>')
    cursor.execute("SELECT used FROM commands WHERE name = 'chad'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'chad'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Chad -- {cupGuild} by {cupUser}")

@chad.error
async def chad_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# Virgin Command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def virgin(ctx, member : discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'virgin'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    virgin_list = ['<:yestick:799590853588811818> Ya no shit' , '<:notick:799590818054668307> Nope, gross' , '<:yestick:799590853588811818> Obviously' , '<:notick:799590818054668307> Fuck Master']
    virgin = random.choice(virgin_list)
    await ctx.channel.send(f"{virgin}")
    cursor.execute("SELECT used FROM commands WHERE name = 'virgin'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'virgin'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Virgin -- {cupGuild} by {cupUser}")

# Virgin Error Handler
@virgin.error
async def virgin_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention someone to check their virginity")
    if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# We hate...
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def hate(ctx, member : discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'hate'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await ctx.send(f"We Hate {member.mention}!")
    cursor.execute("SELECT used FROM commands WHERE name = 'hate'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'hate'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Hate -- {cupGuild} by {cupUser}")

# Hate Error Handler
@hate.error
async def hate_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention someone to Hate them!")
    if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# We love...
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def love(ctx, member : discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'love'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await ctx.send(f"We Love {member.mention}!")
    cursor.execute("SELECT used FROM commands WHERE name = 'love'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'love'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Love -- {cupGuild} by {cupUser}")

# Love error handler
@love.error
async def love_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention someone to Love them!")
    if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# PP size command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def pp(ctx, member : discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'pp'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    pp_list = ['Homies hung as a horse', 'Shrimp gang for life' , 'Aye nothing wrong with average' , '"Have you put it in yet?" Sound familiar?' , '3 inch punisher' , 'Its belived that the ancient Egyptions spoke of a mythical schlong like theirs' , 'Sheesh my guys packin' , 'Hey man, its ok its not the size of the boat its the motion of the ocean right?' , 'ERROR: NO PP DETECTED' , 'A good 6er' , 'IDK when I went to inspect it, it wrapped around my neck and I passed out' , 'Its ok man some like it to be small and soft' ,'Damn theyve got a solid 9 inches soft' , 'Seeing theirs made me want to appologize to Mrs. DoxBot for not being able to give her that']
    pp = random.choice(pp_list)
    await ctx.channel.send(f"{pp}")
    cursor.execute("SELECT used FROM commands WHERE name = 'pp'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'pp'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"PP -- {cupGuild} by {cupUser}")

# pp Error Handler
@pp.error
async def pp_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention someone to check their pp!")
    if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# Tic Tac Toe 
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

# Start Game command
@bot.command(aliases=['ttt'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'tictactoe'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    global count
    global player1
    global player2
    global turn
    global gameOver
    
    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:",
                ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2
    
        # print board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else: 
                line += " " + board[x]
        
        # determine first player 
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + f">'s turn. Type `$place [integer]` to start")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + f">'s turn. Type `$place [integer]` to start")
    else:
        await ctx.send("A game is already in progress! Wait for it to end before starting a new game.")
    cursor.execute("SELECT used FROM commands WHERE name = 'tictactoe'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'tictactoe'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"TTT -- {cupGuild} by {cupUser}")

# place command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def place(ctx, pos : int):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'place'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
  
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
        elif turn == player2:
            mark = ":o2:"
        if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" : 
            board[pos - 1] = mark
            count += 1

            # print board again
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        checkWinner(winningConditions, mark)
        print(count)
        if gameOver == True:
            await ctx.send(mark + " wins!")
        elif count >= 9:
            gameOver = True
            await ctx.send("It's a tie!")

        # switch turns 
        if turn == player1:
            turn = player2
        elif turn == player2:
            turn = player1

        
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send(f"Please start a new game using the `$tictactoe` command.")
    cursor.execute("SELECT used FROM commands WHERE name = 'place'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'place'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Place -- {cupGuild} by {cupUser}")

# Determine winner
def checkWinner(winningConditions, mark):
  global gameOver
  for condition in winningConditions:
    if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
      gameOver = True

# End game command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def endgame(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'endgame'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    global gameOver
    if gameOver == False:
        gameOver = True
        await ctx.send("Game Ended")
    elif gameOver == True:
        await ctx.send("No Game Active")
    cursor.execute("SELECT used FROM commands WHERE name = 'endgame'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'endgame'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Endgame -- {cupGuild} by {cupUser}")

# Error Handlers for ttt
@endgame.error
async def engame_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use this command, ask an admin to end the game!")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

@tictactoe.error
async def tictactoe_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Pease make sure to mention/ping players.")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)


@place.error
async def place_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Pease make sure to enter integer.")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)


# tictactoe help
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def ttthelp(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'ttthelp'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        th = discord.Embed(title = "TicTacToe Help", color = discord.Color.green())
        th.add_field(name = f"`{pre}tictactoe [user][user]`", value = "Use this command to start a TicTacToe game, be sure one of the users is you!", inline = False)
        th.add_field(name = f"`{pre}place [integer]`", value = "Use this command to place your marker, the integer is the tile number counting from left to right, for instance top left corner is intger 1 and bottom right corner is integer 9, or use...", inline = False)
        th.add_field(name = f"`{pre}tictemplate`", value = "Use ths to get a template board so you can see which place is what number", inline = False)
        th.add_field(name = f"`{pre}endgame`", value = "Use this to end a game if innactive, only people with the **Administrator** role can use this", inline = False)
        await ctx.send(embed = th)
    cursor.execute("SELECT used FROM commands WHERE name = 'ttthelp'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'ttthelp'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"TTTHelp -- {cupGuild} by {cupUser}")

@ttthelp.error
async def ttthelp_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# ttt template
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def tictemplate(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'tictemplate'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    global count
    global player1
    global player2
    global turn
    global gameOver
    
    if gameOver:
        global board
        board = [":one:", ":two:", ":three:",
                ":four:", ":five:", ":six:",
                ":seven:", ":eight:", ":nine:"]
        turn = ""
        gameOver = False
        count = 0
    
        # print board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else: 
                line += " " + board[x]
    cursor.execute("SELECT used FROM commands WHERE name = 'tictemplate'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'tictemplate'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"TTTTemplate -- {cupGuild} by {cupUser}")

@tictemplate.error
async def tictemplate_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# server info 
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def server(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'server'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    inf = discord.Embed(
        title=name + " Server Information",
        description="Description: " + description,
        color=discord.Color.gold()
    )
    inf.set_thumbnail(url=icon)
    inf.add_field(name="Server ID", value=id, inline = True)
    inf.add_field(name="Region", value=region, inline = True)
    inf.add_field(name="Member Count", value=memberCount, inline = True)
    
    await ctx.send(embed = inf)
    cursor.execute("SELECT used FROM commands WHERE name = 'server'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'server'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Server -- {cupGuild} by {cupUser}")

@server.error
async def server_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# Stats command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def stats(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'stats'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()[2]
    scount = str(len(bot.guilds))
    users = str(len(bot.users))
    ping = round(bot.latency * 1000,2)
    cursor.execute("SELECT SUM(used) FROM commands")
    sumAllUF = cursor.fetchall()
    sumAll = sumAllUF[0][0]
    embed = discord.Embed(title="DoxBot Stats", color=0xff6666)
    embed.set_thumbnail(url="https://doxbot.xyz/images/doxlogo2")
    embed.add_field(name="Servers:", value=scount, inline=True)
    embed.add_field(name="Users:", value=users, inline=True)
    embed.add_field(name="Commands:", value="162", inline=True)
    embed.add_field(name="Cmds. Run:", value=sumAll, inline=True)
    embed.add_field(name="CPU Usage:", value=f"{cpu}%", inline=True)
    embed.add_field(name="Mem. Usage:", value=f"{mem}%", inline=True)
    embed.add_field(name="Ping:", value=f"{ping}ms", inline=True)
    embed.add_field(name="Library:", value="Discord.py", inline=True)
    embed.add_field(name="Owner:", value="PapaRaG3#6969", inline=True)
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'stats'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'stats'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Stats -- {cupGuild} by {cupUser}")

@stats.error
async def stats_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# vote
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def vote(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'vote'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    vo = discord.Embed(title = "Vote for DoxBot!", description="[Top.gg](https://top.gg/bot/800636967317536778/vote)\n[botsfordiscord.com](https://botsfordiscord.com/bot/800636967317536778/vote)\n[discordbotlist.com](https://discordbotlist.com/bots/doxbot/upvote)\n[discord.boats](https://discord.boats/bot/800636967317536778/vote)\n[inbbotlist.com](https://inbbotlist.com/bots/800636967317536778/vote)", color = discord.Color.gold())
    await ctx.send (embed = vo)
    cursor.execute("SELECT used FROM commands WHERE name = 'vote'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'vote'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Vote -- {cupGuild} by {cupUser}")

@vote.error
async def vote_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# Looking for game command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def lfg(ctx, message):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'lfg'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    author = ctx.message.author.mention

    await ctx.send(author + " wants to play **" + message + "** with someone! DM them!")
    cursor.execute("SELECT used FROM commands WHERE name = 'lfg'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'lfg'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"LFG -- {cupGuild} by {cupUser}")

@lfg.error
async def lfg_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# iq command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def iq(ctx, member: discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'iq'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    iq_list = ['Homies dumb as bricks. IQ = 4', 'Literally 0', 'Our holy overlord. IQ = 10,000', 'Enstein is that you? IQ = 258', 'IQ = 21', 'I am a python script that doesnt even really exist and I am still smarter than this guy. IQ = 1', 'IQ = 14', 'IQ = 413, my god...', 'This forgets his glasses are on his head, IQ = 32', 'About the eqivalant as my creator, IQ = 1947', 'IQ = 46', 'Look up a picture of dumb in the dictionary and you will get a picture of this guy, IQ = 5', 'IQ = 134', 'IQ = 102', 'IQ = 2', 'sO dum i furget hoW 2 spill, ia = -291', 'No :)', 'ERROR: NO IQ DETECTED', 'At least they have a big di.. oh wait no my sources are telling me thats almost as small as their IQ, IQ = -131344', 'You know what they say... actually no I dont know what they say my creator forgot. IQ = 420', 'HAHA FUNNY SEX NUMBER IQ = 69']

    iq = random.choice(iq_list)

    await ctx.send(iq)
    cursor.execute("SELECT used FROM commands WHERE name = 'iq'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'iq'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"IQ -- {cupGuild} by {cupUser}")

@iq.error
async def iq_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please mention someone to test their IQ')
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# avatar command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def avatar(ctx, member: discord.Member = None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'avatar'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    if member is None:
        ctx.send("Please metion a user")
        return
    
    else:
        embed2 = discord.Embed(title=f"{member}'s Avatar!", colour=0x0000ff, timestamp=ctx.message.created_at)
        embed2.add_field(name="Animated?", value=member.is_avatar_animated())
        embed2.set_image(url=member.avatar_url)
        await ctx.send(embed = embed2)
    cursor.execute("SELECT used FROM commands WHERE name = 'avatar'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'avatar'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Avatar -- {cupGuild} by {cupUser}")

@avatar.error
async def avatar_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

def add(n: float, n2: float):
	return n + n2

def sub(n: float, n2: float):
	return n - n2

def rando(n: int, n2: int):
	return random.randint(n, n2)

def div(n: float, n2: float):
	return n / n2

def sqrt(n: float):
	return math.sqrt(n)

def mult(n: float, n2: float):
	return n * n2

# math commands
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def mathadd(ctx, x: float, y: float):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'mathadd'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT used FROM commands WHERE name = 'mathadd'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mathadd'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Add -- {cupGuild} by {cupUser}")
    try:
        result = add(x, y)
        await ctx.send(result)
    except:
        pass

@mathadd.error
async def mathadd_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def mathsub(ctx, x: float, y: float):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'mathsub'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT used FROM commands WHERE name = 'mathsub'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mathsub'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Subtract -- {cupGuild} by {cupUser}")
    try:
        result = sub(x, y)
        await ctx.send(result)
    except:
        pass

@mathsub.error
async def mathsub_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def mathrando(ctx, x: int, y: int):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'mathrando'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT used FROM commands WHERE name = 'mathrando'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mathrando'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"MRando -- {cupGuild} by {cupUser}")
    try:
        result = rando(x, y)
        await ctx.send(result)
    except:
        pass

@mathrando.error
async def mathrando_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def mathdiv(ctx, x: float, y: float):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'mathdiv'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT used FROM commands WHERE name = 'mathdiv'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mathdiv'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Div -- {cupGuild} by {cupUser}")
    try:
        result = div(x, y)
        await ctx.send(result)
    except:
        pass

@mathdiv.error
async def mathdiv_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def mathmulti(ctx, x: float, y: float):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'mathmulti'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT used FROM commands WHERE name = 'mathmulti'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mathmulti'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Multi -- {cupGuild} by {cupUser}")
    try:
        result = mult(x, y)
        await ctx.send(result)
    except:
        pass

@mathmulti.error
async def mathmulti_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def mathsqrt(ctx, x: float):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'mathsqrt'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT used FROM commands WHERE name = 'mathsqrt'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mathsqrt'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Sqrt -- {cupGuild} by {cupUser}")
    try:
        result = sqrt(x)
        await ctx.send(result)
    except:
        pass

@mathsqrt.error
async def mathsqrt_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def mathhelp(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'mathhelp'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        mahe = discord.Embed(title = "Math Commands Help", color = discord.Color.blue())
        mahe.add_field(name = f"`{pre}mathadd [number] [number]`", value="Ask Dox to add two numbers together", inline=False)
        mahe.add_field(name = f"`{pre}mathsub [number] [number]`", value="Ask Dox to subtract two numbers", inline=False)
        mahe.add_field(name = f"`{pre}math [number] [number]`", value="Ask Dox to pick a number between the two given numbers", inline=False)
        mahe.add_field(name = f"`{pre}mathdiv [number] [number]`", value="Ask Dox to divide two numbers", inline=False)
        mahe.add_field(name = f"`{pre}mathmulti [number] [number]`", value="Ask Dox to multiply two numbers", inline=False)
        mahe.add_field(name = f"`{pre}mathsqrt [number]`", value="Ask Dox to find the square root of a number", inline=False)
        await ctx.send(embed = mahe)
    cursor.execute("SELECT used FROM commands WHERE name = 'mathhelp'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mathhelp'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"MathHelp -- {cupGuild} by {cupUser}")

@mathhelp.error
async def mathhelp_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# invite command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def invite(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'invite'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await buttons.send(
        content = "Invite DoxBot to your server!",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "Click Here",
                    style = ButtonType().Link,
                    url = "https://doxbot.xyz/invite"
                )
            ])
        ]
    )
    cursor.execute("SELECT used FROM commands WHERE name = 'invite'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'invite'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Invite -- {cupGuild} by {cupUser}")

@invite.error
async def invite_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# meme command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def meme(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'meme'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    r = requests.get("https://memes.blademaker.tv/api?lang=en")
    res = r.json()
    title = res["title"]
    ups = res["ups"]
    downs = res["downs"]
    sub = res["subreddit"]
    link = "https://reddit.com/" + res["id"]
    author = res["author"]
    m = discord.Embed(title = f"{title}", url = f"{link}",color = discord.Color.orange())
    m.set_image(url = res["image"])
    m.set_footer(text=f"👍: {ups}    Author: {author}")
    await ctx.send(embed = m)
    cursor.execute("SELECT used FROM commands WHERE name = 'meme'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'meme'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Meme -- {cupGuild} by {cupUser}")

@meme.error
async def meme_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# NSFW command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def nsfw(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'wordinfo'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    if ctx.channel.is_nsfw():
        nsfw_list = ['https://www.reddit.com/r/nudes/new.json?sort=hot', 'https://www.reddit.com/r/ass/new.json?sort=hot', 'https://www.reddit.com/r/nsfw/new.json?sort=hot', 'https://www.reddit.com/r/nsfw2/new.json?sort=hot', 'https://www.reddit.com/r/iWantToFuckHer/new.json?sort=hot', 'https://www.reddit.com/r/slut/new.json?sort=hot', 'https://www.reddit.com/r/boobs/new.json?sort=hot', 'https://www.reddit.com/r/happygirls/new.json?sort=hot', 'https://www.reddit.com/r/Nude_Selfie/new.json?sort=hot', 'https://www.reddit.com/r/gonewild/new.json?sort=hot', 'https://www.reddit.com/r/RealGirls/new.json?sort=hot', 'https://www.reddit.com/r/collegesluts/new.json?sort=hot',
        'https://www.reddit.com/r/nudes/new.json?sort=top/?t=all', 'https://www.reddit.com/r/ass/new.json?sort=top/?t=all', 'https://www.reddit.com/r/nsfw/new.json?sort=top/?t=all', 'https://www.reddit.com/r/nsfw2/new.json?sort=top/?t=all', 'https://www.reddit.com/r/iWantToFuckHer/new.json?sort=top/?t=all','https://www.reddit.com/r/slut/new.json?sort=top/?t=all'
        'https://www.reddit.com/r/boobs/new.json?sort=top/?t=all', 'https://www.reddit.com/r/happygirls/new.json?sort=top/?t=all', 'https://www.reddit.com/r/Nude_Selfie/new.json?sort=top/?t=all', 'https://www.reddit.com/r/gonewild/new.json?sort=top/?t=all', 'https://www.reddit.com/r/RealGirls/new.json?sort=top/?t=all', 'https://www.reddit.com/r/collegesluts/new.json?sort=top/?t=all',
        'https://www.reddit.com/r/nudes/new.json?sort=top/?t=year', 'https://www.reddit.com/r/ass/new.json?sort=top/?t=year', 'https://www.reddit.com/r/nsfw/new.json?sort=top/?t=year', 'https://www.reddit.com/r/nsfw2/new.json?sort=top/?t=year', 'https://www.reddit.com/r/iWantToFuckHer/new.json?sort=top/?t=year', 'https://www.reddit.com/r/slut/new.json?sort=top/?t=year',
        'https://www.reddit.com/r/boobs/new.json?sort=top/?t=year', 'https://www.reddit.com/r/happygirls/new.json?sort=top/?t=year', 'https://www.reddit.com/r/Nude_Selfie/new.json?sort=top/?t=year', 'https://www.reddit.com/r/gonewild/new.json?sort=top/?t=year', 'https://www.reddit.com/r/RealGirls/new.json?sort=top/?t=year', 'https://www.reddit.com/r/collegesluts/new.json?sort=top/?t=year',
        'https://www.reddit.com/r/nudes/new.json?sort=top/?t=week', 'https://www.reddit.com/r/ass/new.json?sort=top/?t=week', 'https://www.reddit.com/r/nsfw/new.json?sort=top/?t=week', 'https://www.reddit.com/r/nsfw2/new.json?sort=top/?t=week', 'https://www.reddit.com/r/iWantToFuckHer/new.json?sort=top/?t=week', 'https://www.reddit.com/r/slut/new.json?sort=top/?t=week',
        'https://www.reddit.com/r/boobs/new.json?sort=top/?t=week', 'https://www.reddit.com/r/happygirls/new.json?sort=top/?t=week', 'https://www.reddit.com/r/Nude_Selfie/new.json?sort=top/?t=week', 'https://www.reddit.com/r/gonewild/new.json?sort=top/?t=week', 'https://www.reddit.com/r/RealGirls/new.json?sort=top/?t=week', 'https://www.reddit.com/r/collegesluts/new.json?sort=top/?t=week','https://www.reddit.com/r/nudes/new.json?sort=top/?t=month', 'https://www.reddit.com/r/ass/new.json?sort=top/?t=month', 'https://www.reddit.com/r/nsfw/new.json?sort=top/?t=month', 'https://www.reddit.com/r/nsfw2/new.json?sort=top/?t=month', 'https://www.reddit.com/r/iWantToFuckHer/new.json?sort=top/?t=month', 'https://www.reddit.com/r/slut/new.json?sort=top/?t=month',
        'https://www.reddit.com/r/boobs/new.json?sort=top/?t=month', 'https://www.reddit.com/r/happygirls/new.json?sort=top/?t=month', 'https://www.reddit.com/r/Nude_Selfie/new.json?sort=top/?t=month', 'https://www.reddit.com/r/gonewild/new.json?sort=top/?t=month', 'https://www.reddit.com/r/RealGirls/new.json?sort=top/?t=month', 'https://www.reddit.com/r/collegesluts/new.json?sort=top/?t=month',]
        nsfwsite = random.choice(nsfw_list)
        r = requests.get(nsfwsite)
        res = r.json()
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(nsfwsite) as r:
                    res = await r.json()
                    sub = res['data']['children'] [random.randint(0, 25)]['data']['subreddit']
                    user = ctx.message.author
                    embed = discord.Embed(title=f"Random Nude from r/{sub}", color = discord.Color.gold())  
                    embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                    embed.set_footer(text=f"Requested by: {user}    r/{sub}")
                    await ctx.send(embed=embed)
        except (ValueError,IndexError):
            errorem = discord.Embed(title='NSFW ERROR', color=discord.Color.red())
            errorem.add_field(name="An Error Occured", value="Please try the command again, if the error persists reach out for [support](https://discord.com/invite/zs7UwgBZb9)", inline=False)
            await ctx.send(embed=errorem)
    else:
        await ctx.send('You must be in an NSFW channel to use that command')
    cursor.execute("SELECT used FROM commands WHERE name = 'nsfw'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'nsfw'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"NSFW -- {cupGuild} by {cupUser}")

# nsfw error handler
@nsfw.error
async def nsfw_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# specific reddit search command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def reddit(ctx, reddit):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'reddit'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    subreddit = reddit
    nsfw_list = ['nsfw', 'nudes', 'ass', 'rule34', 'boobs', 'gonewild', 'RealGirls', 'hentai', 'NSFW411', 'WorldPacks', 'celebnsfw', 'AsiansGoneWild', 'collegesluts', 'PetiteGoneWild', 'cumsluts', 'BustyPetite', 'LegalTeens', 'adorableporn', 'gonewildstories', 'WatchItForThePlot', 'gonewildaudio', 'tipofmypenis', 'BreedingMaterial', 'traps', 'nsfwasmr', 'JizzedToThis', 'Cuckold', 'onlyfansgirls101', 'milf', 'porn', 'tiktoknsfw', 'pussy', 'GirlsFinishingTheJob', 'worldpolitics', 'TikThots', 'SluttyConfessions', 'AskRedditAfterDark', 'JerkOffToCelebs', 'TittyDrop', 'gonewild30plus', 'holdthemoan', 'intermittentfasting', 'OnOff', 'OnlyFans101', 'BiggerThanYouThought', 'HotWife', 'Blowjobs', 'GWCouples', 'LEAKEDonlyfans', 'kpopfap', 'NSFWFunny', 'HENTAI_GIF', 'Nude_Selfie', 'nsfw_gifs', 'NaughtyWives', 'porninfifteenseconds', 'StreamersGoneWild', 'Yagamiyato', 'futanari', 'joi', 'homemadexxx', 'tiktokporn', 'pawg', 'Nudes', 'MorbidReality', 'MassiveCocks', 'AsianHotties', 'TwitchGoneWild', 'anal', 'Gonewild18', 'juicyasians', 'TinyTits', 'youtubetitties', '18_19', 'TikTokNude', 'BigBoobsGW', 'bigasses', 'GodPussy', 'NSFWverifiedamateur', 'lewdgames', '18nsfw', 'TooCuteForPorn', 'trashyboners', 'sex_comics', 'OnlyfansPacks', 'palegirls', 'xsmallgirls', 'sissyhypno', 'Amateur', 'FemBoys', 'chubby', 'nhentai', 'fitgirls', 'pornvids', 'freeuse', 'asshole', 'GoneMild', 'YouTubersGoneWild', 'curvy', 'traphentai', 'Stacke', 'Sissies', 'workgonewild', 'nsfwcyoa', 'bodyperfection', 'doujinshi', 'yiff', 'Slut', 'The_Best_NSFW_GIFS', 'Rule34LoL', 'BDSMcommunity', 'stupidslutsclub', 'OnlyFansPromotions', 'nsfwhardcore', 'bdsm', 'NSFWgaming', 'gonewildcouples', 'bigtiddygothgf', 'Upskirt', 'asstastic', 'RealAhegao', 'GaybrosGoneWild', 'ElleKnox', 'nsfwcosplay', 'hugeboobs', 'HoneySelect', 'gwcumsluts', 'NSFW_Korea', 'assholegonewild', 'YoungPrettyHoes', 'WouldYouFuckMyWife', 'paag', 'CuteLittleButts', 'transformation', 'GermanCelebritiesFAP', 'UnderwearGW', 'Tgirls', 'lesbians', 'amateurcumsluts', 'thick', 'normalnudes', 'IncestComics', 'DiscordNudes', 'cursedimages', 'HentaiBeast', 'LabiaGW', 'grool', 'Onlyfanspromoss', 'SexToys', 'dirtypenpals', 'wholesomehentai', 'girlsinyogapants', 'latinas', 'dirtyr4', 'czskhoes', 'GenshinImpactNSFW', 'redgifs', 'SexWorkers', 'eyebleach', 'Bondage', 'Ebony', 'LipsThatGrip', 'deepthroat', 'RateMyNudeBody', 'gaystoriesgonewild', 'twinks', 'Exxxtras', 'MonsterGirl', 'thighdeology', 'gwpublic', 'BDSMGW', 'HairyPussy', 'GoneWildTrans', 'PLASTT', 'BBW', 'ladybonersgw', 'Freealbum4u', 'dirtysmall', 'Overwatch_Porn', 'StreetsIsWatchin', 'AnalGW', 'needysluts', 'IndiansGoneWild', 'ratemycock', 'Onlyfans_Promo', 'DMT', 'cleavage', 'ProgressiveGrowth', 'wifesharing', 'CollegeAmateurs', 'burstingout', 'bimbofetish', 'ButtsAndBareFeet', 'MedicalGore', 'VAMscenes', 'extramile', 'amateurgirlsbigcocks', 'FitNakedGirls', 'darkjokes', 'FunWithFriends', 'StraightGirlsPlaying', 'penis', 'hentaicaptions', 'cumfetish', 'altgonewild', 'SheLikesItRough', 'ecchi', 'homegrowntits', 'HugeDickTinyChick', 'SexInFrontOfOthers', 'GirlswithGlasses', 'couplegonewild', 'buttplug', 'RPDRDRAMA', 'gettingherselfoff', 'Hololewd', 'damngoodinterracial', 'Femdom', 'NSFWRare', 'MsPuiYi', 'SexyTummies', 'gonewildcolor', 'gentlefemdom', 'hentaimemes', 'Slutblonde', 'IWantToSuckCock', 'ginger', 'BBCSluts', 'Omeglesex', 'DKCelebs', 'quiver', 'rule34_comics', 'feet', 'IndianBabes', 'chickflixxx', 'FestivalSluts', 'creampies', 'hardbodies', 'PreggoPorn', '40plusGoneWild', 'BadDragon', 'CamSluts', 'Swingersgw', 'Stuffers', 'sexstories', 'Slutsofonlyfans', 'Tomxcontents', 'theratio', 'chastity', 'DegradingHoles','Sexy','NSfw', 'nuDeS', 'aSs', 'rULE34', 'BOoBS', 'goneWiLD', 'reaLgIrLS', 'HeNtAI', 'nsfw411', 'WoRldPaCkS', 'ceLEbnsFW', 'AsIAnSgOnewild', 'CoLlegesluTS', 'pETitEgOnewiLd', 'CUmslUTS', 'BUStYpeTiTE', 'LegalTeeNs', 'ADORaBLEPoRn', 'gonEwILdstORiEs', 'wATchITforTheplOt', 'GOnEwIlDaUDIO', 'tipOfMYpeNIs', 'BReEdIngMATERIAL', 'TRAPs', 'NsFwaSMR', 'jizZeDtothIS', 'CUCKOLd', 'onLyFANSGiRLs101', 'MiLF', 'PORN', 'tIKTOKnSfW', 'puSSY', 'GIrLSFInISHiNGTheJOb', 'WorLDpoLItics', 'TiKtHotS', 'slutTyCONFESSiOnS', 'aSkReDDiTAFTerdARK', 'jeRkOFFtoCeLebs', 'TitTydrOp', 'GOnEwIld30pLuS', 'HoldtHemOAN', 'intermITTENtfaStING', 'onoff', 'onLYFaNs101', 'BIGgERthanyOuTHouGHT', 'hOTwife', 'BLowjoBs', 'gWCouPlES', 'leakedoNlyfans', 'KpoPfAp', 'NsfWFUnNy', 'HEnTai_gIf', 'NUDE_sElfiE', 'NSFW_gIfS', 'nAugHtywivES', 'pornInfiFtEENSeconDS', 'StREAMeRSGoNEWILd', 'YaGAMIyAtO', 'futANArI', 'joI', 'hOMeMadeXxX', 'tiKTokpOrN', 'PaWG', 'nudes', 'MoRbiDREALIty', 'MaSsIVECocKS', 'aSIANHottiES', 'tWitChGONewiLd', 'AnAl', 'gOnEwiLD18', 'JUICYaSiaNS', 'TiNytItS', 'YoutubetIttiEs', '18_19', 'tIKTOknuDE', 'bIGBooBsgw', 'BiGaSSes', 'godPuSsY', 'NSFwVeriFiedAMaTEUR', 'lEwDGaMes', '18NSFw', 'toOcUtEFORPOrN', 'tRAshyBoNerS', 'seX_COMicS', 'onLYfAnSpACkS', 'PalegIRLs', 'XSMAllgIRLS', 'SISSYhYPno', 'amATEUr', 'fEmBoYs', 'chUbBy', 'NheNtai', 'FitgIRlS', 'PoRnViDs', 'FReeuse', 'ASshoLE', 'GOnemIld', 'yoUtubErSgonEWIld', 'CURVY', 'TrAPhEntAi', 'STacKE', 'sIssIES', 'wOrkGonEwilD', 'nsFwcYoA', 'bODYPerFectIon', 'doUJiNShi', 'yIfF', 'SLUt', 'THE_best_nsFW_GiFS', 'rULE34lol', 'BdSmcomMuNity', 'StupIdSlutSClUb', 'onlyFAnSpRoMOTiONs', 'nSfWhArdCORE', 'bdSM', 'nsfWgaMINg', 'GoneWilDCOuPlEs', 'BIGTiddyGothgF', 'uPSkirT', 'ASsTasTIC', 'reaLahEGAo', 'gAYBroSgONeWild', 'ELLEknoX', 'NsfwcOsPLAY', 'HugEbOOBS', 'HONEySeLeCt', 'gwcUMslUts', 'NSFW_KOrea', 'AsShOLEGONeWIld', 'yOUngpRETTYhOEs', 'WoulDyoufUCKmYwife', 'Paag', 'cUtELitTLebutts', 'TRANSfoRmatIon', 'GERMancELebrItiEsFap', 'UNdErWeARgw', 'TGiRlS', 'LESBiANS', 'AMaTEurcuMsLuTS', 'THicK', 'NormALNudES', 'incESTCOmicS', 'DIScorDnUdeS', 'CursedIMAGEs', 'HENtaIbEAST', 'LAbIagW', 'grool', 'OnLyFansProMoSs', 'SEXtoYs', 'dIRtypeNPals', 'WHoLESomeheNtaI', 'girLSINyoGapaNtS', 'laTINAS', 'DiRTyr4', 'czSkhOes', 'GenSHInIMpactnSfW', 'ReDGifs', 'sExwoRKers', 'EyeblEAch', 'bonDaGE', 'eBOny', 'liPstHATGRIP', 'dEePTHroat', 'raTEMyNUDEBOdY', 'GaYSToRIESgoNewILD', 'tWINks', 'eXxxtras', 'moNsTERgIrL', 'thighDeOlOgy', 'gWpUBlIc', 'bdsmGW', 'haIRyPusSy', 'gOnEwildtRAnS', 'PlasTT', 'Bbw', 'LaDyboNERsGw', 'FReealbuM4u', 'DIRTySmAlL', 'OVErWaTCh_pOrN', 'StreeTsISwAtChiN', 'AnAlGw', 'NEedYSLuTs', 'INdiANsgOnEwILD', 'rateMYcock', 'onLYfAnS_proMO', 'DmT', 'CLeAvAgE', 'pRoGrEsSIVEGrOwth', 'WifESHARING', 'coLLegeaMATEUrs', 'bURSTInGoUt', 'biMboFeTiSH', 'ButTSANdBAReFEET', 'meDicaLgORe', 'VAmsCeNeS', 'eXtRAMILe', 'amATEurGirLSbiGcOcks', 'FITNakeDGIrlS', 'dARkjokes', 'FUNwitHfrienDs', 'StRaIGHtGirlsPlAyING', 'PENis', 'HENtaICAPTioNS', 'CUmFEtiSh', 'AlTGONEwiLd', 'ShELiKeSitrOugh', 'ECcHi', 'HoMeGRoWNtits', 'hugEDicKTiNYChICK', 'sexInFrontofOTHeRs', 'girLSwITHglAsses', 'cOUpleGonEWild', 'bUTTpLuG', 'rPDRDRAMA', 'geTtInGhersElfoFf', 'HololewD', 'daMnGoOdIntErRAciaL', 'FeMdoM', 'NsFWrare', 'MsPuiyI', 'SeXYtumMIes', 'goNewiLDColor', 'GEnTlefEmDoM', 'HENTAIMEMES', 'SlutbLoNdE', 'IWAnTtOSUcKCocK', 'GingeR', 'BBCSLUTS', 'OmEGLeseX', 'dKceLEbs', 'QUIVeR', 'RuLe34_cOmiCS', 'FEet', 'inDIaNbAbEs', 'cHiCkFLiXXX', 'FEstiValSLutS', 'CREampIES', 'HARDbODIes', 'pREGGOpOrN', '40PlUsgONewILd', 'BADdraGon', 'CAMSLuts', 'SWIngERsgW', 'stUFFerS', 'SeXsToRIes', 'SLuTSOFOnLyFaNs', 'TOmXcontEnts', 'theraTIO', 'ChAStitY', 'NSFW', 'NUDES', 'ASS', 'RULE34', 'BOOBS', 'GONEWILD', 'REALGIRLS', 'HENTAI', 'NSFW411', 'WORLDPACKS', 'CELEBNSFW', 'ASIANSGONEWILD', 'COLLEGESLUTS', 'PETITEGONEWILD', 'CUMSLUTS', 'BUSTYPETITE', 'LEGALTEENS', 'ADORABLEPORN', 'GONEWILDSTORIES', 'WATCHITFORTHEPLOT', 'GONEWILDAUDIO', 'TIPOFMYPENIS', 'BREEDINGMATERIAL', 'TRAPS', 'NSFWASMR', 'JIZZEDTOTHIS', 'CUCKOLD', 'ONLYFANSGIRLS101', 'MILF', 'PORN', 'TIKTOKNSFW', 'PUSSY', 'GIRLSFINISHINGTHEJOB', 'WORLDPOLITICS', 'TIKTHOTS', 'SLUTTYCONFESSIONS', 'ASKREDDITAFTERDARK', 'JERKOFFTOCELEBS', 'TITTYDROP', 'GONEWILD30PLUS', 'HOLDTHEMOAN', 'INTERMITTENTFASTING', 'ONOFF', 'ONLYFANS101', 'BIGGERTHANYOUTHOUGHT', 'HOTWIFE', 'BLOWJOBS', 'GWCOUPLES', 'LEAKEDONLYFANS', 'KPOPFAP', 'NSFWFUNNY', 'HENTAI_GIF', 'NUDE_SELFIE', 'NSFW_GIFS', 'NAUGHTYWIVES', 'PORNINFIFTEENSECONDS', 'STREAMERSGONEWILD', 'YAGAMIYATO', 'FUTANARI', 'JOI', 'HOMEMADEXXX', 'TIKTOKPORN', 'PAWG', 'NUDES', 'MORBIDREALITY', 'MASSIVECOCKS', 'ASIANHOTTIES', 'TWITCHGONEWILD', 'ANAL', 'GONEWILD18', 'JUICYASIANS', 'TINYTITS', 'YOUTUBETITTIES', '18_19', 'TIKTOKNUDE', 'BIGBOOBSGW', 'BIGASSES', 'GODPUSSY', 'NSFWVERIFIEDAMATEUR', 'LEWDGAMES', '18NSFW', 'TOOCUTEFORPORN', 'TRASHYBONERS', 'SEX_COMICS', 'ONLYFANSPACKS', 'PALEGIRLS', 'XSMALLGIRLS', 'SISSYHYPNO', 'AMATEUR', 'FEMBOYS', 'CHUBBY', 'NHENTAI', 'FITGIRLS', 'PORNVIDS', 'FREEUSE', 'ASSHOLE', 'GONEMILD', 'YOUTUBERSGONEWILD', 'CURVY', 'TRAPHENTAI', 'STACKE', 'SISSIES', 'WORKGONEWILD', 'NSFWCYOA', 'BODYPERFECTION', 'DOUJINSHI', 'YIFF', 'SLUT', 'THE_BEST_NSFW_GIFS', 'RULE34LOL', 'BDSMCOMMUNITY', 'STUPIDSLUTSCLUB', 'ONLYFANSPROMOTIONS', 'NSFWHARDCORE', 'BDSM', 'NSFWGAMING', 'GONEWILDCOUPLES', 'BIGTIDDYGOTHGF', 'UPSKIRT', 'ASSTASTIC', 'REALAHEGAO', 'GAYBROSGONEWILD', 'ELLEKNOX', 'NSFWCOSPLAY', 'HUGEBOOBS', 'HONEYSELECT', 'GWCUMSLUTS', 'NSFW_KOREA', 'ASSHOLEGONEWILD', 'YOUNGPRETTYHOES', 'WOULDYOUFUCKMYWIFE', 'PAAG', 'CUTELITTLEBUTTS', 'TRANSFORMATION', 'GERMANCELEBRITIESFAP', 'UNDERWEARGW', 'TGIRLS', 'LESBIANS', 'AMATEURCUMSLUTS', 'THICK', 'NORMALNUDES', 'INCESTCOMICS', 'DISCORDNUDES', 'CURSEDIMAGES', 'HENTAIBEAST', 'LABIAGW', 'GROOL', 'ONLYFANSPROMOSS', 'SEXTOYS', 'DIRTYPENPALS', 'WHOLESOMEHENTAI', 'GIRLSINYOGAPANTS', 'LATINAS', 'DIRTYR4', 'CZSKHOES', 'GENSHINIMPACTNSFW', 'REDGIFS', 'SEXWORKERS', 'EYEBLEACH', 'BONDAGE', 'EBONY', 'LIPSTHATGRIP', 'DEEPTHROAT', 'RATEMYNUDEBODY', 'GAYSTORIESGONEWILD', 'TWINKS', 'EXXXTRAS', 'MONSTERGIRL', 'THIGHDEOLOGY', 'GWPUBLIC', 'BDSMGW', 'HAIRYPUSSY', 'GONEWILDTRANS', 'PLASTT', 'BBW', 'LADYBONERSGW', 'FREEALBUM4U', 'DIRTYSMALL', 'OVERWATCH_PORN', 'STREETSISWATCHIN', 'ANALGW', 'NEEDYSLUTS', 'INDIANSGONEWILD', 'RATEMYCOCK', 'ONLYFANS_PROMO', 'DMT', 'CLEAVAGE', 'PROGRESSIVEGROWTH', 'WIFESHARING', 'COLLEGEAMATEURS', 'BURSTINGOUT', 'BIMBOFETISH', 'BUTTSANDBAREFEET', 'MEDICALGORE', 'VAMSCENES', 'EXTRAMILE', 'AMATEURGIRLSBIGCOCKS', 'FITNAKEDGIRLS', 'DARKJOKES', 'FUNWITHFRIENDS', 'STRAIGHTGIRLSPLAYING', 'PENIS', 'HENTAICAPTIONS', 'CUMFETISH', 'ALTGONEWILD', 'SHELIKESITROUGH', 'ECCHI', 'HOMEGROWNTITS', 'HUGEDICKTINYCHICK', 'SEXINFRONTOFOTHERS', 'GIRLSWITHGLASSES', 'COUPLEGONEWILD', 'BUTTPLUG', 'RPDRDRAMA', 'GETTINGHERSELFOFF', 'HOLOLEWD', 'DAMNGOODINTERRACIAL', 'FEMDOM', 'NSFWRARE', 'MSPUIYI', 'SEXYTUMMIES', 'GONEWILDCOLOR', 'GENTLEFEMDOM', 'HENTAIMEMES', 'SLUTBLONDE', 'IWANTTOSUCKCOCK', 'GINGER', 'BBCSLUTS', 'OMEGLESEX', 'DKCELEBS', 'QUIVER', 'RULE34_COMICS', 'FEET', 'INDIANBABES', 'CHICKFLIXXX', 'FESTIVALSLUTS', 'CREAMPIES', 'HARDBODIES', 'PREGGOPORN', '40PLUSGONEWILD', 'BADDRAGON', 'CAMSLUTS', 'SWINGERSGW', 'STUFFERS', 'SEXSTORIES', 'SLUTSOFONLYFANS', 'TOMXCONTENTS', 'THERATIO', 'CHASTITY', 'DEGRADINGHOLES','SEXY', 'nsfw', 'nudes', 'ass', 'rule34', 'boobs', 'gonewild', 'realgirls', 'hentai', 'nsfw411', 'worldpacks', 'celebnsfw', 'asiansgonewild', 'collegesluts', 'petitegonewild', 'cumsluts', 'bustypetite', 'legalteens', 'adorableporn', 'gonewildstories', 'watchitfortheplot', 'gonewildaudio', 'tipofmypenis', 'breedingmaterial', 'traps', 'nsfwasmr', 'jizzedtothis', 'cuckold', 'onlyfansgirls101', 'milf', 'porn', 'tiktoknsfw', 'pussy', 'girlsfinishingthejob', 'worldpolitics', 'tikthots', 'sluttyconfessions', 'askredditafterdark', 'jerkofftocelebs', 'tittydrop', 'gonewild30plus', 'holdthemoan', 'intermittentfasting', 'onoff', 'onlyfans101', 'biggerthanyouthought', 'hotwife', 'blowjobs', 'gwcouples', 'leakedonlyfans', 'kpopfap', 'nsfwfunny', 'hentai_gif', 'nude_selfie', 'nsfw_gifs', 'naughtywives', 'porninfifteenseconds', 'streamersgonewild', 'yagamiyato', 'futanari', 'joi', 'homemadexxx', 'tiktokporn', 'pawg', 'nudes', 'morbidreality', 'massivecocks', 'asianhotties', 'twitchgonewild', 'anal', 'gonewild18', 'juicyasians', 'tinytits', 'youtubetitties', '18_19', 'tiktoknude', 'bigboobsgw', 'bigasses', 'godpussy', 'nsfwverifiedamateur', 'lewdgames', '18nsfw', 'toocuteforporn', 'trashyboners', 'sex_comics', 'onlyfanspacks', 'palegirls', 'xsmallgirls', 'sissyhypno', 'amateur', 'femboys', 'chubby', 'nhentai', 'fitgirls', 'pornvids', 'freeuse', 'asshole', 'gonemild', 'youtubersgonewild', 'curvy', 'traphentai', 'stacke', 'sissies', 'workgonewild', 'nsfwcyoa', 'bodyperfection', 'doujinshi', 'yiff', 'slut', 'the_best_nsfw_gifs', 'rule34lol', 'bdsmcommunity', 'stupidslutsclub', 'onlyfanspromotions', 'nsfwhardcore', 'bdsm', 'nsfwgaming', 'gonewildcouples', 'bigtiddygothgf', 'upskirt', 'asstastic', 'realahegao', 'gaybrosgonewild', 'elleknox', 'nsfwcosplay', 'hugeboobs', 'honeyselect', 'gwcumsluts', 'nsfw_korea', 'assholegonewild', 'youngprettyhoes', 'wouldyoufuckmywife', 'paag', 'cutelittlebutts', 'transformation', 'germancelebritiesfap', 'underweargw', 'tgirls', 'lesbians', 'amateurcumsluts', 'thick', 'normalnudes', 'incestcomics', 'discordnudes', 'cursedimages', 'hentaibeast', 'labiagw', 'grool', 'onlyfanspromoss', 'sextoys', 'dirtypenpals', 'wholesomehentai', 'girlsinyogapants', 'latinas', 'dirtyr4', 'czskhoes', 'genshinimpactnsfw', 'redgifs', 'sexworkers', 'eyebleach', 'bondage', 'ebony', 'lipsthatgrip', 'deepthroat', 'ratemynudebody', 'gaystoriesgonewild', 'twinks', 'exxxtras', 'monstergirl', 'thighdeology', 'gwpublic', 'bdsmgw', 'hairypussy', 'gonewildtrans', 'plastt', 'bbw', 'ladybonersgw', 'freealbum4u', 'dirtysmall', 'overwatch_porn', 'streetsiswatchin', 'analgw', 'needysluts', 'indiansgonewild', 'ratemycock', 'onlyfans_promo', 'dmt', 'cleavage', 'progressivegrowth', 'wifesharing', 'collegeamateurs', 'burstingout', 'bimbofetish', 'buttsandbarefeet', 'medicalgore', 'vamscenes', 'extramile', 'amateurgirlsbigcocks', 'fitnakedgirls', 'darkjokes', 'funwithfriends', 'straightgirlsplaying', 'penis', 'hentaicaptions', 'cumfetish', 'altgonewild', 'shelikesitrough', 'ecchi', 'homegrowntits', 'hugedicktinychick', 'sexinfrontofothers', 'girlswithglasses', 'couplegonewild', 'buttplug', 'rpdrdrama', 'gettingherselfoff', 'hololewd', 'damngoodinterracial', 'femdom', 'nsfwrare', 'mspuiyi', 'sexytummies', 'gonewildcolor', 'gentlefemdom', 'hentaimemes', 'slutblonde', 'iwanttosuckcock', 'ginger', 'bbcsluts', 'omeglesex', 'dkcelebs', 'quiver', 'rule34_comics', 'feet', 'indianbabes', 'chickflixxx', 'festivalsluts', 'creampies', 'hardbodies', 'preggoporn', '40plusgonewild', 'baddragon', 'camsluts', 'swingersgw', 'stuffers', 'sexstories', 'slutsofonlyfans', 'tomxcontents', 'theratio', 'chastity', 'degradingholes','sexy', 'nSFw', 'nUdes', 'asS', 'rulE34', 'BOoBs', 'gOnewild', 'rEALGirls', 'HeNTaI', 'Nsfw411', 'wOrlDPacKS', 'celeBNsFw', 'aSIansgONeWILd', 'cOLleGeSLUtS', 'peTITeGonewilD', 'CumSlUTs', 'buStYPetIte', 'LEgaLtEEns', 'adORaBLepoRN', 'goneWIldSToRies', 'wAtChITfORTHePlOt', 'GOnewIldauDIo', 'TiPOFmyPenIS', 'brEedINGMateriAl', 'TRaPS', 'nSfWasMr', 'JiZzeDtoThiS', 'cuckOlD', 'OnLYFANsgiRLs101', 'MiLF', 'porN', 'TiktOKnsfw', 'PuSsy', 'GIRLSFinIsHINGThEjoB', 'worldPOLItICS', 'TIKTHoTS', 'sluTTYcOnFESSIONS', 'aSkREDdITAfteRdaRk', 'jeRKOFFToCelebS', 'TIttYDROP', 'goNEWILD30PluS', 'HOLDthEMoAn', 'InTERMITTeNTfaStING', 'oNoFF', 'onLyFANS101', 'BiggerThaNyouThOuGhT', 'HOTWife', 'bLoWJObS', 'gWcoUPles', 'lEaKEdOnLyfAns', 'KPOPfap', 'nsfWFUNNy', 'HENtAI_GiF', 'NUDe_SELFie', 'nsFW_GIfs', 'NaUgHtYWiveS', 'poRNinFIFTeeNSEcondS', 'strEamERSGONEWilD', 'YAGAmIyAto', 'fuTANaRI', 'jOI', 'HomEMAdExXx', 'TIKTOKPORn', 'PaWg', 'nUdES', 'MoRbiDreaLitY', 'MassIVecOckS', 'ASIanhOTTIeS', 'twiTCHgonewILD', 'ANAL', 'GONEwiLd18', 'juICyASiANS', 'TiNytITs', 'YoUTuBeTItTIES', '18_19', 'TiKtoKNude', 'BIgboObSGw', 'bIgaSSES', 'godpUSsy', 'nSFwVERiFIeDaMATeUR', 'lEWdGAMES', '18nsfw', 'tOOCUTefORpORn', 'tRaShYBoNERs', 'sex_CoMics', 'onlYfANSPACKS', 'PAlEgIrLs', 'xSmalLGIrLs', 'siSsYhyPNO', 'AmaTeur', 'FemBOYs', 'cHUBBY', 'nHenTaI', 'FiTGiRls', 'pOrNvids', 'FReEuSe', 'ASsHoLE', 'GONemIlD', 'YoUtuBersGoNEWiLD', 'cURVy', 'traphenTai', 'sTAcKe', 'SISsiES', 'wOrKgONEwILd', 'NsFWCYOa', 'BOdYPERFeCtIon', 'douJiNshI', 'YifF', 'SLut', 'THE_best_nSFw_gIfs', 'rulE34LOl', 'BDSMcOmMUnItY', 'sTUpIDsluTSClUb', 'OnlyFANsproMoTionS', 'NSFWHARDCOre', 'Bdsm', 'nSFWgAmIng', 'GoNEwiLDcOUPlES', 'bIGtidDYgoThGF', 'upsKIRt', 'aSSTastiC', 'ReaLAHegAO', 'GAYbrOsGoNewiLd', 'eLlekNOx', 'nSFwcospLAy', 'HugEbOOBs', 'HOnEySeLeCt', 'GwcumSluTS', 'nSFw_KoREA', 'assHoleGoneWILd', 'YOUNgPREttyHOEs', 'wouLDyoufuckMywiFE', 'paaG', 'cUTeLITTLebUtts', 'trANSFoRmaTIOn', 'geRMANCelEbrITIESfap', 'uNderWeARGW', 'TgirlS', 'lESbiAns', 'amATEUrcUmslutS', 'ThiCk', 'nORMAlnuDes', 'incESTcOmICs', 'DisCoRDnUdeS', 'cUrSedimaGeS', 'HentaibEAsT', 'laBiagw', 'GrOOL', 'onLyFANSPrOMosS', 'SeXTOyS', 'DirTypEnpalS', 'wHolEsomEhentAi', 'GIRlsINyOgAPantS', 'LATInAs', 'DIRTyr4', 'cZsKHOes', 'GenshinImpACtnsFW', 'REDGIFS', 'sExworkERS', 'EyEblEACH', 'BOndAGe', 'eBoNy', 'LipStHatGRIp', 'deEpthroat', 'RATEmyNUdebodY', 'GAYStorIesGoNewiLD', 'TWInks', 'ExxxtRAs', 'mONSteRgiRL', 'tHiGHdEOLogY', 'GWPuBliC', 'bdSmGW', 'hAirypUssy', 'gONEwiLDtRANs', 'pLastt', 'BbW', 'lAdyBoNerSgW', 'FreEAlbuM4u', 'DirTYsMall', 'ovErWatch_porn', 'sTrEetsiswAtChIn', 'anAlGW', 'NeEDySLUTs', 'iNdIANSGONEWIlD', 'RATeMYcOck', 'onlYfans_prOmO', 'dMT', 'cleaVaGE', 'ProGrEssIvEGRowtH', 'WIfEshARing', 'ColLEgEamateURs', 'BURSTInGOUT', 'BIMbofeTiSH', 'buttSAnDbAREFEET', 'medIcAlGOre', 'vamsCeNeS', 'extRamILE', 'amateuRgirlSbiGcOckS', 'FitnaKEdGIRlS', 'daRkjOkEs', 'funwIThfRIenDs', 'straIGHTgiRLsPlAyiNG', 'PENIs', 'HentaIcAptioNs', 'cUMfeTisH', 'alTGoNeWIlD', 'ShElIKEsItroUGh', 'ECChI', 'hOmeGrowNtITS', 'hUgEDiCkTInycHick', 'SexInFrOntoFOtHerS', 'giRLSwITHGlAsseS', 'COUPlEGONeWild', 'butTPLuG', 'RpDrdrAMa', 'GETTiNGherSELfoFf', 'hoLoLeWD', 'daMNgOODINTerRaciAL', 'FemdOm', 'NsFWraRe', 'mspUiYI', 'sEXytumMIes', 'GoNEwIlDcOlOr', 'gEnTleFEmdOM', 'hentaIMeMES', 'SLutBloNDe', 'IwAnTtoSucKcocK', 'GingeR', 'BbcSLuTs', 'OMeGLEseX', 'dKcElebS', 'QuIveR', 'RuLE34_COmics', 'fEET', 'inDianbAbEs', 'CHicKflixXX', 'fesTIVAlSlUTs', 'CREAmPIEs', 'HaRDBOdIEs', 'pReggOpoRn', '40plUSGonEwilD', 'BAddRagON', 'cAmslUts', 'swinGErSGw', 'stUFfeRs', 'SeXstORIeS', 'SlutSofonLYfaNs', 'TOmXconTenTS', 'TheRATIO', 'CHastITY', 'deGRADinGHolES','SExy', 'nsfW', 'NUdES', 'aSS', 'RULE34', 'BOOBS', 'GOnEwILd', 'RealGIrLS', 'HenTai', 'nSFw411', 'WOrlDPACKS', 'celEBNsfw', 'AsiANSgOneWiLd', 'COlLEGesLuts', 'pETiTEgonEwiLD', 'cUmsLuTS', 'BusTyPEtiTe', 'lEgALTeeNS', 'ADOraBLePORN', 'gOneWILDstORiES', 'watchitfORTHEplOT', 'gOneWilDAudIO', 'tIpOFmypEniS', 'BReEdInGMatErIal', 'TRAps', 'nsfWasmR', 'jiZzedtOtHiS', 'cucKOlD', 'oNLYFANsGiRls101', 'MiLf', 'pOrn', 'TIktokNsFw', 'PUsSy', 'GIrLsfinisHinGtHejoB', 'wOrLdPOlItiCs', 'tiktHOtS', 'sLuTTyCONFeSSiONs', 'asKrEdDItaftErdArk', 'jeRKoFFtOCElebs', 'tiTTydRoP', 'GOnEwild30Plus', 'HOLdThEmOan', 'interMiTteNTfaStiNg', 'onoFF', 'oNLyfans101', 'BiGGertHanYOUTHouGHt', 'HOtWIFe', 'blowjObS', 'gWcoUpLeS', 'LEAkEDOnlyFaNs', 'KpoPfap', 'NSFWfuNny', 'HeNTAI_GIf', 'nude_selfiE', 'nsFW_GIFs', 'naugHtyWIVeS', 'poRniNfiFteensecondS', 'STReAMErsGOneWiLD', 'YaGAmiyatO', 'fUTaNArI', 'JoI', 'homeMAdEXxX', 'tIkTOKpOrN', 'PawG', 'nudES', 'MoRBiDrEALItY', 'MaSSIVecoCKS', 'AsIanhotTIeS', 'tWiTCHgoNEwiLD', 'AnAL', 'goNeWILd18', 'JUICyaSIAns', 'tInYTitS', 'yOUtUBEtITTiES', '18_19', 'tIKTOKNuDe', 'bIGBoObsgW', 'bIGaSsES', 'godPussy', 'nSfwVERIFIedaMATeUR', 'LeWdGaMes', '18NSFW', 'TooCUtEFOrPoRn', 'tRAshYBOnErS', 'SEX_coMiCS', 'OnLyFANSpAcKs', 'pAlEgIrls', 'xSmALlGIRLS', 'siSsYHYpno', 'aMAteUr', 'feMBoYs', 'ChuBbY', 'NHeNtAI', 'FiTGiRLS', 'POrnVIDS', 'fREeuSE', 'aSshOLE', 'GoneMiLD', 'YOUTUBeRsGONEwILD', 'CUrvY', 'TraPhEntai', 'sTaCKE', 'SiSsIES', 'WorKgonEWild', 'nsFwCYOA', 'bODyPerFectIOn', 'DOUJINShI', 'yIFF', 'SLUt', 'The_BEST_NsFw_GIFS', 'RUle34LoL', 'bdsmCOMmuNIty', 'STuPidslutSCLuB', 'onlyfANsPROMOtIONS', 'NsfWHARdcore', 'bDsM', 'NSfWgAmInG', 'gonEwildcOuPLES', 'bIgTIdDyGoThgF', 'UpsKiRT', 'ASSTasTIC', 'REalAheGAo', 'gAybrOSGONeWIld', 'ELleKnOx', 'nSfwCosplaY', 'hUGEBOobS', 'hoNEySElECT', 'GwCUmSlutS', 'nsFW_koREA', 'ASSHolegonEwiLD', 'yOUNgpRETTYHoES', 'WOULDYOufuCKmyWiFe', 'PAAg', 'cutELITTlEBUTts', 'TrAnSFOrmatIoN', 'GErmAnCelEBriTiesFAp', 'undERWEarGw', 'TGIRLS', 'lEsBiaNS', 'amAteURcUMSluts', 'thiCk', 'nOrmaLnUdEs', 'inCeStCOmiCS', 'DisCOrDNUdes', 'cURSEdImaGeS', 'heNtaIbeaST', 'LABiaGW', 'GRoOl', 'ONlyfanSProMOss', 'SextOYS', 'DirtyPEnpAlS', 'WhOlESomEHeNTai', 'GIrLSINYoGapAnTS', 'LatInAs', 'DiRtyR4', 'CZskHoEs', 'GeNShiNiMpAcTNsFW', 'REDGIfS', 'sExworkerS', 'EyEBlEaCh', 'boNDAGe', 'EbonY', 'LipsTHaTGRIp', 'deePThROaT', 'rAtemyNudeBOdy', 'gAysTORIesgONewiLd', 'TwiNks', 'ExXXTras', 'MoNstErgirL', 'THiGhdeology', 'GwpuBLiC', 'BDSMgW', 'hAiRYpussy', 'GonEwiLdTRAnS', 'pLAStt', 'bbw', 'laDYboNErsGW', 'freeALBUM4u', 'DIRtYsmalL', 'oveRWAtCH_POrn', 'StrEetSisWATchIN', 'aNAlGw', 'NeedySlUts', 'INDIaNSgonEwIld', 'RAteMyCOck', 'ONlyFaNS_pROmO', 'DMt', 'cleAvage', 'ProgREssIvEgroWTh', 'wifEsHAring', 'cOlleGeAMAteurs', 'BurstIngoUt', 'BimBofEtiSh', 'bUttSaNdBarEFEET', 'mEDICaLgOrE', 'vamscenEs', 'extrAMilE', 'aMatEUrgirLSBiGcOcKs', 'FItNakedGiRLs', 'DarkJokes', 'fuNwIThfrIEnds', 'sTraightGirLSpLaYiNG', 'pEniS', 'hENtaiCAptIOns', 'cUMfETiSh', 'ALtGONeWiLD', 'shelikeSitrOUgH', 'eCchi', 'homEGrowNtitS', 'HuGedICKtinYChICk', 'sExiNfRonTOFoTHeRs', 'GiRLsWITHGLaSSes', 'COuplEgONewild', 'BUttpLuG', 'rpDRdrAma', 'gEtTINgheRSElFOfF', 'hoLOLEwD', 'dAMnGOOdintErrAciaL', 'FEMDom', 'NSFWRAre', 'MSpUIYi', 'sExYtumMiEs', 'GonEWildcOlOr', 'gEntLeFemDOm', 'HeNTAIMemeS', 'slUtBLondE', 'IWaNTTOSUcKCOck', 'GinGEr', 'bBCsLutS', 'oMeGLEsex', 'dkCelebs', 'QUIVEr', 'RuLE34_cOMiCS', 'fEET', 'iNdianBABES', 'CHiCKflixXX', 'FEsTivaLSlUtS', 'CReaMPIes', 'HardBODIES', 'PReggOpORn', '40PLUsGoNewiLd', 'BaDDRAgOn', 'CaMslUtS', 'swiNGERSGw', 'sTUffERS', 'seXSTOrIeS', 'SLUTsOFOnLyFANs', 'tOMxCoNtEnTS', 'THERaTIo', 'ChASTItY', 'DegRadinGHoLeS','SExY',]
    if subreddit in nsfw_list:
        nsem = discord.Embed(title="NSFW SUBREDDIT", color=discord.Color.red())
        nsem.add_field(name="Please use `$nsfw` in an NSFW channel!", value="If you belive this to be an error please reach out on the [support server](https://discord.com/invite/zs7UwgBZb9)", inline=False)
        await ctx.send(embed=nsem)
    else:
        r = requests.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=hot')
        res = r.json()
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://www.reddit.com/r/{subreddit}/new.json?sort=hot') as r:
                res = await r.json()
                sub = res['data']['children'] [random.randint(0, 25)]['data']['subreddit']
                picurl = res['data']['children'] [random.randint(0, 25)]['data']['url']
                user = ctx.message.author
                embed = discord.Embed(title=f"Random pic from r/{sub}", color = discord.Color.orange())
                embed.set_image(url=picurl)
                embed.set_footer(text=f"Requested by: {user}  r/{sub}")
            await ctx.send(embed = embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'reddit'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'reddit'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Reddit -- {cupGuild} by {cupUser}")

@reddit.error
async def reddit_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a subreddit")

# coin flip
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def coinflip(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'coinflip'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    result_list = ['tails', 'heads']
    result = random.choice(result_list)
    if result == 'heads':
        await ctx.send('<:simp_coin:824720566241853460> Heads!')
    elif result == 'tails':
        await ctx.send('<:fuck_coin:824720614543196220> Tails!')
    cursor.execute("SELECT used FROM commands WHERE name = 'coinflip'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'coinflip'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"CoinFlip -- {cupGuild} by {cupUser}")

@coinflip.error
async def coinflip_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# donate command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def donate(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'donate'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    embed = discord.Embed(title="Donate To DoxBot", url='https://doxbot.xyz/donate', color=0xff6666)
    embed.add_field(name="Help support DoxBot", value="Donating is not required, but is greatly appreciated. For more info click [Here](https://doxbot.xyz/faq)", inline=False)
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'donate'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'donate'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Donate -- {cupGuild} by {cupUser}")

@donate.error
async def donate_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# poll command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def poll(ctx, *, args):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'poll'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    channel = ctx.channel
    message = args
    try:
        opt1 , opt2 = message.split("or")
        na = f"Poll: {opt1} or {opt2}"
    except:
        errorembed = discord.Embed(title="Error", description="The correct syntax is `$poll [option1] or [option2]`", color=discord.Color.red())
        await channel.send(embed=errorembed)

    opt1 , opt2 = message.split("or")
    na = f"Poll: {opt1} or {opt2}"
    embed = discord.Embed(title=f"{na}", color=discord.Color.green())
    embed.set_footer(text="React with 1️⃣ for option 1 or 2️⃣ for option 2")
    message_ = await channel.send(embed=embed)
    await message_.add_reaction("1️⃣")
    await message_.add_reaction("2️⃣")
    await ctx.message.delete()
    cursor.execute("SELECT used FROM commands WHERE name = 'poll'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'poll'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Poll -- {cupGuild} by {cupUser}")

@poll.error
async def poll_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredPermissions):
        await ctx.send("Please follow the poll syntax: `poll [option 1] or [option 2]` make sure you include the 'OR'")

# music stuff
# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** by **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    def create_embed(self):
        embed = (discord.Embed(title='Now playing',
                               description='```css\n{0.source.title}\n```'.format(self),
                               color=discord.Color.blurple())
                 .add_field(name='Duration', value=self.source.duration)
                 .add_field(name='Requested by', value=self.requester.mention)
                 .add_field(name='Uploader', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                 .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                 .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Try to get the next song within 3 minutes.
                # If no song will be added to the queue in time,
                # the player will disconnect due to performance
                # reasons.
                try:
                    async with timeout(180):  # 3 minutes
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('This command can\'t be used in DM channels.')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send('Error: **{}**'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _join(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'join'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.message.add_reaction('👍')
        cursor.execute("SELECT used FROM commands WHERE name = 'join'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'join'")
          db.commit()
          cupGuild = ctx.guild.name
          cupUser = ctx.author
          print(f"Join -- {cupGuild} by {cupUser}")

    @commands.command(name='summon')
    @commands.cooldown(1,1,commands.BucketType.guild)
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'summon'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Summons the bot to a voice channel.

        If no channel was specified, it joins your channel.
        """

        if not channel and not ctx.author.voice:
            raise VoiceError('You are neither connected to a voice channel nor specified a channel to join.')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            
            return

        ctx.voice_state.voice = await destination.connect()
        await ctx.message.add_reaction('👍')
        cursor.execute("SELECT used FROM commands WHERE name = 'summon'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'summon'")
          db.commit()
          cupGuild = ctx.guild.name
          cupUser = ctx.author
          print(f"Summon -- {cupGuild} by {cupUser}")

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _leave(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'leave'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]
        await ctx.message.add_reaction('👋')
        cursor.execute("SELECT used FROM commands WHERE name = 'leave'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'leave'")
          db.commit()
          cupGuild = ctx.guild.name
          cupUser = ctx.author
          print(f"Leave -- {cupGuild} by {cupUser}")

    @commands.command(name='volume')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _volume(self, ctx: commands.Context, *, volume: int):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'volume'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))
        cursor.execute("SELECT used FROM commands WHERE name = 'volume'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'volume'")
          db.commit()
          cupGuild = ctx.guild.name
          cupUser = ctx.author
          print(f"Volume -- {cupGuild} by {cupUser}")

    @commands.command(name='now', aliases=['current', 'playing'])
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _now(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'now'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())
        cursor.execute("SELECT used FROM commands WHERE name = 'now'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'now'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Now -- {cupGuild} by {cupUser}")

    @commands.command(name='pause')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _pause(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'pause'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Pauses the currently playing song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')
        cursor.execute("SELECT used FROM commands WHERE name = 'pause'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'pause'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Pause -- {cupGuild} by {cupUser}")

    @commands.command(name='resume')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _resume(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'resume'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Resumes a currently paused song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')
        cursor.execute("SELECT used FROM commands WHERE name = 'resume'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'resume'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Resume -- {cupGuild} by {cupUser}")

    @commands.command(name='stop')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _stop(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'stop'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')
        cursor.execute("SELECT used FROM commands WHERE name = 'stop'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'stop'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Stop -- {cupGuild} by {cupUser}")

    @commands.command(name='skip')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _skip(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'skip'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Vote to skip a song. The requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Not playing any music right now...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Skip vote added, currently at **{}/3**'.format(total_votes))

        else:
            await ctx.send('You have already voted to skip this song.')
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Skip -- {cupGuild} by {cupUser}")

    @commands.command(name='queue')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'queue'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Shows the player's queue.

        You can optionally specify the page to show. Each page contains 10 elements.
        """

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} tracks:**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Viewing page {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)
        cursor.execute("SELECT used FROM commands WHERE name = 'queue'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'queue'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Queue -- {cupGuild} by {cupUser}")

    @commands.command(name='shuffle')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _shuffle(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'suffle'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')
        cursor.execute("SELECT used FROM commands WHERE name = 'shuffle'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'shuffle'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Shuffle -- {cupGuild} by {cupUser}")

    @commands.command(name='remove')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _remove(self, ctx: commands.Context, index: int):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'remove'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')
        cursor.execute("SELECT used FROM commands WHERE name = 'remove'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'remove'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Remove -- {cupGuild} by {cupUser}")

    @commands.command(name='loop')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _loop(self, ctx: commands.Context):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'loop'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Loops the currently playing song.

        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Loop -- {cupGuild} by {cupUser}")

    @commands.command(name='play')
    @commands.cooldown(1,1,commands.BucketType.guild)
    async def _play(self, ctx: commands.Context, *, search: str):
        guildID = ctx.guild.id
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'play'")
        cmdCheck = cursor.fetchone()
        if cmdCheck != None:
            return
        else:
            pass
        """Plays a song.

        If there are songs in the queue, this will be queued until the
        other songs finished playing.

        This command automatically searches from various sites if no URL is provided.
        A list of these sites can be found here: https://rg3.github.io/youtube-dl/supportedsites.html
        """

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('An error occurred while processing this request: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Enqueued {}'.format(str(source)))
        cursor.execute("SELECT used FROM commands WHERE name = 'play'")
        used = cursor.fetchone()
        for num in used:
          num += 1
          cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'play'")
          db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Play -- {cupGuild} by {cupUser}")

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('You are not connected to any voice channel.')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Bot is already in a voice channel.')

bot.add_cog(Music(bot))

# music help
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def musichelp(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'musichelp'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Music Help", color=discord.Color.teal())
        embed.add_field(name=f"{pre}play [song]", value="Play a song in a voice channel using DoxBot", inline=False)
        embed.add_field(name=f"{pre}queue", value="Display the queue", inline=False)
        embed.add_field(name=f"{pre}skip", value="Skip the current song and play the next in queue", inline=False)
        embed.add_field(name=f"{pre}remove [queue number]", value="Remove a specific song in queue", inline=False)
        embed.add_field(name=f"{pre}join", value="Make DoxBot join the voice channel you are in", inline=False)
        embed.add_field(name=f"{pre}leave", value="Make DoxBot leave the current VC", inline=False)
        embed.add_field(name=f"{pre}summon [channel id]", value="Tell Dox to join a specific channel (User must have Manage Channel permission)", inline=False)
        embed.add_field(name=f"{pre}pause", value="Pauses the song currently playing", inline=False)
        embed.add_field(name=f"{pre}resume", value="Resumes playing the paused song", inline=False)
        embed.add_field(name=f"{pre}stop", value="Stops the song playing", inline=False)
        embed.add_field(name=f"{pre}volume [number 1-100]", value="Sets the volume of the player", inline=False)
        embed.add_field(name=f"{pre}loop", value="Loop the song currently playing", inline=False)
        embed.add_field(name=f"{pre}shuffle", value="Shuffles the queue", inline=False)
        embed.add_field(name=f"{pre}now", value="Displays the song currently playing", inline=False)
        embed.set_footer(text="Note: Some of these commands will in the future be a premium feature so enjoy them now :)")
        await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'musichelp'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'musichelp'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"MusicHelp -- {cupGuild} by {cupUser}")

@musichelp.error
async def musichelp_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# afk command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def afk(ctx, *, args):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'afk'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    message = args
    author = ctx.message.author.mention
    await ctx.send(f"{author} is now AFK: **{message}**")
    cursor.execute("SELECT used FROM commands WHERE name = 'afk'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'afk'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"AFK -- {cupGuild} by {cupUser}")

@afk.error
async def afk_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("An AFK message is required")

# 8ball command
@bot.command(aliases=['8ball'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def eightball(ctx, *, args):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = '8ball'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    res_list = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Dont count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt', 'Yes.', 'Yes – definitely.', 'You may rely on it.']
    res = random.choice(res_list)
    ques = args
    author = ctx.message.author
    embed = discord.Embed(title="Magic 8 Ball")
    embed.set_thumbnail(url='https://img.pngio.com/magic-8-ball-by-horoscopecom-get-free-divination-games-just-for-fun-magic-8-ball-png-300_300.png')
    embed.add_field(name=f"A: {res}", value=f"Q: {ques}", inline=False)
    embed.set_footer(text=f"{author}")
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'eightball'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'eightball'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"8ball -- {cupGuild} by {cupUser}")

@eightball.error
async def eightball_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("A question is required")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# dog command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def dog(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'dog'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    r = requests.get('https://www.reddit.com/r/DogPics/new.json?sort=hot')
    res = r.json()
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/DogPics/new.json?sort=hot') as r:
                res = await r.json()
                picurl = res['data']['children'] [random.randint(0, 25)]['data']['url']
                user = ctx.message.author
                embed = discord.Embed(title="Here's a dog", color = discord.Color.dark_green())
                embed.set_image(url=picurl)
                embed.set_footer(text=f"Requested by: {user}  r/DogPics")
            await ctx.send(embed = embed)
    except (ValueError,IndexError):
        errorem = discord.Embed(title='DOG ERROR', color=discord.Color.red())
        errorem.add_field(name="An Error Occured", value="Please try the command again, if the error persists reach out for [support](https://discord.com/invite/zs7UwgBZb9)", inline=False)
        await ctx.send(embed=errorem)
    cursor.execute("SELECT used FROM commands WHERE name = 'dog'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'dog'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Dog -- {cupGuild} by {cupUser}")

@dog.error
async def dog_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# cat command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def cat(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'cat'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    r = requests.get('https://www.reddit.com/r/catpics/new.json?sort=hot')
    res = r.json()
    try:
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/catpics/new.json?sort=hot') as r:
                res = await r.json()
                picurl = res['data']['children'] [random.randint(0, 25)]['data']['url']
                user = ctx.message.author
                embed = discord.Embed(title="Here's a cat", color = discord.Color.dark_purple())
                embed.set_image(url=picurl)
                embed.set_footer(text=f"Requested by: {user}  r/catpics")
            await ctx.send(embed = embed)
    except (ValueError,IndexError):
        errorem = discord.Embed(title='CAT ERROR', color=discord.Color.red())
        errorem.add_field(name="An Error Occured", value="Please try the command again, if the error persists reach out for [support](https://discord.com/invite/zs7UwgBZb9)", inline=False)
        await ctx.send(embed=errorem)
    cursor.execute("SELECT used FROM commands WHERE name = 'cat'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'cat'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Cat -- {cupGuild} by {cupUser}")

@cat.error
async def cat_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# gif command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def gif(ctx,*,q="random"):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'gif'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    api_key=os.getenv('GIPHYAPI')
    api_instance = giphy_client.DefaultApi()
    my_channel = bot.get_channel(825193245445324810)

    try: 
    # Search Endpoint
        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)
        user = ctx.message.author

        emb = discord.Embed(title=f'{q} GIF', url=f'https://media.giphy.com/media/{giff.id}/giphy.gif', color=discord.Color.random())
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')
        emb.set_footer(text=f"{user} | Powered by GIPHY")

        await ctx.channel.send(embed=emb)
    except ApiException as e:
      timestamp = datetime.now()
      apierror = discord.Embed(title="GIPHY API ERROR", color=discord.Color.red())
      apierror.add_field(name="Exception when calling DefaultApi", value="gifs_search_get: %s\n" % e, inline=False)
      apierror.set_footer(text=f"{timestamp}")
      await my_channel.send(embed=apierror)
    cursor.execute("SELECT used FROM commands WHERE name = 'gif'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'gif'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"GIF -- {cupGuild} by {cupUser}")

@gif.error
async def gif_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# custom prefixes 2.0
# adding guild to database based on join (perm)
@bot.event
async def on_guild_join(guild):
    guildID = guild.id
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(guildID))
    result = cursor.fetchall()
    if(len(result)) == 0:
        cursor.execute("INSERT INTO `prefixes` (`guild_id`, `prefix`) VALUES ('" + str(guildID) + "', '$')")
        db.commit()
        cupGuild = guild.name
        print(f"Added new guild to DB -- {cupGuild}")
        return

# on message stuff
@bot.event
async def on_message(msg):
    guildID = msg.guild.id
    channelID = msg.channel.id
    userID = msg.author.id
    userMen = msg.author.mention
    user = msg.author
    # prefix
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(guildID))
    preUF = cursor.fetchone()
    if preUF == None or preUF == ('',):
        cursor.execute("INSERT INTO `prefixes` (`guild_id`, `prefix`) VALUES ('" + str(guildID) + "', '$')")
        db.commit()
        cupGuild = msg.guild.name
        print(f"Added guild to DB -- {cupGuild}")
        return
    elif bot.user.mentioned_in(msg):
        if "@everyone" in msg.content:
            return
        else:
            pass
        for pre in preUF:
            embedPre = discord.Embed(title=f"Prefix for this server: {pre}")
            await msg.channel.send(embed=embedPre)
    # word game
    if msg.author == bot.user:
        pass
    else:
        cursor.execute(f"SELECT channel_id FROM wordGame WHERE guild_id = {guildID}")
        chanIDUF = cursor.fetchone()
        if chanIDUF == None:
            pass
        else:
            for wordChanID in chanIDUF:
                if channelID == wordChanID:
                    cursor.execute(f"SELECT lastuser_id FROM wordGame WHERE guild_id = {guildID} AND channel_id = {wordChanID}")
                    lastUserIDUF = cursor.fetchone()
                    for lastUserID in lastUserIDUF:
                        cursor.execute(f"SELECT lastletter FROM wordGame WHERE guild_id = {guildID}")
                        letterUF = cursor.fetchone()
                        for lastLetter in letterUF:
                            cursor.execute(f"SELECT count FROM wordGame WHERE guild_id = {guildID}")
                            countUF = cursor.fetchone()
                            for count in countUF:
                                cursor.execute(f"SELECT highscore FROM wordGame WHERE guild_id = {guildID}")
                                highUF = cursor.fetchone()
                                for high in highUF:
                                    msg_str = str(msg.content)
                                    lastLet = msg_str[-1]
                                    firstLet = msg_str[0]
                                    if letterUF == ('',) and userID != lastUserID and count <= high:
                                        count += 1
                                        cursor.execute(f"UPDATE `wordGame` SET `lastLetter` = '{lastLet}', `lastuser_id` = {userID}, count = {count} WHERE `guild_id` = {guildID} AND `channel_id` = {wordChanID}")
                                        db.commit()
                                        await msg.add_reaction("✅")
                                        pass
                                    elif firstLet == lastLetter and userID != lastUserID and count <= high:
                                        count += 1
                                        cursor.execute(f"UPDATE `wordGame` SET `lastLetter` = '{lastLet}', `lastuser_id` = {userID}, count = {count} WHERE `guild_id` = {guildID} AND `channel_id` = {wordChanID}")
                                        db.commit()
                                        await msg.add_reaction("✅")
                                        pass
                                    elif firstLet == lastLetter and userID != lastUserID and count >= high:
                                        count += 1
                                        cursor.execute(f"UPDATE `wordGame` SET `lastLetter` = '{lastLet}', `lastuser_id` = {userID}, count = {count}, highscore = {count} WHERE `guild_id` = {guildID} AND `channel_id` = {wordChanID}")
                                        db.commit()
                                        await msg.add_reaction("⭐")
                                        pass
                                    elif firstLet != lastLetter and userID != lastUserID:
                                        cursor.execute(f"UPDATE `wordGame` SET `lastLetter` = '', `lastuser_id` = 1, `count` = 1 WHERE `guild_id` = {guildID} AND `channel_id` = {wordChanID}")
                                        db.commit()
                                        await msg.add_reaction("❌")
                                        await msg.channel.send(f"{userMen} **MESSED IT UP!! Your string was {count} words long!** Your word should have started with **{lastLetter}** rather than **{firstLet}**. Game restarted.")
                                        pass
                                    elif userID == lastUserID:
                                        cursor.execute(f"UPDATE `wordGame` SET `lastLetter` = '', `lastuser_id` = 1, `count` = 1 WHERE `guild_id` = {guildID} AND `channel_id` = {wordChanID}")
                                        db.commit()
                                        await msg.add_reaction("❌")
                                        await msg.channel.send(f"{userMen} **MESSED IT UP!! Your string was {count} words long!** You can't go twice in a row! Game restarted.")
                                        pass

    # counting game
    cursor.execute("SELECT count FROM counting WHERE guild_id = " + str(guildID))
    result = cursor.fetchone()
    if result == None:
        pass
    else:
        for count in result:
            cursor.execute("SELECT lastuser_id FROM counting WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
            lastUserUF = cursor.fetchone()
            if lastUserUF == None:
              pass
            else:
              for lastUser in lastUserUF:
                  cursor.execute("SELECT channel_id FROM counting WHERE guild_id = '" + str(guildID) + "'")
                  chanIDUF = cursor.fetchone()
                  if chanIDUF == None:
                    pass
                  else:
                    for chanID in chanIDUF:
                        cursor.execute("SELECT highscore FROM counting WHERE guild_id = '" + str(guildID) + "'")
                        high = cursor.fetchone()
                        if high == None:
                            pass
                        else:
                            for highS in high:
                                if msg.author == bot.user:
                                    pass
                                else:
                                    isNum = msg.content
                                    try:
                                        tmp = int(isNum)
                                        if msg.content == f"{count}" and userID != lastUser and channelID == chanID:
                                            if count >= highS and count > 1:
                                                count += 1
                                                cursor.execute("UPDATE counting SET count = '" + str(count) + "' WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
                                                cursor.execute("UPDATE counting SET lastuser_id = '" + str(userID) + "' WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
                                                cursor.execute("UPDATE counting SET highscore = '" + str(count) + "' WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
                                                db.commit()
                                                await msg.add_reaction("⭐")
                                                pass
                                            else:
                                                count += 1
                                                cursor.execute("UPDATE counting SET count = '" + str(count) + "' WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
                                                cursor.execute("UPDATE counting SET lastuser_id = '" + str(userID) + "' WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
                                                db.commit()
                                                await msg.add_reaction("✅")
                                                pass
                                        else:
                                            cursor.execute("UPDATE counting SET count = '1' WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
                                            cursor.execute("UPDATE counting SET lastuser_id = '1' WHERE guild_id = '" + str(guildID) + "' AND channel_id = '" + str(channelID) + "'")
                                            db.commit()
                                            await msg.add_reaction("❌")
                                            await msg.channel.send(f"{userMen} **RUINED IT AT {count}!!** The next number is **1**")
                                            pass
                                    except:
                                        pass
    await bot.process_commands(msg)

# set prefix command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'setprefix'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    if(len(prefix)) <= 8:
        cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
        result = cursor.fetchall()
        if(len(result)) == 0:
            print('Guild is not in DB... adding...')
            cursor.execute("INSERT INTO prefixes VALUES("  + str(ctx.guild.id) + "," + str(prefix) + ")")
            db.commit()
            pre = prefix
            embed = discord.Embed(title="Prefix Updated", color=discord.Color.random())
            embed.add_field(name=f"Updated to {pre}", value=f"To change it back use `{pre}setprefix`", inline=False)
            await ctx.send(embed=embed)
        else:
            guildID = ctx.guild.id
            pre = prefix
            cursor.execute("UPDATE prefixes SET prefix = '" + str(pre) + "' WHERE guild_id = '" + str(guildID) + "'")
            db.commit()
            embed = discord.Embed(title="Prefix Updated", color=discord.Color.random())
            embed.add_field(name=f"Updated to {pre}", value=f"To change it back use `{pre}setprefix`", inline=False)
            await ctx.send(embed=embed)
    elif(len(prefix)) > 8:
        await ctx.send("Prefix must be less than or equal to 8 characters")
    cursor.execute("SELECT used FROM commands WHERE name = 'setprefix'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'setprefix'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SetPrefix -- {cupGuild} by {cupUser}")

@setprefix.error
async def setprefix_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use that command")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please include a prefix, `{pre}setprefix [prefix]`")
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# prefix get command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def prefix(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'prefix'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        await ctx.send(f"The prefix for this server is **{pre}**")
    cursor.execute("SELECT used FROM commands WHERE name = 'prefix'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'prefix'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Prefix -- {cupGuild} by {cupUser}")

@prefix.error
async def prefix_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# command stats 
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def cstats(ctx, command):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'cstats'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userMention = ctx.author.mention
    userName = ctx.author
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        userID = ctx.author.id
        cursor.execute("SELECT used FROM commands WHERE name = '" + str(command) +"'")
        comUF = cursor.fetchall()
        if command == "all":
            if userID == owner_id:
                cursor.execute("SELECT SUM(used) FROM commands")
                sumAllUF = cursor.fetchall()
                sumAll = sumAllUF[0][0]
                embed = discord.Embed(title="Commands Run", description=f"Dox has executed **{sumAll}** commands", color=discord.Color.random())
                embed.set_footer(text=f"Since Febuary 29, 2021 | {userName}  ")
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{userMention} **{command}** Is not a valid command please try again")
        else:
            for comUF1 in comUF:
                for com in comUF1:
                    embed1 = discord.Embed(title="Command Stats", description=f"**{pre}{command}** has been used **{com}** times", color=discord.Color.random())
                    embed1.set_footer(text=f"Since Febuary 29, 2021 | {userName}  ")
                    await ctx.send(embed=embed1)
    cursor.execute("SELECT used FROM commands WHERE name = 'cstats'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'cstats'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Cstats -- {cupGuild} by {cupUser}")

@cstats.error
async def cstats_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# socials stuff
# socials set
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def set(message, social, account):
    guildID = message.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'set'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userID = message.author.id
    guildID = message.guild.id
    if social == "twitter":
        cursor.execute("SELECT twitter FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '" + str(account) + "', '', '', '', '', '', '', '', '', '', '')")
            db.commit()
            await message.send("Twitter Set!")
        else:
            cursor.execute("UPDATE socials SET twitter = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Twitter Set!")
    elif social == "instagram":
        cursor.execute("SELECT instagram FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '"+ str(account) +"', '', '', '', '', '', '', '', '', '')")
            db.commit()
            await message.send("Intagram Set!")
        else:
            cursor.execute("UPDATE socials SET instagram = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Instagram Set!")
    elif social == "tiktok":
        cursor.execute("SELECT tiktok FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '"+ str(account) +"', '', '', '', '', '', '', '', '')")
            db.commit()
            await message.send("TikTok Set!")
        else:
            cursor.execute("UPDATE socials SET tiktok = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("TikTok Set!")
    elif social == "snapchat":
        cursor.execute("SELECT snapchat FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '"+ str(account) +"', '', '', '', '', '', '', '')")
            db.commit()
            await message.send("Snapchat Set!")
        else:
            cursor.execute("UPDATE socials SET snapchat = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Snapchat Set!")
    elif social == "spotify":
        cursor.execute("SELECT spotify FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '', '"+ str(account) +"', '', '', '', '', '', '')")
            db.commit()
            await message.send("Spotify Set!")
        else:
            cursor.execute("UPDATE socials SET spotify = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Spotify Set!")
    elif social == "youtube":
        cursor.execute("SELECT youtube FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '', '', '"+ str(account) +"', '', '', '', '', '')")
            db.commit()
            await message.send("YouTube Set!")
        else:
            cursor.execute("UPDATE socials SET youtube = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("YouTube Set!")
    elif social == "twitch":
        cursor.execute("SELECT twitch FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '', '', '', '"+ str(account) +"', '', '', '', '')")
            db.commit()
            await message.send("Twitch Set!")
        else:
            cursor.execute("UPDATE socials SET twitch = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Twitch Set!")
    elif social == "steam":
        cursor.execute("SELECT steam FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '', '', '', '', '"+ str(account) +"', '', '', '')")
            db.commit()
            await message.send("Steam Set!")
        else:
            cursor.execute("UPDATE socials SET steam = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Steam Set!")
    elif social == "xbox":
        cursor.execute("SELECT xbox FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '', '', '', '', '', '"+ str(account) +"', '', '')")
            db.commit()
            await message.send("Xbox Set!")
        else:
            cursor.execute("UPDATE socials SET xbox = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Xbox Set!")
    elif social == "playstation":
        cursor.execute("SELECT playstation FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '', '', '', '', '', '', '"+ str(account) +"', '')")
            db.commit()
            await message.send("PlayStation Set!")
        else:
            cursor.execute("UPDATE socials SET playstation = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("PlayStation Set!")
    elif social == "reddit":
        cursor.execute("SELECT reddit FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        result = cursor.fetchone()
        if result == None:
            cursor.execute("INSERT INTO `socials` (`user_id`, `guild_id`, `twitter`, `instagram`, `tiktok`, `snapchat`, `spotify`, `youtube`, `twitch`, `steam`, `xbox`, `playstation`, `reddit`) VALUES ('" + str(userID) + "', '" + str(guildID) + "', '', '', '', '', '', '', '', '', '', '', '"+ str(account) +"')")
            db.commit()
            await message.send("Reddit Set!")
        else:
            cursor.execute("UPDATE socials SET reddit = '" + str(account) + "' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
            db.commit()
            await message.send("Reddit Set!")
    cursor.execute("SELECT used FROM commands WHERE name = 'set'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'set'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SetSocial -- {cupGuild} by {cupUser}")

@set.error
async def set_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please include a social media account name")
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# socials get
@bot.command(aliases= ['soc'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def socials(ctx, member: discord.Member=None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'socials'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    if member == None:
        userID = ctx.author.id
        userName = ctx.author.name
    else:
        userID = member.id
        userName = member.name
    try:
        cursor.execute("SELECT twitter FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        twitterUF = cursor.fetchmany()
        if twitterUF != None:
            for twitter1 in twitterUF:
                for twitter2 in twitter1:
                    if twitter2 == "":
                        twitter = "Not Set"
                    else:
                        twitter = twitter2

        cursor.execute("SELECT instagram FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        instagramUF = cursor.fetchmany()
        if instagramUF != None:
            for instagram1 in instagramUF:
                for instagram2 in instagram1:
                    if instagram2 == "":
                        instagram = "Not Set"
                    else:
                        instagram = instagram2

        cursor.execute("SELECT tiktok FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        tiktokUF = cursor.fetchmany()
        if tiktokUF != None:
            for tiktok1 in tiktokUF:
                for tiktok2 in tiktok1:
                    if tiktok2 == "":
                        tiktok = "Not Set"
                    else:
                        tiktok = tiktok2

        cursor.execute("SELECT snapchat FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        snapchatUF = cursor.fetchmany()
        if snapchatUF != None:
            for snapchat1 in snapchatUF:
                for snapchat2 in snapchat1:
                    if snapchat2 == "":
                        snapchat = "Not Set"
                    else:
                        snapchat = snapchat2

        cursor.execute("SELECT spotify FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        spotifyUF = cursor.fetchmany()
        if snapchatUF != None:
            for spotify1 in spotifyUF:
                for spotify2 in spotify1:
                    if spotify2 == "":
                        spotify = "Not Set"
                    else:
                        spotify = spotify2

        cursor.execute("SELECT youtube FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        youtubeUF = cursor.fetchmany()
        if youtubeUF != None:
            for youtube1 in youtubeUF:
                for youtube2 in youtube1:
                    if youtube2 == "":
                        youtube = "Not Set"
                    else:
                        youtube = youtube2

        cursor.execute("SELECT twitch FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        twitchUF = cursor.fetchmany()
        if twitchUF != None:
            for twitch1 in twitchUF:
                for twitch2 in twitch1:
                    if twitch2 == "":
                        twitch = "Not Set"
                    else:
                        twitch = twitch2

        cursor.execute("SELECT steam FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        steamUF = cursor.fetchmany()
        if steamUF != None:
            for steam1 in steamUF:
                for steam2 in steam1:
                    if steam2 == "":
                        steam = "Not Set"
                    else:
                        steam = steam2

        cursor.execute("SELECT xbox FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        xboxUF = cursor.fetchmany()
        if xboxUF != None:
            for xbox1 in xboxUF:
                for xbox2 in xbox1:
                    if xbox2 == "":
                        xbox = "Not Set"
                    else:
                        xbox = xbox2

        cursor.execute("SELECT playstation FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        playstationUF = cursor.fetchmany()
        if playstationUF != None:
            for playstation1 in playstationUF:
                for playstation2 in playstation1:
                    if playstation2 == "":
                        playstation = "Not Set"
                    else:
                        playstation = playstation2

        cursor.execute("SELECT reddit FROM socials WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        redditUF = cursor.fetchmany()
        if redditUF != "('',)":
            for reddit1 in redditUF:
                for reddit2 in reddit1:
                    if reddit2 == "":
                        reddit = "Not Set"
                    else:
                        reddit = reddit2

        embed = discord.Embed(title=f"{userName}'s Socials Profile", color=discord.Color.blue())
        embed.add_field(name="<:twitter:826679916078170132> Twitter:", value=twitter, inline=False)
        embed.add_field(name="<:instagram:826679941415960616> Instagram:", value=instagram, inline=False)
        embed.add_field(name="<:tiktok:826679851649073172> TikTok:", value=tiktok, inline=False)
        embed.add_field(name="<:snapchat:826679778861121566> Snapchat:", value=snapchat, inline=False)
        embed.add_field(name="<:spotify:826679972512137216> Spotify:", value=spotify, inline=False)
        embed.add_field(name="<:youtube:826679826386649110> YouTube:", value=youtube, inline=False)
        embed.add_field(name="<:twitch:826679714357182495> Twitch:", value=twitch, inline=False)
        embed.add_field(name="<:steam:826679805851205663> Steam:", value=steam, inline=False)
        embed.add_field(name="<:xbox:826679738679820338> Xbox:", value=xbox, inline=False)
        embed.add_field(name="<:playstation:826680220764340225> PlayStation:", value=playstation, inline=False)
        embed.add_field(name="<:reddit:826679760477618187> Reddit:", value=reddit, inline=False)

        await ctx.send(embed=embed)
    
    except:
        await ctx.send(f"{userName} has not added any social media's to their profile")

    cursor.execute("SELECT used FROM commands WHERE name = 'soc'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'soc'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Socials -- {cupGuild} by {cupUser}")

@socials.error
async def socials_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a user to get their socials profile")
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)
    
# delete socials
@bot.command(aliases= ['socdel'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def socialdelete(ctx, social):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'socialdelete'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userID = ctx.author.id
    guildID = ctx.guild.id
    
    if social == "twitter":
        cursor.execute("UPDATE socials SET twitter = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Twitter Removed")

    if social == "instagram":
        cursor.execute("UPDATE socials SET instagram = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Instagram Removed")

    if social == "tiktok":
        cursor.execute("UPDATE socials SET tiktok = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("TikTok Removed")
    
    if social == "snapchat":
        cursor.execute("UPDATE socials SET snapchat = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Snapchat Removed")

    if social == "spotify":
        cursor.execute("UPDATE socials SET spotify = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Spotify Removed")
    
    if social == "youtube":
        cursor.execute("UPDATE socials SET youtube = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("youtube Removed")
    
    if social == "twitch":
        cursor.execute("UPDATE socials SET twitch = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Twitch Removed")
    
    if social == "steam":
        cursor.execute("UPDATE socials SET steam = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Steam Removed")

    if social == "xbox":
        cursor.execute("UPDATE socials SET xbox = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Xbox Removed")

    if social == "playstation":
        cursor.execute("UPDATE socials SET playstation = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("PlayStation Removed")
    
    if social == "reddit":
        cursor.execute("UPDATE socials SET reddit = '' WHERE user_id = '" + str(userID) + "' AND guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Reddit Removed")
    cursor.execute("SELECT used FROM commands WHERE name = 'socdel'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'socdel'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SocialsDel -- {cupGuild} by {cupUser}")

@socialdelete.error
async def socialdelete_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please name a social media to remove from your profile")
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# supported socials
@bot.command(aliases= ['suso'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def supportedsocials(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'supportedsocials'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    embed = discord.Embed(title="Supported Social Media's", description="Twitter, Instagram, TikTok, Snapchat, Spotify, YouTube, Twitch, Steam, Xbox, PlayStation, Reddit",color=discord.Color.random())
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'suso'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'suso'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Suso -- {cupGuild} by {cupUser}")

@supportedsocials.error
async def supportedsocials_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# social help
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def socialshelp(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'socialshelp'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Socials Help", description="Socials is a system to display your social media's to everyone in the server", color=discord.Color.orange())
        embed.add_field(name=f"{pre}set [social media] [account name]", value="Add a social media to your socials profile", inline=False)
        embed.add_field(name=f"{pre}socials [user]", value=f"Get the socials profile for anyone in the server. Aliases: {pre}soc", inline=False)
        embed.add_field(name=f"{pre}socialdelete [social media]", value=f"Delete one of your social media's from your profile. Aliases: {pre}socdel", inline=False)
        embed.add_field(name=f"{pre}supportedsocials", value=f"See a list of the supported social media's. Aliases: {pre}suso", inline=False)
        await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'socialshelp'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'socialshelp'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SocialsHelp -- {cupGuild} by {cupUser}")

@socialshelp.error
async def socialshelp_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# counting stuff
# set channel
@bot.command(aliases=['secoca'])
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def setcountchannel(ctx, channel: discord.TextChannel):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'setcountchannel'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    channelID = channel.id
    cursor.execute("SELECT count FROM counting WHERE guild_id = '" + str(guildID) + "'")
    result = cursor.fetchone()
    if result == None:
        cursor.execute("INSERT INTO `counting` (`guild_id`, `channel_id`, `lastuser_id`, `count`, `highscore`) VALUES ('" + str(guildID) + "', '" + str(channelID) + "', '1', '1', '1')")
        db.commit()
        await ctx.send("Counting channel set")
    elif result != None: 
        cursor.execute("UPDATE counting SET channel_id = '" + str(channelID) + "' WHERE guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Counting channel updated. Count was not reset")
    cursor.execute("SELECT used FROM commands WHERE name = 'secoca'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'secoca'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Secoca -- {cupGuild} by {cupUser}")

@setcountchannel.error
async def setcountchannel_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a text channel to set")    
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use that command")
        elif isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
            await ctx.send(embed=embed)

# for actual counting function see line 1722

# counting rules
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def countrules(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'countrules'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Counting Rules", color=discord.Color.blue())
        embed.add_field(name="Don't count twice in a row:", value="If anyone counts twice in a row the count will be reset!", inline=False)
        embed.add_field(name="Don't mess it up:", value="If any user sends the wrong number, the count will be reset and they will experience a gret deal of grief and shame", inline=False)
        embed.set_footer(text=f"For more info about the game use {pre}countinfo")
        await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'socialshelp'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'countrules'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Countrules -- {cupGuild} by {cupUser}")

@countrules.error
async def countrules_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# counting info
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def countinfo(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'countinfo'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Counting Game Info",description="The counting game is a game where all you have to do is (in the specified channel) send the number that comes after the last number sent. *Example:* If I were to send **1** then Dox would send **2** and so on.", color=discord.Color.gold())
        embed.add_field(name=f"{pre}setcountchannel [channel]", value=f"Set a specified channel for the counting game (Must have the 'Administrator' permission). Alias: {pre}secoca", inline=False)
        embed.add_field(name=f"{pre}countrules", value="See all of the rules for the counting game", inline=False)
        embed.add_field(name=f"{pre}counthigh", value="See the highscore for your server", inline=False)
        embed.add_field(name=f"{pre}countchannel", value="Forgot the counting channel? Don't worry this command will remind you what it is", inline=False)
        embed.set_footer(text=f"For info about the rules use {pre}countrules")
        await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'countinfo'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'countinfo'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Countinfo -- {cupGuild} by {cupUser}")

@countinfo.error
async def countinfo_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# get count channel
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def countchannel(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'countchannel'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        guildID = ctx.guild.id
        cursor.execute("SELECT channel_id FROM counting WHERE guild_id =" + str(guildID))
        channelUF = cursor.fetchone()
        for coChan in channelUF:
            await ctx.send(f"The counting channel is <#{coChan}>")
    cursor.execute("SELECT used FROM commands WHERE name = 'countchannel'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'countchannel'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Countchannel -- {cupGuild} by {cupUser}")

@countchannel.error
async def countchannel_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# get high score
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def counthigh(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'counthigh'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    cursor.execute("SELECT highscore FROM counting WHERE guild_id = '" + str(guildID) + "'")
    highSUF = cursor.fetchone()
    for highS in highSUF:
        if highS == 1:
            highS -= 1
            await ctx.send(f"The highscore for this server is **{highS}**")
        else:
            highS -= 1
            await ctx.send(f"The highscore for this server is **{highS}**")
    cursor.execute("SELECT used FROM commands WHERE name = 'highscore'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'highscore'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Counthigh -- {cupGuild} by {cupUser}")

@counthigh.error
async def counthigh_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# Dad joke 
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def dadjoke(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'dadjoke'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userName = ctx.author
    dadjoke = Dadjoke()
    embed = discord.Embed(title=dadjoke.joke, color=discord.Color.random())
    embed.set_footer(text=f"Requested by: {userName}")
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'dadjoke'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'dadjoke'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Dadjoke -- {cupGuild} by {cupUser}")

@dadjoke.error
async def dadjoke_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# Affirmation command
@bot.command(aliases=['isad', 'aff'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def affirmation(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'affirmation'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    r = requests.get('https://www.affirmations.dev/')
    res = r.json()
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.affirmations.dev/') as r:
            res = await r.json()
            aff = res['affirmation']
            user = ctx.message.author.name
            embed = discord.Embed(title=aff, color = discord.Color.random())  
            embed.set_footer(text=f"Feel better {user}")
            await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'affirmation'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'affirmation'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Aff -- {cupGuild} by {cupUser}")

@affirmation.error
async def affirmation_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# translate command
@bot.command(aliases=['tr'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def translate(ctx, lang_to, *args):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'translate'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate text to")

    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text

    embed = discord.Embed(title=text_translated, description=text, color=discord.Color.green())
    embed.set_footer(text=f"{ctx.author} | Lang: {lang_to}")

    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'translate'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'translate'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Translate -- {cupGuild} by {cupUser}")

@translate.error
async def translate_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="That is not a supported language", description="Please click [Here](https://cloud.google.com/translate/docs/languages) for a list of supported languages and codes", color=discord.Color.red())
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"{ctx.author} \u200b")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# languages command
@bot.command(aliases=['sl', 'langs'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def languages(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'languages'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    embed = discord.Embed(title="Supported Languages", url="https://cloud.google.com/translate/docs/languages", description="Please click [Here](https://cloud.google.com/translate/docs/languages) for a list of supported languages and codes", color=discord.Color.random())
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{ctx.author} \u200b")
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'languages'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'languages'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Langs -- {cupGuild} by {cupUser}")

@languages.error
async def languages_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# say command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def say(ctx, *, message):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'say'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await ctx.send(f"{message} | **{ctx.author}**" .format(message))
    cursor.execute("SELECT used FROM commands WHERE name = 'say'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'say'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Say -- {cupGuild} by {cupUser}")

@say.error
async def say_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include something for DoxBot to say!")

# roast command
@bot.command(aliases=['insult'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def roast(ctx, *, member: discord.Member=None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'roast'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://insult.mattbas.org/api/insult.json') as r:
            res = await r.json(content_type=None)
            insult = res['insult']
            if member == None:
                embed1 = discord.Embed(title=insult, color=discord.Color.red())
                await ctx.send(embed=embed1)
            else:
                embed2 = discord.Embed(title=f"{member.name} {insult}", color=discord.Color.red())
                await ctx.send(embed=embed2)
    cursor.execute("SELECT used FROM commands WHERE name = 'roast'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'roast'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Roast -- {cupGuild} by {cupUser}")

@roast.error
async def roast_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# short url 
@bot.command(aliases=['surl'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def shorturl(ctx, url):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'shorturl'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    linkRequest = {
        "destination": url,
        "domain": { "fullName": "rebrand.ly" }
    }

    requestHeaders = {
        "Content-type": "application/json",
        "apikey": os.getenv('SURLAPI'),
    }

    r = requests.post("https://api.rebrandly.com/v1/links", 
        data = json.dumps(linkRequest),
        headers=requestHeaders)

    if (r.status_code == requests.codes.ok):
        link = r.json()
        embed = discord.Embed(title="Shortened URL", url="https://" + link["shortUrl"], color=discord.Color.random())
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"{ctx.author} \u200b")
        await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'shorturl'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'shorturl'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Surl -- {cupGuild} by {cupUser}")

@shorturl.error
async def shorturl_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a URL to shorten!")

# wanted
@bot.command()
@commands.cooldown(1,3,commands.BucketType.guild)
async def wanted(ctx, user: discord.Member=None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'wanted'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    if user == None:
        user = ctx.author
        userID = ctx.author.id
    else:
        user = user
        userID = user.id

    wanted = Image.open("wanted.jpg")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((177,177))

    wanted.paste(pfp, (120,212))
    wanted.save(f"profile{userID}.jpg")

    await ctx.send(file=discord.File(f"profile{userID}.jpg"))
    os.remove(f"profile{userID}.jpg")
    cursor.execute("SELECT used FROM commands WHERE name = 'wanted'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'wanted'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Wanted -- {cupGuild} by {cupUser}")

@wanted.error
async def wanted_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# qr code generator
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def qr(ctx, url):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'qr'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    embed = discord.Embed(title="Original URL", url=url)
    embed.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}")

    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'qr'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'qr'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"QR -- {cupGuild} by {cupUser}")

@qr.error
async def qr_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a URL for a QR code")

# hex code generator
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def rcolor(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'rcolor'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    levels = range(32,256,32)
    rgb = tuple(random.choice(levels) for _ in range(3))
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://www.thecolorapi.com/id?rgb=rgb{rgb}') as r:
            res = await r.json(content_type=None)

            hexC = res['hex']['value']
            hexClean = res['hex']['clean']
            hexURL = res['image']['bare']

            embed = discord.Embed(title=hexC, url=f"https://www.color-hex.com/color/{hexClean}")
            embed.set_image(url=f"https://singlecolorimage.com/get/{hexClean}/125x125")
            embed.set_footer(text=f"{ctx.author}")
            
            await ctx.send(embed=embed)  
            cursor.execute("SELECT used FROM commands WHERE name = 'rcolor'")
            used = cursor.fetchone()
            for num in used:
                num += 1
                cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'rcolor'")
                db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Rcolor -- {cupGuild} by {cupUser}")

@rcolor.error
async def rcolor_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# love tester
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def lovetest(ctx, member: discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'lovetest'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    identity = getIdentity()

    url = "https://love-calculator.p.rapidapi.com/getPercentage"

    querystring = {"fname":f"{member.name}","sname":f"{ctx.author.name}"}

    headers = {
        'x-rapidapi-key': os.getenv('LOVEAPI'),
        'x-rapidapi-host': "love-calculator.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    res = response.json()
    perc = res["percentage"]
    result = res["result"]

    embed = discord.Embed(title="Love Test", color=0xFF00D4)
    embed.add_field(name=result, value=f"Love %: **{perc}%**", inline=False)
    embed.set_footer(text=ctx.author)

    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'lovetest'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'lovetest'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Lovetest -- {cupGuild} by {cupUser}")

@lovetest.error
async def lovetest_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a user to test your love with them")

# today in history
@bot.command(aliases=['tih', 'datefact'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def todayinhistory(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'todayinhistory'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    today = date.today()
    d1 = today.strftime("%m/%d")
    
    url = f"https://numbersapi.p.rapidapi.com/{d1}/date"

    querystring = {"fragment":"false","json":"true"}

    headers = {
        'x-rapidapi-key': os.getenv('TODAYIHAPI'),
        'x-rapidapi-host': "numbersapi.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()

    fact = res['text']
    year = res['year']

    embed = discord.Embed(title="Today in History:", description=f"**In {year},** {fact}", color=discord.Color.random())
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{ctx.author} \u200b")

    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'todayinhistory'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'todayinhistory'")
      db.commit() 
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"TIH -- {cupGuild} by {cupUser}")  

@todayinhistory.error
async def todayinhistory_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# number facts
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def numfact(ctx, number):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'numfact'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    url = f"https://numbersapi.p.rapidapi.com/{number}/math"

    querystring = {"fragment":"false","json":"true"}

    headers = {
        'x-rapidapi-key': os.getenv('NUMFACTAPI'),
        'x-rapidapi-host': "numbersapi.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()

    fact = res['text']

    embed = discord.Embed(title="Number Fact:", description=f"**{number}**: {fact}", color=discord.Color.random())
    embed.set_footer(text=ctx.author)

    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'numfact'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'numfact'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Numfact -- {cupGuild} by {cupUser}")

@numfact.error
async def numfact_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a number to get a fact about it!")

# weather 
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def weather(ctx, location):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'weather'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q":f"{location} "}

    headers = {
        'x-rapidapi-key': os.getenv('WEATHERAPI'),
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()

    locName = res['location']['name']
    locReg = res['location']['region']
    locCoun = res['location']['country']
    tempC = res['current']['temp_c']
    tempF = res['current']['temp_f']
    cond = res['current']['condition']['text']
    iconURL = res['current']['condition']['icon']
    windMph = res['current']['wind_mph']
    windKph = res['current']['wind_kph']
    windDir = res['current']['wind_dir']
    humid = res['current']['humidity']
    cloud = res['current']['cloud']
    feelsC = res['current']['feelslike_c']
    feelsF = res['current']['feelslike_f']
    visKm = res['current']['vis_km']
    visM = res['current']['vis_miles']
    uv = res['current']['uv']

    embed = discord.Embed(title=f"Weather: {locName}, {locReg}, {locCoun}", color=discord.Color.blue())
    embed.set_thumbnail(url=f"https:{iconURL}")
    embed.add_field(name="Temp:", value=f"{tempC} ℃ / {tempF} ℉", inline=True)
    embed.add_field(name="Condition:", value=cond, inline=True)
    embed.add_field(name="Wind:", value=f"{windKph} Kmph / {windMph} Mph {windDir}", inline=True)
    embed.add_field(name="Feels Like:", value=f"{feelsC} ℃ / {feelsF} ℉", inline=True)
    embed.add_field(name="Humidity:", value=f"{humid}%", inline=True)
    embed.add_field(name="Cloud Cov:", value=f"{cloud}%", inline=True)
    embed.add_field(name="Visibility:", value=f"{visKm} Km / {visM} Mi", inline=True)
    embed.add_field(name="UV Index:", value=uv, inline=True)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{ctx.author} \u200b")

    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'weather'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'weather'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Weather -- {cupGuild} by {cupUser}")

@weather.error
async def weather_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That is not a valid location")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a location")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# notes system
# set notes command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def setnote(ctx, member: discord.Member, *, note):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'setnote'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    memberID = member.id
    guildID = ctx.guild.id
    modID = ctx.author.id

    # set unique note id
    noteIDIN = random.randint(100000, 999999)
    cursor.execute("SELECT note_id FROM notes")
    idCheck = cursor.fetchall()
    if noteIDIN == idCheck:
        noteIDIN = random.randint(100000, 999999)
    else:
        pass

    cursor.execute("SELECT note FROM notes WHERE user_id = '" + str(memberID) + "' AND guild_id = '" + str(guildID) + "'")
    result = cursor.fetchone()
    
    if result == None: # if user has no notes
        cursor.execute("INSERT INTO `notes` (`guild_id`, `user_id`, `mod_id`, `note_id`, `note`) VALUES ('" + str(guildID) + "', '" + str(memberID) + "', '" + str(modID) + "', '" + str(noteIDIN) + "', '" + str(note) + "')")
        db.commit()
        await ctx.send(f"Note set for **{member}**")
    
    else: # if user has notes
        # check if at note cap
        cursor.execute(f"SELECT GROUP_CONCAT(DISTINCT note SEPARATOR '##') FROM notes WHERE user_id = '{memberID}' AND guild_id = '{guildID}'")
        notesNumUF = cursor.fetchone()
        str6 = ''.join(notesNumUF)
        notesNum = str6
        notesNum_list = notesNum.split("##")
        numNotes = len(notesNum_list)
        
        if numNotes >= 10:
            await ctx.send(f"**{member}** Has reached the unique note limit (10 for now). Please use `deletenote [note id]` to remove a note!")

        elif numNotes <= 10:
            cursor.execute("INSERT INTO `notes` (`guild_id`, `user_id`, `mod_id`, `note_id`, `note`) VALUES ('" + str(guildID) + "', '" + str(memberID) + "', '" + str(modID) + "', '" + str(noteIDIN) + "', '" + str(note) + "')")
            db.commit()

            await ctx.send(f"Note set for **{member}**")

    cursor.execute("SELECT used FROM commands WHERE name = 'setnote'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'setnote'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Setnote -- {cupGuild} by {cupUser}")

@setnote.error
async def setnote_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please either include a user or a note to set")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# get notes command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def notes(ctx, member: discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'notes'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    memberID = member.id
    guildID = ctx.guild.id
    pfp = member.avatar_url
    # get note
    cursor.execute(f"SELECT GROUP_CONCAT(DISTINCT note SEPARATOR '##') FROM notes WHERE user_id = '{memberID}' AND guild_id = '{guildID}'")
    notesUF = cursor.fetchone()
    str = ''.join(notesUF)
    notes = str
    notes_list = notes.split("##")
    numNotes = len(notes_list)
    # get note id
    cursor.execute(f"SELECT GROUP_CONCAT(DISTINCT note_id SEPARATOR '##') FROM notes WHERE user_id = '{memberID}' AND guild_id = '{guildID}'")
    noteIDUF = cursor.fetchone()
    str2 = ''.join(noteIDUF)
    noteID = str2
    noteID_list = noteID.split("##")
    numNoteIDs = len(noteID_list)
    # get the mod id
    cursor.execute(f"SELECT GROUP_CONCAT(mod_id SEPARATOR '##') FROM notes WHERE user_id = '{memberID}' AND guild_id = '{guildID}'")
    modIDUF = cursor.fetchone()
    str3 = ''.join(modIDUF)
    modID = str3
    modID_list = modID.split("##")
    numModIDs = len(modID_list)
    # set up the embed
    embed = discord.Embed(title="Notes:", color=0xff6666)
    embed.set_author(name=f"{member} ID: {member.id}", icon_url=pfp)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{ctx.author} \u200b")
    embed.add_field(name=f"Note #{noteID_list[0]}", value=f"'{notes_list[0]}'  Mod: {await bot.fetch_user(modID_list[0])}", inline=True)
    try:
        embed.add_field(name=f"Note #{noteID_list[1]}", value=f"'{notes_list[1]}' Mod: {await bot.fetch_user(modID_list[1])}", inline=True)
        try:
            embed.add_field(name=f"Note #{noteID_list[2]}", value=f"'{notes_list[2]}' Mod: {await bot.fetch_user(modID_list[2])}", inline=True)
            try:
                embed.add_field(name=f"Note #{noteID_list[3]}", value=f"'{notes_list[3]}' Mod: {await bot.fetch_user(modID_list[3])}", inline=True)
                try:
                    embed.add_field(name=f"Note #{noteID_list[4]}", value=f"'{notes_list[4]}' Mod: {await bot.fetch_user(modID_list[4])}", inline=True)
                    try:
                        embed.add_field(name=f"Note #{noteID_list[5]}", value=f"'{notes_list[5]}' Mod: {await bot.fetch_user(modID_list[5])}", inline=True)
                        try:
                            embed.add_field(name=f"Note #{noteID_list[6]}", value=f"'{notes_list[6]}' Mod: {await bot.fetch_user(modID_list[6])}", inline=True)
                            try:
                                embed.add_field(name=f"Note #{noteID_list[7]}", value=f"'{notes_list[7]}' Mod: {await bot.fetch_user(modID_list[7])}", inline=True)
                                try:
                                    embed.add_field(name=f"Note #{noteID_list[8]}", value=f"'{notes_list[8]}' Mod: {await bot.fetch_user(modID_list[8])}", inline=True)
                                    try:
                                        embed.add_field(name=f"Note #{noteID_list[9]}", value=f"'{notes_list[9]}' Mod: {await bot.fetch_user(modID_list[9])}", inline=True)
                                        try:
                                            embed.add_field(name=f"Note #{noteID_list[10]}", value=f"'{notes_list[10]}' Mod: {await bot.fetch_user(modID_list[10])}", inline=True)
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                        except:
                            pass
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
    except:
        pass
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'notes'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'notes'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Notes -- {cupGuild} by {cupUser}")

@notes.error
async def notes_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user to get their notes")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# delete specific note
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def deletenote(ctx, noteID):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'deletenote'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    cursor.execute(f"DELETE FROM `notes` WHERE guild_id = '{guildID}' AND note_id = '{noteID}'")
    db.commit()
    await ctx.send(f"Deleted note #**{noteID}**")
    cursor.execute("SELECT used FROM commands WHERE name = 'deletenote'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'deletenote'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Deletenote -- {cupGuild} by {cupUser}")

@deletenote.error
async def deletenote_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a note ID. Use `notes [user]` to get note ID's")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# clear notes
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def clearnotes(ctx, member: discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'clearnotes'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    memberID = member.id
    guildID = ctx.guild.id
    if member == ctx.author and member != ctx.guild.owner:
        await ctx.send("You can't clear your own notes! Only the server owner can clear their own notes.")
    else:
        pass
    cursor.execute(f"DELETE FROM `notes` WHERE user_id = '{memberID}' AND guild_id = '{guildID}'")
    db.commit()
    await ctx.send(f"Cleared notes for **{member}**")
    cursor.execute("SELECT used FROM commands WHERE name = 'clearnotes'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'clearnotes'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"ClearNotes -- {cupGuild} by {cupUser}")

@clearnotes.error
async def clearnotes_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user to clear their notes")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# bot idea system
@bot.command(aliases=['bi'])
@commands.cooldown(1,1,commands.BucketType.guild)
async def botidea(ctx, *, idea):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'botidea'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    ideaChannel = bot.get_channel(801478447951249437)
    userID = ctx.author.id
    userName = ctx.author.name
    pfp = ctx.author.avatar_url
    # set unique note id
    ideaIDIN = random.randint(100000, 999999)
    cursor.execute("SELECT idea_id FROM userSuggestions")
    idCheck = cursor.fetchall()
    if ideaIDIN == idCheck:
        ideaIDIN = random.randint(100000, 999999)
    else:
        pass
    cursor.execute(f"INSERT INTO `userSuggestions` (`user_id`, `idea_id`, `idea`, `status`) VALUES ('{userID}', '{ideaIDIN}', '{idea}', 'Pending')")
    db.commit()
    embed1 = discord.Embed(title="User Suggested Idea", color=discord.Color.blurple())
    embed1.set_author(name=f"{userName} ID: {userID}", icon_url=pfp)
    embed1.add_field(name=f"Idea ID: #{ideaIDIN}", value=idea)
    await ideaChannel.send(embed=embed1)

    embed2 = discord.Embed(title="Thank you for your idea!", description="For updates on your suggestion, join the support server [HERE](https://discord.gg/zs7UwgBZb9)", color=discord.Color.green())
    await ctx.send(embed=embed2)
    cursor.execute("SELECT used FROM commands WHERE name = 'botidea'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'botidea'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Botidea -- {cupGuild} by {cupUser}")

@botidea.error
async def botidea_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commnads.MissingRequiredArgument):
        await ctx.send("Please incude an idea")

# bug report
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def bugreport(ctx, *, bug):
    bugChannel = bot.get_channel(834218634887954472)
    userID = ctx.author.id
    userName = ctx.author.name
    user = ctx.author
    pfp = ctx.author.avatar_url
    # set unique note id
    bugIDIN = random.randint(100000, 999999)
    cursor.execute("SELECT bug_id FROM bug_report")
    idCheck = cursor.fetchall()
    if bugIDIN == idCheck:
        bugIDIN = random.randint(100000, 999999)
    else:
        pass
    cursor.execute(f"INSERT INTO `bug_report` (`user_id`, `bug_id`, `bug`, `status`) VALUES ('{userID}', '{bugIDIN}', '{bug}', 'Active')")
    db.commit()
    embed1 = discord.Embed(title="User Bug Report:", color=discord.Color.red())
    embed1.set_author(name=f"{user} ID: {userID}", icon_url=pfp)
    embed1.add_field(name=f"Bug ID: #{bugIDIN}", value=bug)
    embed1.timestamp = datetime.datetime.utcnow()
    await bugChannel.send(embed=embed1)

    embed2 = discord.Embed(title="Thank you for reporting the bug!", description="For help join the support server [HERE](https://discord.gg/zs7UwgBZb9)", color=discord.Color.green())
    await ctx.send(embed=embed2)
    cursor.execute("SELECT used FROM commands WHERE name = 'bugreport'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'botidea'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Botidea -- {cupGuild} by {cupUser}")

@bugreport.error
async def bugreport_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please incude a bug")

# apporve
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def biapprove(ctx, ideaid, **reason):
    ideaChannel = bot.get_channel(801478447951249437)
    if reason == {}:
        reason = "None"
    else:
        reason = reason
    cursor.execute(f"SELECT idea_id FROM userSuggestions WHERE idea_id = '{ideaid}'")
    idCheckUF = cursor.fetchone()
    cursor.execute(f"SELECT status FROM userSuggestions WHERE idea_id = '{ideaid}'")
    statusCheckUF = cursor.fetchone()
    if idCheckUF == None:
        await ctx.send("That ID doesn't exist! Please check the ID and try again!")
    elif statusCheckUF != ('Pending',):
        await ctx.send("That idea has already been approved!")
    else:
        if ctx.author.id == owner_id:
            for idCheck in idCheckUF:
                cursor.execute(f"SELECT user_id FROM userSuggestions WHERE idea_id = '{ideaid}'")
                userIDUF = cursor.fetchone()
                for userID in userIDUF:
                    cursor.execute(f"SELECT idea FROM userSuggestions WHERE idea_id = '{ideaid}'")
                    ideaUF = cursor.fetchone()
                    for idea in ideaUF:
                        cursor.execute(f"UPDATE `userSuggestions` SET `status`= 'approved' WHERE `idea_id` = '{ideaid}'")
                        db.commit()
                        dm = await bot.fetch_user(userID)

                        dmEmbed = discord.Embed(title="Idea approved!", description=f"Idea: '{idea}' Reason **{reason}**", color=discord.Color.green())
                        dmEmbed.add_field(name="Congrats!", value="Your idea for DoxBot has been approved! Please join the [Support Server](https://discord.gg/zs7UwgBZb9) for further updates!")
                        
                        embed1 = discord.Embed(title="Idea Approved", description=f"Reason: {reason}", color=discord.Color.green())
                        embed1.add_field(name=f"Idea ID: #{ideaid}", value=f"Idea: '{idea}'")

                        await DMChannel.send(dm, embed=dmEmbed)
                        await ideaChannel.send(embed=embed1)
                        await ctx.send(f"Idea **#{ideaid}** has been approved!")

        else:
            await ctx.send("Only the bot owner (PapaRaG3#6969) can use that command!")

@biapprove.error
async def biapprove_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# idea deny
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def bideny(ctx, ideaid, *, reason):
    ideaChannel = bot.get_channel(801478447951249437)
    cursor.execute(f"SELECT idea_id FROM userSuggestions WHERE idea_id = '{ideaid}'")
    idCheckUF = cursor.fetchone()
    if idCheckUF == None:
        await ctx.send("That ID doesn't exist! Please check the ID and try again!")
    else:
        if ctx.author.id != owner_id:
            await ctx.send("Only the bot owner (PapaRaG3#6969) can use that command!")
        else:
            cursor.execute(f"SELECT user_id FROM userSuggestions WHERE idea_id = '{ideaid}'")
            userIDUF = cursor.fetchone()
            for userID in userIDUF:
                cursor.execute(f"SELECT idea FROM userSuggestions WHERE idea_id = '{ideaid}'")
                ideaUF = cursor.fetchone()
                for idea in ideaUF:
                    cursor.execute(f"DELETE FROM `userSuggestions` WHERE idea_id = '{ideaid}'")
                    db.commit()
                    dm = await bot.fetch_user(userID)

                    dmEmbed = discord.Embed(title="Idea Denied", description=f"Idea '{idea}'", color=discord.Color.red())
                    dmEmbed.add_field(name="Sorry", value=f"Your idea for DoxBot has been denied for the following reason: **{reason}** Please join the [Support Server](https://discord.gg/zs7UwgBZb9) for further updates!")

                    embed1 = discord.Embed(title="Idea Denied", description=f"Reason: {reason}", color=discord.Color.red())
                    embed1.add_field(name=f"Idea ID: #{ideaid}", value=f"Idea: '{idea}'")

                    await DMChannel.send(dm, embed=dmEmbed)
                    await ideaChannel.send(embed=embed1)
                    await ctx.send(f"Idea **{ideaid}** has been denied! Reason: **{reason}**")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Bideny -- {cupGuild} by {cupUser}")

@bideny.error
async def bideny_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# this person does not exist
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def doesntexist(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'doesntexist'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userID = ctx.author.id
    picture = await get_online_person() 
    from thispersondoesnotexist import save_picture
    await save_picture(picture, f"doesntexist_{userID}.jpeg")
    await ctx.send("This person does not exist:")
    await ctx.send(file=discord.File(f"doesntexist_{userID}.jpeg"))
    os.remove(f"doesntexist_{userID}.jpeg")
    cursor.execute("SELECT used FROM commands WHERE name = 'doesntexist'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'doesntexist'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Doesntexist -- {cupGuild} by {cupUser}")

@doesntexist.error
async def doesntexist_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

#sex command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def sex(ctx, member: discord.Member):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sex'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userID = member
    userName = member.name
    userMen = member.mention
    authMen = ctx.author.mention
    authName = ctx.author.name
    channel = ctx.channel

    no_list = [f"Sorry **{authName}**, **{userName}** hates your guts and wants you to die 😔", f"**{authName}** Turns out that **{userName}** drove their car off a cliff because the very thought of touching you was so horrid", f"Yikes. Don't worry, **{authName}** I'm sure it was just a misclick", f"**{authName}** Turns out that **{userName}** is actually sleeping with your dad... Yikes", f"**{authName}**, Well... **{userName}** said no, but dont worry I'll tickle your pickle pal!"]
    noRes = random.choice(no_list)

    yes_list = [f"Congrats **{authName}**, **{userName}** said yes! Now get to fuckin' you two!", f"Umm this has got to be a bug... **{userName}** said yes? No shot.", f"Everyone I'd like to formally announce that **{authName}** and **{userName}** are doin' the sex!", f"**{authName}**, **{userName}** said yes! Ah they grow up so fast. I remember when you used to put your lil tiny pp in your teddy bear", f"Well... **{userName}** did say yes but **{authName}** couldn't get it up. F"]
    yesRes = random.choice(yes_list)

    react = await channel.send(f"{userMen}, **{authName}** Wants to do the nasty with you... do you consent (You have 2 minutes to decide)")
    await react.add_reaction('✅')
    await react.add_reaction('❌')

    def check(reaction, user):
        return user == member and str(reaction.emoji) in ["✅", "❌"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=120, check=check)

            if str(reaction.emoji) == "✅":
                await channel.send(yesRes)
                break

            elif str(reaction.emoji) == "❌":
                await channel.send(noRes)
                break

            else:
                await message.remove_reaction(reaction, user)
    
        except asyncio.TimeoutError:
            await channel.send(f"Sorry, **{authName}**, **{userName}** didn't answer in time... Take that as a no, focus on yourself")
            break

    cursor.execute("SELECT used FROM commands WHERE name = 'sex'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'sex'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Sex -- {cupGuild} by {cupUser}")

@sex.error
async def sex_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a user to have sex with")

# word game
# set channel
@bot.command(aliases=['sewoch'])
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator = True)
async def setwordchan(ctx, channel: discord.TextChannel):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'setwordchan'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    chanID = channel.id
    cursor.execute(f"SELECT channel_id FROM wordGame WHERE guild_id = '{guildID}'")
    result = cursor.fetchone()
    if result == None:
        cursor.execute(f"INSERT INTO `wordGame` (`guild_id`, `channel_id`, `lastuser_id`, `lastletter`, `count`, `highscore`) VALUES ('{guildID}', '{chanID}', '1', '', '1', '1')")
        db.commit()
        await ctx.send("Word Game channel set")
    else:
        cursor.execute(f"UPDATE `wordGame` SET `guild_id`= {guildID},`channel_id`= {chanID},`lastuser_id`= 1, `count` = 1 WHERE guild_id = {guildID}")
        db.commit()
        await ctx.send("Word Game channel set")
    cursor.execute("SELECT used FROM commands WHERE name = 'setwordchan'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'setwordchan'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Sewoch -- {cupGuild} by {cupUser}")

@setwordchan.error
async def setwordchan_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please incude a channel")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# get channel
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def wordchan(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'wordchan'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    cursor.execute(f"SELECT channel_id FROM wordGame WHERE guild_id = '{guildID}'")
    channelUF = cursor.fetchone()
    if channelUF == None:
        await ctx.send("No channel has been set for the word game! Ask an admin to use `setwordchan [channel]`")
    else:
        for channel in channelUF:
            await ctx.send(f"The word game channel is <#{channel}>")
    cursor.execute("SELECT used FROM commands WHERE name = 'wordchan'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'wordchan'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Wordchan -- {cupGuild} by {cupUser}")

@wordchan.error
async def wordchan_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# get highscore
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def wordhigh(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'wordhigh'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    cursor.execute(f"SELECT highscore FROM wordGame WHERE guild_id = '{guildID}'")
    highUF = cursor.fetchone()
    for high in highUF:
        await ctx.send(f"The high score for this server is **{high}**")
    cursor.execute("SELECT used FROM commands WHERE name = 'wordhigh'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'wordhigh'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Wordhigh -- {cupGuild} by {cupUser}")

@wordhigh.error
async def wordhigh_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# word game info
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def wordinfo(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'wordinfo'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    embed = discord.Embed(title="Word Game Info", description="The word game is simple, in the designated channel (found with `wordchan`) one user will send a word then the next user will have to start their word with the last letter of the word before. Example: PapaRaG3: Dog DoxBot: God PapaRaG3: Dude. And so on", color=discord.Color.random())
    embed.add_field(name="Commands (for more info use `help [command]`)", value="`setwordchan [channel]`, `wordchan`, `wordhigh`")
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'wordinfo'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'wordinfo'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Wordinfo -- {cupGuild} by {cupUser}")

@wordinfo.error
async def wordinfo_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# command toggle system
# disable command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def disable(ctx, command):
    guildID = ctx.guild.id
    modID = ctx.author.id
    mod = ctx.author
    if command == "disable":
        await ctx.send("You can't disable the disable commnand silly")
    elif command == "enable":
        await ctx.send("You can't disable the enable command silly")
    elif command == "help":
        await ctx.send("You can't disable the help command silly")
    else:
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = '{command}'")
        cmdUF = cursor.fetchone()
        if cmdUF == None:
            cursor.execute(f"INSERT INTO `dis_cmds` (`guild_id`, `mod_id`, `command`) VALUES ('{guildID}', '{modID}', '{command}')")
            db.commit()
            await ctx.send(f"**{mod}** Disabled the **{command}** command")
        else:
            await ctx.send("That command is already disabled")
    cursor.execute("SELECT used FROM commands WHERE name = 'disable'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'disable'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Disable -- {cupGuild} by {cupUser}")

@disable.error
async def disable_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a command to disable")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# enable command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def enable(ctx, command):
    guildID = ctx.guild.id
    mod = ctx.author
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = '{command}'")
    cmdUF = cursor.fetchone()
    if cmdUF == None:
        await ctx.send("That command is already enabled")
    else:
        cursor.execute(f"DELETE FROM `dis_cmds` WHERE guild_id = {guildID} AND command = '{command}'")
        db.commit()
        await ctx.send(f"**{mod}** enabled the **{command}** command")
    cursor.execute("SELECT used FROM commands WHERE name = 'enable'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'enable'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Enable -- {cupGuild} by {cupUser}")

@enable.error
async def enable_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a command to enable")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# list disabled 
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def disabledcmds(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'disabledcmds'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    cursor.execute(f"SELECT GROUP_CONCAT(DISTINCT command SEPARATOR '##') FROM dis_cmds WHERE guild_id = '{guildID}'")
    cmdsUF = cursor.fetchall()
    for cmdsUF1 in cmdsUF:
        for cmds in cmdsUF1:
            str1 = ''.join(cmds)
            cmdsS = str1
            cmds_listUF = cmdsS.split("##")
            cmds_list = str(cmds_listUF)[1:-1]

            embed = discord.Embed(title="Server Disabled Commands", description=cmds_list, color=discord.Color.random())
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"{ctx.author} \u200b")

            await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'disabledcmds'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'disabledcmds'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Disabledcmds -- {cupGuild} by {cupUser}")

@disabledcmds.error
async def disabledcmds_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("There are no disabled commands for the server")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# economy stuff
# balance
@bot.command(aliases = ['bal'])
@commands.cooldown(1, 3, commands.BucketType.member)
async def balance(ctx, member: discord.Member = None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'balance'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    if member == None:
        user = ctx.author
        userID = ctx.author.id
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
        balUF = cursor.fetchone()
        if balUF == None:
            embed = discord.Embed(title=f"{user}'s Balance:", description=f"You have <:simp_coin:824720566241853460> **0** DXC", color=0xff6666)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            for bal in balUF:
                embed = discord.Embed(title=f"{user}'s Balance:", description=f"You have <:simp_coin:824720566241853460> **{bal}** DXC", color=0xff6666)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
    else:
        user = member
        userID = member.id
        react = await ctx.send(f"{member.mention} {ctx.author} Wants to see how many Dox Coins you have, is that ok? (You have 2 minutes to respond)")
        await react.add_reaction('✅')
        await react.add_reaction('❌')

        def check(reaction, user):
            return user == member and str(reaction.emoji) in ["✅", "❌"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=120, check=check)
                if user == bot.user:
                    break
                else:
                    if str(reaction.emoji) == "✅":
                        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
                        balUF = cursor.fetchone()
                        if balUF == None:
                            await ctx.send(f"{user.mention} Has **0** Dox Coins")
                        else:
                            for bal in balUF:
                                await ctx.send(f"{user.mention} Has **{bal}** Dox Coins")
                        break

                    elif str(reaction.emoji) == "❌":
                        await ctx.send(f"Sorry, **{ctx.author}**, **{user}** said no")
                        break

                    else:
                        await message.remove_reaction(reaction, user)
        
            except asyncio.TimeoutError:
                await ctx.send(f"Sorry, **{ctx.author.mention}**, **{user}** didn't answer in time")
                break
        pass
    cursor.execute("SELECT used FROM commands WHERE name = 'balance'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'balance'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Balance -- {cupGuild} by {cupUser}")

@balance.error
async def balance_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# beg
@bot.command()
@commands.cooldown(1, 120, commands.BucketType.member)
async def beg(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'beg'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    userID = ctx.author.id

    beg_list = ['I pity you *scoffs*', 'Yuck go take a shower', '"Be the sun in someones sky" *Im the sun mf*', "I only do this to feel good about myself", "I AM A GOD AMONGST MEN", "Ur kinda cute UwU", "Ugh I guess"]
    begRes = random.choice(beg_list)
    begNumRes = random.randint(1, 200)

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    if balUF == None:
        cursor.execute(f"INSERT INTO `econ` (`guild_id`, `user_id`, `coins`, `day_streak`, `fishpole_dura`) VALUES ('{guildID}', '{userID}', '{begNumRes}', '0', '50')")
        db.commit()

        embed = discord.Embed(title=begRes, description=f"Here's **{begNumRes}** coins", color=discord.Color.random())
        embed.set_footer(text=ctx.author)

        await ctx.send(embed=embed)
    else:
        for bal in balUF:
            bal += begNumRes

            cursor.execute(f"UPDATE `econ` SET `guild_id`={guildID},`user_id`={userID},`coins`={bal} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            
            embed = discord.Embed(title=begRes, description=f"Here's **{begNumRes}** coins", color=discord.Color.random())
            embed.set_footer(text=f"{ctx.author} | Bal: {bal} Dox Coins")

            await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'beg'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'beg'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Beg -- {cupGuild} by {cupUser}")

@beg.error
async def beg_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# daily 
@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.member)
async def daily(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'daily'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    userID = ctx.author.id

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()

    if balUF == None:
        cursor.execute(f"INSERT INTO `econ` (`guild_id`, `user_id`, `coins`, `day_streak`, `fishpole_dura`) VALUES ('{guildID}', '{userID}', '1000', '0', '50')")
        db.commit()

        embed = discord.Embed(title="Daily Dox Coins Collected", description="**1000** Coins have been deposited into your bank!", color=discord.Color.random())
        embed.set_footer(text=f"{ctx.author} | Bal: 1000 Coins")

        await ctx.send(embed=embed)
    
    else:
        for bal in balUF:
            bal += 1000

            cursor.execute(f"UPDATE `econ` SET `coins` = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()

            embed = discord.Embed(title="Daily Dox Coins Collected", description="**1000** Coins have been deposited into your bank!", color=discord.Color.random())
            embed.set_footer(text=f"{ctx.author} | Bal: {bal} Coins")

            await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'daily'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'daily'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Daily -- {cupGuild} by {cupUser}")

    
@daily.error
async def daily_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after / 3600
        embed = discord.Embed(title=f"{coolDownMsg}", description="You can do that in **{:.0f}** hours".format(cooldown))
        await ctx.send(embed=embed)

# fish
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.member)
async def fish(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'fish'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    
    guildID = ctx.guild.id
    userID = ctx.author.id

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    
    if balUF == None:
        cursor.execute(f"INSERT INTO `econ` (`guild_id`, `user_id`, `coins`, `day_streak`, `fishpole_dura`) VALUES ('{guildID}', '{userID}', '0', '0', '50')")
        db.commit()
        pass
    else:
        pass
    cursor.execute(f"SELECT fishingpole FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    fishPUF = cursor.fetchone()

    cursor.execute(f"SELECT fishpole_dura FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    fishPDuraUF = cursor.fetchone()
    for fishPDura in fishPDuraUF:
        pass

    if fishPUF == ('',):
        await ctx.send("You do not have a fishing pole! Use `shop` to buy one!")
        return
    elif fishPDura <= 0:
        cursor.execute(f"UPDATE `econ` SET `fishingpole` = '', `fishpole_dura` = 50 WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        await ctx.send("Your fishing pole is broken please purchase a new one with `shop`")
        return
    else:
        pass
    
    for fishPDura in fishPDuraUF:
        pass
    
    fish_list = ['Nothing','Nothing','Nothing','Nothing','Nothing','Nothing','Nothing','Nothing','Nothing','Nothing','Nothing','Nothing','Anchovy', 'Anchovy','Anchovy','Anchovy','Anchovy','Anchovy','Anchovy','Anchovy','Blue Tang', 'Blue Tang','Blue Tang','Blue Tang','Blue Tang','Blue Tang','Blue Tang','Blue Tang','Carp', 'Carp','Carp','Carp','Carp','Carp','Puffer Fish', 'Puffer Fish','Puffer Fish','Puffer Fish','Clown Fish', 'Clown Fish','Clown Fish','Clown Fish','Clown Fish','Clown Fish','Blowfish', 'Blowfish','Blowfish','Catfish', 'Catfish','Catfish','Boot','Boot','Boot','Boot','Boot','Boot','Boot','Boot','Boot','Boot','Boot','Boot','Treasure Chest']
    fish = random.choice(fish_list)

    if fish == 'Anchovy':
        weight = "1 oz"
        price = 15
        pass
    elif fish == 'Blue Tang':
        weight = "1.3 lbs"
        price = 40
        pass
    elif fish == 'Carp':
        weight = "5 lbs"
        price = 50
        pass
    elif fish == 'Puffer Fish':
        weight = "30 lbs"
        price = 200
        pass
    elif fish == 'Clown Fish':
        weight = "8 oz"
        price = 75
        pass
    elif fish == 'Blowfish':
        weight = "25 lbs"
        price = 175
        pass
    elif fish == 'Catfish':
        weight = "50 lbs"
        price = 300
        pass
    elif fish == 'Boot':
        weight = "5 lbs"
        price = 15
        pass
    elif fish == 'Treasure Chest':
        weight = "55 lbs"
        price = 1000
        pass
    elif fish == 'Nothing':
        for bal in balUF:
            bal -= 10
            fishPDura -= 2
            cursor.execute(f"UPDATE `econ` SET `coins` = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
            cursor.execute(f"UPDATE `econ` SET `fishpole_dura` = {fishPDura} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            embed = discord.Embed(title="You got nothin'", description=f"You lost **10** DXC in fishing fees. Durability: {fishPDura}")
            embed.set_footer(text=f"{ctx.author} | Bal: {bal} DXC")
            await ctx.send(embed=embed)
            return
    
    for bal in balUF:
        bal += price
        fishPDura -= 2
        cursor.execute(f"UPDATE `econ` SET `coins` = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
        cursor.execute(f"UPDATE `econ` SET `fishpole_dura` = {fishPDura} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()

        embed = discord.Embed(title="Got Something!", description=f"Fishing Pole Durability: {fishPDura}", color=0x0078ff)
        embed.add_field(name=f"You caught: {fish}", value=f"Price: **{price}** DXC | Weight: {weight}", inline=False)
        embed.set_footer(text=f"{ctx.author} | Bal: {bal} DXC")

        await ctx.send(embed=embed)
    
    cursor.execute("SELECT used FROM commands WHERE name = 'fish'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'fish'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Fish -- {cupGuild} by {cupUser}")

@fish.error
async def fish_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# shop command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def shop(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'shop'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userID = ctx.author.id
    guildID = ctx.guild.id
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    if balUF == None:
        bal = 0
        pass
    else:
        pass
    for bal in balUF:
        for pre in prefix:
            embed = discord.Embed(title="DoxBot Shop", description=f"To purchase, do `{pre}buy [number]`. Example: `{pre}buy 1`. DXC = Dox Coin", color=0x057e57)
            embed.add_field(name="1. Fishing Pole - 500 DXC", value=f"The fishing pole is required to be able to use the `{pre}fish` command. `{pre}buy 1`", inline=False)
            embed.add_field(name="2. Wood Pickaxe - 100 DXC", value=f"The most basic of pickaxes to use the `{pre}mine` commnad. `{pre}buy 2`", inline=False)
            embed.add_field(name="3. Stone Pickaxe - 200 DXC", value=f"A marginally better pickaxe to use the `{pre}mine` commnad. `{pre}buy 3`", inline=False)
            embed.add_field(name="4. Iron Pickaxe - 300 DXC", value=f"A solid pickaxe to use the `{pre}mine` commnad. `{pre}buy 4`", inline=False)
            embed.add_field(name="5. Gold Pickaxe - 400 DXC", value=f"A pretty damn sturdy pickaxe to use the `{pre}mine` commnad. `{pre}buy 5`", inline=False)
            embed.add_field(name="6. Diamond Pickaxe - 650 DXC", value=f"The best pickaxe money can buy to use the `{pre}mine` commnad. `{pre}buy 6`", inline=False)
            embed.set_footer(text=f"{ctx.author} | Bal: {bal} DXC")
            await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'shop'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'shop'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Shop -- {cupGuild} by {cupUser}")

@shop.error
async def shop_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# buy commands
@bot.group(name='buy', invoke_without_command=True)
@commands.cooldown(1,1,commands.BucketType.guild)
async def buy_cmd(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'buy'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await ctx.send("Please use a shop number to buy an item. `shop` for items")
    cursor.execute("SELECT used FROM commands WHERE name = 'buy'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'buy'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Buy -- {cupGuild} by {cupUser}")

@buy_cmd.command(name='1')
async def one_subcom(ctx):
    userID = ctx.author.id
    guildID = ctx.guild.id
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    cursor.execute(f"SELECT fishingpole FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    fspl = cursor.fetchone()
    for bal in balUF:
        pass
    if bal >= 500:
        if fspl == None or fspl == ('',):
            bal -= 500
            cursor.execute(f"UPDATE `econ` SET `fishingpole` = 'Yes', `coins` = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.send(f"Purchased a **Fishing Pole!** Updated balance: **{bal}** DXC")
            return
        else:
            await ctx.send(f"You already have a fishing pole!")
    elif bal < 500:
        await ctx.send(f"You do not have enough Dox Coins! Balance: **{bal}** DXC")
    print(f"Buy 1 -- {cupGuild} by {cupUser}")

# gift 
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.member)
async def gift(ctx, user: discord.User, coins: int):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'gift'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    userID = user.id
    authID = ctx.author.id
    guildID = ctx.guild.id
    authMen = ctx.author.mention
    userMen = user.mention
    auth = ctx.author

    if userID == authID:
        await ctx.send("You can't gift yourself Dox Coins dummy")
        return
    else:
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {authID}")
        authBalUF = cursor.fetchone()
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
        userBalUF = cursor.fetchone()

        if authBalUF == None:
            await ctx.send(f"{authMen} You don't have enough Dox Coins. Balance: **0**")
            return
        else:
            for authBal in authBalUF:
                if userBalUF == None:
                    await ctx.send(f"{userMen} Has no DXC in their account! Please use `daily` to claim coins and proceed with the transaction!")
                    return
                else:
                    for userBal in userBalUF:
                        pass
                    if authBal < coins:
                        await ctx.send(f"{authMen} You don't have enough coins to do that! Balance: **{authBal}** DXC")
                        return
                    elif authBal >= coins:
                        react = await ctx.send(f"{authMen} are you sure you want to give {userMen} **{coins}** DXC? (You have 2 mins to answer)")
                        await react.add_reaction('✅')
                        await react.add_reaction('❌')
                        def check(reaction, user):
                            return user == auth and str(reaction.emoji) in ["✅", "❌"]
                        while True:
                            try:
                                reaction, user = await bot.wait_for("reaction_add", timeout=120, check=check)
                                if user == bot.user:
                                    break
                                else:
                                    if str(reaction.emoji) == "✅":
                                        userBal += coins
                                        authBal -= coins

                                        cursor.execute(f"UPDATE `econ` SET `coins` = {userBal} WHERE guild_id = {guildID} AND user_id = {userID}")
                                        cursor.execute(f"UPDATE econ SET coins = {authBal} WHERE guild_id = {guildID} AND user_id = {authID}")
                                        db.commit()
                                        db.commit()
                                    
                                        await ctx.send(f"Successfully transfered **{coins}** DXC from {authMen} to {userMen}")
                                        break

                                    elif str(reaction.emoji) == "❌":
                                        await ctx.send(f"Transaction Canceled.")
                                        break

                                    else:
                                        await message.remove_reaction(reaction, user)
                            
                            except asyncio.TimeoutError:
                                await ctx.send(f"Transaction Canceled. **{auth}** Didn't answer in time")
                                break
    cursor.execute("SELECT used FROM commands WHERE name = 'gift'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'gift'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Gift -- {cupGuild} by {cupUser}")

@gift.error
async def gift_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You forgot to either mention a user or include an amount! Syntax: gift [user] [amount]")

# high low
@bot.command(aliases=['hl'])
@commands.cooldown(1, 15, commands.BucketType.member)
async def highlow(ctx):
    AguildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {AguildID} AND command = 'highlow'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    global num
    num = random.randint(0, 100)
    global hint
    hint = random.randint(0, 100)
    global earn
    earn = random.randint(20, 200)
    global guildID
    guildID = ctx.guild.id
    global userID
    userID = ctx.author.id

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    global balUF
    balUF = cursor.fetchone()

    embed = discord.Embed(title=f"Higher / Lower | Hint: {hint}", description=f"A random number between 1 and 100 has been chosen. Your hint is **{hint}**. Chose one of the buttons below, higher if the number is higher than the hint, lower if the number is lower than the hint, or equal if the number is equal to the hint.")
    global message
    message = await buttons.send(
        embed = embed,
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "Higher",
                    style = ButtonType().Secondary,
                    custom_id = "HL_b1",
                ),
                Button(
                    label = "Lower", 
                    style = ButtonType().Secondary,
                    custom_id = "HL_b2",
                ),
                Button(
                    label = "Equal",
                    style = ButtonType().Secondary,
                    custom_id = "HL_b3",
                )
            ])
        ]
    )
    cursor.execute("SELECT used FROM commands WHERE name = 'highlow'")
    used = cursor.fetchone()
    for numU in used:
      numU += 1
      cursor.execute("UPDATE commands SET used = '" + str(numU) + "' WHERE name = 'highlow'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Highlow -- {cupGuild} by {cupUser}")

@buttons.click
async def HL_b1(ctx):
    if num > hint:
        for bal in balUF:
            bal += earn
            cursor.execute(f"UPDATE econ SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.reply(f"**Higher Lower:** Congrats! The number was **{num}**, you earned **{earn} DXC** and your new balance is **{bal} DXC**")
            pass
    else:
        await ctx.reply(f"**Higher Lower:** Nope! The number was **{num}**")
        pass
    await ctx.message.delete()

@buttons.click
async def HL_b2(ctx):
    if num < hint:
        for bal in balUF:
            bal += earn
            cursor.execute(f"UPDATE econ SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.reply(f"**Higher Lower:** Congrats! The number was **{num}**, you earned **{earn} DXC** and your new balance is **{bal} DXC**")
            pass
    else:
        await ctx.reply(f"**Higher Lower:** Nope! The number was **{num}**")
        pass
    await ctx.message.delete()

@buttons.click
async def HL_b3(ctx):
    if num == hint:
        for bal in balUF:
            bal += earn
            cursor.execute(f"UPDATE econ SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.reply(f"**Higher Lower:** Congrats! The number was **{num}**, you earned **{earn} DXC** and your new balance is **{bal} DXC**")
            pass
    else:
        await ctx.reply(f"**Higher Lower:** Nope! The number was **{num}**")
        pass
    await ctx.message.delete()

@highlow.error
async def highlow_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# richest
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def richest(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'richest'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    userID = ctx.author.id
    guildName = ctx.guild.name

    cursor.execute(f"SELECT MAX(coins) FROM econ WHERE guild_id = {guildID}")
    coinsUF = cursor.fetchone()

    if coinsUF == None:
        coins = 0
        await ctx.send("No one in this server has any Dox Coins")
        return
    elif coinsUF != None:
        for coins in coinsUF:
            cursor.execute(f"SELECT user_id FROM econ WHERE coins = {coins} AND guild_id = {guildID}")
            richUserUF = cursor.fetchone()
            for richUser in richUserUF:
                userRich = richUser
                embed = discord.Embed(title=f"Richest User in {guildName}", description=f"**<:simp_coin:824720566241853460> {coins} DXC** - <@{userRich}>", color=discord.Color.gold())
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f"{ctx.author} \u200b")
                await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'richest'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'richest'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Richest -- {cupGuild} by {cupUser}")

@richest.error
async def richest_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# slot machines
@bot.command(aliases=['slot', 'slotmachine'])
@commands.cooldown(1, 3, commands.BucketType.member)
async def slots(ctx, amount: int):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'slots'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    userID = ctx.author.id
    userName = ctx.author

    if amount < 10:
        await ctx.send("You must bet at least **10** DXC")
        return
    else:
        pass

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balCheckUF = cursor.fetchone()

    if balCheckUF == None:
        await ctx.send("You have no Dox Coins to bet!")
        return
    else:
        for balCheck in balCheckUF:
            pass

    if balCheck < amount:
        await ctx.send(f"You don't have {amount} DXC! You have **{balCheck}** DXC")
        return
    else:
        pass

    emoji_list = ['🎉','💎','🏆','💯','👖','🛒']
    emoji1 = random.choice(emoji_list)
    emoji2 = random.choice(emoji_list)
    emoji3 = random.choice(emoji_list)
    
    win = 1

    if emoji1 == emoji2 and emoji3 == emoji1:
        win = 3
    
    if emoji1 == emoji2 and emoji3 != emoji1:
        win = 2
    
    if emoji2 == emoji3 and emoji1 != emoji2:
        win = 2

    if win == 3:
        embed = discord.Embed(title=f"{userName}'s Slots", description=f"**>** {emoji1} {emoji2} {emoji3} **<**", color=discord.Color.gold())
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
        balUF = cursor.fetchone()
        for bal in balUF:
            pass
        coins = amount * 3
        bal += coins
        cursor.execute(f"UPDATE `econ` SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        embed.add_field(name="Jackpot!", value=f"Winnings: {coins}")
        embed.set_footer(text=f"{ctx.author} | Bal: {bal} DXC")
        pass

    elif win == 2:
        embed = discord.Embed(title=f"{userName}'s Slots", description=f"**>** {emoji1} {emoji2} {emoji3} **<**", color=discord.Color.green())
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
        balUF = cursor.fetchone()
        for bal in balUF:
            pass
        coins = amount * 1.5
        bal += coins
        cursor.execute(f"UPDATE `econ` SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        embed.add_field(name="You won!", value=f"Winnings: {coins}")
        embed.set_footer(text=f"{ctx.author} | Bal: {bal} DXC")
        pass

    elif win == 1:
        embed = discord.Embed(title=f"{userName}'s Slots", description=f"**>** {emoji1} {emoji2} {emoji3} **<**", color=discord.Color.red())
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
        balUF = cursor.fetchone()
        for bal in balUF:
            pass
        bal -= amount
        cursor.execute(f"UPDATE `econ` SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        embed.add_field(name="You lost!", value=f"Losings: {amount}")
        embed.set_footer(text=f"{ctx.author} | Bal: {bal} DXC")
        pass
    
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'slots'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'slots'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Slots -- {cupGuild} by {cupUser}")


@slots.error
async def slot_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include an amount of coins to gamble!")

# rock paper sissors
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.member)
async def rps(ctx, amount: int, move):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'rps'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    userID = ctx.author.id
    userName = ctx.author.name
    user = ctx.author

    if amount < 10:
        await ctx.send("Please bet more than 10 coins!")
        return
    elif amount > 5000:
        await ctx.send("Please bet less than 5000 coins!")
        return
    else:
        pass

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()

    if balUF == None:
        await ctx.send("You don't have any Dox Coins, please use `daily` to get some!")
        return
    
    else:
        for bal in balUF:
            pass

    if amount > bal:
        await ctx.send(f"You don't have {amount} coins! Balance **{bal}** DXC")
        return
    else:
        pass

    opMove_list = [':rock:', '📄', '✂️']
    opMove = random.choice(opMove_list)

    if move == "rock" or move == "Rock":
        move = ':rock:'
    elif move == "paper" or move == "Paper":
        move = "📄"
    elif move == "scissors" or move == "Scissors":
        move = "✂️"
    else:
        await ctx.send("That is not a valid play. Please use 'rock', 'paper', or 'scissors'")
        return

    res = 0

    if move == opMove:
        res = 1
        pass
    elif move == ":rock:" and opMove == "📄":
        res = 2
        pass
    elif move == ":rock:" and opMove == "✂️":
        res = 3
        pass
    elif move == "📄" and opMove == ":rock:":
        res = 4
        pass
    elif move == "📄" and opMove == "✂️":
        res = 5
        pass
    elif move == "✂️" and opMove == ":rock:":
        res = 6
        pass
    elif move == "✂️" and opMove == "📄":
        res = 7
        pass

    if res == 1:
        desc = f"**{userName}** Plays {move}\nDoxBot Plays {opMove}\n\nThat's a Tie! You didn't lose any coins!"
        color = discord.Color.blurple()
        pass
    elif res == 2 or res == 5 or res == 6:
        bal -= amount
        cursor.execute(f"UPDATE econ SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        desc = f"**{userName}** Plays {move}\nDoxBot Plays {opMove}\n\n**DoxBot** won! You lost **{amount}** DXC!"
        color = discord.Color.red()
        pass
    elif res == 3 or res == 4 or res == 7:
        bal += amount
        cursor.execute(f"UPDATE econ SET coins = {bal} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        desc = f"**{userName}** Plays {move}\nDoxBot Plays {opMove}\n\n**{userName}** won! You got **{amount}** DXC!"
        color = discord.Color.green()
        pass

    embed = discord.Embed(title="Rock Paper Sissors", description=desc, color=color)
    embed.set_footer(text=f"{user} | Bal: {bal} DXC")
    await ctx.send(embed=embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'rps'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'rps'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"RPS -- {cupGuild} by {cupUser}")

@rps.error
async def rps_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include an amount of coins to gamble or a play!")

# rob stuff
@bot.command()
@commands.cooldown(1, 172800, commands.BucketType.member)
async def rob(ctx, user: discord.User):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'rob'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    victID = user.id
    vict = user
    authID = ctx.author.id
    auth =  ctx.author
    percent_take = random.randint(1,25) / 100
    success_perc = random.randint(1,100)
    criminals = 1
    bail_perc = random.randint(5, 25) / 100

    #check if vict is auth
    if vict == auth:
        await ctx.send("You can't rob yourself dumbass")
        return
    else:
        pass

    # check if victim has any coins in the first place
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {victID}")
    victBalUF = cursor.fetchone()
    if victBalUF == None or victBalUF == ('',):
        await ctx.send(f"**{user}** has no DXC so you can't rob them (broke bitch)")
        return
    else:
        for victBal in victBalUF:
            pass

    # allow additional members to join
    #await ctx.send(f"Heist started! Type **'join heist'** to join in! You have 1 minute to join. **{auth}** You do not need to join you are already in!")

    #def check(m):
        #return m.content == 'join heist' and m.channel == ctx.channel

    #while True:
        #try:
            #msg = await ('message', timeout=60.0, check=check)
        #except asyncio.TimeoutError:
            #await ctx.send(f'Heist started with **{criminals}** criminals')
            #break
        #else:
            #try:
                #criminals += 1
                #await ctx.send(f'**{msg.author}** joined the heist')
            #except asyncio.TimeoutError:
                #await ctx.send(f"Heist started with **{criminals}** criminals")
                #break

    take = round(victBal * percent_take, 0)

    if criminals == 1: 
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {authID}")
        crimBalUF = cursor.fetchone()
        for crimBal in crimBalUF:
            take * .5
            if success_perc >= 1 and success_perc <= 35:
                success = True
                pass
            else:
                success = False
                pass
            if success == True:
                crimBalIn = round(crimBal + take, 0) 
                victBalIn = round(victBal - take, 0)
                cursor.execute(f"UPDATE econ SET coins = {crimBalIn} WHERE guild_id = {guildID} AND user_id = {authID}")
                cursor.execute(f"UPDATE econ SET coins = {victBalIn} WHERE guild_id = {guildID} AND user_id = {victID}")
                db.commit()
                sucEmbed = discord.Embed(title="The Robbery Was a Success!", description=f"{auth.mention} got away with **{take}** DXC and {vict.mention} lost **{take}** DXC!", color=discord.Color.green())
                await ctx.send(embed=sucEmbed)
                pass
            elif success == False:
                bail_cost = round(crimBal * bail_perc, 0)
                crimBal -= bail_cost
                cursor.execute(f"UPDATE econ SET coins = {crimBal} WHERE guild_id = {guildID} AND user_id = {authID}")
                db.commit()
                failEmbed = discord.Embed(title="The Robbery Was a Failure!", description=f"{auth.mention} was arrested and had to pay **{bail_cost}** DXC", color=discord.Color.red())
                await ctx.send(embed=failEmbed)
                pass
    #elif criminals > 1:
        #take / criminals
        #if criminals == 2:
            #if success_perc >= 1 and success_perc <= 20:
                #success = True
                #pass
            #else:
                #success = False
                #pass

    cursor.execute("SELECT used FROM commands WHERE name = 'rob'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'rob'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Rob -- {cupGuild} by {cupUser}")

@rob.error
async def rob_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after / 3600
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f} hour(s)".format(cooldown))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include someone to rob!")

# owner add coins
@bot.group(name='coins', invoke_without_command=True)
async def coins_cmd(ctx):
    authID = ctx.author.id
    if authID != owner_id:
        return
    else:
        await ctx.send('add [user] [amount]  |  remove [user] [amount]')

# owner add coins to user
@coins_cmd.command(name='add')
async def coinadd_subcom(ctx, amount: int, user: discord.User=None):
    if ctx.author.id != owner_id:
        return
    else:
        pass

    if user == None:
        user = ctx.author
        pass
    else:
        user = user
        pass

    guildID = ctx.guild.id
    userID = user.id

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balCheckUF = cursor.fetchone()
    if balCheckUF == None or balCheckUF == ('',):
        cursor.execute(f"INSERT INTO `econ` (`guild_id`, `user_id`, `coins`) VALUES ('{guildID}', '{userID}', '{amount}')")
        db.commit()
        await ctx.send(f"Successfully gave {user.mention} **{amount}** DXC")
        pass
    else:
        for balCheck in balCheckUF:
            balCheck += amount
            cursor.execute(f"UPDATE econ SET coins = {balCheck} WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.send(f"Successfully gave {user.mention} **{amount}** DXC")
            pass

# owner remove coins from user
@coins_cmd.command(name='remove')
async def coinrem_subcom(ctx, amount: int, user: discord.User=None):
    if ctx.author.id != owner_id:
        return
    else:
        pass

    if user == None:
        user = ctx.author
        pass
    else:
        user = user
        pass

    guildID = ctx.guild.id
    userID = user.id

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balCheckUF = cursor.fetchone()
    if balCheckUF == None or balCheckUF == ('',):
        await ctx.send(f"{user.mention} Has **0** DXC so you can't take any away")
    else:
        for balCheck in balCheckUF:
            if amount > balCheck:
                await ctx.send(f"{user.mention} only has **{balCheck}** DXC so you can't take that much")
                return
            else:
                balCheck -= amount
                cursor.execute(f"UPDATE econ SET coins = {balCheck} WHERE guild_id = {guildID} AND user_id = {userID}")
                db.commit()
                await ctx.send(f"Successfully removed **{amount}** DXC from {user.mention}")
                pass

# starboard
# set chan
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def setstarboard(ctx, channel: discord.TextChannel):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'setstarboard'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    chanID = channel.id

    cursor.execute(f"SELECT channel_id FROM starboard WHERE guild_id = {guildID}")
    chanCheckUF = cursor.fetchone()

    if chanCheckUF == None:
        cursor.execute(f"INSERT INTO `starboard` (`guild_id`, `channel_id`, `thresh`, `high_user_id`, `high_num`, `high_url`) VALUES ('{guildID}', '{chanID}', '5', '', '', '')")
        db.commit()
        pass
    elif chanCheckUF != None:
        for chanCheck in chanCheckUF:
            cursor.execute(f"UPDATE starboard SET channel_id = {chanID}, thresh = 5 WHERE guild_id = {guildID}")
            db.commit()
            pass

    await ctx.send(f"Set Starboard to <#{chanID}>, the star threshold is set to 5 stars, to change the threshold use `starthresh [num]`")
    channel = bot.get_channel(chanID)
    await channel.send("This channel has been set as a Starboard")

    cursor.execute("SELECT used FROM commands WHERE name = 'setstarboard'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'setstarboard'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Setstarboard -- {cupGuild} by {cupUser}")

@setstarboard.error
async def setstarboard_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a text channel")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# set thresh
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def starthresh(ctx, thresh: int):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'starthresh'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id

    cursor.execute(f"SELECT channel_id FROM starboard WHERE guild_id = {guildID}")
    chanCheckUF = cursor.fetchone()

    if chanCheckUF == None:
        await ctx.send("A starboard channel has not been set! Please use `setstarboard`")
        return
    else:
        cursor.execute(f"UPDATE starboard SET thresh = {thresh} WHERE guild_id = {guildID}")
        db.commit()
        await ctx.send(f"Set Starboard threshold to **{thresh}**")

    cursor.execute("SELECT used FROM commands WHERE name = 'starthresh'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'starthresh'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Starthresh -- {cupGuild} by {cupUser}")

@starthresh.error
async def starthresh_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a number!")
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# detect react
@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "⭐":

        guildID = reaction.message.guild.id
        userID = reaction.message.author.id
        channelID = reaction.message.channel.id
        msgID = reaction.message.id
        msgUrl = f"https://discord.com/channels/{guildID}/{channelID}/{msgID}"
        starCount = reaction.count
        msgCont = reaction.message.content
        channelIn = bot.get_channel(channelID)
        pfp = reaction.message.author.avatar_url
        user = reaction.message.author

        cursor.execute(f"SELECT channel_id FROM starboard WHERE guild_id = {guildID}")
        starChanUF = cursor.fetchone()

        if starChanUF == None:
            return
        
        else:
            for starChanID in starChanUF:
                starChan = bot.get_channel(starChanID)
        
        cursor.execute(f"SELECT thresh FROM starboard WHERE guild_id = {guildID}")
        threshUF = cursor.fetchone()
        for thresh in threshUF:
            pass

        embed = discord.Embed(description=f"{msgCont}", color=discord.Color.gold())
        embed.set_author(name=f"{user}", icon_url=pfp)
        embed.timestamp = datetime.datetime.utcnow()

        if reaction.message.attachments == []:
            pass

        elif reaction.message.attachments != []:
            msgAt = reaction.message.attachments[0]
            msgAttachUrl = msgAt.url
            embed.set_image(url=msgAttachUrl)
        
        embed.add_field(name="Jump", value=f"[Here]({msgUrl})", inline=False)

        if starCount == thresh:
            global starTell
            starTell = await starChan.send(f"⭐ **{starCount}** in {channelIn.mention}")
            await starChan.send(embed=embed)
        
        elif starCount > thresh:
            await starTell.edit(content=f"⭐ **{starCount}** in {channelIn.mention}")
        
        cursor.execute(f"SELECT high_num FROM starboard WHERE guild_id = {guildID}")
        highStarUF = cursor.fetchone()

        for highStar in highStarUF:
            pass
        
        if starCount > highStar:
            cursor.execute(f"UPDATE starboard SET high_user_id = {userID}, high_num = {starCount}, high_url = '{msgUrl}' WHERE guild_id = {guildID}")
            db.commit()

# get highest star
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def highstar(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'highstar'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    guildName = ctx.guild.name

    cursor.execute(f"SELECT high_user_id FROM starboard WHERE guild_id = {guildID}")
    highUserUF = cursor.fetchone()

    for highUser in highUserUF:
        pass

    if highUser == 0:
        await ctx.send("A starboard has not been set up in this server, or no one has starred any messages")
        return
    else:
        pass

    cursor.execute(f"SELECT high_num FROM starboard WHERE guild_id = {guildID}")
    starHighUF = cursor.fetchone()

    for starHigh in starHighUF:
        pass

    cursor.execute(f"SELECT high_url FROM starboard WHERE guild_id = {guildID}")
    highUrlUF = cursor.fetchone()

    for highUrl in highUrlUF:
        pass
    
    embed = discord.Embed(title=f"Highest Stars in {guildName}", description=f"⭐ **{starHigh}** by <@{highUser}> | Link: [Here]({highUrl})", color=discord.Color.gold())

    await ctx.send(embed=embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'highstar'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'highstar'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Highstar -- {cupGuild} by {cupUser}")

@highstar.error
async def highstar_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# server stats
# setup
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def statsetup(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'statsetup'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    totalCount = len(ctx.guild.members) 
    humanCount = len([m for m in ctx.guild.members if not m.bot])
    botCount = totalCount - humanCount

    cursor.execute(f"SELECT guild_id FROM serverstats WHERE guild_id = {guildID}")
    setCheck = cursor.fetchone()
    if setCheck != None:
        await ctx.send("Server Stats has already been setup! Please use `statsreset` to start again!")
        return
    elif setCheck == None:
        pass
    
    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False)
    }
    
    await ctx.guild.create_category(name="Server Stats", overwrites=overwrites, reason=None, position=0)

    category = discord.utils.get(ctx.guild.categories, name="Server Stats")
    await ctx.guild.create_voice_channel(f"All Members: {totalCount}", category=category, sync_permissions=True)
    await ctx.guild.create_voice_channel(f"Humans: {humanCount}", category=category, sync_permissions=True)
    await ctx.guild.create_voice_channel(f"Bots: {botCount}", category=category, sync_permissions=True)

    allMemChan = discord.utils.get(ctx.guild.channels, name=f"All Members: {totalCount}")
    allMemChanID = allMemChan.id
    humanChan = discord.utils.get(ctx.guild.channels, name=f"Humans: {humanCount}")
    humanChanID = humanChan.id
    botChan = discord.utils.get(ctx.guild.channels, name=f"Bots: {botCount}")
    botChanID = botChan.id

    cursor.execute(f"INSERT INTO `serverstats` (`guild_id`, `allmem_chan_id`, `human_chan_id`, `bot_chan_id`) VALUES ('{guildID}', '{allMemChanID}', '{humanChanID}', '{botChanID}')")
    db.commit()
    
    await ctx.send("Server stat counters setup!")
    cursor.execute("SELECT used FROM commands WHERE name = 'statsetup'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'statsetup'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Statsetup -- {cupGuild} by {cupUser}")

@statsetup.error
async def statsetup_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# member joins
@bot.event
async def on_member_join(member):
    guildID = member.guild.id
    totalCount = len(member.guild.members) 
    humanCount = len([m for m in member.guild.members if not m.bot])
    botCount = totalCount - humanCount

    cursor.execute(f"SELECT allmem_chan_id FROM serverstats WHERE guild_id = {guildID}")
    allMemChanIDUF = cursor.fetchone()
    if allMemChanIDUF == None:
        return
    elif allMemChanIDUF != None:
        pass

    cursor.execute(f"SELECT human_chan_id FROM serverstats WHERE guild_id = {guildID}")
    humanChanIDUF = cursor.fetchone()
    cursor.execute(f"SELECT bot_chan_id FROM serverstats WHERE guild_id = {guildID}")
    botChanIDUF = cursor.fetchone()

    for allMemChanID in allMemChanIDUF:
        for humanChanID in humanChanIDUF:
            for botChanID in botChanIDUF:
                pass

    allMemChan = bot.get_channel(allMemChanID)
    humanChan = bot.get_channel(humanChanID)
    botChan = bot.get_channel(botChanID)

    if allMemChanID != 0:
        await allMemChan.edit(name=f"All Members: {totalCount}")
        pass
    try:
        if member.bot == True and botChanID != 0:
            await botChan.edit(name=f"Bots: {botCount}")
            return
    except:
        if member.bot != True and humanChanID != 0:
            await humanChan.edit(name=f"Humans: {humanCount}")

# member leave
@bot.event
async def on_member_remove(member):
    guildID = member.guild.id
    totalCount = len(member.guild.members) 
    humanCount = len([m for m in member.guild.members if not m.bot])
    botCount = totalCount - humanCount

    cursor.execute(f"SELECT allmem_chan_id FROM serverstats WHERE guild_id = {guildID}")
    allMemChanIDUF = cursor.fetchone()
    if allMemChanIDUF == None:
        return
    elif allMemChanIDUF != None:
        pass

    cursor.execute(f"SELECT human_chan_id FROM serverstats WHERE guild_id = {guildID}")
    humanChanIDUF = cursor.fetchone()
    cursor.execute(f"SELECT bot_chan_id FROM serverstats WHERE guild_id = {guildID}")
    botChanIDUF = cursor.fetchone()
    for allMemChanID in allMemChanIDUF:
        for humanChanID in humanChanIDUF:
            for botChanID in botChanIDUF:
                pass

    allMemChan = bot.get_channel(allMemChanID)
    humanChan = bot.get_channel(humanChanID)
    botChan = bot.get_channel(botChanID)

    if allMemChanID != 0:
        await allMemChan.edit(name=f"All Members: {totalCount}")
        pass
    try:
        if member.bot == True and botChanID != 0:
            await botChan.edit(name=f"Bots: {botCount}")
            return
    except:
        if member.bot != True and humanChanID != 0:
            await humanChan.edit(name=f"Humans: {humanCount}")

# reset counters
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def statsreset(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'resetstats'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id

    cursor.execute(f"SELECT allmem_chan_id FROM serverstats WHERE guild_id = {guildID}")
    allMemChanIDUF = cursor.fetchone()
    if allMemChanIDUF == None:
        await ctx.send('Server Stats has not been setup and thus can not be reset')
        return
    elif allMemChanIDUF != None:
        pass

    cursor.execute(f"SELECT human_chan_id FROM serverstats WHERE guild_id = {guildID}")
    humanChanIDUF = cursor.fetchone()
    cursor.execute(f"SELECT bot_chan_id FROM serverstats WHERE guild_id = {guildID}")
    botChanIDUF = cursor.fetchone()
    for allMemChanID in allMemChanIDUF:
        for humanChanID in humanChanIDUF:
            for botChanID in botChanIDUF:
                pass
    
    cursor.execute(f"DELETE FROM `serverstats` WHERE guild_id = {guildID}")
    db.commit()

    category = discord.utils.get(ctx.guild.categories, name="Server Stats")
    allMemChan = bot.get_channel(allMemChanID)
    humanChan = bot.get_channel(humanChanID)
    botChan = bot.get_channel(botChanID)

    if allMemChanID != 0:
        await allMemChan.delete()
        pass
    elif humanChanID != 0:
        await humanChan.delete()
        pass
    elif botChanID != 0:
        await botChan.delete()
        pass
    await category.delete()

    await ctx.send("Server stat counters reset")
    cursor.execute("SELECT used FROM commands WHERE name = 'resetstats'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'resetstats'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Resetstats -- {cupGuild} by {cupUser}")

@statsreset.error
async def statsreset_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# disable counters
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def removecounter(ctx, counter):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'removecounter'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    
    cursor.execute(f"SELECT allmem_chan_id FROM serverstats WHERE guild_id = {guildID}")
    allMemChanIDUF = cursor.fetchone()
    if allMemChanIDUF == None:
        await ctx.send('Server Stats has not been setup! Run `statsetup`')
        return
    elif allMemChanIDUF != None:
        pass

    cursor.execute(f"SELECT human_chan_id FROM serverstats WHERE guild_id = {guildID}")
    humanChanIDUF = cursor.fetchone()
    cursor.execute(f"SELECT bot_chan_id FROM serverstats WHERE guild_id = {guildID}")
    botChanIDUF = cursor.fetchone()
    for allMemChanID in allMemChanIDUF:
        for humanChanID in humanChanIDUF:
            for botChanID in botChanIDUF:
                pass

    category = discord.utils.get(ctx.guild.categories, name="Server Stats")

    if counter == 'all':
        allMemChan = bot.get_channel(allMemChanID)
        await allMemChan.delete()
        cursor.execute(f"UPDATE `serverstats` SET allmem_chan_id = 0 WHERE allmem_chan_id = {allMemChanID} AND guild_id = {guildID}")
        db.commit()
        pass
    elif counter == 'bots':
        botChan = bot.get_channel(botChanID)
        await botChan.delete()
        cursor.execute(f"UPDATE `serverstats` SET bot_chan_id = 0 WHERE bot_chan_id = {botChanID} AND guild_id = {guildID}")
        db.commit()
        pass
    elif counter == 'humans':
        humanChan = bot.get_channel(humnaChanID)
        await humanChan.delete()
        cursor.execute(f"UPDATE `serverstats` SET human_chan_id = 0 WHERE human_chan_id = {humanChanID} AND guild_id = {guildID}")
        db.commit()
        pass

    await ctx.send(f'Deleted **{counter}** Counter')
    cursor.execute("SELECT used FROM commands WHERE name = 'removecounter'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'removecounter'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Removecounter -- {cupGuild} by {cupUser}")

@removecounter.error
async def removecounter_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# add counter
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
@commands.has_permissions(administrator=True)
async def addcounter(ctx, counter):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'addcounter'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    guildID = ctx.guild.id
    totalCount = len(ctx.guild.members) 
    humanCount = len([m for m in ctx.guild.members if not m.bot])
    botCount = totalCount - humanCount
    
    cursor.execute(f"SELECT allmem_chan_id FROM serverstats WHERE guild_id = {guildID}")
    allMemChanIDUF = cursor.fetchone()
    if allMemChanIDUF == None:
        await ctx.send('Server Stats has not been setup! Run `statsetup`')
        return
    elif allMemChanIDUF != None:
        pass

    cursor.execute(f"SELECT human_chan_id FROM serverstats WHERE guild_id = {guildID}")
    humanChanIDUF = cursor.fetchone()
    cursor.execute(f"SELECT bot_chan_id FROM serverstats WHERE guild_id = {guildID}")
    botChanIDUF = cursor.fetchone()
    for allMemChanID in allMemChanIDUF:
        for humanChanID in humanChanIDUF:
            for botChanID in botChanIDUF:
                pass

    category = discord.utils.get(ctx.guild.categories, name="Server Stats")

    if counter == 'all' and allMemChanID == 0:
        await ctx.guild.create_voice_channel(f"All Members: {totalCount}", category=category, sync_permissions=True)
        allMemChan = discord.utils.get(ctx.guild.channels, name=f"All Members: {totalCount}")
        allMemChanID = allMemChan.id
        cursor.execute(f"UPDATE serverstats SET allmem_chan_id = {allMemChanID} WHERE guild_id = {guildID}")
        db.commit()
        pass
    elif counter == 'bots':
        await ctx.guild.create_voice_channel(f"Bots: {botCount}", category=category, sync_permissions=True)
        botChan = discord.utils.get(ctx.guild.channels, name=f"Bots: {botCount}")
        botChanID = botChan.id
        cursor.execute(f"UPDATE serverstats SET bot_chan_id = {botChanID} WHERE guild_id = {guildID}")
        db.commit()
        pass
    elif counter == 'humans':
        await ctx.guild.create_voice_channel(f"Humans: {humanCount}", category=category, sync_permissions=True)
        humanChan = discord.utils.get(ctx.guild.channels, name=f"Humans: {humanCount}")
        humanChanID = humanChan.id
        cursor.execute(f"UPDATE serverstats SET human_chan_id = {humanChanID} WHERE guild_id = {guildID}")
        db.commit()
        pass

    await ctx.send(f'Added **{counter}** Counter')
    cursor.execute("SELECT used FROM commands WHERE name = 'addcounter'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'addcounter'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Addcounter -- {cupGuild} by {cupUser}")

@addcounter.error
async def addcounter_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# counters
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def counters(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'counters'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    embed = discord.Embed(title="Server Stats Counters:", color=discord.Color.random())
    embed.add_field(name="all", value="This counter counts all members in your server, bots and humans", inline=False)
    embed.add_field(name="humans", value="This counter counts all the humans in your server", inline=False)
    embed.add_field(name="bots", value="This counter counts all the bots in your server", inline=False)

    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'counters'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'counters'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Counters -- {cupGuild} by {cupUser}")

@counters.error
async def counters_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# sound effects
async def play_file(ctx, filename):
    if not ctx.author.voice:
        await ctx.send("You are not in a voice channel.")
        return

    voice_channel = ctx.author.voice.channel
    try:
        voice_channel = await voice_channel.connect()

    # catching most common errors that can occur while playing effects
    except discord.Forbidden:
        await ctx.send(
            "Command raised error \"403 Forbidden\". Please check if bot has permission to join and speak in voice "
            "channel")
        return
    except TimeoutError:
        await ctx.send(
            "There was an error while joining channel (Timeout). It's possible that either Discord API or bot host "
            "has latency/connection issues. Please try again later if issues will continue contact bot owner.")
        return
    except discord.ClientException:
        await ctx.send("I am already playing a sound! Please wait to the current sound is done playing!")
        return
    except Exception as e:
        await ctx.send(
            "There was an error processing your request. Please try again. If issues persists please join the support server for help https://discord.com/invite/zs7UwgBZb9")
        print(f'Error trying to join a voicechannel: {e}')
        return

    # There is a 1 in 100th chance that it
    # will do a rickroll instead of the desired sound
    random_chance = random.randint(1, 200)
    if random_chance == 1:
        source = discord.FFmpegPCMAudio("sounds/rickroll.mp3")
        await ctx.send("Get rolled. There's a .5% chance of that happening, good job!")
    else:
        try:
            source = discord.FFmpegPCMAudio(filename)

        # edge case: missing file error
        except FileNotFoundError:
            await ctx.send(
                "There was an issue with playing sound: File Not Found.")
    try:
        voice_channel.play(source)
    # catching most common errors that can occur while playing effects
    except discord.Forbidden:
        await ctx.send("There was issue playing a sound effect. please check if bot has speak permission")
        await voice_channel.disconnect()
        return
    except TimeoutError:
        await ctx.send(
            "There was a error while attempting to play the sound effect (Timeout) its possible that either discord "
            "API or bot host has latency or network issues. Please try again later, if issues will continue contact "
            "bot owner")
        await voice_channel.disconnect()
        return
    except Exception as e:
        await ctx.send(
            "There was an issue playing the sound. Please try again later. If issues will continue contact bot owner.")
        await voice_channel.disconnect()
        print(f'Error trying to play a sound: {e}')
        return

    await ctx.send(":thumbsup: played the effect!")
    while voice_channel.is_playing():
        await asyncio.sleep(1)

    voice_channel.stop()

    await voice_channel.disconnect()

@bot.group(name='sfx', invoke_without_command=True)
async def sfx_cmd(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    user = ctx.author
    embed = discord.Embed(title="Available Sound Effects", description="To play a sound effect join a vc and type `sfx [sound name]` sound names are below...", color=0xff6666)
    embed.add_field(name="Sound Effects", value="`airhorn`, `bazinga`, `justdoit`, `clap`, `oof`, `nope`, `suspense`, `sad`, `gay`, `fail`, `no`, `godno`, `dootstorm`, `wtf`, `fuckedup`, `ohno`, `ohhh`, `thuglife`, `djhorn`, `phintro`, `memereview`, `spongebob`, `mariocoin`, `honk`, `goodone`, `crickets`, `jumpscare`, `deez`, `door`, `fart`", inline=False)
    embed.set_footer(text=f"{user}")
    await ctx.send(embed=embed)
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="airhorn")
async def airhorn_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/airhorn.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Airhorn -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="bazinga")
async def bazinga_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/bazinga.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Bazinga -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="justdoit")
async def justdoit_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/justdoit.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX JustDoIt -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="clap")
async def clap_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/clap.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Clap -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="oof")
async def oof_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/oof.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Oof -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="nope")
async def nope_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/nope.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Nope -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="suspense")
async def suspense_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/suddensus.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Suspense -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="sad")
async def sad_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/sadmusic.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Sad -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="gay")
async def gay_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/hagay.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Gay -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="fail")
async def fail_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/fail.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Fail -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="no")
async def no_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/no.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX No -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="godno")
async def godno_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/godno.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX GodNo -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="dootstorm")
async def dootstorm_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/dootstorm.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX DootStorm -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="wtf")
async def wtf_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/WTF.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX WTF -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="fuckedup")
async def fuckedup_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/fuckedup.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX FuckedUp -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="ohno")
async def ohno_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/ohno.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX OhNo -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="ohhh")
async def ohhh_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/ohhh.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Ohhh -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="thuglife")
async def thuglife_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/thuglife.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX ThugLife -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="djhorn")
async def djhorn_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/djhorn.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX DJHorn -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="phintro")
async def phintro_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/phintro.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX PHintro -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="memereview")
async def memereview_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/meme-review.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX MemeReview -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="spongebob")
async def spongebob_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/spongebob.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Spongebob -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="mariocoin")
async def mariocoin_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/mario_coin.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX MarioCoin -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="honk")
async def honk_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/honk.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Honk -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="goodone")
async def goodone_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/good-one.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX GoodOne -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="crickets")
async def crickets_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/crickets.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Crickets -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="jumpscare")
async def jumpscare_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/jump-scare.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX JumpScare -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="deez")
async def deez_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/nuts.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Deez -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="door")
async def door_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/door.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Door -- {cupGuild} by {cupUser}")

@sfx_cmd.command(name="fart")
async def fart_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'sfx'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await play_file(ctx, "sounds/fart.mp3")
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"SFX Fart -- {cupGuild} by {cupUser}")

# mining system 
@bot.command()
@commands.cooldown(1,20,commands.BucketType.member)
async def mine(ctx):
    guildID = ctx.guild.id
    userID = ctx.author.id
    userName = ctx.author.name
    user = ctx.author

    # check if user has pickaxe
    cursor.execute(f"SELECT pickAxe_type FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    pickTypeUF = cursor.fetchone()
    if pickTypeUF == ('',):
        await ctx.send("You do not have a pickaxe! Please buy one using `shop`")
        return
    else:
        pass
    for pickType in pickTypeUF:
        pass

    # check the durability of the pickaxe
    cursor.execute(f"SELECT pickAxe_dura FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    pickDuraUF = cursor.fetchone()
    for pickDura in pickDuraUF:
        pass
    if pickDura <= 0:
        await ctx.send("Your pickaxe is broken! Please buy a new one using `shop`")
        cursor.execute(f"UPDATE econ SET pickAxe_type = '', pickAxe_dura = 0 WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        return
    else:
        pass

    # get users balance
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    if balUF == None:
        bal = 0
        pass
    elif balUF != None:
        for bal in balUF:
            pass

    # cringe people fall in lava (super rare)
    lava_chance = random.randint(1, 1000000)
    if lava_chance == 1:
        balMin = bal * .5
        balN = balMin - bal
        cursor.execute(f"UPDATE econ SET pickAxe_type = '', pickAxe_dura = 0, coins = {balN} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        embed = discord.Embed(title="OH NO!", color=discord.Color.red())
        embed.add_field(name="You fell in lava!!", value=f"There a 0.0001% chance of that happening!! You lost your pickaxe and {balMin} DXC!", inline=False)
        embed.set_footer(text=f"{userName} | Bal: {balN} DXC")
        await ctx.send(embed=embed)
        print(f"{user} Fell in lava!!")
        return

    # get the block info. Doing it this way instead of with random so i can set percentages for each
    block_choice = random.randint(1,600)
    if block_choice == 1:
        block = "Diamond"
        price = 500
        dura = pickDura - 10
        pass
    elif block_choice > 1 and block_choice <= 50:
        block = "Gold"
        price = 250
        dura = pickDura - 6
        pass
    elif block_choice > 50 and block_choice <= 150:
        block = "Iron"
        price = 150
        dura = pickDura - 5
        pass
    elif block_choice > 150 and block_choice <= 275:
        block = "Coal"
        price = 50
        dura = pickDura - 2
        pass
    elif block_choice > 275 and block_choice <= 450:
        block = "Cobblestone"
        price = 10
        dura = pickDura - 1
        pass
    elif block_choice > 450 and block_choice <= 600:
        block = "Dirt" 
        price = 5
        dura = pickDura - 1
        pass

    # update balance and pick dura
    balN = bal + price
    cursor.execute(f"UPDATE econ SET coins = {balN}, pickAxe_dura = {dura} WHERE guild_id = {guildID} AND user_id = {userID}")
    db.commit()

    # embed
    embed = discord.Embed(title=f"Mined: {block}", color=discord.Color.green())
    embed.add_field(name=f"Value: {price} DXC", value=f"Durability: {dura}", inline=False)
    embed.set_footer(text=f"{userName} | Bal: {balN} DXC")

    await ctx.send(embed=embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'mine'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'mine'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Mine -- {cupGuild} by {cupUser}")

@mine.error
async def mine_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# buying picks
# wood pick
@buy_cmd.command(name='2')
async def two_subcom(ctx):
    userID = ctx.author.id
    guildID = ctx.guild.id
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    cursor.execute(f"SELECT pickAxe_type FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    pick = cursor.fetchone()
    for bal in balUF:
        pass
    if bal >= 100:
        if pick == None or pick == ('',):
            bal -= 100
            cursor.execute(f"UPDATE `econ` SET `pickAxe_type` = 'Wood', `coins` = {bal}, `pickAxe_dura` = 50 WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.send(f"Purchased a **Wood Pickaxe!** Updated balance: **{bal}** DXC")
            return
        else:
            await ctx.send(f"You already have a Pickaxe")
    elif bal < 100:
        await ctx.send(f"You do not have enough Dox Coins! Balance: **{bal}** DXC")

# stone pick
@buy_cmd.command(name='3')
async def three_subcom(ctx):
    userID = ctx.author.id
    guildID = ctx.guild.id
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    cursor.execute(f"SELECT pickAxe_type FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    pick = cursor.fetchone()
    for bal in balUF:
        pass
    if bal >= 200:
        if pick == None or pick == ('',):
            bal -= 200
            cursor.execute(f"UPDATE `econ` SET `pickAxe_type` = 'Stone', `coins` = {bal}, `pickAxe_dura` = 75 WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.send(f"Purchased a **Stone Pickaxe!** Updated balance: **{bal}** DXC")
            return
        else:
            await ctx.send(f"You already have a Pickaxe")
    elif bal < 200:
        await ctx.send(f"You do not have enough Dox Coins! Balance: **{bal}** DXC")

# iron pick
@buy_cmd.command(name='4')
async def three_subcom(ctx):
    userID = ctx.author.id
    guildID = ctx.guild.id
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    cursor.execute(f"SELECT pickAxe_type FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    pick = cursor.fetchone()
    for bal in balUF:
        pass
    if bal >= 300:
        if pick == None or pick == ('',):
            bal -= 300
            cursor.execute(f"UPDATE `econ` SET `pickAxe_type` = 'Iron', `coins` = {bal}, `pickAxe_dura` = 100 WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.send(f"Purchased a **Iron Pickaxe!** Updated balance: **{bal}** DXC")
            return
        else:
            await ctx.send(f"You already have a Pickaxe")
    elif bal < 300:
        await ctx.send(f"You do not have enough Dox Coins! Balance: **{bal}** DXC")

# gold pick
@buy_cmd.command(name='5')
async def three_subcom(ctx):
    userID = ctx.author.id
    guildID = ctx.guild.id
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    cursor.execute(f"SELECT pickAxe_type FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    pick = cursor.fetchone()
    for bal in balUF:
        pass
    if bal >= 400:
        if pick == None or pick == ('',):
            bal -= 400
            cursor.execute(f"UPDATE `econ` SET `pickAxe_type` = 'Gold', `coins` = {bal}, `pickAxe_dura` = 150 WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.send(f"Purchased a **Gold Pickaxe!** Updated balance: **{bal}** DXC")
            return
        else:
            await ctx.send(f"You already have a Pickaxe")
    elif bal < 400:
        await ctx.send(f"You do not have enough Dox Coins! Balance: **{bal}** DXC")

# diamond pick
@buy_cmd.command(name='6')
async def three_subcom(ctx):
    userID = ctx.author.id
    guildID = ctx.guild.id
    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    balUF = cursor.fetchone()
    cursor.execute(f"SELECT pickAxe_type FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
    pick = cursor.fetchone()
    for bal in balUF:
        pass
    if bal >= 650:
        if pick == None or pick == ('',):
            bal -= 650
            cursor.execute(f"UPDATE `econ` SET `pickAxe_type` = 'Diamond', `coins` = {bal}, `pickAxe_dura` = 250 WHERE guild_id = {guildID} AND user_id = {userID}")
            db.commit()
            await ctx.send(f"Purchased a **Diamond Pickaxe!** Updated balance: **{bal}** DXC")
            return
        else:
            await ctx.send(f"You already have a Pickaxe")
    elif bal < 650:
        await ctx.send(f"You do not have enough Dox Coins! Balance: **{bal}** DXC")

# leaderboards
@bot.group(name="leaderboard", invoke_without_command=True)
async def lead_cmd(ctx):
    embed = discord.Embed(title="Leaderboard Commands", description="To use: type `leaderboard [name]` the names are down below", color=discord.Color.random())
    embed.add_field(name="coins", value="Get the leaderboard for coins in your server", inline=False)
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'leaderboard'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'leaderboard'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Leaderboard -- {cupGuild} by {cupUser}")

# coins leaderboard
@lead_cmd.command(name='coins')
@commands.cooldown(1,1,commands.BucketType.guild)
async def coins_lead_subcom(ctx):
    authID = ctx.author.id
    authName = ctx.author.name
    guildID = ctx.guild.id
    guildName = ctx.guild.name

    cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} ORDER BY coins DESC")
    coins_listUF = cursor.fetchall()
    coins_list_len = len(coins_listUF)
    for coins_list in coins_listUF:
        pass

    embed = discord.Embed(title=f"Economy Leaderboard For {guildName}", color=discord.Color.random())
    embed.set_footer(text=f"{authName} | Top 5 Users")

    try:
        for coins0 in coins_listUF[0]:
            pass
        cursor.execute(f"SELECT user_id FROM econ WHERE guild_id = {guildID} AND coins = {coins0}")
        user0UF = cursor.fetchone()
        for user0 in user0UF:
            pass
        userName0 = await bot.fetch_user(user0)
        embed.add_field(name=f"1. {userName0}", value=f"{coins0} DXC", inline=False)

        try:
            for coins1 in coins_listUF[1]:
                pass
            cursor.execute(f"SELECT user_id FROM econ WHERE guild_id = {guildID} AND coins = {coins1}")
            user1UF = cursor.fetchone()
            for user1 in user1UF:
                pass
            userName1 = await bot.fetch_user(user1)
            embed.add_field(name=f"2. {userName1}", value=f"{coins1} DXC", inline=False)

            try:
                for coins2 in coins_listUF[2]:
                    pass
                cursor.execute(f"SELECT user_id FROM econ WHERE guild_id = {guildID} AND coins = {coins2}")
                user2UF = cursor.fetchone()
                for user2 in user2UF:
                    pass
                userName2 = await bot.fetch_user(user2)
                embed.add_field(name=f"3. {userName2}", value=f"{coins2} DXC", inline=False)

                try:
                    for coins3 in coins_listUF[3]:
                        pass
                    cursor.execute(f"SELECT user_id FROM econ WHERE guild_id = {guildID} AND coins = {coins3}")
                    user3UF = cursor.fetchone()
                    for user3 in user3UF:
                        pass
                    userName3 = await bot.fetch_user(user3)
                    embed.add_field(name=f"4. {userName3}", value=f"{coins3} DXC", inline=False)

                    try:
                        for coins4 in coins_listUF[4]:
                            pass
                        cursor.execute(f"SELECT user_id FROM econ WHERE guild_id = {guildID} AND coins = {coins4}")
                        user4UF = cursor.fetchone()
                        for user4 in user4UF:
                            pass
                        userName4 = await bot.fetch_user(user4)
                        embed.add_field(name=f"5. {userName4}", value=f"{coins4} DXC", inline=False)
                        
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
    except:
        pass

    await ctx.send(embed=embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'coins_leaderboard'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'coins_leaderboard'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Coins Leaderboard -- {cupGuild} by {cupUser}")

# cringe command
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def cringe(ctx, user: discord.User=None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'cringe'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    if user != None:
        await ctx.send(f"{user.mention} Cringe")
        pass
    
    api_key=os.getenv('GIPHYAPI')
    api_instance = giphy_client.DefaultApi()
    my_channel = bot.get_channel(825193245445324810)
    q = "cringe"

    try: 
    # Search Endpoint
        
        api_response = api_instance.gifs_search_get(api_key, q, limit=100, rating='r')
        lst = list(api_response.data)
        giff = random.choice(lst)
        user = ctx.message.author

        emb = discord.Embed(url=f'https://media.giphy.com/media/{giff.id}/giphy.gif', color=discord.Color.random())
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)

    except ApiException as e:
      timestamp = datetime.now()
      apierror = discord.Embed(title="GIPHY API ERROR", color=discord.Color.red())
      apierror.add_field(name="Exception when calling DefaultApi", value="gifs_search_get: %s\n" % e, inline=False)
      apierror.set_footer(text=f"{timestamp}")
      await my_channel.send(embed=apierror)

    cursor.execute("SELECT used FROM commands WHERE name = 'cringe'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'cringe'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Cringe -- {cupGuild} by {cupUser}")

@cringe.error
async def cringe_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

#urban dict
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def urban(ctx, *term):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'urban'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

    querystring = {"term":term}

    headers = {
        'x-rapidapi-key': "ff4fdc9533msh82425dbe3f15b31p195105jsn02cd7bdabde2",
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()

    definition = res["list"][0]['definition']
    link = res["list"][0]['permalink']
    thumbsUp = res["list"][0]['thumbs_up']
    thumbsDown = res["list"][0]['thumbs_down']
    author = res["list"][0]['author']
    example = res["list"][0]['example']
    word = res["list"][0]['word']
    
    embed = discord.Embed(title=word, url=link, description=f"**Def:** {definition}\n\nExample:\n{example}", color=discord.Color.blue())
    embed.set_author(name=f"By: {author}")
    embed.set_footer(text=f"👍: {thumbsUp} | 👎: {thumbsDown}")

    await ctx.send(embed=embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'urban'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'urban'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Urban -- {cupGuild} by {cupUser}")

@urban.error
async def urban_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a word to search on Urban Dictionary")

# Akinator
@bot.group(name="aki", invoke_without_command=True)
async def aki_cmd(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'aki'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    embed = discord.Embed(title="Akinator Commands", color=discord.Color.random())
    embed.add_field(name="1. start", value="Use this to start a game", inline=False)
    embed.add_field(name="2. answers", value="Use this to see valid answers to Akinators questions", inline=False)
    
    await ctx.send(embed=embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'akinator'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'akinator'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Aki -- {cupGuild} by {cupUser}")

@aki_cmd.command(name="start")
async def aki_start_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'aki'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    await ctx.send("Akinator game starting please wait...")

    # get game stats
    cursor.execute(f"SELECT games_total FROM aki_stats")
    gamesTotalUF = cursor.fetchone()
    for gamesTotal in gamesTotalUF:
        pass
    gamesTotal += 1
    cursor.execute(f"UPDATE `aki_stats` SET `games_total`={gamesTotal}")
    db.commit()

    cursor.execute(f"SELECT won FROM aki_stats")
    gamesWonUF = cursor.fetchone()
    for gamesWon in gamesWonUF:
        pass

    cursor.execute(f"SELECT lost FROM aki_stats")
    gamesLostUF = cursor.fetchone()
    for gamesLost in gamesLostUF:
        pass

    # start game
    aki = akinator.Akinator()
    ques = aki.start_game(language=None)

    Qembed = discord.Embed(title=ques)
    Qembed.set_footer(text="Answer with yes, no, idk, probably, probably not, or back")

    await ctx.send(embed=Qembed)

    def check(m):
        return m.content == 'yes' or m.content == 'no' or m.content == 'back'  or m.content == 'idk'  or m.content == 'probably'  or m.content == 'probably not' or m.content == 'y'  or m.content == 'n'  or m.content == 'b'  or m.content == 'i'  or m.content == 'p'  or m.content == 'pn' and m.channel == ctx.channel and m.author == ctx.author

    # wait for answer
    while aki.progression <= 80:
        try:
            ans = await bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You didn't answer in time. Game ended")
            break
            return
        else:
            if ctx.message.content == 'back':
                try:
                    ques = aki.back()
                except akinator.CantGoBackAnyFurther:
                    await ctx.send("You can't go back any further")
                    pass
            else:
                ques = aki.answer(ans.content)
                Qembed2 = discord.Embed(title=ques)
                Qembed2.set_footer(text="Answer with yes, no, idk, probably, probably not, or back")
                await ctx.send(embed=Qembed2)

    # aki win?
    win = aki.win()
    name = win['name']
    desc = win['description']
    pic = win['absolute_picture_path']

    embed = discord.Embed(title="Is Your Character...", description=f"**{name}**\n{desc}", color=discord.Color.gold())
    embed.set_image(url=pic)
    embed.set_footer(text="Answer with 'yes' or 'no'")
    await ctx.send(embed=embed)

    # wait for answer
    def check2(m):
        return m.content == 'yes' or m.content == 'no'  or m.content == 'y'  or m.content == 'n' and m.channel == ctx.channel and m.author == ctx.author

    while True:
        try:
            winTrue = await bot.wait_for('message', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
            await ctx.send("You didn't answer in time, I guess I win?")
            break
            return
        else:
            if winTrue.content == 'yes' or winTrue.content == 'y':
                gamesWon += 1
                cursor.execute(f"UPDATE `aki_stats` SET `won`={gamesWon}")
                db.commit()
                WinEmbed = discord.Embed(title="HAHA I win!", description=f"I've won **{gamesWon}** games", color=discord.Color.green())
                await ctx.send(embed=WinEmbed)
                break
            elif winTrue.content == 'no' or winTrue.content == 'n':
                gamesLost += 1
                cursor.execute(f"UPDATE `aki_stats` SET `lost`={gamesLost}")
                db.commit()
                LossEmbed = discord.Embed(title="Dang! You Won...", description=f"I've lost **{gamesLost}** games", color=discord.Color.red())
                await ctx.send(embed=LossEmbed)
                break
    
    cursor.execute("SELECT used FROM commands WHERE name = 'aki start'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'aki start'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Aki Start -- {cupGuild} by {cupUser}")
 
@aki_cmd.command(name="answers")
async def aki_ans_subcom(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'aki'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass

    embed = discord.Embed(title="Valid Akinator Answers", description="yes/y, no/n, idk/i, probably/p, probably not/pn, back/b", color=discord.Color.random())
    await ctx.send(embed=embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'aki answers'")
    used = cursor.fetchone()
    for num in used:
      num += 1
      cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'aki answers'")
      db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Aki answers -- {cupGuild} by {cupUser}")

# slash commands section theres a lot of shit here might make this into a seperate file

# meme slash
@slash.slash(name="meme", description="Sends a random meme from a selection of SubReddits")
@commands.cooldown(1,1,commands.BucketType.guild)
async def s_meme(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'meme'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    r = requests.get("https://memes.blademaker.tv/api?lang=en")
    res = r.json()
    title = res["title"]
    ups = res["ups"]
    downs = res["downs"]
    sub = res["subreddit"]
    link = "https://reddit.com/" + res["id"]
    author = res["author"]
    m = discord.Embed(title = f"{title}", url = f"{link}",color = discord.Color.orange())
    m.set_image(url = res["image"])
    m.set_footer(text=f"👍: {ups}    Author: {author}")
    await ctx.send(embed = m)
    cursor.execute("SELECT used FROM commands WHERE name = 'meme'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'meme'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Meme -- {cupGuild} by {cupUser}")

@s_meme.error
async def s_meme_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# invite slash
@slash.slash(name="invite", description="Get the bots invite link to add it to your server!")
@commands.cooldown(1,1,commands.BucketType.guild)
async def s_invite(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'invite'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    await buttons.send(
        content = "Invite DoxBot to your server!",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "Click Here",
                    style = ButtonType().Link,
                    url = "https://doxbot.xyz/invite"
                )
            ])
        ]
    )
    cursor.execute("SELECT used FROM commands WHERE name = 'invite'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'invite'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Invite -- {cupGuild} by {cupUser}")

@s_invite.error
async def s_invite_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# stats slash
@slash.slash(name="stats", description="Get some interesting stats about the bot")
@commands.cooldown(1,1,commands.BucketType.guild)
async def s_stats(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'stats'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()[2]
    scount = str(len(bot.guilds))
    users = str(len(bot.users))
    ping = round(bot.latency * 1000,2)
    cursor.execute("SELECT SUM(used) FROM commands")
    sumAllUF = cursor.fetchall()
    sumAll = sumAllUF[0][0]
    embed = discord.Embed(title="DoxBot Stats", color=0xff6666)
    embed.set_thumbnail(url="https://doxbot.xyz/images/doxlogo2")
    embed.add_field(name="Servers:", value=scount, inline=True)
    embed.add_field(name="Users:", value=users, inline=True)
    embed.add_field(name="Commands:", value="162", inline=True)
    embed.add_field(name="Cmds. Run:", value=sumAll, inline=True)
    embed.add_field(name="CPU Usage:", value=f"{cpu}%", inline=True)
    embed.add_field(name="Mem. Usage:", value=f"{mem}%", inline=True)
    embed.add_field(name="Ping:", value=f"{ping}ms", inline=True)
    embed.add_field(name="Library:", value="Discord.py", inline=True)
    embed.add_field(name="Owner:", value="PapaRaG3#6969", inline=True)
    await ctx.send(embed=embed)
    cursor.execute("SELECT used FROM commands WHERE name = 'stats'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'stats'")
        db.commit()
        cupGuild = ctx.guild.name
        cupUser = ctx.author
        print(f"Stats -- {cupGuild} by {cupUser}")

@s_stats.error
async def s_stats_error(ctx, error):
    coolDownMsg = random.choice(coolDown_list)
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title=f"{coolDownMsg}", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# dox slash
@slash.slash(name="dox",
            description="Use this to get 100% real info about someone wink wink.",
            options=[
                create_option(
                    name="User",
                    description="Who you want to dox, if left blank, you will be doxxed",
                    option_type=2,
                    required=False
                )
            ])
async def s_dox(ctx, User: str = None):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'dox'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        pass
    identity = getIdentity()

    if User == None:
        userName = ctx.author.name
    else:
        userName = User

    embed = discord.Embed(title=f"Doxing {userName}...", color=discord.Color.red())
    embed.add_field(name="Full Name:", value=identity.name, inline=False)
    embed.add_field(name="Height:", value=identity.height + " / " + identity.heightcm + " cm", inline=False)
    embed.add_field(name="Weight:", value=identity.weight + "lbs / " + identity.weightkg + "kg", inline=False)
    embed.add_field(name="Birthday:", value=identity.birthday, inline=False)
    embed.add_field(name="Address:", value=identity.address, inline=False)
    embed.add_field(name="Coordinates:", value=identity.coords, inline=False)
    embed.add_field(name="Email:", value=identity.email, inline=False)
    embed.add_field(name="Phone Number:", value=identity.phone, inline=False)
    embed.add_field(name="Discord Password:", value=identity.password, inline=False)
    embed.add_field(name="SSN:", value=identity.ssn, inline=False)
    embed.add_field(name="Credit Card:", value="Num: " + identity.card + " Exp: " + identity.expiration + " CVV: " + identity.cvv2, inline=False)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"Requested by: {ctx.author} \u200b")

    await ctx.send(embed = embed)

    cursor.execute("SELECT used FROM commands WHERE name = 'dox'")
    used = cursor.fetchone()
    for num in used:
        num += 1
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'dox'")
        db.commit()
    cupGuild = ctx.guild.name
    cupUser = ctx.author
    print(f"Dox -- {cupGuild} by {cupUser}")

# Run bot
web_server()
pub_tweet.start()
print(db)
print("Online")
bot.run(os.getenv('TOKEN'))