import boto3
import os
import logging
from botocore.exceptions import ClientError
from datetime import datetime

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
ec2_client = boto3.client('ec2')
s3_client = boto3.client('s3')
cloudwatch_client = boto3.client('cloudwatch')

# Configuration
TAG_SCHEMA = {'Environment': 'Production', 'Compliance': 'SOC-2'}
METADATA_TABLE_NAME = os.getenv('METADATA_TABLE_NAME')
HISTORY_TABLE_NAME = os.getenv('HISTORY_TABLE_NAME')
ACTIONS_TABLE_NAME = os.getenv('ACTIONS_TABLE_NAME')


def lambda_handler(event, context):
    try:
        # Fetch resources
        ec2_instances = fetch_ec2_instances()
        s3_buckets = fetch_s3_buckets()

        # Process resources
        for resource in ec2_instances + s3_buckets:
            process_resource(resource)

        logger.info('Tagging process completed successfully.')

    except ClientError as e:
        logger.error(f"ClientError: {str(e)}")
        send_alert_to_cloudwatch(str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        send_alert_to_cloudwatch(str(e))


def fetch_ec2_instances():
    instances = ec2_client.describe_instances()
    return instances['Reservations']


def fetch_s3_buckets():
    buckets = s3_client.list_buckets()
    return buckets['Buckets']


def process_resource(resource):
    resource_id = get_resource_id(resource)
    if not is_resource_tagged(resource):
        apply_tags(resource_id)
        store_metadata(resource_id)
        log_user_action(resource_id)


def is_resource_tagged(resource):
    tags = resource.get('Tags', [])
    for key, value in TAG_SCHEMA.items():
        if not any(tag['Key'] == key and tag['Value'] == value for tag in tags):
            return False
    return True


def apply_tags(resource_id):
    # Apply tags based on resource type
    if 'i-' in resource_id:
        ec2_client.create_tags(Resources=[resource_id], Tags=TAG_SCHEMA.items())
    elif 'arn:aws:s3:::' in resource_id:
        s3_client.put_bucket_tagging(Bucket=resource_id.split(':::')[1], Tagging={'TagSet': TAG_SCHEMA.items()})
    logger.info(f"Tags applied to {resource_id}")


def store_metadata(resource_id):
    table = dynamodb.Table(METADATA_TABLE_NAME)
    table.put_item(Item={
        'resource_id': resource_id,
        'tag_values': TAG_SCHEMA,
        'timestamp': datetime.now().isoformat(),
        'user_info': get_user_info()
    })
    logger.info(f"Metadata stored for {resource_id}")


def log_user_action(resource_id):
    table = dynamodb.Table(ACTIONS_TABLE_NAME)
    table.put_item(Item={
        'action_id': f"{resource_id}_{datetime.now().isoformat()}",
        'resource_id': resource_id,
        'user_info': get_user_info(),
        'action_type': 'Tagging',
        'timestamp': datetime.now().isoformat()
    })
    logger.info(f"User action logged for {resource_id}")


def get_resource_id(resource):
    if 'Instances' in resource:
        return resource['Instances'][0]['InstanceId']
    elif 'Name' in resource:
        return f"arn:aws:s3:::{resource['Name']}"
    return None


def get_user_info():
    # Dummy user information, replace with actual data
    return {'user': 'auto-tagger', 'group': 'devops'}


def send_alert_to_cloudwatch(message):
    cloudwatch_client.put_metric_alarm(
        AlarmName='AWSAssetTaggingError',
        AlarmDescription=message,
        ActionsEnabled=True,
        AlarmActions=[],
        MetricName='AWSAssetTaggingErrors',
        Namespace='AWS/Lambda',
        Statistic='Sum',
        Period=60,
        EvaluationPeriods=1,
        Threshold=1,
        ComparisonOperator='GreaterThanOrEqualToThreshold'
    )
    logger.info('Alert sent to CloudWatch')


if __name__ == "__main__":
    lambda_handler({}, None)
