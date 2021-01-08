import boto3
from datetime import datetime, timedelta

# TODO: Change hours=2 to hours = global variable

def add_Claimant(member, system, base, table):
    
    expires = datetime.utcnow().replace(microsecond=0) + timedelta(hours=2)
    expires = expires.isoformat()
    
    PK = "SYSTEM#"+system
    SK = "CLAIMENDS#"+expires
    
    
    
    response = table.put_item(
        Item={
            'PK': PK,
            'SK': SK,
            'Claimant_ID': member.id,
            'Claimant_Tag': member.display_name,
            'System_Name': system,
            'Base_Level': str(base),
            'Reclaim_Number':str(0)
        }
    )
    
    return response

# TODO: Add claimaint to the DB when they !claim [system]
# TODO: Check for current claims active on a system
# TODO: Update current claim to Release it or Reclaim it
# TODO: End Claims that have expired
# TODO: If system is Unclaimed and reclaimed by the same person before original time out, reinstate timeout
# TODO: 