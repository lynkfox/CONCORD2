import pytest
import json
from claims import system_match_helper as helper


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
    
    with open('claims/region_jsons/cache.json') as f:
        cache_systems = json.load(f)
        
    # Act
    
    matches = helper.FindSystemMatch(system_name, cache_systems)
    
    # Assert
    assert len(matches) == 1
    assert "2-2EWC" in matches
    
def test_fn_FindSystemMatch_returns_multiple_systems_With_similar_letter_names_ignoring_tack():
    # Arrange
    search_system = "TT"
    
    with open('claims/region_jsons/cache.json') as f:
        cache_systems = json.load(f)
        
    # Act
    matches = helper.FindSystemMatch(search_system, cache_systems)
    
    assert "RV5-TT" in matches
    assert "W2T-TR" in matches
    
def test_fn_FindSystemMatch_returns_zero_systems_when_no_matches():
    # Arrange
    search_system = "aa"
    
    with open('claims/region_jsons/cache.json') as f:
        cache_systems = json.load(f)
        
    # Act
    matches = helper.FindSystemMatch(search_system, cache_systems)
    
    assert len(matches) == 0
    
def test_FindSystemMatch_returns_system_when_zero_and_o_transposed():
    # Arrange
    system_name = "0-5TN1" #note the 0(zero) instead of a O
    
    with open('claims/region_jsons/cache.json') as f:
        cache_systems = json.load(f)
        
    # Act
    matches = helper.FindSystemMatch(system_name, cache_systems)
    
    # Assert
    assert "O-5TN1" in matches
    
def test_FindSystemMatch_returns_system_when_eight_and_B_transposed9():
    # Arrange
    system_name = "B-SPNN" #note the B instead of an 8(eight)
    
    with open('claims/region_jsons/cache.json') as f:
        cache_systems = json.load(f)
        
    # Act
    matches = helper.FindSystemMatch(system_name, cache_systems)
    
    # Assert
    assert "8-SPNN" in matches
