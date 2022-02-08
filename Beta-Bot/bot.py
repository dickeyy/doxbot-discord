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
import pymongo
import sys
import numbers
from dadjokes import Dadjoke
import googletrans
from fng_api import *
from discord import DMChannel
from dotenv import load_dotenv
from web import keep_alive
import ffmpeg
from datetime import date
from discord_buttons_plugin import *

load_dotenv()

# database stuff
db = mysql.connector.connect(
    host= os.getenv("HOST"),
    user= os.getenv("USER"),
    password= os.getenv("PASSWORD"),
    database= os.getenv("DATABASE"),
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

# define stuff
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = True
owner_id = 489264179472236557
bot = commands.Bot(command_prefix="beta$", intents=intents)
buttons = ButtonsClient(bot)

bot.remove_command('help')

@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="doxbot.xyz"))

# iq command
@bot.command()
async def iq(ctx, member: discord.Member):

  iq_list = ['Homies dumb as bricks. IQ = 4', 'Literally 0', 'Our holy overlord. IQ = 10,000', 'Enstein is that you? IQ = 258', 'IQ = 21', 'I am a python script that doesnt even really exist and I am still smarter than this guy. IQ = 1', 'IQ = 14', 'IQ = 413, my god...', 'This forgets his glasses are on his head, IQ = 32', 'About the eqivalant as my creator, IQ = 1947', 'IQ = 46', 'Look up a picture of dumb in the dictionary and you will get a picture of this guy, IQ = 5', 'IQ = 134', 'IQ = 102', 'IQ = 2', 'sO dum i furget hoW 2 spill, ia = -291', 'No :)', 'ERROR: NO IQ DETECTED', 'At least they have a big di.. oh wait no my sources are telling me thats almost as small as their IQ, IQ = -131344', 'You know what they say... actually no I dont know what they say my creator forgot. IQ = 420', 'HAHA FUNNY SEX NUMBER IQ = 69']

  iq = random.choice(iq_list)

  await ctx.send(iq)

@iq.error
async def iq_error(ctx, error):
  print(error)
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('Please mention someone to test their IQ')

# avatar 
@bot.command()
async def avatar(ctx, member: discord.Member = None):
  if member is None:
    ctx.send("Please metion a user u dumb ass")
    return
  
  else:
    embed2 = discord.Embed(title=f"{member}'s Avatar!", colour=0x0000ff, timestamp=ctx.message.created_at)
    embed2.add_field(name="Animated?", value=member.is_avatar_animated())
    embed2.set_image(url=member.avatar_url)
    await ctx.send(embed = embed2)

# math
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

@bot.command()
async def mathadd(ctx, x: float, y: float):
	try:
		result = add(x, y)
		await ctx.send(result)

	except:
		pass

@bot.command()
async def mathsub(ctx, x: float, y: float):
	try:
		result = sub(x, y)
		await ctx.send(result)

	except:
		pass

@bot.command()
async def mathrando(ctx, x: int, y: int):
	try:
		result = rando(x, y)
		await ctx.send(result)

	except:
		pass

@bot.command()
async def mathdiv(ctx, x: float, y: float):
	try:
		result = div(x, y)
		await ctx.send(result)

	except:
		pass

@bot.command()
async def mathmult(ctx, x: float, y: float):
	try:
		result = mult(x, y)
		await ctx.send(result)

	except:
		pass

@bot.command()
async def mathsqrt(ctx, x: float):
	try:
		result = sqrt(x)
		await ctx.send(result)

	except:
		pass

# invite command
@bot.command()
async def invite(ctx):
  invem = discord.Embed(title = 'Invite DoxBot to Your Server!', description='[Click Here](https://doxbot.xyz/invite)', color = discord.Color.gold())
  await ctx.send(embed = invem)

# meme command
@bot.command()
async def meme(ctx):
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
  
# NSFW command
@bot.command()
async def nsfw(ctx):
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
            user = ctx.message.author.name
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

# specific reddit search 
@bot.command()
async def reddit(ctx, reddit):
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
        user = ctx.message.author.name
        embed = discord.Embed(title=f"Random pic from r/{sub}", color = discord.Color.orange())
        embed.set_image(url=picurl)
        embed.set_footer(text=f"Requested by: {user}  r/{sub}")
    await ctx.send(embed = embed)

# coin flip
@bot.command()
async def coinflip(ctx):
  result_list = ['tails', 'heads']
  result = random.choice(result_list)
  if result == 'heads':
    await ctx.send('<:simp_coin:824720566241853460> Heads!')
  elif result == 'tails':
    await ctx.send('<:fuck_coin:824720614543196220> Tails!')
  

# donate command
@bot.command()
async def donate(ctx):
  embed = discord.Embed(title="Donate To DoxBot", url='https://www.paypal.com/donate/?business=P4XFFUMHFWJ98&item_name=Support+DoxBot+and+allow+it+to+continue+running%21&currency_code=USD', color=0xff6666)
  embed.add_field(name="Help support DoxBot", value="Donating is not required, but is greatly appreciated. For more info click [Here](https://doxbot.xyz/faq)", inline=False)
  await ctx.send(embed=embed)

# poll command
@bot.command()
async def poll(ctx, *, args):
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
                    async with timeout(300):  # 5 minutes
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
        await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(name='join', invoke_without_subcommand=True)
    async def _join(self, ctx: commands.Context):
        """Joins a voice channel."""

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(name='summon')
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
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

    @commands.command(name='leave', aliases=['disconnect'])
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):
        """Clears the queue and leaves the voice channel."""

        if not ctx.voice_state.voice:
            return await ctx.send('Not connected to any voice channel.')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(name='volume')
    async def _volume(self, ctx: commands.Context, *, volume: int):
        """Sets the volume of the player."""

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        if 0 > volume > 100:
            return await ctx.send('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send('Volume of the player set to {}%'.format(volume))

    @commands.command(name='now', aliases=['current', 'playing'])
    async def _now(self, ctx: commands.Context):
        """Displays the currently playing song."""

        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(name='pause')
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):
        """Pauses the currently playing song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='resume')
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):
        """Resumes a currently paused song."""

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            await ctx.message.add_reaction('⏯')

    @commands.command(name='stop')
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):
        """Stops playing song and clears the queue."""

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(name='skip')
    async def _skip(self, ctx: commands.Context):
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

    @commands.command(name='queue')
    async def _queue(self, ctx: commands.Context, *, page: int = 1):
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

    @commands.command(name='shuffle')
    async def _shuffle(self, ctx: commands.Context):
        """Shuffles the queue."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(name='remove')
    async def _remove(self, ctx: commands.Context, index: int):
        """Removes a song from the queue at a given index."""

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('Empty queue.')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(name='loop')
    async def _loop(self, ctx: commands.Context):
        """Loops the currently playing song.

        Invoke this command again to unloop the song.
        """

        if not ctx.voice_state.is_playing:
            return await ctx.send('Nothing being played at the moment.')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(name='play')
    async def _play(self, ctx: commands.Context, *, search: str):
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
async def musichelp(ctx):
  embed = discord.Embed(title="Music Help", color=discord.Color.teal())
  embed.set_thumbnail(url="https://doxbot.xyz/images/groovin-dox.png")
  embed.add_field(name="$play [song]", value="Play a song in a voice channel using DoxBot", inline=False)
  embed.add_field(name="$queue", value="Display the queue", inline=False)
  embed.add_field(name="$skip", value="Skip the current song and play the next in queue", inline=False)
  embed.add_field(name="$remove [queue number]", value="Remove a specific song in queue", inline=False)
  embed.add_field(name="$join", value="Make DoxBot join the voice channel you are in", inline=False)
  embed.add_field(name="$leave", value="Make DoxBot leave the current VC", inline=False)
  embed.add_field(name="$summon [channel id]", value="Tell Dox to join a specific channel (User must have Manage Channel permission)", inline=False)
  embed.add_field(name="$pause", value="Pauses the song currently playing", inline=False)
  embed.add_field(name="$resume", value="Resumes playing the paused song", inline=False)
  embed.add_field(name="$stop", value="Stops the song playing", inline=False)
  embed.add_field(name="$volume [number 1-100]", value="Sets the volume of the player", inline=False)
  embed.add_field(name="$loop", value="Loop the song currently playing", inline=False)
  embed.add_field(name="$shuffle", value="Shuffles the queue", inline=False)
  embed.add_field(name="$now", value="Displays the song currently playing", inline=False)
  embed.set_footer(text="Note: Some of these commands will in the future be a premium feature so enjoy them now :)")
  await ctx.send(embed=embed)

# afk command
@bot.command()
async def afk(ctx, *, args):
  message = args
  author = ctx.message.author.mention
  await ctx.send(f"{author} is now AFK: **{message}**")

# 8ball command
@bot.command(aliases=['8ball'])
async def eightball(ctx, *args):
  res_list = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Dont count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt', 'Yes.', 'Yes – definitely.', 'You may rely on it.']
  res = random.choice(res_list)
  ques = " ".join(args[:])
  author = ctx.message.author
  embed = discord.Embed(title="Magic 8 Ball")
  embed.set_thumbnail(url='https://img.pngio.com/magic-8-ball-by-horoscopecom-get-free-divination-games-just-for-fun-magic-8-ball-png-300_300.png')
  embed.add_field(name=f"A: {res}", value=f"Q: {ques}", inline=False)
  embed.set_footer(text=f"{author}")
  await ctx.send(embed=embed)

# dog command
@bot.command()
async def dog(ctx):
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

# cat command
@bot.command()
async def cat(ctx):
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

# gif command
@bot.command()
async def gif(ctx,*,q="random"):

    api_key=os.getenv("GIPHYAPI")
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
        print("Added new guild to DB")
        return

# adding guild to database based on message(temp), and counting game
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
            pass
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
    # xp stuff
    #if msg.author == bot.user:
        #return
    #elif msg.author != bot.user:
        #pass
    #cursor.execute(f"SELECT xp FROM levels WHERE guild_id = {guildID} AND user_id = {userID}")
    #xpUF = cursor.fetchone()
    #if xpUF == None:
        #xp = 0
        #pass
    #elif xpUF != None:
        #xpUF = xpUF
        #for xp in xpUF:
            #pass
    #xp_add = random.randint(1, 15)
    #xpIn = xp + xp_add
    #if pre in msg.content:
        #pass
    #elif pre not in msg.content:
        #cursor.execute(f"SELECT msg_chan FROM level_stngs WHERE guild_id = {guildID}")
        #levelChanUF = cursor.fetchone()
        #if levelChanUF == None or levelChanUF == ('',):
            #levelChan = msg.channel
            #pass
        #elif levelChanUF != None or levelChanUF != ('',):
            #for levelChan1 in levelChanUF:
                #levelChan = bot.get_channel(levelChan1)
                #pass
        #if xp == 0:
            #cursor.execute(f"INSERT INTO `levels` (`guild_id`, `user_id`, `xp`, `level`) VALUES ('{guildID}', '{userID}', '{xpIn}', '1')")
            #db.commit()
            #await levelChan.send(f"Congrats {msg.author.mention}, you just leveled up to level **1**")
            #pass
        #elif xp != 0:
            #cursor.execute(f"UPDATE `levels` SET `xp` = {xpIn} WHERE guild_id = {guildID} and user_id = {userID}")
            #db.commit()
            #pass
        #cursor.execute(f"SELECT level FROM levels WHERE guild_id = {guildID} AND user_id = {userID}")
        #levelUF = cursor.fetchone()
        #for level in levelUF:
            #pass
        #level 1 = 0-150 level 2 = 151-400 level 3 = 401-700 level 4 = 701-1200 levl 5 = 1201-2000
        #if xpIn >= 151 and xpIn <= 400:
            #levelNew = 2
            #if level == levelNew:
                #pass
            #elif level != levelNew:
                #cursor.execute(f"UPDATE levels SET level = {levelNew} WHERE guild_id = {guildID} and user_id = {userID}")
                #db.commit()
                #await levelChan.send(f"Congrats {msg.author.mention}, you just leveled up to level **{levelNew}**")
                #pass
        #elif xpIn >= 401 and xpIn <= 700:
            #levelNew = 3
            #if level == levelNew:
                #pass
            #elif level != levelNew:
                #cursor.execute(f"UPDATE levels SET level = {levelNew} WHERE guild_id = {guildID} and user_id = {userID}")
                #db.commit()
                #await levelChan.send(f"Congrats {msg.author.mention}, you just leveled up to level **{levelNew}**")
                #pass
        #elif xpIn >= 701 and xpIn <= 1200:
            #levelNew = 4
            #if level == levelNew:
                #pass
            #elif level != levelNew:
                #cursor.execute(f"UPDATE levels SET level = {levelNew} WHERE guild_id = {guildID} and user_id = {userID}")
                #db.commit()
                #await levelChan.send(f"Congrats {msg.author.mention}, you just leveled up to level **{levelNew}**")
                #pass
        #elif xpIn >= 1201 and xpIn <= 2000:
            #levelNew = 5
            #if level == levelNew:
                #pass
            #elif level != levelNew:
                #cursor.execute(f"UPDATE levels SET level = {levelNew} WHERE guild_id = {guildID} and user_id = {userID}")
                #db.commit()
                #await levelChan.send(f"Congrats {msg.author.mention}, you just leveled up to level **{levelNew}**")
                #pass

    # stuff to announce a message to all servers
    cursor.execute(f"SELECT guild_id FROM dont_broad WHERE guild_id = {guildID}")
    isBroadcasted = cursor.fetchone()
    if isBroadcasted == None:
        if msg.author == bot.user:
            return
        else:
            broadEmbed = discord.Embed(title="Attention DoxBot users...", description="This is a message from dickey#6969 (bot owner). I have some news for y'all... DoxBot recently hit 75 servers, this means that the bot is available for verification. If the bot were to get verified by Discord, then it would be able to join more servers and get a little check mark next to it's name. **Unfortunatly, Discord denied our verification request.** This means that we are currently limited to joining 100 servers and can't grow past that. This is obviously bad. Our only real option is to make a new bot and hope Discord gives us another shot at verification. This new bot will be the exact same code and there will be no data loss. **The old DoxBot will be shutting down soon, please invite the new bot at by clicking [Here](https://doxbot.xyz/invite).** You can kick this old bot when you invite the new one. I'm sorry for the any inconvenience. Thank you for choosing DoxBot", color=discord.Color.red())
            broadEmbed.add_field(name='Please add new DoxBot Here...', value='[Click Here](https://doxbot.xyz/invite) -- https://doxbot.xyz/invite', inline=False)
            broadEmbed.add_field(name='For more info...', value='[Click Here](https://doxbot.xyz/server) -- https://doxbot.xyz/server', inline=False)
            await msg.channel.send(embed=broadEmbed)
            cursor.execute(f"INSERT INTO `dont_broad` (`guild_id`) VALUES ('{guildID}')")
            db.commit()
            print(f"Brodcasted to {guildID}")
            pass
    else:
        pass

    await bot.process_commands(msg)

# set prefix command
@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
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


@setprefix.error
async def setprefix_error(ctx, error):
    print(error)
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use that command")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Please include a prefix, `{pre}setprefix [prefix]`")

@bot.command()
async def prefix(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        await ctx.send(f"The prefix for this server is **{pre}**")
    cursor.execute("SELECT used FROM commands WHERE command = prefix")
    used = cursor.fetchone()
    for num in used:
        cursor.execute("UPDATE commands SET used = '" + str(num) + "' WHERE name = 'prefix'")
        db.commit()

# counting stuff
# set channel
@bot.command()
@commands.has_permissions(administrator=True)
async def csetup(ctx, channel: discord.TextChannel):
    guildID = ctx.guild.id
    channelID = channel.id
    cursor.execute("SELECT count FROM counting WHERE guild_id = '" + str(guildID) + "'")
    result = cursor.fetchone()
    print(result)
    if result == None:
        cursor.execute("INSERT INTO `counting` (`guild_id`, `channel_id`, `lastuser_id`, `count`) VALUES ('" + str(guildID) + "', '" + str(channelID) + "', '1', '1')")
        db.commit()
        await ctx.send("Counting channel set")
    elif result != None: 
        cursor.execute("UPDATE counting SET channel_id = '" + str(channelID) + "' WHERE guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Counting channel set")

# for actual counting function see line 1129

# counting rules
@bot.command()
async def countrules(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Counting Rules", color=discord.Color.blue())
        embed.add_field(name="Only numbers in the channel:", value="The specified counting channel is only for numbers, any message that is not the correct next number, will result in count being reset!", inline=False)
        embed.add_field(name="Don't count twice in a row:", value="If anyone counts twice in a row the count will be reset!", inline=False)
        embed.add_field(name="Don't mess it up:", value="If any user sends the wrong number, the count will be reset and they will experience a gret deal of grief and shame", inline=False)
        embed.set_footer(text=f"For more info about the game use {pre}countinfo")
        await ctx.send(embed=embed)

# counting info
@bot.command()
async def countinfo(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Counting Game Info", color=discord.Color.gold())
        embed.add_field(name="Info:", value="The counting game is a game where all you have to do is (in the specified channel) send the number that comes after the last number sent. *Example:* If I were to send **1** then Dox would send **2** and so on.", inline=False)
        embed.set_footer(text=f"For info about the rules use {pre}countrules")
        await ctx.send(embed=embed)

# get count channel
@bot.command()
async def countchannel(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        guildID = ctx.guild.id
        cursor.execute("SELECT channel_id FROM counting WHERE guild_id =" + str(guildID))
        channelUF = cursor.fetchone()
        for coChan in channelUF:
            await ctx.send(f"The counting channel is <#{coChan}>")

# get high score
@bot.command()
async def highscore(ctx):
    guildID = ctx.guild.id
    cursor.execute("SELECT highscore FROM counting WHERE guild_id = '" + str(guildID) + "'")
    highSUF = cursor.fetchone()
    for highS in highSUF:
        if highS == 1:
            highS -= 1
            await ctx.send(f"The highscore for this server is **{highS}**")
        else:
            await ctx.send(f"The highscore for this server is **{highS}**")

# command stats 
@bot.command()
async def cstats(ctx, command):
    userMention = ctx.author.mention
    userName = ctx.author.name
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        userID = ctx.author.id
        cursor.execute("SELECT used FROM commands WHERE name = '" + str(command) +"'")
        comUF = cursor.fetchall()
        if(len(comUF)) == 0:
            if userID == owner_id:
                cursor.execute("SELECT * FROM commands")
                allUF = cursor.fetchall()
                await ctx.send(allUF)
            else:
                await ctx.send(f"**{command}** Is not a valid command please try again")
        else:
            for comUF1 in comUF:
                for com in comUF1:
                    embed1 = discord.Embed(title="Command Stats", description=f"**{pre}{command}** has been used **{com}** times", color=discord.Color.random())
                    embed1.set_footer(text=f"Requested by: {userName} | Since Febuary 29, 2021")
                    await ctx.send(embed=embed1)

# new stats
@bot.command()
async def stat2(ctx):
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory()[2]
    scount = str(len(bot.guilds))
    users = str(len(bot.users))
    ping = round(bot.latency * 1000,2)
    pyver = sys.version
    pyverF = pyver.split()[0]
    embed = discord.Embed(title="DoxBot Stats", color=0xff6666)
    embed.set_thumbnail(url="https://doxbot.xyz/images/doxlogo2")
    embed.add_field(name="Servers:", value=scount, inline=True)
    embed.add_field(name="Users:", value=users, inline=True)
    embed.add_field(name="Commands:", value="62", inline=True)
    embed.add_field(name="CPU Usage:", value=f"{cpu}%", inline=True)
    embed.add_field(name="Mem. Usage:", value=f"{mem}%", inline=True)
    embed.add_field(name="Ping:", value=f"{ping}ms", inline=True)
    embed.add_field(name="Library:", value="Discord.py", inline=True)
    embed.add_field(name="Py Version:", value=pyverF, inline=True)
    embed.add_field(name="Owner:", value="PapaRaG3#6969", inline=True)
    await ctx.send(embed=embed)

# socials stuff
# socials set
@bot.command()
async def set(message, social, account):
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
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(guildID))
    prefix = cursor.fetchone()
    for pre in prefix:
        if social != "twitter" or "instagram" or "tiktok" or "snapchat" or "spotify" or "youtube" or "twitch" or "steam" or "xbox" or "playstation" or "reddit":
            await message.send(f"That social media is not supported! Please do **{pre}supportedsocials**")
    
# socials get
@bot.command(aliases= ['soc'])
async def socials(ctx, member: discord.Member=None):
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
    
# delete socials
@bot.command(aliases= ['socdel'])
async def socialdelete(ctx, social):
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

# supported socials
@bot.command(aliases= ['suso'])
async def supportedsocials(ctx):
    embed = discord.Embed(title="Supported Social Media's", description="Twitter, Instagram, TikTok, Snapchat, Spotify, YouTube, Twitch, Steam, Xbox, PlayStation, Reddit",color=discord.Color.random())
    await ctx.send(embed=embed)

# social help
@bot.command()
async def socialshelp(ctx):
    cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
    prefix = cursor.fetchone()
    for pre in prefix:
        embed = discord.Embed(title="Socials Help", description="Socials is a system to display your social media's to everyone in the server", color=discord.Color.orange())
        embed.add_field(name=f"{pre}set [social media] [account name]", value="Add a social media to your socials profile", inline=False)
        embed.add_field(name=f"{pre}socials [user]", value=f"Get the socials profile for anyone in the server. Aliases: {pre}soc", inline=False)
        embed.add_field(name=f"{pre}socialdelete [social media]", value=f"Delete one of your social media's from your profile. Aliases: {pre}socdel", inline=False)
        embed.add_field(name=f"{pre}supportedsocials", value=f"See a list of the supported social media's. Aliases: {pre}suso", inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def pecok(ctx):
    guildID = ctx.guild.id
    cursor.execute("SELECT highscore FROM counting WHERE guild_id = '" + str(guildID) + "'")
    high = cursor.fetchone()
    print(high)

# Dad joke 
@bot.command()
async def dadjoke(ctx):
    userName = ctx.author.name
    dadjoke = Dadjoke()
    embed = discord.Embed(title=dadjoke.joke, color=discord.Color.random())
    embed.set_footer(text=f"Requested by {userName}")
    await ctx.send(embed=embed)

# Affirmation command
@bot.command(aliases=['isad', 'aff'])
async def affirmation(ctx):
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

# Nerd Translate
@bot.command(aliases=['ntran'])
async def nerdtranslate(ctx, language, text):
    lang = language
    text = text
    r = requests.get(f'https://api.funtranslations.com/translate/{lang}.json?text={text}')
    res = r.json()
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://api.funtranslations.com/translate/{lang}.json?text={text}') as r:
            res = await r.json()
            transd = res['contents']['translated']
            user = ctx.message.author
            embed = discord.Embed(title=transd, description=f"Language: {lang} Original: {text}", color=discord.Color.random())
            embed.set_footer(text=f"Requested by: {user}")
            await ctx.send(embed=embed)

# website ss
@bot.command()
async def webss(ctx, url):
    embed = discord.Embed(title=f"Screenshot of {url}", color=discord.Color.random())
    embed.set_image(url=f'http://api.screenshotlayer.com/api/capture?access_key=6eec00f3cf74c7691d979b1fd3b73696&url={url}')
    await ctx.send(embed=embed)

# translate
@bot.command(aliases=['tr'])
async def translate(ctx, lang_to, *args):

    lang_to = lang_to.lower()
    if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
        raise commands.BadArgument("Invalid language to translate text to")

    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text

    embed = discord.Embed(title=text_translated, description=text, color=discord.Color.green())
    embed.set_footer(text=f"{ctx.author} | Lang: {lang_to}")

    await ctx.send(embed=embed)

@translate.error
async def translate_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="That is not a supported language", description="Please click [Here](https://cloud.google.com/translate/docs/languages) for a list of supported languages and codes", color=discord.Color.red())
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"{ctx.author} \u200b")
        await ctx.send(embed=embed)

# languages command
@bot.command(aliases=['sl', 'langs'])
async def languages(ctx):
    embed = discord.Embed(title="Supported Languages", url="https://cloud.google.com/translate/docs/languages", description="Please click [Here](https://cloud.google.com/translate/docs/languages) for a list of supported languages and codes", color=discord.Color.random())
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{ctx.author} \u200b")
    await ctx.send(embed=embed)

# say command
@bot.command()
@commands.cooldown(1,2,commands.BucketType.guild)
async def say(ctx, *, message):
    await ctx.send(f"{message}" .format(message))

# time test
@bot.command()
@commands.cooldown(1,2,commands.BucketType.guild)
async def time(ctx):
    embed = discord.Embed(title="Time", color=discord.Color.red())
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text='\u200b')
    await ctx.send(embed=embed)

# roast command
@bot.command(aliases=['insult'])
async def roast(ctx, *, member: discord.Member=None):
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

# short url 
@bot.command(aliases=['surl'])
async def shorturl(ctx, url):
    linkRequest = {
        "destination": url,
        "domain": { "fullName": "rebrand.ly" }
    }

    requestHeaders = {
        "Content-type": "application/json",
        "apikey": os.getenv("SURLAPI")
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

# new dox w api
@bot.command()
async def dox2(ctx, member: discord.Member=None):
    identity = getIdentity()

    if member == None:
        userName = ctx.author.name
    else:
        userName = member.name

    embed = discord.Embed(title=f"Doxing : {userName}...", color=discord.Color.red())
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

# wanted command
from PIL import Image
from io import BytesIO

@bot.command()
async def wanted(ctx, user: discord.Member=None):
    if user == None:
        user = ctx.author
        userID = ctx.author.id
    else:
        user = user
        userID = user.id

    wanted = Image.open("doxbot-beta\wanted.jpg")
    asset = user.avatar_url_as(size = 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((177,177))

    wanted.paste(pfp, (120,212))
    wanted.save(f"profile{userID}.jpg")

    await ctx.send(file=discord.File(f"profile{userID}.jpg"))
    os.remove(f"profile{userID}.jpg")

# qr code generator
@bot.command()
async def qr(ctx, url):

    embed = discord.Embed(title="Original URL", url=url)
    embed.set_image(url=f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url}")

    await ctx.send(embed=embed)

# hex code generator
@bot.command()
async def rcolor(ctx):
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

# love tester
@bot.command()
async def lovetest(ctx, member: discord.Member):

    identity = getIdentity()

    url = "https://love-calculator.p.rapidapi.com/getPercentage"

    querystring = {"fname":f"{member.name}","sname":f"{ctx.author.name}"}

    headers = {
        'x-rapidapi-key': os.getenv("LOVEAPI"),
        'x-rapidapi-host': "love-calculator.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    res = response.json()
    print(res)
    perc = res["percentage"]
    result = res["result"]

    embed = discord.Embed(title="Love Test", color=0xFF00D4)
    embed.add_field(name=result, value=f"Love %: **{perc}%**", inline=False)
    embed.set_footer(text=ctx.author)

    await ctx.send(embed=embed)

# today in history
from datetime import date

@bot.command(aliases=['tih', 'datefact'])
async def todayinhistory(ctx):

    today = date.today()
    d1 = today.strftime("%m/%d")
    
    url = f"https://numbersapi.p.rapidapi.com/{d1}/date"

    querystring = {"fragment":"false","json":"true"}

    headers = {
        'x-rapidapi-key':  os.getenv("TODAYIHAPI"),
        'x-rapidapi-host': "numbersapi.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()

    fact = res['text']
    year = res['year']

    embed = discord.Embed(title="Today in History:", description=f"**In {year},** {fact}", color=discord.Color.random())
    embed.set_footer(text=ctx.author)

    await ctx.send(embed=embed)    

# number facts
@bot.command()
async def numfact(ctx, number):
    url = f"https://numbersapi.p.rapidapi.com/{number}/math"

    querystring = {"fragment":"false","json":"true"}

    headers = {
        'x-rapidapi-key': os.getenv("NUMFACTAPI"),
        'x-rapidapi-host': "numbersapi.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()

    fact = res['text']

    embed = discord.Embed(title="Number Fact:", description=f"**{number}**: {fact}", color=discord.Color.random())
    embed.set_footer(text=ctx.author)

    await ctx.send(embed=embed)

# weather 
@bot.command()
async def weather(ctx, location):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q":f"{location} "}

    headers = {
        'x-rapidapi-key': os.getenv("WEATHERAPI"),
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
    embed.add_field(name="Feels Like:", value=f"{feelsC} ℃ {feelsF} / ℉", inline=True)
    embed.add_field(name="Humidity:", value=f"{humid}%", inline=True)
    embed.add_field(name="Cloud Cov:", value=f"{cloud}%", inline=True)
    embed.add_field(name="Visibility:", value=f"{visKm} Km / {visM} Mi", inline=True)
    embed.add_field(name="UV Index:", value=uv, inline=True)

    await ctx.send(embed=embed)

@weather.error
async def weather_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That is not a valid location")

# Moderation stuff
# ban user
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx,  member: discord.Member, *, reason=None):
    if member == None:
        await ctx.send("You must include a member to ban")
    elif reason == None:
        reason = "None"
    await ctx.send(f"**{member}** Has been banned. Reason: **{reason}**")
    await ctx.guild.ban(member, reason=reason)

# unban user
@bot.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"{user} Has been unbanned")

# kick user
@bot.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == None:
        await ctx.send("Please mention a member to kick")
    elif reason == None:
        reason = "None"
        pass
    await ctx.guild.kick(member, reason=reason)
    await ctx.send(f"**{member}** Has been kicked. Reason: **{reason}**")
    
# add to banned words
@bot.command(aliases = ['bw'])
@commands.has_permissions(administrator = True)
async def banword(ctx, word):
    guildID = ctx.guild.id
    cursor.execute("SELECT command FROM dis_com WHERE guild_id = '" + str(guildID) + "'")
    resultUF = cursor.fetchall()
    for result1 in resultUF:
        for result in result1:
            print(result)
            if result == "banword":
                return
            elif result != "banword":
                cursor.execute("SELECT words FROM banned_words WHERE guild_id = '" + str(guildID) + "'")
                result = cursor.fetchone()
                if result == None:
                    cursor.execute("INSERT INTO `banned_words` (`guild_id`, `words`) VALUES ('" + str(guildID) + "', '" + str(word) + "')")
                    db.commit()
                    await ctx.send("Added word to banned words")
                else:
                    cursor.execute("SELECT words FROM banned_words WHERE guild_id = '" + str(guildID) + "'")
                    wordsUF = cursor.fetchall()
                    for words1 in wordsUF:
                        for words in words1:
                            cursor.execute("UPDATE banned_words SET words = '" + str(word) + ", " + str(words) + "' WHERE guild_id = '" + str(guildID) + "'")
                            db.commit()
                            await ctx.send("Added word to banned words")

# create / set mute role
@bot.command()
@commands.has_permissions(manage_guild = True)
async def muterole(ctx):
    perms = discord.Permissions(send_messages=False, speak=False, stream=False)
    await ctx.guild.create_role(name="muted (DoxBot)", permissions=perms)
    await ctx.send("Created **muted** role. Please update channel permissions for it to work")

# mute users
@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    userID = member.id
    userName = member.name
    mod = ctx.author
    role = discord.utils.get(ctx.guild.roles, name = "muted (DoxBot)")
    await member.add_roles(role)
    await ctx.send(f"**{mod}** muted **{member}** **Reason:** {reason}")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        cursor.execute("SELECT prefix FROM prefixes WHERE guild_id = " + str(ctx.guild.id))
        prefix = cursor.fetchone()
        for pre in prefix:
            await ctx.send(f"Mute role not found. Please use **{pre}muterole**")

# log function
@bot.command()
@commands.has_permissions(administrator=True)
async def setmodlog(ctx, channel: discord.TextChannel):
    guildID = ctx.guild.id
    channelID = channel.id
    cursor.execute("SELECT channel_id FROM modlogs WHERE guild_id = '" + str(guildID) + "'")
    result = cursor.fetchone()
    print(result)
    if result == None:
        cursor.execute("INSERT INTO `modlogs` (`guild_id`, `channel_id`) VALUES ('" + str(guildID) + "', '" + str(channelID) +"')")
        db.commit()
        await ctx.send("Modlog channel set")
    elif result != None: 
        cursor.execute("UPDATE modlogs SET channel_id = '" + str(channelID) + "' WHERE guild_id = '" + str(guildID) + "'")
        db.commit()
        await ctx.send("Modlog channel set")

# message delete
@bot.event
async def on_message_delete(message):
    user = message.author
    pfp = message.author.avatar_url
    guildID = message.guild.id
    delChanName = message.channel.name
    userID = message.author.id

    cursor.execute("SELECT channel_id FROM modlogs WHERE guild_id = '" + str(guildID) + "'")
    channelUF = cursor.fetchone()
    if channelUF == None:
        pass
    else:
        for channelID in channelUF:

            channelSend = bot.get_channel(channelID)

            embed = discord.Embed(title=f"Message deleted in #{delChanName}", description=message.content, color=discord.Color.red())
            embed.set_author(name=user, icon_url=pfp)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"ID: {userID} \u200b")

            await channelSend.send(embed = embed)

# message edit
@bot.event
async def on_message_edit(before, after):
    user = before.author
    pfp = before.author.avatar_url
    guildID = before.guild.id
    delChanName = before.channel.name
    userID = before.author.id

    cursor.execute("SELECT channel_id FROM modlogs WHERE guild_id = '" + str(guildID) + "'")
    channelUF = cursor.fetchone()
    if channelUF == None:
        pass
    else:
        for channelID in channelUF:

            channelSend = bot.get_channel(channelID)

            embed = discord.Embed(title=f"Message edited in #{before.channel.name}", color=discord.Color.blue())
            embed.add_field(name=f"Before: {before.content}", value=f"After: {after.content}", inline=False)
            embed.set_author(name=user, icon_url=pfp)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"ID: {userID} \u200b")

            await channelSend.send(embed = embed)

# channel delete
@bot.event
async def on_guild_channel_delete(channel):
    guildID = channel.guild.id

    cursor.execute("SELECT channel_id FROM modlogs WHERE guild_id = '" + str(guildID) + "'")
    channelUF = cursor.fetchone()
    if channelUF == None:
        pass
    else:
        for channelID in channelUF:

            channelSend = bot.get_channel(channelID)

            embed = discord.Embed(title=f"Channel Deleted", color=discord.Color.red())
            embed.add_field(name=f"Name: {channel.name}", value=f"Category: {channel.category}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"ID: {channel.id} \u200b")

            await channelSend.send(embed = embed)

# channel create
@bot.event
async def on_guild_channel_create(channel):
    guildID = channel.guild.id

    cursor.execute("SELECT channel_id FROM modlogs WHERE guild_id = '" + str(guildID) + "'")
    channelUF = cursor.fetchone()
    if channelUF == None:
        pass
    else:
        for channelID in channelUF:

            channelSend = bot.get_channel(channelID)

            embed = discord.Embed(title=f"Channel Deleted", color=discord.Color.green())
            embed.add_field(name=f"Name: {channel.name}", value=f"Category: {channel.category}")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"ID: {channel.id} \u200b")
            
            await channelSend.send(embed = embed)

# channel update
@bot.event
async def on_guild_channel_update(before, after):
    guildID = before.guild.id

    cursor.execute("SELECT channel_id FROM modlogs WHERE guild_id = '" + str(guildID) + "'")
    channelUF = cursor.fetchone()
    if channelUF == None:
        pass
    else:
        for channelID in channelUF:

            channelSend = bot.get_channel(channelID)

            embed = discord.Embed(title=f"Channel Updated", color=0xddbd4d)
            embed.add_field(name=f"Name After: {after.name}", value=f"Name Before: {before.name}", inline=False)
            embed.add_field(name=f"Category After: {before.category}", value=f"Category Before: {before.category}", inline=False)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f"ID: {before.id} \u200b")
            
            await channelSend.send(embed = embed)

# notes system
# set notes command
@bot.command()
@commands.has_permissions(administrator=True)
async def setnote(ctx, member: discord.Member, *, note):
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

@setnote.error
async def setnote_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please either mention a user to set the note or include a note message")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# get notes command
@bot.command()
@commands.has_permissions(administrator=True)
async def notes(ctx, member: discord.Member):
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

@notes.error
async def notes_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("That user has no notes")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user to get their notes")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# delete specific note
@bot.command()
@commands.has_permissions(administrator=True)
async def deletenote(ctx, noteID):
    guildID = ctx.guild.id
    cursor.execute(f"DELETE FROM `notes` WHERE guild_id = '{guildID}' AND note_id = '{noteID}'")
    db.commit()
    await ctx.send(f"Deleted note {noteID}")

@deletenote.error
async def deletenote_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include a note ID. Use `notes [user]` to get note ID's")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# clear notes
@bot.command()
@commands.has_permissions(administrator=True)
async def clearnotes(ctx, member: discord.Member):
    memberID = member.id
    guildID = ctx.guild.id
    if member == ctx.author and member != ctx.guild.owner:
        await ctx.send("You can't clear your own notes! Only the server owner can clear their own notes.")
    else:
        pass
    cursor.execute(f"DELETE FROM `notes` WHERE user_id = '{memberID}' AND guild_id = '{guildID}'")
    db.commit()
    await ctx.send(f"Cleared notes for **{member}**")

@clearnotes.error
async def clearnotes_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a user to clear their notes")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# bot idea system
@bot.command()
async def botidea(ctx, *, idea):
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
    react = await ideaChannel.send(embed=embed1)
    await react.add_reaction("⬆️")
    await react.add_reaction("⬇️")

    embed2 = discord.Embed(title="Thank you for your idea!", description="For updates on your suggestion, join the support server [HERE](https://discord.gg/zs7UwgBZb9)", color=discord.Color.green())
    await ctx.send(embed=embed2)

# apporve
@bot.command()
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

# idea deny
@bot.command()
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

# bug report
@bot.command()
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

# this person does not exist
from thispersondoesnotexist import get_online_person

@bot.command()
async def doesntexist(ctx):
    userID = ctx.author.id
    picture = await get_online_person() 
    from thispersondoesnotexist import save_picture
    await save_picture(picture, f"doesntexist_{userID}.jpeg")
    await ctx.send("This person does not exist:")
    await ctx.send(file=discord.File(f"doesntexist_{userID}.jpeg"))
    os.remove(f"doesntexist_{userID}.jpeg")

#sex command
@bot.command()
async def sex(ctx, member: discord.Member):
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
                await react.remove_reaction(reaction, user)
    
        except asyncio.TimeoutError:
            await channel.send(f"Sorry, **{authName}**, **{userName}** didn't answer in time... Take that as a no, focus on yourself")
            break

# word assosiation game
# set channel
@bot.command()
@commands.has_permissions(administrator = True)
async def setwordchan(ctx, channel: discord.TextChannel):
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

# get channel
@bot.command()
async def wordchan(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT channel_id FROM wordGame WHERE guild_id = '{guildID}'")
    channelUF = cursor.fetchone()
    if channelUF == None:
        await ctx.send("No channel has been set for the word game! Ask an admin to use `setwordchan [channel]`")
    else:
        for channel in channelUF:
            await ctx.send(f"The word game channel is <#{channel}>")

# get highscore
@bot.command()
async def wordhigh(ctx):
    guildID = ctx.guild.id
    cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = 'wordhigh'")
    cmdCheck = cursor.fetchone()
    if cmdCheck != None:
        return
    else:
        cursor.execute(f"SELECT highscore FROM wordGame WHERE guild_id = '{guildID}'")
        highUF = cursor.fetchone()
        for high in highUF:
            await ctx.send(f"The high score for this server is **{high}**")

# word game info
@bot.command()
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

# command toggle system
# disable command
@bot.command()
async def disable(ctx, command):
    guildID = ctx.guild.id
    modID = ctx.author.id
    mod = ctx.author
    if command == "disable":
        await ctx.send("You can't disable the disable commnand silly")
    elif command == "enable":
        await ctx.send("You can't disable the enable command silly")
    else:
        cursor.execute(f"SELECT command FROM dis_cmds WHERE guild_id = {guildID} AND command = '{command}'")
        cmdUF = cursor.fetchone()
        if cmdUF == None:
            cursor.execute(f"INSERT INTO `dis_cmds` (`guild_id`, `mod_id`, `command`) VALUES ('{guildID}', '{modID}', '{command}')")
            db.commit()
            await ctx.send(f"**{mod}** Disabled the **{command}** command")
        else:
            await ctx.send("That command is already disabled")

@disable.error
async def disable_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")


# enable command
@bot.command()
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

@enable.error
async def enable_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have permission to use that command")

# list disabled 
@bot.command()
async def disabledcmds(ctx):
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

@disabledcmds.error
async def disabledcmds_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("There are no disabled commands for the server")
           
# economy stuff
# balance
@bot.command(aliases = ['bal'])
@commands.cooldown(1, 3, commands.BucketType.user)
async def balance(ctx, member: discord.Member = None):
    guildID = ctx.guild.id
    if member == None:
        user = ctx.author
        userID = ctx.author.id
        cursor.execute(f"SELECT coins FROM econ WHERE guild_id = {guildID} AND user_id = {userID}")
        balUF = cursor.fetchone()
        if balUF == None:
            await ctx.send(f"**{user}** You **0** Dox Coins")
        else:
            for bal in balUF:
                await ctx.send(f"**{user}** You have **{bal}** Dox Coins")
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

@balance.error
async def balance_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Woah there!", description="Take a breather! Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# beg
@bot.command()
@commands.cooldown(1, 120, commands.BucketType.user)
async def beg(ctx):
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

@beg.error
async def beg_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Woah there!", description="Quit beggin! Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# daily 
@bot.command()
@commands.cooldown(1, 86400, commands.BucketType.member)
async def daily(ctx):
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
    
@daily.error
async def daily_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = error.retry_after / 3600
        embed = discord.Embed(title="Slow it down!", description="You can do that in **{:.0f}** hours".format(cooldown))
        await ctx.send(embed=embed)

# fish
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def fish(ctx):
    
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

@fish.error
async def fish_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Woah there!", description="Chill out! Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# shop command
@bot.command()
async def shop(ctx):
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

# buy commands
@bot.group(name='buy', invoke_without_command=True)
async def buy_cmd(ctx):
    await ctx.send("Please use a shop number to buy an item. `shop` for items")

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

# gift 
@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def gift(ctx, user: discord.User, coins: int):
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

@gift.error
async def gift_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Woah there!", description="Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# high low
# new
@bot.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def highlow(ctx):
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
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Hey hey hey!", description="Take a breather! Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)

# richest
@bot.command()
async def richest(ctx):
    guildID = ctx.guild.id
    userID = ctx.author.id
    guildName = ctx.guild.name

    cursor.execute(f"SELECT MAX(coins) FROM econ WHERE guild_id = {guildID}")
    coinsUF = cursor.fetchone()

    if coinsUF == None:
        coins = 0
        await ctx.send("No one in this server has any Dox Coins")
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

# slot machines
@bot.command(aliases=['slot', 'slotmachine'])
@commands.cooldown(1, 3, commands.BucketType.member)
async def slots(ctx, amount: int):
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

    emoji_list = ['🎉','💎','🏆']
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

    embed = discord.Embed(title=f"{userName}'s Slots", description=f"**>** {emoji1} {emoji2} {emoji3} **<**", color=discord.Color.random())
    if win == 3:
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

@slots.error
async def slot_error(ctx, error):
    print(error)
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Hey hey hey!", description="Take a breather! Try again in {:.2f}s".format(error.retry_after))
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include an amount of coins to gamble!")

# rock paper sissors
@bot.command()
async def rps(ctx, amount: int, move):
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

# rob stuff
@bot.command()
async def rob(ctx, user: discord.User):
    guildID = ctx.guild.id
    victID = user.id
    vict = user
    authID = ctx.author.id
    auth =  ctx.author
    percent_take = random.randint(1,50) / 100
    success_perc = random.randint(1,100)
    criminals = 1
    bail_perc = random.randint(5, 25) / 100

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
            #msg = await bot.wait_for('message', timeout=60.0, check=check)
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
                return
            elif success == False:
                bail_cost = round(crimBal * bail_perc, 0)
                crimBal -= bail_cost
                cursor.execute(f"UPDATE econ SET coins = {crimBal} WHERE guild_id = {guildID} AND user_id = {authID}")
                db.commit()
                failEmbed = discord.Embed(title="The Robbery Was a Failure!", description=f"{auth.mention} was arrested and had to pay **{bail_cost}** DXC", color=discord.Color.red())
                await ctx.send(embed=failEmbed)
                return
    #elif criminals > 1:
        #take / criminals
        #if criminals == 2:
            #if success_perc >= 1 and success_perc <= 20:
                #success = True
                #pass
            #else:
                #success = False
                #pass

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
@commands.has_permissions(administrator=True)
async def setstarboard(ctx, channel: discord.TextChannel):
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

# set thresh
@bot.command()
@commands.has_permissions(administrator=True)
async def starthresh(ctx, thresh: int):
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
async def highstar(ctx):
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

# server stats
# setup
@bot.command()
@commands.has_permissions(administrator=True)
async def statsetup(ctx):
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
    elif member.bot == True and botChanID != 0:
        await botChan.edit(name=f"Bots: {botCount}")
        return
    elif member.bot != True and humanChanID != 0:
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
    elif member.bot == True and botChanID != 0:
        await botChan.edit(name=f"Bots: {botCount}")
        return
    elif member.bot != True and humanChanID != 0:
        await humanChan.edit(name=f"Humans: {humanCount}")

# reset counters
@bot.command()
@commands.has_permissions(administrator=True)
async def statsreset(ctx):
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

# disable counters
@bot.command()
@commands.has_permissions(administrator=True)
async def removecounter(ctx, counter):
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

# add counter
@bot.command()
@commands.has_permissions(administrator=True)
async def addcounter(ctx, counter):
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

# counters
@bot.command()
async def counters(ctx):
    embed = discord.Embed(title="Server Stats Counters:", color=discord.Color.random())
    embed.add_field(name="all", value="This counter counts all members in your server, bots and humans", inline=False)
    embed.add_field(name="humans", value="This counter counts all the humans in your server", inline=False)
    embed.add_field(name="bots", value="This counter counts all the bots in your server", inline=False)

    await ctx.send(embed=embed)

# custom embed
@bot.command()
async def embed(ctx, *, title):
    title = ctx.message.content.split("title= ")
    embed = discord.Embed(title=title)
    await ctx.send(embed=embed)

# jepordy system
@bot.command()
async def jepordy(ctx):

    r = requests.get("http://jservice.io/api/random")
    res = r.json()
    
    question = res[0]['question']
    answer = res[0]['answer']
    reward = res[0]['value']
    category = res[0]['category']['title']

    embed = discord.Embed(title="Jepordy", description=f"**Category:** {category}\n**Points:** {reward}\n\n**Question:** {question}", color=discord.Color.blue())
    embed.set_footer(text="You have 30 seconds to answer. Respond with 'Who is [answer]'")

    await ctx.send(embed=embed)

    def check(m):
        return m.content == f'Who is {answer}' and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message',  timeout=30, check=check)
    except asyncio.TimeoutError:
        await ctx.send(f"You didn't get the correct answer in time! The answer was **{answer}**")
    else:
        await ctx.send(f'Correct! You recieved **{reward}** points')

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

@sfx_cmd.command(name="bazinga")
async def bazinga_subcom(ctx):
    await play_file(ctx, "sounds/bazinga.mp3")

@sfx_cmd.command(name="justdoit")
async def justdoit_subcom(ctx):
    await play_file(ctx, "sounds/justdoit.mp3")

@sfx_cmd.command(name="clap")
async def clap_subcom(ctx):
    await play_file(ctx, "sounds/clap.mp3")

@sfx_cmd.command(name="oof")
async def oof_subcom(ctx):
    await play_file(ctx, "sounds/oof.mp3")

@sfx_cmd.command(name="nope")
async def nope_subcom(ctx):
    await play_file(ctx, "sounds/nope.mp3")

@sfx_cmd.command(name="suspense")
async def suspense_subcom(ctx):
    await play_file(ctx, "sounds/suddensus.mp3")

@sfx_cmd.command(name="sad")
async def sad_subcom(ctx):
    await play_file(ctx, "sounds/sadmusic.mp3")

@sfx_cmd.command(name="gay")
async def gay_subcom(ctx):
    await play_file(ctx, "sounds/hagay.mp3")

@sfx_cmd.command(name="fail")
async def fail_subcom(ctx):
    await play_file(ctx, "sounds/fail.mp3")

@sfx_cmd.command(name="no")
async def no_subcom(ctx):
    await play_file(ctx, "sounds/no.mp3")

@sfx_cmd.command(name="godno")
async def godno_subcom(ctx):
    await play_file(ctx, "sounds/godno.mp3")

@sfx_cmd.command(name="dootstorm")
async def dootstorm_subcom(ctx):
    await play_file(ctx, "sounds/dootstorm.mp3")

@sfx_cmd.command(name="wtf")
async def wtf_subcom(ctx):
    await play_file(ctx, "sounds/WTF.mp3")

@sfx_cmd.command(name="fuckedup")
async def fuckedup_subcom(ctx):
    await play_file(ctx, "sounds/fuckedup.mp3")

@sfx_cmd.command(name="ohno")
async def ohno_subcom(ctx):
    await play_file(ctx, "sounds/ohno.mp3")

@sfx_cmd.command(name="ohhh")
async def ohhh_subcom(ctx):
    await play_file(ctx, "sounds/ohhh.mp3")

@sfx_cmd.command(name="thuglife")
async def thuglife_subcom(ctx):
    await play_file(ctx, "sounds/thuglife.mp3")

@sfx_cmd.command(name="djhorn")
async def djhorn_subcom(ctx):
    await play_file(ctx, "sounds/djhorn.mp3")

@sfx_cmd.command(name="phintro")
async def phintro_subcom(ctx):
    await play_file(ctx, "sounds/phintro.mp3")

@sfx_cmd.command(name="memereview")
async def memereview_subcom(ctx):
    await play_file(ctx, "sounds/meme-review.mp3")

@sfx_cmd.command(name="spongebob")
async def spongebob_subcom(ctx):
    await play_file(ctx, "sounds/spongebob.mp3")

@sfx_cmd.command(name="mariocoin")
async def mariocoin_subcom(ctx):
    await play_file(ctx, "sounds/mario_coin.mp3")

@sfx_cmd.command(name="honk")
async def honk_subcom(ctx):
    await play_file(ctx, "sounds/honk.mp3")

@sfx_cmd.command(name="goodone")
async def goodone_subcom(ctx):
    await play_file(ctx, "sounds/good-one.mp3")

@sfx_cmd.command(name="crickets")
async def crickets_subcom(ctx):
    await play_file(ctx, "sounds/crickets.mp3")

@sfx_cmd.command(name="jumpscare")
async def jumpscare_subcom(ctx):
    await play_file(ctx, "sounds/jump-scare.mp3")

@sfx_cmd.command(name="deez")
async def deez_subcom(ctx):
    await play_file(ctx, "sounds/nuts.mp3")

@sfx_cmd.command(name="door")
async def door_subcom(ctx):
    await play_file(ctx, "sounds/door.mp3")

@sfx_cmd.command(name="fart")
async def fart_subcom(ctx):
    await play_file(ctx, "sounds/fart.mp3")

# mining system 
@bot.command()
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

    # chance that user falls in lava
    lava_chance = random.randint(1, 1000000)
    if lava_chance == 1:
        balN = bal - 1000
        cursor.execute(f"UPDATE econ SET pickAxe_type = '', pickAxe_dura = 0, coins = {balN} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        embed = discord.Embed(title="OH NO!", color=discord.Color.red())
        embed.add_field(name="You fell in lava!!", value="There a 0.0001% chance of that happening!! You lost your pickaxe and 1000 DXC!", inline=False)
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

# leveling system
# check rank
@bot.command()
async def rank(ctx, *, user:discord.User = None):
    #level 1 = 0-150 level 2 = 151-400 level 3 = 401-700 level 4 = 701-1200 levl 5 = 1201-2000
    if user == None:
        user = ctx.author
        pass
    elif user != None:
        user = user
        pass
    guildID = ctx.guild.id

    cursor.execute(f"SELECT xp FROM levels WHERE guild_id = {guildID} AND user_id = {user.id}")
    xpUF = cursor.fetchone()
    if xpUF == None:
        xp = 0
        pass
    elif xpUF != None:
        xpUF = xpUF
        for xp in xpUF:
            pass

    cursor.execute(f"SELECT level FROM levels WHERE guild_id = {guildID} AND user_id = {user.id}")
    levelUF = cursor.fetchone()
    if levelUF == None:
        level = 0
        pass
    elif levelUF != None:
        levelUF = levelUF
        for level in levelUF:
            pass
    
    cursor.execute(f"SELECT level FROM levels WHERE guild_id = {guildID}")
    ranksUF = cursor.fetchall()
    print(ranksUF)

    embed = discord.Embed(title=f"Rank Card")
    embed.set_author(name=user, icon_url=user.avatar_url)
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text=f"{ctx.author} \u200b")

    if level == 0:
        levelIn = 1
        levelXp = 1
        embed.add_field(name=f"Level: 0", value=f"XP: 0")
    elif level == 1:
        levelIn = xp - 1
        levelXp = 150 - 1
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 150")
        pass
    elif level == 2:
        levelIn = xp - 151
        levelXp = 400 - 151
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 400")
        pass
    elif level == 3:
        levelIn = xp - 401
        levelXp = 700 - 401
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 700")
        pass
    elif level == 4:
        levelIn = xp - 701
        levelXp = 1200 - 701
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 1200")
        pass
    elif level == 5:
        levelIn = xp - 1201
        levelXp = 2000 - 1201
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 2000")
        pass
    elif level == 6:
        levelIn = xp - 2001
        levelXp = 3000 - 2001
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 3000")
        pass
    elif level == 7:
        levelIn = xp - 3001
        levelXp = 45000 - 3001
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 4500")
        pass
    elif level == 8:
        levelIn = xp - 4501
        levelXp = 6750 - 4501
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 6750")
        pass
    elif level == 9:
        levelIn = xp - 6751
        levelXp = 8750 - 6751
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 8750")
        pass
    elif level == 10:
        levelIn = xp - 8750
        levelXp = 10000 - 8750
        embed.add_field(name=f"Level: {level}", value=f"XP: {xp} / 10000")
        pass

    boxes = int((levelIn/levelXp)*10)

    embed.add_field(name="Level Progress", value=boxes * ":blue_square:" + (10-boxes) * ":white_large_square:", inline=False)

    await ctx.send(embed=embed)

# xp group
@bot.group(name='xp', invoke_without_command=True)
async def xp_cmd(ctx):
    embed = discord.Embed(title="XP Commands", color=discord.Color.random())
    embed.add_field(name="xp give [user] [amount]", value="Use this to give some (or all) of your XP to another user")
    await ctx.send(embed=embed)

# give xp
@xp_cmd.command(name='give')
async def give_subcom(ctx, user: discord.User, amount: int):
    guildID = ctx.guild.id
    authID = ctx.author.id
    userID = user.id
    authMen = ctx.author.mention
    userMen = user.mention
    auth = ctx.author

    cursor.execute(f"SELECT xp FROM levels WHERE user_id = {authID} AND guild_id = {guildID}")
    authXpUF = cursor.fetchone()
    if authXpUF == None:
        await ctx.send("You don't have any XP! Please send some messages to get some")
        return
    elif authXpUF != None:
        for authXp in authXpUF:
            pass
    
    cursor.execute(f"SELECT xp FROM levels WHERE user_id = {userID} AND guild_id = {guildID}")
    userXpUF = cursor.fetchone()
    if userXpUF == None:
        userXp = 0 
        pass
    elif userXpUF != None:
        for userXp in userXpUF:
            pass

    if authXp < amount:
        await ctx.send(f"{authMen}, you do not have {amount} XP you have **{authXp}**")
        return
    
    else:
        react = await ctx.send(f"{authMen} are you sure you want to give {userMen} **{amount}** XP? You have 1 minute to answer.")
        await react.add_reaction('✅')
        await react.add_reaction('❌')
        def check(reaction,user):
            return user == auth and str(reaction.emoji) in ["✅", "❌"]
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                if user == bot.user:
                    break
                else:
                    if str(reaction.emoji) == "✅":
                        authXp -= amount
                        userXp += amount
                        cursor.execute(f"UPDATE levels SET xp = {authXp} WHERE user_id = {authID} AND guild_id = {guildID}")
                        db.commit()
                        cursor.execute(f"UPDATE levels SET xp = {userXp} WHERE user_id = {userID} AND guild_id = {guildID}")
                        db.commit()

                        await ctx.send(f"Successfully transfered **{amount}** XP from {authMen} to {userMen}")
                        break
                    
                    elif str(reaction.emoji) == "❌":
                        await ctx.send("Transfer Canceled.")
                        break

                    else:
                        await message.remove_reaction(reaction, user)
            
            except asyncio.TimeoutError:
                await ctx.send(f"Transfer Canceled. **{auth}** Didn't answer in time")
                break

# add xp (owner)
@xp_cmd.command(name="add")
async def addxp_subcom(ctx, user: discord.User=None, amount: int=0):
    guildID = ctx.guild.id
    
    if ctx.author.id != owner_id:
        await ctx.send("Only the bot owner (PapaRaG3#6969) can do that!")
        return
    elif ctx.author.id == owner_id:
        pass

    if user == None:
        user = ctx.author.id
        pass
    elif user != None:
        user = user 
        pass    
    
    cursor.execute(f"SELECT xp FROM levels WHERE guild_id = {guildID} AND user_id = {user.id}")
    xpUF = cursor.fetchone()

    if xpUF == None:
        xp = 0
        xpIn = xp + amount
        cursor.execute(f"INSERT INTO `levels` (`guild_id`, `user_id`, `xp`, `level`) VALUES ('{guildID}', '{user.id}', '{xpIn}', '0')")
        db.commit()
        pass
    else:
        for xp in xpUF:
            xpIn = xp + amount
            cursor.execute(f"UPDATE levels SET xp = {xpIn} WHERE guild_id = {guildID} AND user_id = {user.id}")
            db.commit()
            pass
    
    await ctx.send(f"Successfully gave **{amount}** XP to {user.mention}")

# set xp msg channel
@xp_cmd.command(name="msgchannel")
async def levelchan_subcom(ctx, channel: discord.TextChannel):
    guildID = ctx.guild.id

    cursor.execute(f"SELECT msg_chan FROM level_stngs WHERE guild_id = {guildID}")
    chanCheckUF = cursor.fetchone()
    if chanCheckUF == None or chanCheckUF == ('',):
        cursor.execute("INSERT INTO `level_stngs` (`guild_id`, `msg_chan`, `level_msg`, `xp_rate`) VALUES ('" + str(guildID) + "', '" + str(channel.id) + "', 'Congrats {msg.author.mention}, you just leveled up to level **1**', '15')")
        db.commit()
        pass
    elif chanCheckUF != None or chanCheckUF != ('',):
        cursor.execute(f"UPDATE level_stngs SET msg_chan = {channel.id} WHERE guild_id = {guildID}")
        db.commit()
        pass
    await ctx.send(f"Set level up message channel to <#{channel.id}>")

# set xp msg
@xp_cmd.command(name="levelmsg")
async def levelmsg_subcom(ctx, *, msg):
    guildID = ctx.guild.id

    cursor.execute(f"SELECT level_msg FROM level_stngs WHERE guild_id = {guildID}")
    msgCheckUF = cursor.fetchone()
    if msgCheckUF == None or msgCheckUF == ('',):
        cursor.execute("INSERT INTO `level_stngs` (`guild_id`, `msg_chan`, `level_msg`, `xp_rate`) VALUES ('" + str(guildID) + "', '', '{msg.author.mention} " + str(msg) + "', '15')")
        db.commit()
        pass
    elif msgCheckUF != None or msgCheckUF != ('',):
        cursor.execute("UPDATE level_stngs SET level_msg = {msg.author.mention} " + str(msg) + "")
        db.commit()
        pass
    await ctx.send("Set the level up message!")

#birthday stuff
# set birthday
@bot.command()
async def setbday(ctx, bday):
    guildID = ctx.guild.id
    userID = ctx.author.id

    cursor.execute(f"SELECT bday FROM bday WHERE guild_id = {guildID} AND user_id = {userID}")
    bdayCheckUF = cursor.fetchone()
    if bdayCheckUF == None or bdayCheckUF == ('',):
        cursor.execute(f"INSERT INTO `bday` (`guild_id`, `user_id`, `bday`) VALUES ('{guildID}', '{userID}', '{bday}')")
        db.commit()
        pass
    else:
        cursor.execute(f"UPDATE bday SET bday = {bday} WHERE guild_id = {guildID} AND user_id = {userID}")
        db.commit()
        pass
    await ctx.send(f"Birthday set to **{bday}**")

# bday view
@bot.command()
async def viewbday(ctx, user: discord.User=None):
    guildID = ctx.guild.id

    if user == None:
        user = ctx.author
        pass
    else:
        user = user

    userID = user.id

    cursor.execute(f"SELECT bday FROM bday WHERE guild_id = {guildID} AND user_id = {userID}")
    bdayUF = cursor.fetchone()
    if bdayUF == None:
        await ctx.send(f"{user} has no birthday set!")
        return
    else:
        for bday in bdayUF:
            await ctx.send(f"**{user}'s** birthday is **{bday}**")

# get the amount of all commands used
@bot.command()
async def allcmds(ctx):
    cursor.execute("SELECT SUM(used) FROM commands")
    sumAllUF = cursor.fetchall()
    sumAll = sumAllUF[0][0]
    await ctx.send(sumAll)

# cringe command
@bot.command()
async def cringe(ctx, user: discord.User=None):
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

# hand written 
import pywhatkit as kit

@bot.command()
async def hand(ctx, *text):
    pywhatkit.text_to_handwriting(text, rgb=(0,0,0))
    await ctx.send(file=discord.File("pywhatkit.png"))

#urban dict
@bot.command()
async def urban(ctx, *term):
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

# leaderboards
@bot.group(name="leaderboard", invoke_without_command=True)
async def lead_cmd(ctx):
    embed = discord.Embed(title="Leaderboard Commands", description="To use: type `leaderboard [name]` the names are down below", color=discord.Color.random())
    embed.add_field(name="coins", value="Get the leaderboard for coins in your server", inline=False)
    await ctx.send(embed=embed)

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

# Akinator
import akinator 

@bot.group(name="aki", invoke_without_command=True)
async def aki_cmd(ctx):
    embed = discord.Embed(title="Akinator Commands", color=discord.Color.random())
    embed.add_field(name="1. start", value="Use this to start a game", inline=False)
    embed.add_field(name="2. answers", value="Use this to see valid answers to Akinators questions", inline=False)
    
    await ctx.send(embed=embed)

@aki_cmd.command(name="start")
async def aki_start_subcom(ctx):
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
                if aki.progression <= 80:
                    def check3(m):
                        return m.content == 'yes' or m.content == 'no' or m.content == 'back'  or m.content == 'idk'  or m.content == 'probably'  or m.content == 'probably not' or m.content == 'y'  or m.content == 'n'  or m.content == 'b'  or m.content == 'i'  or m.content == 'p'  or m.content == 'pn' and m.channel == ctx.channel and m.author == ctx.author
                    while True:
                        try:
                            winFailTry2 = await bot.wait_for('message', timeout=60.0, check=check3)
                        except asyncio.TimeoutError:
                            await ctx.send("You didn't answer in time, I guess I win?")
                            gamesWon += 1
                            cursor.execute(f"UPDATE `aki_stats` SET `won`={gamesWon}")
                            db.commit()
                            break 
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
                                if win == True:
                                    print("p")

                                gamesLost += 1
                                cursor.execute(f"UPDATE `aki_stats` SET `lost`={gamesLost}")
                                db.commit()
                                LossEmbed = discord.Embed(title="Dang! You Won...", description=f"I've lost **{gamesLost}** games", color=discord.Color.red())
                                await ctx.send(embed=LossEmbed)
                                break
               
@aki_cmd.command(name="answers")
async def aki_ans_subcom(ctx):
    embed = discord.Embed(title="Valid Akinator Answers", description="yes/y, no/n, idk/i, probably/p, probably not/pn, back/b", color=discord.Color.random())
    await ctx.send(embed=embed)

# buttons
@bot.command()
async def button(ctx): 
    await buttons.send(
        content = "this is a message",
        channel = ctx.channel.id,
        components =  [
            ActionRow([
                Button(
                    label = "A button",
                    style = ButtonType().Primary,
                    custom_id = "b1",
                ),
                Button(
                    label = "Another one",
                    style = ButtonType().Secondary,
                    custom_id = "b2",
                ),
                Button(
                    label = "Send a nuke",
                    style = ButtonType().Danger,
                    custom_id = "b3",
                ),
                Button(
                    emoji = {
                        "id": None,
                        "name": "🙃",
                        "animated": False
                    },
                    disabled = True,
                    custom_id = "b4",
                )
            ])
        ]
    )

@buttons.click
async def b1(ctx):
    await ctx.reply(content="penis", flags=MessageFlags().EPHEMERAL)

@buttons.click
async def b2(ctx):
    await ctx.reply(content="penis", flags=MessageFlags().EPHEMERAL)

@buttons.click
async def b3(ctx):
    await ctx.reply(content="penis", flags=MessageFlags().EPHEMERAL)

@buttons.click
async def b4(ctx):
    await ctx.reply(content="penis", flags=MessageFlags().EPHEMERAL)

# vote
@bot.command()
@commands.cooldown(1,1,commands.BucketType.guild)
async def vote(ctx):
    await buttons.send(
        content = "Vote Here..",
        channel = ctx.channel.id,
        components = [
            ActionRow([
                Button(
                    label = "Top.gg",
                    style = ButtonType().Link,
                    url = "https://top.gg/bot/800636967317536778/vote"
                ),
                Button(
                    label = "botsfordiscord.com",
                    style = ButtonType().Link,
                    url = "https://botsfordiscord.com/bot/800636967317536778/vote"
                ),
                Button(
                    label = "discordbotlist.com",
                    style = ButtonType().Link,
                    url = "https://discordbotlist.com/bots/doxbot/upvote"
                ),
            ])
        ]
    )

@bot.command()
async def testies(message):
    guildID = message.guild.id
    await message.send(guildID)

# slash commands
from discord_slash import SlashCommand

slash = SlashCommand(bot)

slashGuildID = [801360477984522260]

@slash.slash(name="test", description="Displays your pfp")
async def pfp(ctx):
    await ctx.send("penis")

@slash.slash(name="meme", description="Sends a random meme from a selection of SubReddits")
async def s_meme(ctx):
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

# slash command w params
from discord_slash.utils.manage_commands import create_option

@slash.slash(name="param", 
            guild_ids=slashGuildID,
            description="slash cmd w params.",
            options=[
                create_option(
                    name="User",
                    description="User to dox", 
                    option_type=2,
                    required=False
                )
            ])
async def params(ctx, option1: str = None):
    if option1 == None:
        option1 = "none"
    await ctx.send(content=f"I got you, you said {option1}")

# dox slash
@slash.slash(name="pee", guild_ids=slashGuildID, description="Use this to get 100% real info about someone wink wink.", options=[create_option(name="User",description="Who you want to dox, if left blank, you will be doxxed",option_type=2,required=False)])
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

# ticket system
@bot.command()
async def ticket(ctx):
    tickIDNum = random.randint(1000,9999)
    tickIDLet1 = chr(random.randint(ord('A'), ord('Z')))
    tickIDLet2 = chr(random.randint(ord('A'), ord('Z')))
    tickIDLet3 = chr(random.randint(ord('A'), ord('Z')))
    tickID = str(f"{tickIDLet1}{tickIDLet2}{tickIDLet3}{tickIDNum}")
    




# run bot
print(db)
print("Online")
bot.run(os.getenv('TOKEN'))