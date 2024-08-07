package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/cloudwatch"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/sns"
)

const (
	DynamoDBTableName = "ResourceTaggingMetadata"
	SNSTopicArn       = "arn:aws:sns:region:account-id:topic"
	TagKey            = "SOC2Compliance"
	TagValue          = "True"
)

func main() {
	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion("us-west-2"))
	if err != nil {
		log.Fatalf("unable to load SDK config, %v", err)
	}

	ec2Client := ec2.NewFromConfig(cfg)
	dynamodbClient := dynamodb.NewFromConfig(cfg)
	snsClient := sns.NewFromConfig(cfg)
	cloudwatchClient := cloudwatch.NewFromConfig(cfg)

	resourceID := "i-1234567890abcdef0"
	user := "admin-user"

	err = tagResource(ec2Client, resourceID)
	if err != nil {
		log.Printf("Error tagging resource: %v", err)
		sendAlert(snsClient, cloudwatchClient, fmt.Sprintf("Error tagging resource: %v", err))
		return
	}

	err = updateDynamoDB(dynamodbClient, resourceID, user)
	if err != nil {
		log.Printf("Error updating DynamoDB: %v", err)
		sendAlert(snsClient, cloudwatchClient, fmt.Sprintf("Error updating DynamoDB: %v", err))
		return
	}
}

func tagResource(client *ec2.Client, resourceID string) error {
	tag := ec2.Tag{
		Key:   aws.String(TagKey),
		Value: aws.String(TagValue),
	}
	_, err := client.CreateTags(context.TODO(), &ec2.CreateTagsInput{
		Resources: []string{resourceID},
		Tags:      []ec2.Tag{tag},
	})
	if err != nil {
		return fmt.Errorf("failed to tag resource: %w", err)
	}
	log.Printf("Successfully tagged resource %s", resourceID)
	return nil
}

func updateDynamoDB(client *dynamodb.Client, resourceID, user string) error {
	item := map[string]dynamodb.AttributeValue{
		"ResourceId": {S: aws.String(resourceID)},
		"User":       {S: aws.String(user)},
		"Action":     {S: aws.String("Tagging")},
	}
	_, err := client.PutItem(context.TODO(), &dynamodb.PutItemInput{
		TableName: aws.String(DynamoDBTableName),
		Item:      item,
	})
	if err != nil {
		return fmt.Errorf("failed to update DynamoDB: %w", err)
	}
	log.Printf("Metadata updated in DynamoDB for resource %s", resourceID)
	return nil
}

func sendAlert(snsClient *sns.Client, cloudwatchClient *cloudwatch.Client, message string) {
	_, err := snsClient.Publish(context.TODO(), &sns.PublishInput{
		TopicArn: aws.String(SNSTopicArn),
		Message:  aws.String(message),
	})
	if err != nil {
		log.Printf("Error sending alert: %v", err)
	}

	_, err = cloudwatchClient.PutMetricData(context.TODO(), &cloudwatch.PutMetricDataInput{
		Namespace: aws.String("TaggingScript"),
		MetricData: []cloudwatch.MetricDatum{
			{
				MetricName: aws.String("TaggingErrors"),
				Value:      aws.Float64(1.0),
				Unit:       cloudwatch.StandardUnitCount,
			},
		},
	})
	if err != nil {
		log.Printf("Error sending CloudWatch metric: %v", err)
	}

	log.Printf("Alert sent: %s", message)
}
