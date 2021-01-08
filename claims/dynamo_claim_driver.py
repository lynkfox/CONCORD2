import boto3
from datetime import datetime, timedelta

# Pulling variables out for future change to allow them to be modable
RECLAIMS = 1
CLAIM_HOURS = 2

def add_Claimant(member, system, base, table):
    
    now =datetime.utcnow().replace(microsecond=0)
    expires = now + timedelta(hours=CLAIM_HOURS)
    expiresISO = expires.isoformat()
    nowISO = now.isoformat()
    
    PK = "SYSTEM#"+system
    SK = "CLAIMENDS#"+expiresISO
    
    
    
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
            'Updated_at': nowISO
        }
    )
    
    return response

# TODO: Add claimaint to the DB when they !claim [system]
# TODO: Check for current claims active on a system
# TODO: Update current claim to Release it or Reclaim it
# TODO: End Claims that have expired
# TODO: If system is Unclaimed and reclaimed by the same person before original time out, reinstate timeout
# TODO: 