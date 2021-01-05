import discord
import os, json, logging, time
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
from claims.claims_cog import Claims
from utility.utilities import getInvocationInformation

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
 
    logger.info(f'ON_READY: {bot.user} has logged in.')
    bot.add_cog(Claims(bot, logger))
    
    servers = list(bot.guilds)
    logger.info(f'Connected on {str(len(servers))} servers:')
    for server in servers:
        logger.info(f'   {server.name}')
        
        
@bot.command(name='license')
async def liscence(ctx):
    invoke = getInvocationInformation(ctx)
    
    await invoke.author.send("CONCORD2-Bot is provided under the GNU Affero General Public License v3.0.\n"
                             "You can find the latest code available at: https://github.com/lynkfox/CONCORD2")


bot.run(TOKEN)