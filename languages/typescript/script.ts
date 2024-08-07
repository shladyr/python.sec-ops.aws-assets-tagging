import { EC2Client, CreateTagsCommand } from "@aws-sdk/client-ec2";
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";
import { SNSClient, PublishCommand } from "@aws-sdk/client-sns";
import { CloudWatchClient, PutMetricDataCommand } from "@aws-sdk/client-cloudwatch";
import { logger } from "./logger";

const DYNAMODB_TABLE = "ResourceTaggingMetadata";
const SNS_TOPIC_ARN = "arn:aws:sns:region:account-id:topic";
const TAG_KEY = "SOC2Compliance";
const TAG_VALUE = "True";

const ec2Client = new EC2Client({});
const dynamoDbClient = new DynamoDBClient({});
const snsClient = new SNSClient({});
const cloudWatchClient = new CloudWatchClient({});

export const handler = async (event: any) => {
  const resourceId = event.resourceId;
  const user = event.user;

  if (!resourceId || !user) {
    logger.error("Missing resourceId or user in event");
    await sendAlert("Missing resourceId or user in event");
    return;
  }

  try {
    await tagResource(resourceId);
    await updateDynamoDb(resourceId, user);
  } catch (error) {
    logger.error("Error in handler: ", error);
    await sendAlert(`Error processing resource ${resourceId}: ${error}`);
  }
};

const tagResource = async (resourceId: string) => {
  const command = new CreateTagsCommand({
    Resources: [resourceId],
    Tags: [{ Key: TAG_KEY, Value: TAG_VALUE }],
  });

  try {
    await ec2Client.send(command);
    logger.info(`Successfully tagged resource ${resourceId}`);
  } catch (error) {
    logger.error(`Error tagging resource ${resourceId}: `, error);
    throw error;
  }
};

const updateDynamoDb = async (resourceId: string, user: string) => {
  const command = new PutItemCommand({
    TableName: DYNAMODB_TABLE,
    Item: {
      ResourceId: { S: resourceId },
      User: { S: user },
      Action: { S: "Tagging" },
    },
  });

  try {
    await dynamoDbClient.send(command);
    logger.info(`Metadata updated in DynamoDB for resource ${resourceId}`);
  } catch (error) {
    logger.error(`Error updating DynamoDB for resource ${resourceId}: `, error);
    throw error;
  }
};

const sendAlert = async (message: string) => {
  const snsCommand = new PublishCommand({
    TopicArn: SNS_TOPIC_ARN,
    Message: message,
  });

  try {
    await snsClient.send(snsCommand);
    logger.info(`Alert sent: ${message}`);
  } catch (error) {
    logger.error(`Error sending alert: `, error);
  }

  const cloudWatchCommand = new PutMetricDataCommand({
    Namespace: "TaggingScript",
    MetricData: [
      {
        MetricName: "TaggingErrors",
        Value: 1,
        Unit: "Count",
      },
    ],
  });

  try {
    await cloudWatchClient.send(cloudWatchCommand);
  } catch (error) {
    logger.error(`Error sending CloudWatch metric: `, error);
  }
};
