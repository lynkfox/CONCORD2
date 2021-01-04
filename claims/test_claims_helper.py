import pytest
import json
from claims import claim_helper as helper


def test_fn_CleanSystemName_removes_tack():
    # Arrange
    system_name = "B-T2BT"
    
    # Act
    actual_name = helper.CleanSystemName(system_name)
    
    # Assert
    assert actual_name == "BT2BT"
    
def test_fn_CleanSystemName_returns_UPPER():
    # Arrange
    system_name = "abCDe"
    
    # Act
    actual_name = helper.CleanSystemName(system_name)
    
    # Assert
    assert actual_name == "ABCDE"
    
def test_fn_FindSystemMatch_returns_only_one_system_with_full_name():
    # Arrange
    system_name = "2-2EWC"
    
    with open('claims/cache_systems.json') as f:
        cache_systems = json.load(f)
        
    # Act
    
    matches = helper.FindSystemMatch(system_name, cache_systems)
    
    # Assert
    assert len(matches) == 1
    assert "2-2EWC" in matches
    
def test_fn_FindSystemMatch_returns_multiple_systems_With_similar_letter_names_ignoring_tack():
    # Arrange
    search_system = "TT"
    
    with open('claims/cache_systems.json') as f:
        cache_systems = json.load(f)
        
    # Act
    matches = helper.FindSystemMatch(search_system, cache_systems)
    
    assert "RV5-TT" in matches
    assert "W2T-TR" in matches