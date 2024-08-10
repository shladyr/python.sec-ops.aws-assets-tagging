# Technical Documentation for AWS Asset Tagging Script for SOC-2 Compliance

## 4.1 Introduction
This document describes the technical details of the AWS Asset Tagging Script developed to meet SOC-2 compliance requirements. The script tags AWS resources across all Data Centers in a specified AWS account and stores metadata in DynamoDB.

## 4.2 System Overview
The script interacts with various AWS services using Boto3, applies predefined tags, and stores metadata in DynamoDB tables. The script also includes error handling, logging, and alerting mechanisms.

## 4.3 Modules Description
- **Main Module:** Initializes the Lambda function, loads configuration, and triggers the tagging process.
- **AWS Interaction Module:** Handles communication with AWS services.
- **Tagging Logic Module:** Contains the logic to apply tags to AWS resources.
- **DynamoDB Interaction Module:** Manages the storage and retrieval of metadata from DynamoDB.
- **Error Handling Module:** Captures exceptions and logs them to CloudWatch.

## 4.4 Database Schema
- **TagsMetadata Table:**
  - `resource_id`: Partition key, string, unique identifier of the AWS resource.
  - `tag_values`: Map, stores key-value pairs of tags.
  - `timestamp`: String, ISO 8601 format, the time when the tag was applied.
  - `user_info`: Map, stores user/group information associated with the tagging operation.

- **TagHistory Table:**
  - `resource_id`: Partition key, string, unique identifier of the AWS resource.
  - `tag_values`: Map, stores historical key-value pairs of tags.
  - `timestamp`: String, ISO 8601 format, the time when the tag was applied.

- **UserActions Table:**
  - `action_id`: Partition key, string, unique identifier for the action.
  - `resource_id`: String, ID of the resource involved in the action.
  - `user_info`: Map, stores user/group information.
  - `action_type`: String, type of action performed (e.g., tagging).
  - `timestamp`: String, ISO 8601 format, the time of the action.

## 4.5 Error Handling and Alerts
- Errors are logged to CloudWatch Logs, and critical errors trigger CloudWatch Alarms.
- Alerts are sent via SNS or other configured notification services.

## 4.6 Security Measures
- Implement IAM roles with least privilege access.
- Encrypt sensitive data using AWS KMS.
- Use input validation to prevent injection attacks.

## 4.7 Testing and Validation
- Unit tests ensure each module functions as expected.
- Integration tests validate AWS interactions and overall script functionality.
- Code quality checks ensure adherence to PEP 8 standards.
