import boto3
import discord
import bo

def getServerChannelIDs(ctx):
    guild = ctx.guild
    author = ctx.author
    current_channel = ctx.channel
    
    dynamoPK = "SERVER#"+guild.id
    
    ddb = boto3.resource("dynamodb")
    table = ddb.Table("concord_bot_ee_table")
    table.query()