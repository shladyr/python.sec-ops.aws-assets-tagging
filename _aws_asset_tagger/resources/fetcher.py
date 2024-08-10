from aws_asset_tagger.aws_clients import ec2_client, s3_client

def fetch_ec2_instances():
    instances = ec2_client.describe_instances()
    return instances['Reservations']

def fetch_s3_buckets():
    buckets = s3_client.list_buckets()
    return buckets['Buckets']
