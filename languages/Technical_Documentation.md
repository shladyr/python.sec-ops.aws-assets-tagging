# Technical Documentation for Automatic AWS Assets Tagging Solution

## Introduction
This document provides detailed technical documentation for the AWS assets tagging solution, which ensures SOC-2 compliance by automatically tagging AWS resources and storing metadata in DynamoDB.

## System Components
### AWS Lambda Function
- The Lambda function contains the main script that handles tagging AWS resources.
- The function is triggered by events that include resource IDs and user information.

### AWS DynamoDB
- Stores metadata related to tagged AWS resources, including resource attributes, user/group information, and tag values.
- DynamoDB table structure includes the following fields:
  - **ResourceId** (Primary Key)
  - **Tags**
  - **User**
  - **Action**

### AWS SNS
- SNS is used to send alerts in case of errors during the tagging process.
- Alerts are sent to a specified SNS topic.

### AWS CloudWatch
- CloudWatch is used to monitor and log operations for auditing and error tracking.
- Custom metrics are published to CloudWatch to track tagging errors and other relevant data.

## Script Workflow
1. The script is triggered by an event containing a resource ID and user information.
2. The script creates a tag on the specified AWS resource using the EC2 client.
3. Metadata is updated in the DynamoDB table with the resource ID, tags, user, and action information.
4. If an error occurs during the process, an alert is sent to the specified SNS topic, and a custom metric is sent to CloudWatch.

## Configuration
- **Environment Variables:**
  - `DYNAMODB_TABLE`: The DynamoDB table name where metadata is stored.
  - `SNS_TOPIC_ARN`: The ARN of the SNS topic where alerts are sent.
  - `TAG_KEY`: The key of the tag to be applied.
  - `TAG_VALUE`: The value of the tag to be applied.

## Security
- AWS IAM roles and policies are configured to ensure the Lambda function has the necessary permissions to interact with EC2, DynamoDB, SNS, and CloudWatch.
- Sensitive data is managed securely using AWS Secrets Manager or environment variables.

## Logging and Monitoring
- The script uses built-in logging mechanisms provided by the AWS SDK to log operations and errors.
- CloudWatch is configured to monitor and alert on specific metrics such as tagging errors.

## Deployment
- The script is deployed as an AWS Lambda function.
- Configuration is managed through environment variables and AWS Systems Manager Parameter Store.

## Troubleshooting
- If tagging fails, check the CloudWatch logs for detailed error messages.
- Ensure that the necessary IAM roles and policies are correctly configured.
- Validate that the DynamoDB table and SNS topic exist and are correctly configured.
