import pytest, boto3
import aws_testing.mock_dynamo_setup as test_dynamo
from moto import mock_dynamodb2
import os

@pytest.fixture(scope="function")
def aws_credentials():
    # Mocked AWS Credentials for moto
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    
@pytest.fixture(scope="function")
def dynamodb(aws_credentials):
    with mock_dynamodb2():
        yield boto3.client("dynamodb", region_name="us-east-1")
    
@mock_dynamodb2
class TestDynamoDBMockSetup():
    def setup(self):
        test_dynamo.setup()
    
    def teardown(self):
        ddb = boto3.resource("dynamodb")
        ddb.Table("testTable").delete()
        
    def test_mock_data_successfully_setup(self):
        ddb= boto3.resource("dynamo3b")
        table = ddb.Table("testTable")
        all_items = table.scan()
        return len(all_items["Items"]) == 3