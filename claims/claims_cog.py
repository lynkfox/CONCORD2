import discord
import claims.system_match_helper
import json, os, logging
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from utility.utilities import getInvocationInformation, getServerSpecificChannelInfo
from claims import claim_embed_generation as generateEmbed

class Claims(commands.Cog):
    def __init__(self, bot, logger):
        self.bot = bot
        self._last_member = None
        self.RefreshClaimList.start()
        
        current_time = current_time = datetime.now().strftime("%H:%M:%S")
        
        logger.info(f'({current_time}) CLAIMS: Claim Cog Inititialized.')
        
    def setup(bot, logger):
        self.bot.add_cog(Claims(bot, logger))
        
    def cog_unload(self):
        self.RefreshClaimList.cancel()
        
    @commands.command()
    async def claimadmin(self,ctx,*, switcher=None, member:discord.Member = None):
        # claim admin command for adminstrative purposes
        
        # Commands only allowed to work if on Alliance Master Server
        
        if switcher.upper() == "FORCE": # and author == Approved Claim Mod
            print('Force')
            # Check to see if system is Active
            # End claim, require Reason
            # Update DB
            # Update Claim List
            # Delete Invocations
        elif switcher.upper() == "HISTORY": # and author == approved Claim Mod
            print('History')
            # Make sure it has a Member attached
            # check the table for all claims for Member
            # output embed to channel
        elif switcher.upper() == "BASE": # and author == approved Claim Mod
            print('Base')
            # Takes a Region (Cache, Gem-East, Gem-West)
            # Returns the latest reported Base Level and the date it was reported
                
    @commands.command()
    async def claim(self, ctx, *, args):
        # Claim command !claim (followed by the switcher, defaulting to Help if someone does not use one)
        
        
        #split args by " "
        # [0] = Switcher or System
        # if a number then System Level
        # if a member then Deputy
        # otherwise Loot
        # if following * then comment
        
        arg_list = args.split(" ")
        
        switcher = arg_list[0]
        
        base_level = 0
        deputy = None
        comments = "No Comment" # loot or other comments can go here.
        
        for additional_arg in arg_list[1:]:
            if additional_arg.isnumeric():
                base_level = additional_arg
            elif isinstance(additional_arg, discord.Member):
                deputy = additional_arg
            else additional_arg[0] is '*':
                comments = str(arg_list[arg_list.index(additional_arg):])
                break
            
                
        
        if switcher.upper() == "RECLAIM":
            print('Reclaim')
            # Check to see if active claim
            # check to see if within limit of X free reclaims
            # check to see if within T-15 mins of claim ends
            # extend claim to T+2hrs
            # Record Claim in DB
            # Update Claim List
            # Delete Invocations
        elif switcher.upper() == "RELEASE":
            print('Release')
            # Find active claim
            # Remove from Claim list
            # Update DB for Claim Released
            # Update Claim List
            # Delete Invocations
        elif switcher.upper() == "INFO"
            print('Info')
            # Find active system
            # return information in DM about Expires, Deputy, Loot Structure, Comments
        elif switcher.upper() == "HELP":
            print('Help/Default')
            # send HELP dm
            # delete invocations
        else #system Name
            print('Claim')
            # Check if prexisting Claim in DB still hasn't expired for the Same System
            # Make sure that BaseLevel is included - else request (listener)
            # Find matching systems, and request (listener)
            # Initiate a Claim for author
            # Claim system for Time+2 hrs
            # Mark 0 Reclaims
            # Record Claim in DB
            # Update Claim List
            # Delete Invocations
    
    @tasks.loop(seconds=10.0)
    async def RefreshClaimList(self):
        
        # TODO: DynamoDB Search for all unique ServerIDs and their associated master servers
        
        # For each Server in the same Alliance, send a message to their associated claim channels
        
        guild = self.bot.get_guild(int('759960149313585202'))
        server_channels = getServerSpecificChannelInfo(guild)
        
        # TODO: Add a global dictionary of all Regions to be included here (to replace ["Cache"])
        
        system_list = generateEmbed.generateSystems(["Cache"])
        
        # TODO: Loop through each of the systems_lists for each different region and create an embed for each
        embed_description = generateEmbed.generateEmbedDescription(system_list['Cache'])
        
        current_time = current_time = datetime.utcnow()
        
        claim_embed = discord.Embed(Title="Cache System Claims", color=0x40E0D0,
                                    description=embed_description,
                                    timestamp=current_time)
        
        
        messages = await self.bot.get_channel(server_channels.claim_channel).history(limit=100).flatten()
        
        await self.bot.get_channel(server_channels.claim_channel).delete_messages(messages)
            
        await self.bot.get_channel(server_channels.claim_channel).send(embed=claim_embed)