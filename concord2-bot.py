import discord
import os, json, logging, time
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from claims.claims_cog import Claims

# Env Variables for security
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Discord Bot Token

# set the command prefix to bang
bot = commands.Bot(command_prefix='!')

# remove the default help command
bot.remove_command('help')

# logger setup
logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
 
    logger.info(f'({current_time}) ON_READY: {bot.user} has logged in.')
    bot.add_cog(Claims(bot, logger))
    
    servers = list(bot.guilds)
    print("Connected on " + str(len(servers)) + " servers:")
    for server in servers:
        print('   ' + server.name)
        
        
bot.run(TOKEN)