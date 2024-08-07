import unittest
from unittest.mock import patch
from moto import mock_dynamodb2, mock_sns, mock_ec2
import boto3
from script import lambda_handler, update_dynamodb, tag_resource

class TestTaggingScript(unittest.TestCase):

    @mock_dynamodb2
    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.create_table(
            TableName='ResourceTaggingMetadata',
            KeySchema=[{'AttributeName': 'ResourceId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'ResourceId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        self.table.meta.client.get_waiter('table_exists').wait(TableName='ResourceTaggingMetadata')

    @mock_sns
    def test_send_alert(self):
        sns = boto3.client('sns')
        sns.create_topic(Name='TestTopic')
        response = sns.list_topics()
        self.assertTrue(len(response['Topics']) > 0)

    @mock_ec2
    def test_tag_resource(self):
        ec2 = boto3.client('ec2')
        ec2.create_instances(ImageId='ami-12345678', MinCount=1, MaxCount=1)
        instances = ec2.describe_instances()
        resource_id = instances['Reservations'][0]['Instances'][0]['InstanceId']
        tags = [{'Key': 'SOC2Compliance', 'Value': 'True'}]
        response = tag_resource(resource_id, tags)
        self.assertIsNotNone(response)

    @mock_dynamodb2
    def test_update_dynamodb(self):
        resource_id = 'i-1234567890abcdef0'
        tags = [{'Key': 'SOC2Compliance', 'Value': 'True'}]
        user = 'admin-user'
        response = update_dynamodb(resource_id, tags, user)
        self.assertIsNotNone(response)

    @mock_dynamodb2
    @mock_ec2
    @mock_sns
    def test_lambda_handler(self):
        event = {
            'resource_id': 'i-1234567890abcdef0',
            'user': 'admin-user'
        }
        context = None
        response = lambda_handler(event, context)
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()
