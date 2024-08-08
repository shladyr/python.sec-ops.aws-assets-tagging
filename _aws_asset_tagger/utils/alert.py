from aws_asset_tagger.aws_clients import cloudwatch_client
from aws_asset_tagger.utils.logger import get_logger

logger = get_logger()

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
