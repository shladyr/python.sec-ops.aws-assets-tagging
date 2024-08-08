from aws_asset_tagger.aws_clients import dynamodb, ec2_client, s3_client
from aws_asset_tagger.config import TAG_SCHEMA, METADATA_TABLE_NAME, ACTIONS_TABLE_NAME
from aws_asset_tagger.utils.logger import get_logger
from aws_asset_tagger.utils.user_info import get_user_info

logger = get_logger()

def process_resource(resource):
    resource_id = get_resource_id(resource)
    if not is_resource_tagged(resource):
        apply_tags(resource_id)
        store_metadata(resource_id)
        log_user_action(resource_id)

def get_resource_id(resource):
    if 'Instances' in resource:
        return resource['Instances'][0]['InstanceId']
    elif 'Name' in resource:
        return f"arn:aws:s3:::{resource['Name']}"
    return None

def is_resource_tagged(resource):
    tags = resource.get('Tags', [])
    for key, value in TAG_SCHEMA.items():
        if not any(tag['Key'] == key and tag['Value'] == value for tag in tags):
            return False
    return True

def apply_tags(resource_id):
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
