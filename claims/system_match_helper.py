import json

def CleanSystemName(system_name):
    return system_name.replace('-','').upper().replace('0','O').replace('8','B')

def FindSystemMatch(system_name, systems):
    matches = []
    
    for area in systems:
        if len(system_name) == 6 and system_name in systems[area]:
            matches.append(system_name)
            break
        elif len(system_name) <= 6:
            for name in systems[area]:
                if CleanSystemName(system_name) in CleanSystemName(name):
                    matches.append(name) 
                
            
       
    return matches