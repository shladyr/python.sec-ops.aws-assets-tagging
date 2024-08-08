# Automatic AWS Assets Tagging Solution

## Overview
This project provides an automatic AWS assets tagging solution that meets SOC-2 compliance requirements. The solution is implemented as an AWS Lambda function that tags AWS resources across all data centers in a specified AWS account and stores metadata in DynamoDB. It also sends alerts to SNS and CloudWatch in case of errors.

## Features
- **Automatic Tagging:** Tags AWS resources across all data centers in a specified AWS account.
- **Metadata Storage:** Stores resource metadata in DynamoDB for auditing and compliance.
- **Error Handling:** Sends alerts to SNS and logs errors to CloudWatch.
- **Security:** Ensures compliance with SOC-2 security controls.

## Setup and Installation
1. Clone the repository.
2. Install dependencies for your chosen language (Python, Rust, Go, TypeScript).
3. Deploy the Lambda function:
   - Package the code using your preferred method (e.g., zip for Python, cargo build for Rust).
   - Deploy the package to AWS Lambda using the AWS CLI or AWS Management Console.

## Configuration
- Set the following environment variables in your Lambda function:
  - `DYNAMODB_TABLE`: The name of the DynamoDB table to store metadata.
  - `SNS_TOPIC_ARN`: The ARN of the SNS topic to send alerts.
  - `TAG_KEY`: The key of the tag to apply to resources.
  - `TAG_VALUE`: The value of the tag to apply to resources.

## Usage
- Trigger the Lambda function with an event containing `resource_id` and `user` fields.
- The function will automatically tag the specified resource and store the metadata in DynamoDB.

## Testing
- **Unit Tests:** Run the provided unit tests to validate functionality.

## Contributing
- Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
