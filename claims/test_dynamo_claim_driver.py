import boto3, pytest, discord, collections
from claims import dynamo_claim_driver as claim_driver
from aws_testing import mock_dynamo_setup
from moto import mock_dynamodb2

@mock_dynamodb2
def test_fn_addClaimant_successfully_increases_total_count_of_dynamo_items_by_one():
    # Arrange
    mock_dynamo_setup.setup()
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('testTable')
    
    mock_member = collections.namedtuple('Member', 'display_name id')
    mock_member.display_name = "[TST]Name"
    mock_member.id = "9999999999"
    
    
    # Act
    response = claim_driver.add_Claimant(mock_member, "BT-6BT", 7, table)
    all_items = table.scan()
    
    # Assert
    assert len(all_items["Items"]) == 4
    
    
    