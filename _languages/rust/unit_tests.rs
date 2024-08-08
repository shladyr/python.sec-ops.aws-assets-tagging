#[cfg(test)]
mod tests {
    use super::*;
    use aws_sdk_dynamodb::model::AttributeValue;
    use aws_sdk_dynamodb::Client as DynamoDbClient;
    use aws_sdk_ec2::Client as Ec2Client;
    use aws_sdk_sns::Client as SnsClient;
    use aws_sdk_cloudwatch::Client as CloudWatchClient;
    use aws_sdk_sns::model::MessageAttributeValue;
    use mockito::mock;

    #[tokio::test]
    async fn test_tag_resource_success() {
        let _m = mock("POST", "/")
            .with_status(200)
            .with_body("{}")
            .create();

        let client = Ec2Client::new(&aws_config::load_from_env().await);
        let result = tag_resource(&client, "i-1234567890abcdef0").await;

        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_update_dynamodb_success() {
        let _m = mock("POST", "/")
            .with_status(200)
            .with_body("{}")
            .create();

        let client = DynamoDbClient::new(&aws_config::load_from_env().await);
        let result = update_dynamodb(&client, "i-1234567890abcdef0", "admin-user").await;

        assert!(result.is_ok());
    }

    #[tokio::test]
    async fn test_send_alert_success() {
        let _m = mock("POST", "/")
            .with_status(200)
            .with_body("{}")
            .create();

        let sns_client = SnsClient::new(&aws_config::load_from_env().await);
        let cloudwatch_client = CloudWatchClient::new(&aws_config::load_from_env().await);
        let result = send_alert(&sns_client, &cloudwatch_client, "Test alert").await;

        assert!(result.is_ok());
    }
}
