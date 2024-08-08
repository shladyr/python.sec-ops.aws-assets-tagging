package main

import (
	"context"
	"testing"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/cloudwatch"
	"github.com/aws/aws-sdk-go-v2/service/dynamodb"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
	"github.com/aws/aws-sdk-go-v2/service/sns"
	"github.com/golang/mock/gomock"
	"github.com/stretchr/testify/assert"
)

func TestTagResource_Success(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	mockEC2Client := NewMockEC2Client(ctrl)
	mockEC2Client.EXPECT().CreateTags(gomock.Any(), gomock.Any()).Return(&ec2.CreateTagsOutput{}, nil)

	err := tagResource(mockEC2Client, "i-1234567890abcdef0")
	assert.Nil(t, err)
}

func TestUpdateDynamoDB_Success(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	mockDynamoDBClient := NewMockDynamoDBClient(ctrl)
	mockDynamoDBClient.EXPECT().PutItem(gomock.Any(), gomock.Any()).Return(&dynamodb.PutItemOutput{}, nil)

	err := updateDynamoDB(mockDynamoDBClient, "i-1234567890abcdef0", "admin-user")
	assert.Nil(t, err)
}

func TestSendAlert_Success(t *testing.T) {
	ctrl := gomock.NewController(t)
	defer ctrl.Finish()

	mockSNSClient := NewMockSNSClient(ctrl)
	mockCloudWatchClient := NewMockCloudWatchClient(ctrl)

	mockSNSClient.EXPECT().Publish(gomock.Any(), gomock.Any()).Return(&sns.PublishOutput{}, nil)
	mockCloudWatchClient.EXPECT().PutMetricData(gomock.Any(), gomock.Any()).Return(&cloudwatch.PutMetricDataOutput{}, nil)

	sendAlert(mockSNSClient, mockCloudWatchClient, "Test alert")
}
