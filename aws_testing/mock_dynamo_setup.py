import boto3, botocore, csv, os, sys, json
from moto import mock_dynamodb2

@mock_dynamodb2
def setup():
    # get the Dynamo client
    ddb = boto3.resource("dynamodb")
    
    # initialize a table for mock
    ddb.create_table(
        TableName='testTable',
        AttributeDefinitions=[
            {'AttributeName': 'PK', "AttributeType": "STRING"},
            {'AttributeName': 'SK', "AttributeType": "STRING"}
        ],
        KeySchema=[
            {'AttributeName': 'PK', "KeyType": "HASH"},
            {'AttributeName': 'SK', "KeyType": "RANGE"}
        ],
    )
    
    with open("aws_testing/mock_database.json") as f:
        
        client = boto3.client("dynamodb")
        items = json.loads(f.read())
        response = client.batch_write_item(RequestItems=items)
        print(response)