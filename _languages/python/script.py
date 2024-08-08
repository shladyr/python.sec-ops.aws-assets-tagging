import boto3
import logging
import json
from botocore.exceptions import ClientError

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS services clients
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
cloudwatch = boto3.client('cloudwatch')

# Configuration
DYNAMODB_TABLE = 'ResourceTaggingMetadata'
SNS_TOPIC_ARN = 'arn:aws:sns:region:account-id:topic'
TAG_KEY = 'SOC2Compliance'
TAG_VALUE = 'True'

# Helper function to send alerts
def send_alert(message):
    try:
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message
        )
        logger.info(f"Alert sent: {response['MessageId']}")
    except ClientError as e:
        logger.error(f"Error sending alert: {e}")
        cloudwatch.put_metric_data(
            Namespace='TaggingScript',
            MetricData=[{
                'MetricName': 'TaggingErrors',
                'Value': 1,
                'Unit': 'Count'
            }]
        )

# Function to tag an AWS resource
def tag_resource(resource_id, tags):
    try:
        ec2 = boto3.client('ec2')
        response = ec2.create_tags(
            Resources=[resource_id],
            Tags=tags
        )
        logger.info(f"Successfully tagged resource {resource_id}")
        return response
    except ClientError as e:
        logger.error(f"Error tagging resource {resource_id}: {e}")
        send_alert(f"Error tagging resource {resource_id}: {e}")
        return None

# Function to update DynamoDB with tagging metadata
def update_dynamodb(resource_id, tags, user):
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.put_item(
            Item={
                'ResourceId': resource_id,
                'Tags': tags,
                'User': user,
                'Action': 'Tagging'
            }
        )
        logger.info(f"Metadata updated in DynamoDB for resource {resource_id}")
        return response
    except ClientError as e:
        logger.error(f"Error updating DynamoDB for resource {resource_id}: {e}")
        send_alert(f"Error updating DynamoDB for resource {resource_id}: {e}")
        return None

# Main function
def lambda_handler(event, context):
    resource_id = event.get('resource_id')
    user = event.get('user')
    tags = [{'Key': TAG_KEY, 'Value': TAG_VALUE}]

    if not resource_id or not user:
        logger.error("Missing resource_id or user in event")
        send_alert("Missing resource_id or user in event")
        return

    tag_response = tag_resource(resource_id, tags)
    if tag_response:
        update_dynamodb(resource_id, tags, user)

if __name__ == "__main__":
    # Example event for testing locally
    event = {
        'resource_id': 'i-1234567890abcdef0',
        'user': 'admin-user'
    }
    lambda_handler(event, None)
