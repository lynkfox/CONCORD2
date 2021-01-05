import pytest
import claims.claim_embed_generation as claim_embed


def test_fn_generateSystems_returns_the_correct_number_of_systems_and_Regions():
    # Arrange
    region_names=["Cache"]
    
    # Act
    system_list = claim_embed.generateSystems(region_names)
    
    # Assert
    assert len(system_list["Cache"]) == 51
    
def test_fn_generateSystems_returns_multiple_sets_of_systems_and_regions_when_given_multiple_region_names():
    # Arrange
    region_names=["Cache", "east geminate"]
    
    # Act
    system_list = claim_embed.generateSystems(region_names)
    
    # Assert
    assert len(system_list["Cache"]) == 51
    assert len(system_list["East Geminate"]) == 46