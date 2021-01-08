import boto3, collections, botocore
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime, timedelta

# Pulling variables out for future change to allow them to be modable
RECLAIMS = 1
CLAIM_HOURS = 2

def create_timers():
    timer_tuple = collections.namedtuple("Timers", "now expires nowISO expiresISO past pastISO")
    timer_tuple.now =datetime.utcnow().replace(microsecond=0)
    timer_tuple.expires = timer_tuple.now + timedelta(hours=CLAIM_HOURS)
    timer_tuple.expiresISO = timer_tuple.expires.isoformat()
    timer_tuple.nowISO = timer_tuple.now.isoformat()
    timer_tuple.past = timer_tuple.now + timedelta(hours=-CLAIM_HOURS)
    timer_tuple.pastISO = timer_tuple.past.isoformat()
    
    return timer_tuple

def add_Claimant(member, system, base, table, *, deputy=None, comments="None"):
    
    timers = create_timers()
    
    PK = "SYSTEM#"+system
    SK = "CLAIMENDS#"+timers.expiresISO
    deputy_store = collections.namedtuple('Member', 'display_name id')
    
    if deputy is None:
        deputy_store.display_name = "No Deputy"
        deputy_store.id = None
    else:
        deputy_store.display_name = deputy.display_name
        deputy_store.id = deputy.id
    
    response = table.put_item(
        Item={
            'PK': PK,
            'SK': SK,
            'Claimant_ID': member.id,
            'Claimant_Tag': member.display_name,
            'System_Name': system,
            'Base_Level': str(base),
            'Reclaim_Number':0,
            'Created_At': timers.nowISO,
            'Updated_at': timers.nowISO,
            'Expires_at': timers.expiresISO,
            'Deputy_ID': deputy_store.id,
            'Deputy_Tag':deputy_store.display_name,
            'Comments':comments,
            'Active': 'Yes'
        }
    )
    
    return response


def check_Active_Claims(system, table):
    timers = create_timers()
    
    # System to be searching for
    PK = "SYSTEM#"+system 
    
    # Since only one person can ever claim a system, only return the latest claim
    result = table.query(
        KeyConditionExpression=Key('PK').eq(PK),
        Limit=1
    )
    
    result_expires = datetime.fromisoformat(result["Items"][0]["Expires_at"])
    
    if result_expires < timers.past:
        return None
    else:
        claim_info = collections.namedtuple("Claimant", "display_name id system expires deputy_name deputy_id, comments")
        claim_info.display_name = result["Items"][0]["Claimant_Tag"]
        claim_info.id = result["Items"][0]["Claimant_ID"]
        claim_info.expires = result["Items"][0]["Expires_at"]
        claim_info.system = system
        claim_info.deputy_name =result["Items"][0]["Deputy_Tag"]
        if result["Items"][0]["Deputy_Tag"] is "No Deputy":
            claim_info.deputy_id =result["Items"][0]["Deputy_ID"]
        else:
            claim_info.deputy_id = "None"
        claim_info.comments =result["Items"][0]["Comments"]
            
        return claim_info
    
def get_All_Active_Claims(table):
    timers = create_timers()
    
    response = table.scan(
        FilterExpression=Attr('Expires_at').gt(timers.nowISO)
    )
    
    return response

def release_Claim(system, member, table):
    timers = create_timers()
    
    # System to be searching for
    PK = "SYSTEM#"+system 
    
    # Since only one person can ever claim a system, only return the latest claim
    result = table.query(
        KeyConditionExpression=Key('PK').eq(PK),
        Limit=1
    )
    
    

# TODO: Update current claim to Release it or Reclaim it
# TODO: End Claims that have expired
# TODO: If system is Unclaimed and reclaimed by the same person before original time out, reinstate timeout
# TODO: Claim Returns Error if different member tries to claim it
# TODO: Claim returns error if same member tires to claim it
# TODO: Deputy Acceptance for Reclaim and Release