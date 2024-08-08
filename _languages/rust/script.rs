use aws_sdk_dynamodb::{Client as DynamoDbClient};
use aws_sdk_ec2::{Client as Ec2Client};
use aws_sdk_sns::{Client as SnsClient};
use aws_sdk_cloudwatch::{Client as CloudWatchClient};
use aws_sdk_sns::model::MessageAttributeValue;
use std::collections::HashMap;
use log::{info, error};
use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), aws_sdk_dynamodb::Error> {
    let dynamodb_client = DynamoDbClient::new(&aws_config::load_from_env().await);
    let ec2_client = Ec2Client::new(&aws_config::load_from_env().await);
    let sns_client = SnsClient::new(&aws_config::load_from_env().await);
    let cloudwatch_client = CloudWatchClient::new(&aws_config::load_from_env().await);

    let resource_id = "i-1234567890abcdef0";
    let user = "admin-user";

    match tag_resource(&ec2_client, resource_id).await {
        Ok(_) => {
            update_dynamodb(&dynamodb_client, resource_id, user).await?;
        },
        Err(e) => {
            error!("Error tagging resource: {:?}", e);
            send_alert(&sns_client, &cloudwatch_client, &format!("Error tagging resource: {:?}", e)).await?;
        }
    };

    Ok(())
}

async fn tag_resource(client: &Ec2Client, resource_id: &str) -> Result<(), aws_sdk_ec2::Error> {
    let tag = aws_sdk_ec2::model::Tag::builder()
        .key("SOC2Compliance")
        .value("True")
        .build();
    client.create_tags()
        .resources(resource_id)
        .tags(tag)
        .send()
        .await?;
    info!("Successfully tagged resource {}", resource_id);
    Ok(())
}

async fn update_dynamodb(client: &DynamoDbClient, resource_id: &str, user: &str) -> Result<(), aws_sdk_dynamodb::Error> {
    let mut item = HashMap::new();
    item.insert("ResourceId".to_string(), resource_id.into());
    item.insert("User".to_string(), user.into());
    item.insert("Action".to_string(), "Tagging".into());
    client.put_item()
        .table_name("ResourceTaggingMetadata")
        .set_item(Some(item))
        .send()
        .await?;
    info!("Metadata updated in DynamoDB for resource {}", resource_id);
    Ok(())
}

async fn send_alert(sns_client: &SnsClient, cloudwatch_client: &CloudWatchClient, message: &str) -> Result<(), aws_sdk_sns::Error> {
    sns_client.publish()
        .topic_arn("arn:aws:sns:region:account-id:topic")
        .message(message)
        .send()
        .await?;

    cloudwatch_client.put_metric_data()
        .namespace("TaggingScript")
        .metric_data(aws_sdk_cloudwatch::model::MetricDatum::builder()
            .metric_name("TaggingErrors")
            .value(1.0)
            .unit("Count")
            .build())
        .send()
        .await?;

    info!("Alert sent: {}", message);
    Ok(())
}
