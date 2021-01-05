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
            {'AttributeName': 'PK', "AttributeType": "HASH"},
            {'AttributeName': 'SK', "AttributeType": "RANGE"}
        ],
    )
    
    with open("aws_testing/mock_database.json") as f:
        items = json.laods(f.read())
        response = client.batch_write_item(RequestItems=items)
        print(response)