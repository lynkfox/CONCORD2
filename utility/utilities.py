import boto3
import discord
import collections



def getInvocationInformation(ctx):
    
    # Returns a Named Tupple for use in any command that needs context information - keeps the commands clean and
    
    Invocation = collections.namedtuple('Invocation', 'guild author invoke_msg current_channel is_verified')
    
    # TODO: Connect to dynamodDb and search for  SERVER#guild.id -> get the MasterAlliance flag
    #
    # check if author has verified_role id, set true or false
    verified = True
    # check if author has security_role id, set true or false
    # check if author has claims_admin_role id, set true or false
    # check if server is MasterAlliance server, set true or false
    
    
    
    return Invocation(guild=ctx.guild, author=ctx.author, current_channel=ctx.channel, is_verified=verified, 
                      invoke_msg=ctx.message)
    
def getServerSpecificChannelInfo(guild):
    
    # Returns a Nammed Tupple for use in any function that does NOT have ctx (such as looped/on_ready/on_member_join). 
    
    ServerChannels = collections.namedtuple('ServerChannels', 'claim_channel')
    
    # TODO: Connect to dynamoDB and search for SERVER#guild.id -> get all the channel info
    
    # get guild's modlog channel id, set
    # get guild's claim channel id, set
    claim_id = int('796098452856897597') #test server channel id
    # get guild's bot_console channel id, set
    
    return ServerChannels(claim_channel=claim_id)

    
    
    