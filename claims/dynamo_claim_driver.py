import boto3, collections
from datetime import datetime, timedelta

# Pulling variables out for future change to allow them to be modable
RECLAIMS = 1
CLAIM_HOURS = 2

def add_Claimant(member, system, base, table, *, deputy=None):
    
    now =datetime.utcnow().replace(microsecond=0)
    expires = now + timedelta(hours=CLAIM_HOURS)
    expiresISO = expires.isoformat()
    nowISO = now.isoformat()
    
    PK = "SYSTEM#"+system
    SK = "CLAIMENDS#"+expiresISO
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
            'Reclaim_Number':str(0),
            'Created_At': nowISO,
            'Updated_at': nowISO,
            'Expires_at': expiresISO,
            'Deputy_ID': deputy_store.id,
            'Deputy_Tag':deputy_store.display_name
        }
    )
    
    return response

# TODO: Add claimaint to the DB when they !claim [system]
# TODO: Check for current claims active on a system
# TODO: Update current claim to Release it or Reclaim it
# TODO: End Claims that have expired
# TODO: If system is Unclaimed and reclaimed by the same person before original time out, reinstate timeout
# TODO: 