import { EC2Client, CreateTagsCommand } from "@aws-sdk/client-ec2";
import { DynamoDBClient, PutItemCommand } from "@aws-sdk/client-dynamodb";
import { SNSClient, PublishCommand } from "@aws-sdk/client-sns";
import { CloudWatchClient, PutMetricDataCommand } from "@aws-sdk/client-cloudwatch";
import { handler, tagResource, updateDynamoDb, sendAlert } from "./script";
import { mockClient } from "aws-sdk-client-mock";
import "aws-sdk-client-mock-jest";

describe("AWS Tagging Script", () => {
  const ec2Mock = mockClient(EC2Client);
  const dynamoDbMock = mockClient(DynamoDBClient);
  const snsMock = mockClient(SNSClient);
  const cloudWatchMock = mockClient(CloudWatchClient);

  beforeEach(() => {
    ec2Mock.reset();
    dynamoDbMock.reset();
    snsMock.reset();
    cloudWatchMock.reset();
  });

  it("should successfully tag a resource", async () => {
    ec2Mock.on(CreateTagsCommand).resolves({});
    await tagResource("i-1234567890abcdef0");
    expect(ec2Mock).toHaveReceivedCommandWith(CreateTagsCommand, {
      Resources: ["i-1234567890abcdef0"],
      Tags: [{ Key: "SOC2Compliance", Value: "True" }],
    });
  });

  it("should successfully update DynamoDB", async () => {
    dynamoDbMock.on(PutItemCommand).resolves({});
    await updateDynamoDb("i-1234567890abcdef0", "admin-user");
    expect(dynamoDbMock).toHaveReceivedCommandWith(PutItemCommand, {
      TableName: "ResourceTaggingMetadata",
      Item: {
        ResourceId: { S: "i-1234567890abcdef0" },
        User: { S: "admin-user" },
        Action: { S: "Tagging" },
      },
    });
  });

  it("should successfully send an alert", async () => {
    snsMock.on(PublishCommand).resolves({});
    cloudWatchMock.on(PutMetricDataCommand).resolves({});

    await sendAlert("Test alert");
    expect(snsMock).toHaveReceivedCommandWith(PublishCommand, {
      TopicArn: "arn:aws:sns:region:account-id:topic",
      Message: "Test alert",
    });
    expect(cloudWatchMock).toHaveReceivedCommandWith(PutMetricDataCommand, {
      Namespace: "TaggingScript",
      MetricData: [{
        MetricName: "TaggingErrors",
        Value: 1,
        Unit: "Count",
      }],
    });
  });
});
