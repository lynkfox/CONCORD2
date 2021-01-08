import boto3, pytest, discord, collections, botocore
from boto3.dynamodb.conditions import Key
from claims import dynamo_claim_driver as claim_driver
from aws_testing import mock_dynamo_setup
from moto import mock_dynamodb2
from datetime import datetime, timedelta

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
    
@mock_dynamodb2
def test_fn_addClaimant_successfully_data_to_table_and_can_be_recalled():
    # Arrange
    mock_dynamo_setup.setup()
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('testTable')
    
    mock_member = collections.namedtuple('Member', 'display_name id')
    mock_member.display_name = "[TST]Name"
    mock_member.id = "9999999999"
    
    
    # Act
    response = claim_driver.add_Claimant(mock_member, "BT-6BT", 7, table)
    inserted_item = table.query(
        KeyConditionExpression=Key('PK').eq("SYSTEM#BT-6BT")
    )
    
    # Assert
    assert len(inserted_item["Items"]) == 1
    
@mock_dynamodb2
def test_fn_addClaimant_successfully_is_two_hours_from_insert_time():
    # Arrange
    mock_dynamo_setup.setup()
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('testTable')
    
    mock_member = collections.namedtuple('Member', 'display_name id')
    mock_member.display_name = "[TST]Name"
    mock_member.id = "9999999999"
    
    now =datetime.utcnow().replace(microsecond=0)
    expires = now + timedelta(hours=2)
    expiresISO = expires.isoformat()
    nowISO = now.isoformat()
    
    
    # Act
    response = claim_driver.add_Claimant(mock_member, "BT-6BT", 7, table)
    inserted_item = table.query(
        KeyConditionExpression=Key('PK').eq("SYSTEM#BT-6BT")
    )
    
    # Assert
    assert inserted_item["Items"][0]['SK'] == 'CLAIMENDS#'+expiresISO
    
@mock_dynamodb2
def test_fn_addClaimant_successfully_adds_with_deputy():
    # Arrange
    mock_dynamo_setup.setup()
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('testTable')
    
    mock_member = collections.namedtuple('Member', 'display_name id')
    mock_member.display_name = "[TST]Name"
    mock_member.id = "9999999999"
    
    mock_deputy = collections.namedtuple('Deputy', 'display_name id')
    mock_deputy.display_name = "[TST]Deputy"
    mock_deputy.id = "1111111111"
    
    
    # Act
    response = claim_driver.add_Claimant(mock_member, "BT-6BT", 7, table, deputy=mock_deputy)
    inserted_item = table.query(
        KeyConditionExpression=Key('PK').eq("SYSTEM#BT-6BT")
    )
    
    # Assert
    assert len(inserted_item["Items"]) == 1
    assert inserted_item["Items"][0]["Deputy_Tag"] == mock_deputy.display_name
    
@mock_dynamodb2
def test_fn_checkActiveClaims_returns_claimaint_name_and_expiration_if_one_within_last_two_hours():
    # Arrange
    mock_dynamo_setup.setup()
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('testTable')
    
    mock_member = collections.namedtuple('Member', 'display_name id')
    mock_member.display_name = "[TST]Name"
    mock_member.id = "9999999999"
    
    now =datetime.utcnow().replace(microsecond=0)
    expires = now + timedelta(hours=2)
    expiresISO = expires.isoformat()
    
    # Act
    response = claim_driver.add_Claimant(mock_member, "BT-6BT", 7, table)
    actual_name_response = claim_driver.check_Active_Claims("BT-6BT", table)
    
    assert actual_name_response.display_name == "[TST]Name"
    assert actual_name_response.expires == expiresISO
    
@mock_dynamodb2
def test_fn_checkActiveClaims_returns_none_if_no_active_claim():
    # Arrange
    mock_dynamo_setup.setup()
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('testTable')
    
    mock_member = collections.namedtuple('Member', 'display_name id')
    mock_member.display_name = "[TST]Name"
    mock_member.id = "9999999999"
    
    # Act
    actual_response = claim_driver.check_Active_Claims("B-T6BT", table)
    
    # Assert
    assert actual_response is None
    
@mock_dynamodb2
def test_fn_getAllActiveClaims_returns_all_claims_within_the_active_time():
    # Arrange
    mock_dynamo_setup.setup()
    ddb = boto3.resource('dynamodb')
    table = ddb.Table('testTable')
    
    mock_member = collections.namedtuple('Member', 'display_name id')
    mock_member.display_name = "[TST]Name"
    mock_member.id = "9999999999"
    
    # Act
    response = claim_driver.add_Claimant(mock_member, "BT-6BT", 7, table)
    response = claim_driver.add_Claimant(mock_member, "8-SPNN", 7, table)
    response = claim_driver.add_Claimant(mock_member, "M53-TU", 7, table)
    
    actual_response = claim_driver.get_All_Active_Claims(table)
    
    # Assert
    assert len(actual_response["Items"]) == 3