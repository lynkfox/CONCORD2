import json
import discord
import os


def generateSystems(region_names = ['Cache']):
    
    claims = []
    
    for region in region_names:
        file_name = f'{region.lower()}.json'
        
        file_path = os.path.join('claims', 'region_jsons', file_name)
        
        with open(file_path) as f:
            region = json.load(f)
        
        for constellation in region:
            claims.append(f"__*{constellation}*__")
            for system in region[constellation]:
                claims.append(f"'{system}' :yes:")
            
        return claims
    
    