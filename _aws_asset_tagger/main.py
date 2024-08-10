from aws_asset_tagger.aws_clients import ec2_client, s3_client
from aws_asset_tagger.resources.fetcher import fetch_ec2_instances, fetch_s3_buckets
from aws_asset_tagger.resources.processor import process_resource
from aws_asset_tagger.utils.logger import get_logger
from aws_asset_tagger.utils.alert import send_alert_to_cloudwatch

logger = get_logger()

def lambda_handler(event, context):
    try:
        # Fetch resources
        ec2_instances = fetch_ec2_instances()
        s3_buckets = fetch_s3_buckets()

        # Process resources
        for resource in ec2_instances + s3_buckets:
            process_resource(resource)

        logger.info('Tagging process completed successfully.')

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        send_alert_to_cloudwatch(str(e))


if __name__ == "__main__":
    lambda_handler({}, None)
