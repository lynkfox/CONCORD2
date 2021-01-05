import json
import discord
import os

def generateSystems(region_names = ['Cache']):
    region_lists = {}
    
    for region in region_names:
        claims = []
        file_name = f'{region.lower().replace(" ", "_")}.json'
        
        file_path = os.path.join('claims', 'region_jsons', file_name)
        
        with open(file_path) as f:
            region_systems = json.load(f)
        
        for constellation in region_systems:
            claims.append(f"__**{constellation}**__\n")
            for system in region_systems[constellation]:
                claims.append(f" `{system}`: \U00002705 \n")
        
        region_name = region.lower().title()
          
        region_lists[region_name] = claims
    
    return region_lists
    
    
def generateEmbedDescription(systems):
        
    description = ""
    
    for entry in systems:
        description += entry
        
    return description
        
    

    