import discord
import json, os, logging
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime

class AllianceSetup(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self._last_member = None
        
        current_time = current_time = datetime.now().strftime("%H:%M:%S")
        
        logger.info(f'({current_time}) CLAIMS: Claim Cog Inititialized.')
        
    def setup(bot, logger):
        bot.add_cog(AllianceSetup(bot, logger))
        
    @commands.command()
    async def alliance(self, ctx, *, name=None):
        if name is None:
            print('No Name')
            yield
            
        